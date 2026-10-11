# HealthVault: Unified Digital Health & ABDM Portal

An intelligent, patient-centric digital healthcare platform designed for evidence-based care, Ayushman Bharat Digital Mission (ABDM) integration, and multi-language patient accessibility.

---

## 🌟 Core Pillars & Key Features

### 1. 🔬 Medical Report OCR & Biomarker Scanner
- **Dual Multimodal Vision Engine**: Uses Google Gemini Multimodal Vision API (`gemini-3.5-flash` / `gemini-3.8-flash`) combined with algorithmic lab heuristics for instant, fault-tolerant clinical parameter extraction.
- **Biomarker Mapping**: Automatically identifies test names, observed values, biological units ($mg/dL$, $g/dL$, $\mu IU/mL$), standard reference intervals, and clinical status flags (**Normal**, **Borderline**, **Elevated/Low**, **Critical**).
- **Interactive Scanning Animation**: Real-time laser scanner HUD overlay during report processing.
- **One-Click Presets**: Pre-loaded diagnostic panels for instant testing: Complete Blood Count (CBC), Diabetic HbA1c & Glucose, Lipid & Cholesterol Panel, Renal Function (RFT), and Thyroid Panel (TSH).

### 2. 💡 Health Summary in Simple Language ("Doctor-to-Human Translator")
- **Zero Medical Jargon**: Converts complex clinical terminology into everyday, reassuring language.
- **The Big Picture**: 2-3 sentence executive overview of overall health.
- **What Needs Attention**: Explains elevated or borderline metrics without inducing panic.
- **Actionable Lifestyle Tips**: Practical evidence-based dietary, hydration, sleep, and exercise recommendations.
- **Questions for Your Doctor**: Prepares targeted, intelligent prompt questions with a one-click copy button to take to the clinic.

### 3. 📋 Unified Health Profile & Vitals Cockpit
- **Consolidated Health Record (PHR)**: Single source of truth for vitals (Blood Pressure, Blood Glucose, Heart Rate, SpO2, BMI).
- **Medications & Prescriptions**: Tracks active pharmaceuticals, dosages, frequencies, and clinical purpose.
- **Allergies & Sensitivities**: Records drug and food allergens with severity tagging.
- **Chronic Conditions**: Tracks ongoing health conditions (e.g., Type 2 Diabetes, Hypertension).
- **Emergency Medical Contact**: Instantly accessible contact information linked to emergency responders.
- **Diagnostic History Timeline**: Historical log of all past laboratory investigations and reports.

### 4. 🌐 Multi-Language Accessibility (6 Languages)
- Instant, client-side & server-side translation switcher supporting:
  - **English**
  - **हिन्दी (Hindi)**
  - **తెలుగు (Telugu)**
  - **தமிழ் (Tamil)**
  - **বাংলা (Bengali)**
  - **मराठी (Marathi)**
- Translates navigation menus, health summaries, and ABHA card labels on the fly.

### 5. 🪪 ABDM ABHA Card & Regimes / Consent Manager
- **Official-Spec ABHA Card**: Features 14-digit ABHA Number (`XX-XXXX-XXXX-XXXX`), unique ABHA address (`user@abdm`), user photo, demographic details, and official NHA styling with Indian Tricolor bar.
- **Interactive 3D Flip Card**: Click to flip between Front (identity) and Back (scannable QR code & NHA verification details).
- **Dynamic Scannable QR Code**: Embeds NHA FHIR-compliant demographic payload.
- **Print & Download**: 1-click printable and saveable card badge.
- **ABDM Regimes & Consent Manager**: Explains the 5 core ABDM health regimes (OPD Consultations, Diagnostic Reports, Discharge Summaries, Immunization, e-Prescriptions) with interactive **Grant Access** / **Revoke Access** toggles for linked hospitals and diagnostic centers.

### 6. 🔐 Frictionless Authentication & Demo Profiles
- Sign in with Email, Mobile number, or 14-digit ABHA Number.
- Mobile OTP simulation toggle for instant testing.
- **1-Click Demo Patient Profiles**:
  - `Ramesh Kumar` (Senior Citizen, Type 2 Diabetes, pre-seeded lab reports, ABHA Card).
  - `Priya Sharma` (Young Professional, normal routine checkup, ABHA Card).
- User Registration wizard with automatic ABHA Number and Address generation.

---

## 🚀 Running the Application Locally

### 1. Prerequisites
Ensure Python is installed (Python 3.10+ recommended).

### 2. Dependencies
Install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Start the Server
Run the Flask server:
```bash
python app.py
```
Or double-click `run.bat`.

The application will start at:
```
http://127.0.0.1:5055
```

---

## 🧪 Automated Testing
Run the comprehensive test suite verifying all routes, APIs, and services:
```bash
python test_suite.py
```
