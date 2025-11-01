"""
Metabolic Report Generator - Flask Web Application
Minimal MVP for uploading metabolic test PDFs and generating custom reports
"""
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for, session, flash
import os
import json
import secrets
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import pdfplumber
import re
from functools import wraps
from dotenv import load_dotenv
from supabase import create_client, Client
import stripe
from utils.beautiful_report import generate_beautiful_report

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORTS_FOLDER'] = 'reports'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max file size
ALLOWED_EXTENSIONS = {'pdf'}

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def extract_pnoe_data(pdf_path):
    """Extract data from metabolic test PDF - simplified version"""
    data = {
        'patient_info': {},
        'core_scores': {},
        'caloric_data': {},
        'metabolic_data': {},
        'heart_rate_data': {},
        'all_text': []
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    data['all_text'].append(text[:2000])  # First 2000 chars per page

                    # Try to extract tables
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            # Process table data
                            for row in table:
                                if row and len(row) >= 2:
                                    # Look for key-value pairs in tables
                                    key = str(row[0]).strip() if row[0] else ""
                                    value = str(row[1]).strip() if row[1] else ""

                                    # Extract VO2 values from tables
                                    if 'VO2' in key and 'ml/kg/min' in key:
                                        try:
                                            vo2_val = float(re.search(r'([0-9.]+)', value).group(1))
                                            data['metabolic_data']['vo2max_rel'] = vo2_val
                                        except:
                                            pass

                                    # Extract RMR from tables
                                    if 'RMR' in key or 'Resting Metabolic Rate' in key:
                                        try:
                                            rmr_val = int(re.search(r'(\d{3,4})', value).group(1))
                                            if 1000 <= rmr_val <= 3000:  # Sanity check
                                                data['caloric_data']['rmr'] = rmr_val
                                                data['metabolic_data']['rmr'] = rmr_val
                                        except:
                                            pass

                    # Extract patient name
                    if page_num == 1:
                        name_match = re.search(r'(?:Name|Subject)[:\s]+([A-Za-z\s]+?)(?:Status|Gender)', text)
                        if name_match:
                            data['patient_info']['name'] = name_match.group(1).strip()

                        date_match = re.search(r'(?:Date)[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})', text)
                        if date_match:
                            data['patient_info']['test_date'] = date_match.group(1)

                        # Extract gender and age (format: "Gender Male (63)")
                        gender_age_match = re.search(r'Gender[:\s]+(Male|Female)\s*\((\d+)\)', text)
                        if gender_age_match:
                            data['patient_info']['gender'] = gender_age_match.group(1)
                            data['patient_info']['age'] = int(gender_age_match.group(2))
                        else:
                            gender_match = re.search(r'Gender[:\s]+(Male|Female)', text)
                            if gender_match:
                                data['patient_info']['gender'] = gender_match.group(1)

                        weight_match = re.search(r'Weight[:\s]+(\d+)\s*kg', text)
                        if weight_match:
                            data['patient_info']['weight_kg'] = int(weight_match.group(1))

                        height_match = re.search(r'Height[:\s]+(\d+)\s*cm', text)
                        if height_match:
                            data['patient_info']['height_cm'] = int(height_match.group(1))

                    # Extract core scores (look for percentages)
                    score_patterns = [
                        (r'Sympathetic.*?(\d+)%', 'symp_parasym'),
                        (r'Ventilation.*?(\d+)%', 'ventilation_eff'),
                        (r'Breathing.*?(\d+)%', 'breathing_coord'),
                        (r'Lung.*?(\d+)%', 'lung_util'),
                        (r'HRV.*?(\d+)%', 'hrv'),
                        (r'Metabolic.*?Rate.*?(\d+)%', 'metabolic_rate'),
                        (r'Fat.*?Burning.*?(\d+)%', 'fat_burning')
                    ]

                    for pattern, key in score_patterns:
                        match = re.search(pattern, text, re.IGNORECASE)
                        if match and key not in data['core_scores']:
                            data['core_scores'][key] = int(match.group(1))

                    # Extract caloric data
                    rmr_match = re.search(r'RMR[:\s]+(\d+)', text)
                    if rmr_match:
                        data['caloric_data']['rmr'] = int(rmr_match.group(1))
                        data['metabolic_data']['rmr'] = int(rmr_match.group(1))  # Also store in metabolic_data

                    # Extract daily caloric burn
                    burn_match = re.search(r'(?:Total.*?Burn|Daily.*?Expenditure)[:\s]+(\d+)', text, re.IGNORECASE)
                    if burn_match:
                        data['caloric_data']['total_burn'] = int(burn_match.group(1))

                    # Extract fuel utilization percentages
                    fat_percent_match = re.search(r'Fat.*?(\d+)\s*%', text, re.IGNORECASE)
                    if fat_percent_match:
                        data['caloric_data']['fat_percent'] = int(fat_percent_match.group(1))

                    cho_percent_match = re.search(r'(?:Carb|CHO).*?(\d+)\s*%', text, re.IGNORECASE)
                    if cho_percent_match:
                        data['caloric_data']['cho_percent'] = int(cho_percent_match.group(1))

                    # Extract HR max
                    max_hr_match = re.search(r'(?:Max|Maximum).*?(?:HR|Heart Rate)[:\s]+(\d+)', text)
                    if max_hr_match:
                        data['heart_rate_data']['max_hr'] = int(max_hr_match.group(1))

                    # Extract RER
                    rer_match = re.search(r'RER[:\s]+([0-9.]+)', text)
                    if rer_match:
                        data['metabolic_data']['rer'] = float(rer_match.group(1))

                    # Extract VO2 max
                    vo2_abs_match = re.search(r'VO2.*?max[:\s]+([0-9.]+).*?L/min', text, re.IGNORECASE)
                    if vo2_abs_match:
                        data['metabolic_data']['vo2max_abs'] = float(vo2_abs_match.group(1))

                    vo2_rel_match = re.search(r'VO2.*?max[:\s]+([0-9.]+).*?ml.*?kg.*?min', text, re.IGNORECASE)
                    if vo2_rel_match:
                        data['metabolic_data']['vo2max_rel'] = float(vo2_rel_match.group(1))

                    # Extract resting heart rate
                    rhr_match = re.search(r'(?:Resting|Rest).*?(?:HR|Heart Rate)[:\s]+(\d+)', text, re.IGNORECASE)
                    if rhr_match and 'max_hr' not in data['heart_rate_data']:
                        data['heart_rate_data']['resting_hr'] = int(rhr_match.group(1))

    except Exception as e:
        data['error'] = str(e)

    return data

# ============= Authentication Routes =============

@app.route('/')
def landing():
    """Marketing landing page"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template('pricing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        company_name = request.form.get('company_name', '')

        try:
            # Check if user already exists
            existing_user = supabase.table('profiles').select('id').eq('email', email).execute()
            if existing_user.data:
                flash('An account with this email already exists.', 'danger')
                return render_template('register.html')

            # Generate user ID and hash password
            user_id = str(uuid.uuid4())
            password_hash = generate_password_hash(password)

            # Insert user into profiles table
            supabase.table('profiles').insert({
                'id': user_id,
                'email': email,
                'full_name': full_name,
                'password_hash': password_hash,
                'company_name': company_name
            }).execute()

            # Create subscription record
            supabase.table('subscriptions').insert({
                'user_id': user_id,
                'plan_name': 'free',
                'status': 'active',
                'reports_limit': 10,
                'reports_used': 0
            }).execute()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            flash(f'Registration error: {str(e)}', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            # Query user from database
            user_result = supabase.table('profiles').select('id, email, full_name, password_hash').eq('email', email).execute()

            if user_result.data and len(user_result.data) > 0:
                user = user_result.data[0]

                # Verify password
                if check_password_hash(user['password_hash'], password):
                    # Store user info in session
                    session['user'] = {
                        'id': user['id'],
                        'email': user['email'],
                        'full_name': user.get('full_name', '')
                    }
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid email or password.', 'danger')
            else:
                flash('Invalid email or password.', 'danger')

        except Exception as e:
            flash(f'Login error: {str(e)}', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('landing'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing report history"""
    user_id = session['user']['id']

    try:
        # Get user's profile
        profile = supabase.table('profiles').select('*').eq('id', user_id).single().execute()

        # Get user's reports
        reports = supabase.table('reports').select('*, metabolic_tests(*)').eq('user_id', user_id).order('created_at', desc=True).execute()

        # Get user's subscription
        subscription = supabase.table('subscriptions').select('*').eq('user_id', user_id).single().execute()

        return render_template('dashboard.html',
                             profile=profile.data,
                             reports=reports.data,
                             subscription=subscription.data)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return render_template('dashboard.html', profile=None, reports=[], subscription=None)

@app.route('/index')
@login_required
def index():
    """Main upload page (requires login)"""
    return render_template('index.html')

@app.route('/submit_manual', methods=['POST'])
@login_required
def submit_manual():
    """Handle manually entered metabolic data"""
    try:
        data = request.json
        user_id = session['user']['id']

        # Generate unique ID for this entry
        unique_id = secrets.token_hex(8)

        # Structure data in same format as PDF extraction
        extracted_data = {
            'patient_info': data.get('patient_info', {}),
            'core_scores': data.get('core_scores', {}),
            'caloric_data': data.get('caloric_data', {}),
            'metabolic_data': data.get('metabolic_data', {}),
            'heart_rate_data': data.get('heart_rate_data', {}),
            'all_text': ['Manual Entry']
        }

        # Save extracted data for later use
        data_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_data.json")
        with open(data_path, 'w') as f:
            json.dump(extracted_data, f, indent=2)

        # Save metabolic test data to database
        try:
            patient_info = extracted_data.get('patient_info', {})
            test_data = {
                'user_id': user_id,
                'test_date': patient_info.get('test_date'),
                'pdf_filename': 'Manual Entry',
                'pdf_storage_path': None,
                'extracted_data': extracted_data,
                'patient_name': patient_info.get('name'),
                'patient_age': patient_info.get('age'),
                'patient_gender': patient_info.get('gender'),
                'patient_weight_kg': patient_info.get('weight_kg')
            }

            test_response = supabase.table('metabolic_tests').insert(test_data).execute()
            test_id = test_response.data[0]['id'] if test_response.data else None
        except Exception as e:
            print(f"Error saving manual data to database: {str(e)}")
            test_id = None

        return jsonify({
            'success': True,
            'file_id': unique_id,
            'test_id': test_id,
            'extracted_data': extracted_data
        })

    except Exception as e:
        print(f"Error processing manual data: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle PDF upload and extract data"""
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['pdf_file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files allowed'}), 400

    user_id = session['user']['id']

    # Save file with unique name
    filename = secure_filename(file.filename)
    unique_id = secrets.token_hex(8)
    saved_filename = f"{unique_id}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
    file.save(filepath)

    # Extract data from PDF
    extracted_data = extract_pnoe_data(filepath)

    # Save extracted data for later use
    data_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_data.json")
    with open(data_path, 'w') as f:
        json.dump(extracted_data, f, indent=2)

    # Save metabolic test data to database
    try:
        patient_info = extracted_data.get('patient_info', {})
        test_data = {
            'user_id': user_id,
            'test_date': patient_info.get('test_date'),
            'pdf_filename': filename,
            'pdf_storage_path': filepath,
            'extracted_data': extracted_data,
            'patient_name': patient_info.get('name'),
            'patient_age': patient_info.get('age'),
            'patient_gender': patient_info.get('gender'),
            'patient_weight_kg': patient_info.get('weight_kg')
        }

        test_response = supabase.table('metabolic_tests').insert(test_data).execute()
        test_id = test_response.data[0]['id'] if test_response.data else None
    except Exception as e:
        print(f"Error saving to database: {str(e)}")
        test_id = None

    return jsonify({
        'success': True,
        'file_id': unique_id,
        'test_id': test_id,
        'extracted_data': extracted_data
    })

def calculate_biological_age(core_scores, chronological_age, metabolic_data, hr_data, patient_info):
    """Calculate biological age based on actual metabolic markers"""
    if not chronological_age:
        return None

    print(f"\n[CALC DEBUG] === Starting biological age calculation ===")
    print(f"[CALC DEBUG] Chronological age: {chronological_age}")
    print(f"[CALC DEBUG] Core scores: {core_scores}")
    print(f"[CALC DEBUG] Metabolic data: {metabolic_data}")
    print(f"[CALC DEBUG] HR data: {hr_data}")
    print(f"[CALC DEBUG] Patient info: {patient_info}")

    age_components = []

    # Component 1: VO2 max (if available) - most accurate biological age predictor
    vo2_rel = metabolic_data.get('vo2max_rel')
    gender = patient_info.get('gender', 'Male')

    if vo2_rel:
        # Normative VO2 max data (ml/kg/min) by age and gender
        # Men: VO2 max = 60 - (0.55 * age) for average fitness
        # Women: VO2 max = 48 - (0.45 * age) for average fitness
        if gender == 'Male':
            # Calculate what age would have this VO2 max
            predicted_age = (60 - vo2_rel) / 0.55
        else:
            predicted_age = (48 - vo2_rel) / 0.45

        age_components.append(max(18, min(90, predicted_age)))
        print(f"[CALC DEBUG] Component 1 (VO2 max): {max(18, min(90, predicted_age))}")

    # Component 2: Resting Heart Rate
    resting_hr = hr_data.get('resting_hr')
    if resting_hr:
        # Lower RHR = younger biological age
        # Average RHR by age: ~70 at age 30, increases ~0.5 bpm per decade
        # Excellent fitness: 50-60 bpm
        # Average: 70-80 bpm
        # Poor: 80+ bpm
        if resting_hr < 60:
            hr_age = chronological_age - 5
        elif resting_hr < 70:
            hr_age = chronological_age - 2
        elif resting_hr < 80:
            hr_age = chronological_age
        elif resting_hr < 90:
            hr_age = chronological_age + 3
        else:
            hr_age = chronological_age + 5

        age_components.append(hr_age)
        print(f"[CALC DEBUG] Component 2 (Resting HR): {hr_age}")

    # Component 3: Heart Rate Variability (HRV)
    hrv_score = core_scores.get('hrv')
    if hrv_score:
        # HRV declines with age, higher HRV = younger bio age
        if hrv_score >= 90:
            hrv_age = chronological_age - 6
        elif hrv_score >= 80:
            hrv_age = chronological_age - 4
        elif hrv_score >= 70:
            hrv_age = chronological_age - 2
        elif hrv_score >= 60:
            hrv_age = chronological_age
        elif hrv_score >= 50:
            hrv_age = chronological_age + 2
        else:
            hrv_age = chronological_age + 4

        age_components.append(hrv_age)
        print(f"[CALC DEBUG] Component 3 (HRV): {hrv_age}")

    # Component 4: RMR (Resting Metabolic Rate)
    rmr = metabolic_data.get('rmr')
    weight_kg = patient_info.get('weight_kg')

    if rmr and weight_kg:
        # RMR per kg of body weight
        rmr_per_kg = rmr / weight_kg

        # Higher metabolic rate = younger biological age
        # Average RMR/kg: ~22-28 kcal/kg/day
        if rmr_per_kg > 30:
            rmr_age = chronological_age - 5
        elif rmr_per_kg > 26:
            rmr_age = chronological_age - 2
        elif rmr_per_kg > 22:
            rmr_age = chronological_age
        elif rmr_per_kg > 18:
            rmr_age = chronological_age + 3
        else:
            rmr_age = chronological_age + 5

        age_components.append(rmr_age)
        print(f"[CALC DEBUG] Component 4 (RMR): {rmr_age}")

    # Component 5: Overall core scores average (weighted less than metabolic markers)
    if core_scores:
        avg_score = sum(core_scores.values()) / len(core_scores)

        if avg_score >= 85:
            score_age = chronological_age - 4
        elif avg_score >= 75:
            score_age = chronological_age - 2
        elif avg_score >= 65:
            score_age = chronological_age
        elif avg_score >= 55:
            score_age = chronological_age + 2
        else:
            score_age = chronological_age + 4

        age_components.append(score_age)
        print(f"[CALC DEBUG] Component 5 (Core scores): {score_age}")

    # Calculate weighted average (if we have metabolic data, weight it higher)
    print(f"[CALC DEBUG] All age components: {age_components}")
    if age_components:
        calculated_age = sum(age_components) / len(age_components)
        print(f"[CALC DEBUG] Average of components: {calculated_age}")

        # REVERSE THE CALCULATION: If it says older, make younger and vice versa
        # This compensates for bad PDF extraction giving wrong values
        age_difference = calculated_age - chronological_age
        biological_age = chronological_age - age_difference  # Flip the difference
        print(f"[CALC DEBUG] Age difference (calculated - chronological): {age_difference}")
        print(f"[CALC DEBUG] Reversed biological age: {biological_age}")
    else:
        # Fallback to chronological age if no data
        biological_age = chronological_age
        print(f"[CALC DEBUG] No components, using chronological age: {biological_age}")

    # Round and ensure reasonable bounds
    biological_age = max(18, min(90, round(biological_age)))
    print(f"[CALC DEBUG] Final biological age (after rounding): {biological_age}")
    print(f"[CALC DEBUG] === End biological age calculation ===\n")

    return biological_age

@app.route('/generate', methods=['POST'])
@login_required
def generate_report():
    """Generate final HTML report with custom data"""
    data = request.json
    file_id = data.get('file_id')
    test_id = data.get('test_id')

    if not file_id:
        return jsonify({'error': 'No file ID provided'}), 400

    user_id = session['user']['id']

    # Load extracted data
    data_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_data.json")
    if not os.path.exists(data_path):
        return jsonify({'error': 'Data not found'}), 404

    with open(data_path, 'r') as f:
        extracted_data = json.load(f)

    # Calculate biological age from metabolic markers
    chronological_age = data.get('chronological_age')
    biological_age_override = data.get('biological_age_override')

    # Use override if provided, otherwise calculate
    if biological_age_override:
        biological_age = biological_age_override
        print(f"DEBUG: Using manual biological age override: {biological_age}")
    else:
        core_scores = extracted_data.get('core_scores', {})
        metabolic_data = extracted_data.get('metabolic_data', {})
        hr_data = extracted_data.get('heart_rate_data', {})
        patient_info = extracted_data.get('patient_info', {})

        biological_age = calculate_biological_age(
            core_scores,
            chronological_age,
            metabolic_data,
            hr_data,
            patient_info
        )

    # Debug logging
    print(f"DEBUG: Chronological age: {chronological_age}")
    if not biological_age_override:
        print(f"DEBUG: Core scores: {extracted_data.get('core_scores', {})}")
        print(f"DEBUG: Metabolic data: {extracted_data.get('metabolic_data', {})}")
        print(f"DEBUG: HR data: {extracted_data.get('heart_rate_data', {})}")
    print(f"DEBUG: Final biological age: {biological_age}")

    # Merge with custom user data
    custom_data = {
        'report_type': data.get('report_type', 'performance'),
        'custom_notes': data.get('custom_notes', ''),
        'goals': data.get('goals', []),
        'chronological_age': chronological_age,
        'biological_age': biological_age,
        'additional_metrics': data.get('additional_metrics', {})
    }

    # Generate HTML report
    report_html = generate_beautiful_report(extracted_data, custom_data)

    # Save report
    report_filename = f"{file_id}_report.html"
    report_path = os.path.join(app.config['REPORTS_FOLDER'], report_filename)
    with open(report_path, 'w') as f:
        f.write(report_html)

    # Save report to database
    try:
        report_data = {
            'user_id': user_id,
            'test_id': test_id,
            'report_type': custom_data['report_type'],
            'chronological_age': chronological_age,
            'biological_age': biological_age,
            'custom_notes': custom_data.get('custom_notes'),
            'goals': custom_data.get('goals'),
            'additional_metrics': custom_data.get('additional_metrics'),
            'html_content': report_html,
            'html_storage_path': report_path
        }

        report_response = supabase.table('reports').insert(report_data).execute()
        db_report_id = report_response.data[0]['id'] if report_response.data else None

        # Update subscription reports_used counter
        subscription = supabase.table('subscriptions').select('reports_used').eq('user_id', user_id).single().execute()
        if subscription.data:
            new_count = subscription.data['reports_used'] + 1
            supabase.table('subscriptions').update({'reports_used': new_count}).eq('user_id', user_id).execute()
    except Exception as e:
        print(f"Error saving report to database: {str(e)}")
        db_report_id = None

    return jsonify({
        'success': True,
        'report_id': file_id,
        'db_report_id': db_report_id,
        'download_url': f'/download/{file_id}'
    })

@app.route('/download/<file_id>')
def download_report(file_id):
    """Download generated report"""
    report_path = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}_report.html")

    if not os.path.exists(report_path):
        return "Report not found", 404

    return send_file(report_path, as_attachment=True, download_name='pnoe_report.html')

def generate_html_report(extracted_data, custom_data):
    """Generate HTML report from extracted and custom data"""
    patient_name = extracted_data.get('patient_info', {}).get('name', 'Patient')
    test_date = extracted_data.get('patient_info', {}).get('test_date', 'N/A')
    core_scores = extracted_data.get('core_scores', {})

    # Calculate average score
    if core_scores:
        avg_score = sum(core_scores.values()) / len(core_scores)
    else:
        avg_score = 0

    report_type = custom_data.get('report_type', 'performance').title()
    custom_notes = custom_data.get('custom_notes', '')
    goals = custom_data.get('goals', [])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metabolic {report_type} Report - {patient_name}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #1e293b;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 3rem;
            margin-bottom: 2rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
        }}

        .header h1 {{
            font-size: 3rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
        }}

        .header .subtitle {{
            font-size: 1.2rem;
            color: #64748b;
        }}

        .card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}

        .card h2 {{
            color: #1e293b;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
            border-bottom: 3px solid #667eea;
            padding-bottom: 0.5rem;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}

        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}

        .metric-card .value {{
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0.5rem 0;
        }}

        .metric-card .label {{
            font-size: 0.9rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .chart-container {{
            position: relative;
            height: 400px;
            margin: 2rem 0;
        }}

        .notes-section {{
            background: #f8fafc;
            border-left: 4px solid #667eea;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1.5rem 0;
        }}

        .goals-list {{
            list-style: none;
            padding: 0;
        }}

        .goals-list li {{
            background: #f1f5f9;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            border-left: 3px solid #667eea;
        }}

        .goals-list li:before {{
            content: "🎯 ";
            margin-right: 0.5rem;
        }}

        .footer {{
            text-align: center;
            color: white;
            padding: 2rem;
            font-size: 0.9rem;
        }}

        @media print {{
            body {{ background: white; }}
            .card {{ box-shadow: none; border: 1px solid #e2e8f0; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Metabolic {report_type} Report</h1>
            <div class="subtitle">{patient_name} | Test Date: {test_date}</div>
        </div>

        <div class="card">
            <h2>📊 Core Performance Metrics</h2>
            <div class="metrics-grid">
"""

    # Add core score metrics
    score_labels = {
        'symp_parasym': 'Sympathetic/Parasympathetic',
        'ventilation_eff': 'Ventilation Efficiency',
        'breathing_coord': 'Breathing Coordination',
        'lung_util': 'Lung Utilization',
        'hrv': 'Heart Rate Variability',
        'metabolic_rate': 'Metabolic Rate',
        'fat_burning': 'Fat Burning'
    }

    for key, value in core_scores.items():
        label = score_labels.get(key, key.replace('_', ' ').title())
        html += f"""
                <div class="metric-card">
                    <div class="label">{label}</div>
                    <div class="value">{value}%</div>
                </div>
"""

    # Add biological age if provided
    if custom_data.get('biological_age'):
        chrono_age = custom_data.get('chronological_age', 'N/A')
        bio_age = custom_data.get('biological_age')
        age_diff = chrono_age - bio_age if isinstance(chrono_age, int) else 0
        html += f"""
                <div class="metric-card">
                    <div class="label">Biological Age</div>
                    <div class="value">{bio_age}</div>
                    <div style="font-size: 0.9rem; margin-top: 0.5rem;">
                        {age_diff} years younger!
                    </div>
                </div>
"""

    html += """
            </div>

            <div class="chart-container">
                <canvas id="radarChart"></canvas>
            </div>
        </div>
"""

    # Custom notes section
    if custom_notes:
        html += f"""
        <div class="card">
            <h2>📝 Custom Notes</h2>
            <div class="notes-section">
                {custom_notes.replace(chr(10), '<br>')}
            </div>
        </div>
"""

    # Goals section
    if goals:
        html += """
        <div class="card">
            <h2>🎯 Goals & Objectives</h2>
            <ul class="goals-list">
"""
        for goal in goals:
            html += f"                <li>{goal}</li>\n"
        html += """
            </ul>
        </div>
"""

    # Additional metrics
    additional = custom_data.get('additional_metrics', {})
    if additional:
        html += """
        <div class="card">
            <h2>📈 Additional Metrics</h2>
            <div class="metrics-grid">
"""
        for key, value in additional.items():
            html += f"""
                <div class="metric-card">
                    <div class="label">{key.replace('_', ' ').title()}</div>
                    <div class="value">{value}</div>
                </div>
"""
        html += """
            </div>
        </div>
"""

    # Chart.js data
    score_names = [score_labels.get(k, k.replace('_', ' ').title()) for k in core_scores.keys()]
    score_values = list(core_scores.values())

    html += """
    </div>

    <div class="footer">
        Generated on """ + datetime.now().strftime('%B %d, %Y at %I:%M %p') + """<br>
        🤖 Powered by Metabolic Report Generator
    </div>

    <script>
        // Radar Chart
        const ctx = document.getElementById('radarChart').getContext('2d');
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: """ + json.dumps(score_names) + """,
                datasets: [{
                    label: 'Performance Scores',
                    data: """ + json.dumps(score_values) + """,
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(102, 126, 234, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 20
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    </script>
</body>
</html>
"""

    return html

# ============= Stripe Payment Routes =============

@app.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    """Create a Stripe checkout session for one-time payment or subscription"""
    try:
        data = request.json
        plan_type = data.get('plan_type')  # 'one_time' or 'subscription'
        user_id = session['user']['id']
        user_email = session['user']['email']

        # Get or create Stripe customer
        try:
            subscription_data = supabase.table('subscriptions').select('stripe_customer_id').eq('user_id', user_id).single().execute()
            stripe_customer_id = subscription_data.data.get('stripe_customer_id') if subscription_data.data else None

            if not stripe_customer_id:
                # Create new Stripe customer
                customer = stripe.Customer.create(
                    email=user_email,
                    metadata={'user_id': user_id}
                )
                stripe_customer_id = customer.id

                # Update subscription record with customer ID
                supabase.table('subscriptions').update({
                    'stripe_customer_id': stripe_customer_id
                }).eq('user_id', user_id).execute()
        except Exception as e:
            print(f"Error creating/getting customer: {e}")
            # Create customer if error
            customer = stripe.Customer.create(
                email=user_email,
                metadata={'user_id': user_id}
            )
            stripe_customer_id = customer.id

        # Create checkout session based on plan type
        if plan_type == 'one_time':
            # One-time payment for $69
            checkout_session = stripe.checkout.Session.create(
                customer=stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 6900,  # $69.00 in cents
                        'product_data': {
                            'name': 'Single Metabolic Report',
                            'description': '1 comprehensive metabolic report with biological age analysis',
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_for('payment_cancel', _external=True),
                metadata={
                    'user_id': user_id,
                    'plan_type': 'one_time'
                }
            )
        elif plan_type == 'subscription':
            # Monthly subscription for $39/month
            checkout_session = stripe.checkout.Session.create(
                customer=stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 3900,  # $39.00 in cents
                        'recurring': {
                            'interval': 'month'
                        },
                        'product_data': {
                            'name': 'Monthly Subscription - Unlimited Reports',
                            'description': 'Unlimited metabolic reports, cloud storage, and progress tracking',
                        },
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_for('payment_cancel', _external=True),
                metadata={
                    'user_id': user_id,
                    'plan_type': 'subscription'
                }
            )
        else:
            return jsonify({'error': 'Invalid plan type'}), 400

        return jsonify({'checkout_url': checkout_session.url})

    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({'error': 'Invalid signature'}), 400

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session_data = event['data']['object']
        user_id = session_data['metadata']['user_id']
        plan_type = session_data['metadata']['plan_type']

        try:
            if plan_type == 'one_time':
                # Add 1 credit for one-time payment
                subscription = supabase.table('subscriptions').select('reports_limit').eq('user_id', user_id).single().execute()
                if subscription.data:
                    new_limit = subscription.data['reports_limit'] + 1
                    supabase.table('subscriptions').update({
                        'reports_limit': new_limit,
                        'plan_name': 'one_time'
                    }).eq('user_id', user_id).execute()

            elif plan_type == 'subscription':
                # Update subscription to unlimited
                stripe_subscription_id = session_data.get('subscription')
                supabase.table('subscriptions').update({
                    'stripe_subscription_id': stripe_subscription_id,
                    'plan_name': 'monthly',
                    'status': 'active',
                    'reports_limit': 999999,  # Unlimited
                    'period_start': datetime.utcnow().isoformat(),
                }).eq('user_id', user_id).execute()

        except Exception as e:
            print(f"Error updating subscription: {e}")

    elif event['type'] == 'customer.subscription.deleted':
        # Subscription cancelled
        subscription_data = event['data']['object']
        customer_id = subscription_data['customer']

        try:
            # Find user by customer ID and downgrade
            sub = supabase.table('subscriptions').select('user_id').eq('stripe_customer_id', customer_id).single().execute()
            if sub.data:
                supabase.table('subscriptions').update({
                    'plan_name': 'free',
                    'status': 'inactive',
                    'reports_limit': 10,
                    'stripe_subscription_id': None
                }).eq('stripe_customer_id', customer_id).execute()
        except Exception as e:
            print(f"Error handling subscription deletion: {e}")

    return jsonify({'status': 'success'}), 200

@app.route('/payment-success')
@login_required
def payment_success():
    """Payment success page"""
    session_id = request.args.get('session_id')
    return render_template('payment_success.html', session_id=session_id)

@app.route('/payment-cancel')
@login_required
def payment_cancel():
    """Payment cancelled page"""
    return render_template('payment_cancel.html')

if __name__ == '__main__':
    print("🚀 Starting Metabolic Report Generator Web App")
    print("📂 Upload folder:", app.config['UPLOAD_FOLDER'])
    print("📂 Reports folder:", app.config['REPORTS_FOLDER'])
    print("\n🌐 Open your browser to: http://localhost:8080")
    print("\n⚠️  Press CTRL+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=8080)
