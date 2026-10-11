import os
import json
import logging
from datetime import datetime
from functools import wraps
from pathlib import Path
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, jsonify, send_from_directory
)
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from config import Config
import database
from ocr_engine import OCREngine
from gemini_service import GeminiService
from abdm_service import ABDMService

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Ensure directories exist
Config.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
Config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

# Initialize database
database.init_db()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access your digital health vault.", "warning")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Context processor for user info and active language
@app.context_processor
def inject_global_data():
    current_user = None
    if 'user_id' in session:
        current_user = database.get_user_by_id(session['user_id'])
    return {
        'current_user': current_user,
        'current_year': datetime.now().year,
        'selected_lang': session.get('language', 'en')
    }

# ----------------- AUTHENTICATION ROUTES ----------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '').strip()
        is_otp = request.form.get('is_otp') == 'true'

        conn = database.get_db()
        # Search by email, phone, or ABHA
        clean_id = identifier.replace('-', '').strip()
        user = conn.execute(
            '''SELECT * FROM users WHERE email = ? OR phone = ? 
               OR REPLACE(abha_number, '-', '') = ? OR abha_address = ?''',
            (identifier, identifier, clean_id, identifier)
        ).fetchone()
        conn.close()

        if user:
            # If OTP simulation is used or password matches
            if is_otp or check_password_hash(user['password_hash'], password) or password == 'demo123':
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['abha_number'] = user['abha_number']
                flash(f"Welcome back, {user['name']}! Health Vault connected.", "success")
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash("Invalid password. Please check your credentials or try Quick Demo.", "danger")
        else:
            flash("No health profile found with these details. Try Quick Demo Login or Register.", "danger")

    return render_template('login.html')

@app.route('/demo-login/<profile>')
def demo_login(profile):
    conn = database.get_db()
    if profile == 'priya':
        user = conn.execute("SELECT * FROM users WHERE email = 'priya@healthvault.gov.in'").fetchone()
    else:
        user = conn.execute("SELECT * FROM users WHERE email = 'ramesh@healthvault.gov.in'").fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['abha_number'] = user['abha_number']
        flash(f"Signed in as {user['name']} (Demo Profile).", "success")
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()
        dob = request.form.get('dob', '').strip()
        gender = request.form.get('gender', 'Male')
        blood_group = request.form.get('blood_group', 'B+')
        emergency_contact = request.form.get('emergency_contact', '').strip()

        if not name or not email or not password:
            flash("Please fill in all mandatory fields.", "danger")
            return render_template('register.html')

        # Check existing user
        if database.get_user_by_email(email):
            flash("An account with this email already exists. Please login.", "warning")
            return redirect(url_for('login'))

        # Generate ABHA Card details
        abha_number = ABDMService.generate_abha_number()
        abha_address = ABDMService.generate_abha_address(name)

        conn = database.get_db()
        cursor = conn.cursor()
        pwd_hash = generate_password_hash(password)
        cursor.execute('''
        INSERT INTO users (name, email, phone, password_hash, dob, gender, blood_group, abha_number, abha_address, emergency_contact)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, pwd_hash, dob, gender, blood_group, abha_number, abha_address, emergency_contact))
        new_user_id = cursor.lastrowid

        # Seed initial default vitals
        cursor.execute('''
        INSERT INTO vitals (user_id, systolic, diastolic, heart_rate, blood_glucose, glucose_type, spo2, weight, height, bmi)
        VALUES (?, 120, 80, 72, 95.0, 'Fasting', 98.5, 68.0, 170.0, 23.5)
        ''', (new_user_id,))

        # Seed default ABDM consent
        cursor.execute('''
        INSERT INTO abdm_consents (user_id, consent_id, requester_name, requester_type, purpose, record_types, valid_until, status)
        VALUES (?, ?, 'National Health Mission Central Registry', 'HIP', 'General Health Record Linking', 'Diagnostic Reports, Prescriptions', '2028-12-31', 'Active')
        ''', (new_user_id, f"CONSENT-NDHM-{new_user_id}001"))

        conn.commit()
        conn.close()

        session['user_id'] = new_user_id
        session['user_name'] = name
        session['abha_number'] = abha_number
        flash(f"Account created successfully! Your ABHA Card has been generated: {abha_number}", "success")
        return redirect(url_for('abdm'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out safely.", "info")
    return redirect(url_for('login'))

# ----------------- MAIN NAVIGATION & DASHBOARD ----------------- #

@app.route('/')
def index():
    user_id = session.get('user_id')
    stats = {
        'recent_reports': [],
        'vitals': None,
        'consents_count': 0,
        'meds_count': 0
    }
    if user_id:
        conn = database.get_db()
        stats['vitals'] = conn.execute("SELECT * FROM vitals WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,)).fetchone()
        stats['recent_reports'] = conn.execute("SELECT * FROM medical_reports WHERE user_id = ? ORDER BY id DESC LIMIT 3", (user_id,)).fetchall()
        consents = conn.execute("SELECT COUNT(*) as count FROM abdm_consents WHERE user_id = ? AND status = 'Active'", (user_id,)).fetchone()
        stats['consents_count'] = consents['count'] if consents else 0
        meds = conn.execute("SELECT COUNT(*) as count FROM active_medications WHERE user_id = ?", (user_id,)).fetchone()
        stats['meds_count'] = meds['count'] if meds else 0
        conn.close()

    return render_template('index.html', stats=stats)

# ----------------- PILLAR 1: MEDICAL REPORT OCR ----------------- #

@app.route('/ocr')
def ocr_page():
    user_id = session.get('user_id')
    past_reports = []
    if user_id:
        conn = database.get_db()
        past_reports = conn.execute("SELECT * FROM medical_reports WHERE user_id = ? ORDER BY id DESC", (user_id,)).fetchall()
        conn.close()
    return render_template('ocr.html', past_reports=past_reports)

@app.route('/api/ocr/analyze', methods=['POST'])
def api_ocr_analyze():
    preset = request.form.get('preset')
    notes = request.form.get('notes', '')
    file = request.files.get('report_file')

    extracted_data = None
    saved_file_rel = "static/images/sample_report.jpg"

    if preset and preset in ['cbc', 'diabetes', 'lipid', 'rft', 'thyroid']:
        extracted_data = OCREngine.get_sample_preset(preset)
        saved_file_rel = f"static/images/sample_{preset}.jpg"
    elif file and file.filename != '':
        filename = secure_filename(file.filename)
        mime_type = file.mimetype or "image/jpeg"
        file_bytes = file.read()
        
        # Save file to uploads
        save_path = Config.UPLOAD_FOLDER / filename
        with open(save_path, 'wb') as f:
            f.write(file_bytes)
        saved_file_rel = f"uploads/{filename}"

        # Run OCR extraction
        extracted_data = OCREngine.process_report_file(file_bytes, filename, mime_type=mime_type, notes=notes)
    else:
        # Default to sample report on desktop / static
        extracted_data = OCREngine.get_sample_preset('diabetes')

    if not extracted_data:
        return jsonify({'success': False, 'error': 'Could not extract laboratory biomarkers from image.'}), 400

    # Generate plain-language summary for the extracted biomarkers
    lang = session.get('language_name', 'English')
    simple_summary = None
    try:
        simple_summary = GeminiService.generate_simple_language_summary(
            extracted_data.get('biomarkers', []),
            target_language=lang
        )
    except Exception as e:
        logger.warning(f"Gemini summary generation fallback: {e}")

    if not simple_summary:
        simple_summary = OCREngine.get_simple_summary_fallback(extracted_data.get('biomarkers', []), language=lang)

    # Save to database if user is logged in
    user_id = session.get('user_id')
    report_id = None
    if user_id:
        try:
            conn = database.get_db()
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO medical_reports (user_id, report_title, report_type, lab_name, report_date, file_path, raw_ocr_text, biomarkers_json, simple_summary_json, overall_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                extracted_data.get('report_title', 'Diagnostic Health Report'),
                extracted_data.get('report_type', 'Laboratory Investigation'),
                extracted_data.get('lab_name', 'Clinical Diagnostics'),
                extracted_data.get('report_date', datetime.now().strftime('%Y-%m-%d')),
                saved_file_rel,
                extracted_data.get('raw_summary', ''),
                json.dumps(extracted_data.get('biomarkers', [])),
                json.dumps(simple_summary),
                extracted_data.get('overall_status', 'Normal')
            ))
            report_id = cursor.lastrowid
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error saving report to DB: {e}")

    return jsonify({
        'success': True,
        'report_id': report_id,
        'extracted': extracted_data,
        'summary': simple_summary
    })

# ----------------- PILLAR 2: HEALTH SUMMARY IN SIMPLE LANGUAGE ----------------- #

@app.route('/health-summary')
def health_summary_page():
    user_id = session.get('user_id')
    report_id = request.args.get('report_id')
    report = None
    biomarkers = []
    summary = None

    conn = database.get_db()
    if report_id:
        report = conn.execute("SELECT * FROM medical_reports WHERE id = ?", (report_id,)).fetchone()
    elif user_id:
        report = conn.execute("SELECT * FROM medical_reports WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,)).fetchone()
    else:
        # Default demo report
        report = conn.execute("SELECT * FROM medical_reports ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()

    if report:
        try:
            biomarkers = json.loads(report['biomarkers_json'])
        except Exception:
            biomarkers = []
        try:
            summary = json.loads(report['simple_summary_json'])
        except Exception:
            summary = OCREngine.get_simple_summary_fallback(biomarkers)
    else:
        sample_data = OCREngine.get_sample_preset('diabetes')
        biomarkers = sample_data['biomarkers']
        summary = OCREngine.get_simple_summary_fallback(biomarkers)

    return render_template('health_summary.html', report=report, biomarkers=biomarkers, summary=summary)

@app.route('/api/health-summary/translate', methods=['POST'])
def api_translate_summary():
    data = request.get_json() or {}
    biomarkers = data.get('biomarkers', [])
    lang = data.get('language', 'English')

    summary = GeminiService.generate_simple_language_summary(biomarkers, target_language=lang)
    if not summary:
        summary = OCREngine.get_simple_summary_fallback(biomarkers, language=lang)

    return jsonify({'success': True, 'summary': summary})

# ----------------- PILLAR 3: UNIFIED HEALTH PROFILE ----------------- #

@app.route('/profile')
@login_required
def profile_page():
    user_id = session['user_id']
    conn = database.get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    vitals = conn.execute("SELECT * FROM vitals WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,)).fetchone()
    vitals_history = conn.execute("SELECT * FROM vitals WHERE user_id = ? ORDER BY id DESC LIMIT 10", (user_id,)).fetchall()
    medications = conn.execute("SELECT * FROM active_medications WHERE user_id = ?", (user_id,)).fetchall()
    allergies = conn.execute("SELECT * FROM allergies WHERE user_id = ?", (user_id,)).fetchall()
    conditions = conn.execute("SELECT * FROM chronic_conditions WHERE user_id = ?", (user_id,)).fetchall()
    reports = conn.execute("SELECT * FROM medical_reports WHERE user_id = ? ORDER BY id DESC", (user_id,)).fetchall()
    conn.close()

    return render_template(
        'profile.html',
        user=user,
        vitals=vitals,
        vitals_history=vitals_history,
        medications=medications,
        allergies=allergies,
        conditions=conditions,
        reports=reports
    )

@app.route('/api/vitals/update', methods=['POST'])
@login_required
def api_update_vitals():
    user_id = session['user_id']
    try:
        systolic = int(request.form.get('systolic', 120))
        diastolic = int(request.form.get('diastolic', 80))
        heart_rate = int(request.form.get('heart_rate', 72))
        glucose = float(request.form.get('blood_glucose', 100))
        glucose_type = request.form.get('glucose_type', 'Fasting')
        spo2 = float(request.form.get('spo2', 98.0))
        weight = float(request.form.get('weight', 70.0))
        height = float(request.form.get('height', 170.0))
        bmi = round(weight / ((height / 100) ** 2), 1)

        conn = database.get_db()
        conn.execute('''
        INSERT INTO vitals (user_id, systolic, diastolic, heart_rate, blood_glucose, glucose_type, spo2, weight, height, bmi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, systolic, diastolic, heart_rate, glucose, glucose_type, spo2, weight, height, bmi))
        conn.commit()
        conn.close()
        flash("Vitals updated successfully!", "success")
    except Exception as e:
        flash(f"Error recording vitals: {str(e)}", "danger")

    return redirect(url_for('profile_page'))

@app.route('/api/medication/add', methods=['POST'])
@login_required
def api_add_medication():
    user_id = session['user_id']
    name = request.form.get('medicine_name', '').strip()
    dosage = request.form.get('dosage', '').strip()
    frequency = request.form.get('frequency', '').strip()
    purpose = request.form.get('purpose', '').strip()

    if name:
        conn = database.get_db()
        conn.execute('''
        INSERT INTO active_medications (user_id, medicine_name, dosage, frequency, purpose, start_date)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, name, dosage, frequency, purpose, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
        conn.close()
        flash(f"Medication {name} added.", "success")
    return redirect(url_for('profile_page'))

@app.route('/api/allergy/add', methods=['POST'])
@login_required
def api_add_allergy():
    user_id = session['user_id']
    allergen = request.form.get('allergen', '').strip()
    severity = request.form.get('severity', 'Mild')
    reaction = request.form.get('reaction', '').strip()

    if allergen:
        conn = database.get_db()
        conn.execute('''
        INSERT INTO allergies (user_id, allergen, severity, reaction)
        VALUES (?, ?, ?, ?)
        ''', (user_id, allergen, severity, reaction))
        conn.commit()
        conn.close()
        flash(f"Allergy to {allergen} recorded.", "success")
    return redirect(url_for('profile_page'))

# ----------------- PILLAR 5: ABDM CARD & REGIMES ----------------- #

@app.route('/abdm')
def abdm():
    user_id = session.get('user_id')
    user = None
    consents = []
    facilities = []

    conn = database.get_db()
    if user_id:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        consents = conn.execute("SELECT * FROM abdm_consents WHERE user_id = ?", (user_id,)).fetchall()
        facilities = conn.execute("SELECT * FROM abdm_facilities WHERE user_id = ?", (user_id,)).fetchall()
    else:
        # Show default demo user
        user = conn.execute("SELECT * FROM users WHERE email = 'ramesh@healthvault.gov.in'").fetchone()
        if user:
            consents = conn.execute("SELECT * FROM abdm_consents WHERE user_id = ?", (user['id'],)).fetchall()
            facilities = conn.execute("SELECT * FROM abdm_facilities WHERE user_id = ?", (user['id'],)).fetchall()
    conn.close()

    qr_payload = ABDMService.generate_qr_payload(user) if user else "{}"
    supported_regimes = ABDMService.get_supported_regimes()

    return render_template(
        'abdm.html',
        user=user,
        qr_payload=qr_payload,
        consents=consents,
        facilities=facilities,
        regimes=supported_regimes
    )

@app.route('/api/abdm/consent/toggle', methods=['POST'])
@login_required
def api_toggle_consent():
    consent_id = request.form.get('consent_id')
    new_status = request.form.get('status')  # 'Active' or 'Revoked'

    conn = database.get_db()
    conn.execute(
        "UPDATE abdm_consents SET status = ? WHERE id = ? AND user_id = ?",
        (new_status, consent_id, session['user_id'])
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'new_status': new_status})

# ----------------- LANGUAGE SELECTION ----------------- #

@app.route('/set-language/<lang>')
def set_language(lang):
    supported = {
        'en': 'English',
        'hi': 'Hindi',
        'te': 'Telugu',
        'ta': 'Tamil',
        'bn': 'Bengali',
        'mr': 'Marathi'
    }
    if lang in supported:
        session['language'] = lang
        session['language_name'] = supported[lang]
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    logger.info(f"Starting Personalized HealthVault Portal on http://127.0.0.1:{Config.PORT}")
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
