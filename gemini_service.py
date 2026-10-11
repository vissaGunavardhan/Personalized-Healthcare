import base64
import json
import logging
import re
import requests
from config import Config

logger = logging.getLogger(__name__)

class GeminiService:
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    @classmethod
    def get_api_key(cls):
        return Config.GEMINI_API_KEY

    @classmethod
    def call_gemini(cls, payload, timeout=30):
        key = cls.get_api_key()
        if not key:
            raise ValueError("GEMINI_API_KEY not configured in .env")

        headers = {"Content-Type": "application/json"}
        last_error = None

        # Waterfall through supported models
        for model in Config.GEMINI_MODELS:
            url = f"{cls.BASE_URL}/models/{model}:generateContent?key={key}"
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=timeout)
                if response.status_code == 200:
                    data = response.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        return "".join(p.get("text", "") for p in parts)
                else:
                    last_error = f"Model {model} returned {response.status_code}: {response.text[:200]}"
                    logger.warning(last_error)
            except Exception as e:
                last_error = f"Model {model} exception: {str(e)}"
                logger.warning(last_error)

        raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")

    @classmethod
    def analyze_medical_report_image(cls, image_bytes, mime_type="image/jpeg", notes=""):
        """
        Multimodal OCR & extraction of lab test parameters from report image
        """
        b64_img = base64.b64encode(image_bytes).decode("utf-8")
        
        prompt = f"""
You are an expert clinical laboratory pathologist and medical AI assistant.
Analyze this medical lab report / clinical document image carefully.
Notes from patient: {notes if notes else 'None'}

Extract all laboratory tests and biomarkers found in this report.
Return ONLY valid JSON (no markdown formatting, no code fence, just pure JSON) with the following structure:
{{
  "report_title": "Title of the test (e.g. Complete Blood Count, Comprehensive Metabolic Panel, Outpatient Note, etc.)",
  "report_type": "Category (e.g. Hematology, Biochemistry, Lipid, Diabetes, Cardiology, Renal)",
  "patient_name": "Patient name or Anonymous if obscured",
  "report_date": "Date of collection or reporting (e.g. 2026-09-28)",
  "lab_name": "Name of diagnostic center or hospital (e.g. Metropolis, Apollo, Quest, Lal PathLabs, etc.)",
  "overall_status": "Normal" or "Attention Needed" or "Critical",
  "biomarkers": [
    {{
      "parameter": "Test name (e.g. Hemoglobin, Fasting Blood Sugar, Platelets, TSH)",
      "value": "Observed value (e.g. 13.5)",
      "unit": "Unit (e.g. g/dL, mg/dL, mcL)",
      "ref_range": "Normal reference interval (e.g. 13.0 - 17.0)",
      "status": "Normal" or "High" or "Low" or "Borderline" or "Critical",
      "clinical_note": "A simple 1-sentence patient explanation"
    }}
  ],
  "raw_summary": "Concise summary of findings in 2-3 sentences."
}}
"""

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inlineData": {"mimeType": mime_type, "data": b64_img}}
                ]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 3000
            }
        }

        try:
            raw_text = cls.call_gemini(payload, timeout=35)
            # Clean possible markdown fencing
            cleaned = raw_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            return json.loads(cleaned.strip())
        except Exception as e:
            logger.error(f"Failed Gemini multimodal OCR: {e}")
            return None

    @classmethod
    def generate_simple_language_summary(cls, biomarkers, user_profile=None, target_language="English"):
        """
        Translates complex medical lab biomarkers into patient-friendly, plain language.
        """
        profile_ctx = ""
        if user_profile:
            profile_ctx = f"Patient context: Age {user_profile.get('age', 'Adult')}, Gender: {user_profile.get('gender', 'Unknown')}, Conditions: {user_profile.get('conditions', 'None')}."

        prompt = f"""
You are a compassionate, clear-communicating doctor who explains lab reports to everyday patients in plain, non-intimidating language.
{profile_ctx}
Language requested: {target_language}

Here is the extracted lab data:
{json.dumps(biomarkers, indent=2)}

Translate these results into an easy-to-understand patient health summary.
Return ONLY valid JSON (no markdown formatting, no code fences) with the exact structure:
{{
  "overview": "A clear, reassuring 2-3 sentence overview of overall health based on these numbers in {target_language}.",
  "attention_points": [
    "Clear bullet point explaining elevated or abnormal parameters in plain terms (e.g., 'Your blood sugar is slightly higher than usual...')",
    "Another point..."
  ],
  "lifestyle_tips": [
    "Practical everyday lifestyle, food, or exercise tip 1",
    "Practical everyday lifestyle tip 2",
    "Practical everyday lifestyle tip 3"
  ],
  "doctor_questions": [
    "Specific question 1 the patient can ask their physician at next checkup",
    "Specific question 2 to ask",
    "Specific question 3 to ask"
  ],
  "urgency_level": "Routine" or "Follow-up Soon" or "Urgent"
}}
"""

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2048
            }
        }

        try:
            raw_text = cls.call_gemini(payload, timeout=25)
            cleaned = raw_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            return json.loads(cleaned.strip())
        except Exception as e:
            logger.error(f"Failed Gemini simple summary: {e}")
            return None
