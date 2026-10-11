import sqlite3
import json
import logging
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

logger = logging.getLogger(__name__)

def get_db():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    Config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_db()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        password_hash TEXT NOT NULL,
        dob TEXT,
        gender TEXT,
        blood_group TEXT,
        abha_number TEXT,
        abha_address TEXT,
        emergency_contact TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Vitals Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vitals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        systolic INTEGER,
        diastolic INTEGER,
        heart_rate INTEGER,
        blood_glucose REAL,
        glucose_type TEXT,
        spo2 REAL,
        weight REAL,
        height REAL,
        bmi REAL,
        recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # Medical Reports Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medical_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        report_title TEXT NOT NULL,
        report_type TEXT,
        lab_name TEXT,
        report_date TEXT,
        file_path TEXT,
        raw_ocr_text TEXT,
        biomarkers_json TEXT,
        simple_summary_json TEXT,
        overall_status TEXT DEFAULT 'Normal',
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # Active Medications
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS active_medications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        medicine_name TEXT NOT NULL,
        dosage TEXT,
        frequency TEXT,
        purpose TEXT,
        start_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # Allergies
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS allergies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        allergen TEXT NOT NULL,
        severity TEXT,
        reaction TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # Chronic Conditions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chronic_conditions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        condition_name TEXT NOT NULL,
        diagnosed_year TEXT,
        status TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # ABDM Consents / Regimes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS abdm_consents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        consent_id TEXT NOT NULL,
        requester_name TEXT NOT NULL,
        requester_type TEXT NOT NULL,
        purpose TEXT NOT NULL,
        record_types TEXT NOT NULL,
        valid_until TEXT NOT NULL,
        status TEXT DEFAULT 'Active',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # ABDM Linked Facilities
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS abdm_facilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        facility_name TEXT NOT NULL,
        facility_id TEXT NOT NULL,
        records_count INTEGER DEFAULT 0,
        linked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    seed_demo_data(cursor, conn)
    conn.close()
    logger.info("Database initialized successfully.")

def seed_demo_data(cursor, conn):
    # Check if demo user exists
    cursor.execute("SELECT id FROM users WHERE email = 'ramesh@healthvault.gov.in'")
    if cursor.fetchone():
        return  # already seeded

    # Seed User 1: Ramesh Kumar
    pwd1 = generate_password_hash("ramesh123")
    cursor.execute('''
    INSERT INTO users (name, email, phone, password_hash, dob, gender, blood_group, abha_number, abha_address, emergency_contact)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        "Ramesh Kumar",
        "ramesh@healthvault.gov.in",
        "+91 98765 43210",
        pwd1,
        "1968-08-15",
        "Male",
        "B+",
        "14-8291-5021-9482",
        "ramesh.kumar@abdm",
        "+91 98111 22334 (Son - Amit Kumar)"
    ))
    user1_id = cursor.lastrowid

    # Vitals for Ramesh
    cursor.execute('''
    INSERT INTO vitals (user_id, systolic, diastolic, heart_rate, blood_glucose, glucose_type, spo2, weight, height, bmi)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user1_id, 134, 86, 74, 142.0, "Fasting", 98.0, 76.5, 172.0, 25.9))

    # Medications for Ramesh
    meds1 = [
        ("Metformin", "500 mg", "Twice daily (after meals)", "Blood Glucose Regulation", "2023-04-10"),
        ("Telmisartan", "40 mg", "Once daily (morning)", "Hypertension Management", "2022-11-05"),
        ("Atorvastatin", "10 mg", "Once daily (night)", "Cholesterol Management", "2024-01-18")
    ]
    cursor.executemany('''
    INSERT INTO active_medications (user_id, medicine_name, dosage, frequency, purpose, start_date)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', [(user1_id, *m) for m in meds1])

    # Allergies for Ramesh
    allergies1 = [
        ("Penicillin", "Severe", "Anaphylaxis / Breathing difficulty"),
        ("Dust Mites", "Mild", "Sneezing & rhinitis")
    ]
    cursor.executemany('''
    INSERT INTO allergies (user_id, allergen, severity, reaction)
    VALUES (?, ?, ?, ?)
    ''', [(user1_id, *a) for a in allergies1])

    # Chronic conditions for Ramesh
    conditions1 = [
        ("Type 2 Diabetes Mellitus", "2021", "Managed on oral medication"),
        ("Essential Hypertension", "2020", "Stable with lifestyle & Telmisartan")
    ]
    cursor.executemany('''
    INSERT INTO chronic_conditions (user_id, condition_name, diagnosed_year, status)
    VALUES (?, ?, ?, ?)
    ''', [(user1_id, *c) for c in conditions1])

    # Seed Sample Medical Report for Ramesh
    sample_biomarkers = [
        {"parameter": "Fasting Blood Sugar", "value": "142", "unit": "mg/dL", "ref_range": "70 - 100", "status": "High"},
        {"parameter": "HbA1c (Glycated Hemoglobin)", "value": "7.3", "unit": "%", "ref_range": "4.0 - 5.6", "status": "High"},
        {"parameter": "Total Cholesterol", "value": "218", "unit": "mg/dL", "ref_range": "125 - 200", "status": "Borderline"},
        {"parameter": "LDL Cholesterol", "value": "138", "unit": "mg/dL", "ref_range": "0 - 100", "status": "Borderline"},
        {"parameter": "HDL Cholesterol (Good)", "value": "44", "unit": "mg/dL", "ref_range": "40 - 60", "status": "Normal"},
        {"parameter": "Serum Creatinine", "value": "0.9", "unit": "mg/dL", "ref_range": "0.7 - 1.3", "status": "Normal"},
        {"parameter": "Hemoglobin", "value": "13.8", "unit": "g/dL", "ref_range": "13.0 - 17.0", "status": "Normal"}
    ]
    sample_summary = {
        "overview": "Your blood test indicates that your kidneys and liver are functioning normally, but your blood sugar levels and HbA1c are elevated above standard targets.",
        "attention_points": [
            "Fasting glucose is 142 mg/dL (target is under 100 mg/dL for non-diabetic; discuss personal targets with physician).",
            "HbA1c is 7.3%, showing that average blood sugar over the last 3 months has been slightly higher than recommended.",
            "Total cholesterol is mildly borderline at 218 mg/dL."
        ],
        "lifestyle_tips": [
            "Focus on low-glycemic, fiber-rich whole grains and legumes.",
            "Incorporate a 30-minute brisk walk daily after meals.",
            "Limit refined sugars and processed carbohydrate snacks."
        ],
        "doctor_questions": [
            "Should we adjust the Metformin dosage in light of this 7.3% HbA1c?",
            "Do I need a repeat lipid profile check in 3 months?",
            "Should I start using a home continuous glucose monitor?"
        ]
    }

    cursor.execute('''
    INSERT INTO medical_reports (user_id, report_title, report_type, lab_name, report_date, file_path, raw_ocr_text, biomarkers_json, simple_summary_json, overall_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user1_id,
        "Comprehensive Metabolic & Diabetic Lab Panel",
        "Metabolic / Diabetes",
        "Apollo Health City Laboratories",
        "2026-09-28",
        "static/images/sample_report.jpg",
        "Apollo Labs: Fasting Sugar 142 mg/dL, HbA1c 7.3%, Cholesterol 218 mg/dL, Creatinine 0.9 mg/dL",
        json.dumps(sample_biomarkers),
        json.dumps(sample_summary),
        "Attention Needed"
    ))

    # ABDM Consents for Ramesh
    consents1 = [
        ("CONSENT-NDHM-9021", "Apollo Hospitals Cardiology OPD", "HIU", "Follow-up Cardiac & Glycemic Assessment", "Diagnostic Reports, OPD Prescriptions", "2026-12-31", "Active"),
        ("CONSENT-NDHM-8814", "AIIMS New Delhi Teleconsultation", "HIU", "Specialist Diabetic Second Opinion", "Lab Reports, Vitals History", "2026-11-15", "Active"),
        ("CONSENT-NDHM-7102", "Max Diagnostics Gurgaon", "HIP", "Lab Report Syncing into Health Locker", "Diagnostic Reports", "2026-10-30", "Revoked")
    ]
    cursor.executemany('''
    INSERT INTO abdm_consents (user_id, consent_id, requester_name, requester_type, purpose, record_types, valid_until, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', [(user1_id, *c) for c in consents1])

    # ABDM Facilities for Ramesh
    facilities1 = [
        ("Apollo Health City, Hyderabad", "IN03600021", 5),
        ("Metropolis Diagnostic Center", "IN03600499", 3),
        ("AIIMS OPD Network", "IN00100001", 2)
    ]
    cursor.executemany('''
    INSERT INTO abdm_facilities (user_id, facility_name, facility_id, records_count)
    VALUES (?, ?, ?, ?)
    ''', [(user1_id, *f) for f in facilities1])

    # Seed User 2: Priya Sharma
    pwd2 = generate_password_hash("priya123")
    cursor.execute('''
    INSERT INTO users (name, email, phone, password_hash, dob, gender, blood_group, abha_number, abha_address, emergency_contact)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        "Priya Sharma",
        "priya@healthvault.gov.in",
        "+91 99887 76655",
        pwd2,
        "1996-03-22",
        "Female",
        "O+",
        "23-9182-4412-8801",
        "priya.sharma@abdm",
        "+91 99880 11223 (Sister - Neha Sharma)"
    ))
    user2_id = cursor.lastrowid

    # Vitals for Priya
    cursor.execute('''
    INSERT INTO vitals (user_id, systolic, diastolic, heart_rate, blood_glucose, glucose_type, spo2, weight, height, bmi)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user2_id, 118, 76, 70, 88.0, "Fasting", 99.0, 56.0, 165.0, 20.6))

    conn.commit()

# Helper accessors
def get_user_by_email(email):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user

def get_user_by_abha(abha):
    conn = get_db()
    clean_abha = abha.replace("-", "").strip()
    user = conn.execute(
        "SELECT * FROM users WHERE REPLACE(abha_number, '-', '') = ? OR abha_address = ?",
        (clean_abha, abha)
    ).fetchone()
    conn.close()
    return user
