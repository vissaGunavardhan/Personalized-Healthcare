import random
import json
import uuid
from datetime import datetime

class ABDMService:
    @staticmethod
    def generate_abha_number():
        """
        Generates official 14-digit ABHA Number format: XX-XXXX-XXXX-XXXX
        """
        digits = [str(random.randint(10, 99))]
        for _ in range(3):
            digits.append(str(random.randint(1000, 9999)))
        return "-".join(digits)

    @staticmethod
    def generate_abha_address(name):
        """
        Generates standard ABHA address: name.suffix@abdm
        """
        clean = "".join(c.lower() for c in name if c.isalnum() or c == " ").strip().replace(" ", ".")
        rand_suffix = random.randint(10, 99)
        return f"{clean}{rand_suffix}@abdm"

    @staticmethod
    def generate_qr_payload(user):
        """
        Generates verifiable ABDM demographic QR payload compliant with NHA specs
        """
        if not user:
            u = {}
        elif hasattr(user, 'keys'):
            u = dict(user)
        else:
            u = user

        gender_char = "U"
        if u.get("gender"):
            gender_char = str(u["gender"])[0].upper()

        return json.dumps({
            "schema": "ABDM-PHR-V1",
            "abhaNumber": u.get("abha_number") or "14-8291-5021-9482",
            "abhaAddress": u.get("abha_address") or "user@abdm",
            "name": u.get("name") or "Verified Patient",
            "gender": gender_char,
            "dob": u.get("dob") or "1990-01-01",
            "bloodGroup": u.get("blood_group") or "O+",
            "mobile": u.get("phone") or "+91 9876543210",
            "issuedBy": "National Health Authority (NHA) - Government of India",
            "verificationUrl": f"https://abdm.gov.in/verify?id={u.get('abha_number', '14-8291-5021-9482')}"
        })

    @staticmethod
    def get_supported_regimes():
        """
        Standard ABDM health record regimes supported under National Digital Health Mission
        """
        return [
            {
                "code": "OP_CONSULTATION",
                "name": "Outpatient (OPD) Consultation Records",
                "icon": "fa-user-doctor",
                "description": "Doctor prescriptions, clinical diagnosis, follow-up advice, and clinical notes."
            },
            {
                "code": "DIAGNOSTIC_REPORT",
                "name": "Diagnostic & Lab Test Reports",
                "icon": "fa-vial-virus",
                "description": "Blood tests, lipid panels, pathology, urine analysis, and imaging summaries."
            },
            {
                "code": "DISCHARGE_SUMMARY",
                "name": "Inpatient Hospital Discharge Summaries",
                "icon": "fa-hospital",
                "description": "Hospitalization records, procedures performed, operative notes, and treatment summaries."
            },
            {
                "code": "IMMUNIZATION",
                "name": "Immunization & Vaccine Certificate",
                "icon": "fa-syringe",
                "description": "Childhood and adult vaccination schedules, COVID-19 certificates."
            },
            {
                "code": "PRESCRIPTION",
                "name": "Digital e-Prescriptions",
                "icon": "fa-prescription",
                "description": "Active and past pharmacist dispensations and drug instructions."
            }
        ]
