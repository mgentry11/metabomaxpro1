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
import requests
import stripe
from weasyprint import HTML
from utils.beautiful_report import generate_beautiful_report
from utils.calculate_scores import calculate_biological_age as calculate_bio_age_proper
from ai_recommendations import UniversalRecommendationAI
from blog_posts import get_all_posts, get_post_by_slug, get_recent_posts

# Load environment variables (override=True ensures .env file takes precedence over shell variables)
load_dotenv(override=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORTS_FOLDER'] = 'reports'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max file size

# Session configuration for better reliability
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

ALLOWED_EXTENSIONS = {'pdf'}

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
# Strip all whitespace characters (newlines, tabs, spaces, etc.)
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '').strip().replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
SUPABASE_REST_URL = f"{SUPABASE_URL}/rest/v1"

# Debug: Check key format (only show first/last 10 chars for security)
if SUPABASE_KEY:
    key_preview = f"{SUPABASE_KEY[:10]}...{SUPABASE_KEY[-10:]}"
    key_length = len(SUPABASE_KEY)
    print(f"[SUPABASE] API Key loaded: {key_preview} (length: {key_length})")
else:
    print("[SUPABASE] WARNING: No API key found!")

# Stripe configuration
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

# Stripe Price IDs
STRIPE_PRICE_UNLIMITED_BASIC = 'price_1SQKHOC5St4DyD5v1QFSrM0j'  # $69 Unlimited Basic Reports
STRIPE_PRICE_AI_PACKAGE = 'price_1SQKPBC5St4DyD5vnRp1NXK2'  # $99 AI-Enhanced Package
STRIPE_PRICE_SUBSCRIPTION = 'price_1SOo8NC5St4DyD5vBPXDJrzy'  # $39/month Unlimited Everything

# Create a requests session that forces HTTP/1.1
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util.ssl_ import create_urllib3_context
import ssl

# Force HTTP/1.1 by completely disabling HTTP/2 ALPN
class HTTP11Adapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        try:
            # Create SSL context that explicitly excludes HTTP/2
            context = create_urllib3_context()
            # Try to set ALPN protocols, but don't fail if not supported
            if hasattr(context, 'set_alpn_protocols'):
                context.set_alpn_protocols(['http/1.1'])  # Only allow HTTP/1.1
            kwargs['ssl_context'] = context
        except Exception as e:
            print(f"Warning: Could not configure SSL ALPN: {e}")
            # Continue without custom SSL context
        return super().init_poolmanager(*args, **kwargs)

# Create session with HTTP/1.1 only
http_session = requests.Session()
http_session.mount('https://', HTTP11Adapter())
http_session.mount('http://', HTTP11Adapter())

# HTTP headers for Supabase REST API
def get_supabase_headers():
    return {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

# Startup logging
print("=" * 60)
print("🚀 PNOE WEBAPP STARTING UP")
print(f"📂 Upload folder: {app.config['UPLOAD_FOLDER']}")
print(f"📂 Reports folder: {app.config['REPORTS_FOLDER']}")
print(f"🔑 Supabase configured: {'Yes' if SUPABASE_URL and SUPABASE_KEY else 'No'}")
print(f"💳 Stripe configured: {'Yes' if stripe.api_key else 'No'}")
print("=" * 60)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Debug session
        print(f"[LOGIN_CHECK] Route: {request.endpoint}")
        print(f"[LOGIN_CHECK] Session keys: {list(session.keys())}")
        print(f"[LOGIN_CHECK] Has user: {'user' in session}")

        if 'user' not in session:
            # If this is an AJAX/JSON request, return JSON error instead of redirect
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                print(f"[LOGIN_CHECK] Returning 401 - not logged in (AJAX request)")
                return jsonify({'error': 'Please log in to access this feature', 'login_required': True}), 401
            # Otherwise, redirect to login page
            print(f"[LOGIN_CHECK] Redirecting to login - not logged in")
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))

        print(f"[LOGIN_CHECK] User authenticated: {session['user'].get('id', 'unknown')}")
        return f(*args, **kwargs)
    return decorated_function

def get_user_subscription(user_id):
    """Get user's subscription details"""
    try:
        response = http_session.get(
            f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
            headers=get_supabase_headers()
        )
        if response.ok and response.json():
            return response.json()[0]
        return None
    except Exception as e:
        print(f"Error getting subscription: {e}")
        return None

def can_generate_basic_report(user_id):
    """Check if user can generate a basic report"""
    # Admin bypass - check if user is admin
    if 'user' in session and session['user'].get('email') == 'mark.gentry@gmail.com':
        return True, "Admin access (unlimited)"

    subscription = get_user_subscription(user_id)
    if not subscription:
        return False, "No subscription found"

    reports_used = subscription.get('reports_used', 0)
    reports_limit = subscription.get('reports_limit', 0)

    if reports_used >= reports_limit:
        return False, f"You've used all {reports_limit} of your free reports. Please upgrade to continue."

    return True, f"Report {reports_used + 1} of {reports_limit}"

def can_use_ai_recommendations(user_id):
    """Check if user has AI credits available"""
    # Admin bypass - check if user is admin
    if 'user' in session and session['user'].get('email') == 'mark.gentry@gmail.com':
        return True, "Admin access (unlimited)"

    subscription = get_user_subscription(user_id)
    if not subscription:
        return False, "No subscription found"

    plan_name = subscription.get('plan_name', 'free')
    ai_credits = subscription.get('ai_credits', 0)

    # Subscription users get unlimited AI
    if plan_name == 'subscription':
        return True, "Unlimited AI (subscription)"

    # AI package or one-time purchases
    if ai_credits > 0:
        return True, f"{ai_credits} AI credits remaining"

    return False, "No AI credits available. Please upgrade to add AI recommendations."

def use_ai_credit(user_id):
    """Decrement user's AI credits by 1"""
    # Admin bypass - don't decrement for admin
    if 'user' in session and session['user'].get('email') == 'mark.gentry@gmail.com':
        return True

    subscription = get_user_subscription(user_id)
    if not subscription:
        return False

    plan_name = subscription.get('plan_name', 'free')

    # Subscription users have unlimited, don't decrement
    if plan_name == 'subscription':
        return True

    ai_credits = subscription.get('ai_credits', 0)
    if ai_credits > 0:
        try:
            http_session.patch(
                f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
                headers=get_supabase_headers(),
                json={'ai_credits': ai_credits - 1}
            )
            return True
        except Exception as e:
            print(f"Error using AI credit: {e}")
            return False

    return False

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

    # Detect test source/type (PNOE, CorSense, etc.)
    all_text_combined = ' '.join(data.get('all_text', [])).lower()
    if 'pnoe' in all_text_combined or 'p n o e' in all_text_combined:
        data['patient_info']['test_source'] = 'PNOE'
    elif 'corsense' in all_text_combined:
        data['patient_info']['test_source'] = 'CorSense'
    else:
        data['patient_info']['test_source'] = 'Generic'

    return data

# ============= Authentication Routes =============

@app.route('/')
def landing():
    """Marketing landing page"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({'status': 'ok', 'message': 'App is running'}), 200

@app.route('/version')
def version():
    """Check deployed version"""
    return jsonify({
        'version': '2024-11-02-v4',
        'features': ['my_reports', 'delete_reports', 'view_download_buttons'],
        'last_commit': '810ee30'
    })

@app.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template('pricing.html')

@app.route('/pricing-debug')
def pricing_debug():
    """Pricing debug page to troubleshoot purchase errors"""
    return render_template('pricing_debug.html')

# HIT Coach Pro routes
@app.route('/hitcoachpro')
def hitcoachpro():
    """HIT Coach Pro marketing page"""
    return render_template('hitcoachpro.html')

@app.route('/hitcoach-app')
def hitcoach_app():
    """HIT Coach Pro web application"""
    return render_template('hitcoach_app.html')

# Blog routes
@app.route('/blog')
def blog():
    """Blog listing page"""
    posts = get_all_posts()
    return render_template('blog/index.html', posts=posts)

@app.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post page"""
    post = get_post_by_slug(slug)
    if not post:
        return "Blog post not found", 404
    recent_posts = get_recent_posts(limit=3)
    return render_template('blog/post.html', post=post, recent_posts=recent_posts)

@app.route('/sitemap.xml')
def sitemap():
    """Generate XML sitemap for SEO"""
    posts = get_all_posts()
    sitemap_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://metabomaxpro.com/</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://metabomaxpro.com/pricing</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://metabomaxpro.com/blog</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>'''

    for post in posts:
        sitemap_xml += f'''
    <url>
        <loc>https://metabomaxpro.com/blog/{post['slug']}</loc>
        <lastmod>{post['date'].strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>'''

    sitemap_xml += '\n</urlset>'

    from flask import Response
    return Response(sitemap_xml, mimetype='text/xml')

@app.route('/terms')
def terms():
    """Terms of Service page"""
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html')

@app.route('/sample-report')
def sample_report():
    """Complete sample report page with charts and graphs"""
    return render_template('sample_report.html')

@app.route('/data-guide')
def data_guide():
    """Data input guide page"""
    return render_template('data_guide.html')

@app.route('/sample-data')
def sample_data():
    """Visual display of sample PNOE metabolic test data"""
    return render_template('sample_data.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        company_name = request.form.get('company_name', '')

        try:
            print(f"[REGISTER] Attempting registration for email: {email}")

            # Generate user ID and hash password first (before any DB calls)
            user_id = str(uuid.uuid4())
            password_hash = generate_password_hash(password)
            print(f"[REGISTER] Generated user_id: {user_id}")

            # Check if user already exists
            try:
                response = http_session.get(
                    f"{SUPABASE_REST_URL}/profiles?email=eq.{email}&select=id",
                    headers=get_supabase_headers(),
                    timeout=10
                )
                print(f"[REGISTER] Check existing user status: {response.status_code}")

                if response.ok and response.json():
                    flash('An account with this email already exists.', 'danger')
                    return render_template('register.html')
            except Exception as check_error:
                print(f"[REGISTER] Warning: Could not check existing user: {check_error}")
                # Continue with registration anyway

            # Insert user into profiles table
            profile_data = {
                'id': user_id,
                'email': email,
                'full_name': full_name,
                'password_hash': password_hash,
                'company_name': company_name
            }
            print(f"[REGISTER] Creating profile with data: {list(profile_data.keys())}")

            # Use a fresh session for the POST request
            profile_response = requests.post(
                f"{SUPABASE_REST_URL}/profiles",
                headers=get_supabase_headers(),
                json=profile_data,
                timeout=15
            )

            print(f"[REGISTER] Profile creation status: {profile_response.status_code}")
            print(f"[REGISTER] Profile response: {profile_response.text[:500] if profile_response.text else 'empty'}")

            if not profile_response.ok:
                raise Exception(f"Failed to create profile: {profile_response.text}")

            # Create subscription record with new free tier (2 reports)
            sub_response = requests.post(
                f"{SUPABASE_REST_URL}/subscriptions",
                headers=get_supabase_headers(),
                json={
                    'user_id': user_id,
                    'plan_name': 'free',
                    'status': 'active',
                    'reports_limit': 2,
                    'reports_used': 0,
                    'ai_credits': 0
                },
                timeout=15
            )

            if not sub_response.ok:
                print(f"Warning: Failed to create subscription: {sub_response.text}")

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

        except requests.exceptions.ConnectionError as conn_error:
            print(f"[REGISTER] Connection error: {conn_error}")
            flash('Network error. Please try again.', 'danger')
        except requests.exceptions.Timeout:
            print(f"[REGISTER] Request timeout")
            flash('Request timeout. Please try again.', 'danger')
        except Exception as e:
            print(f"[REGISTER] Error: {type(e).__name__}: {str(e)}")
            flash(f'Registration error. Please try again.', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            # Query user from database
            response = http_session.get(
                f"{SUPABASE_REST_URL}/profiles?email=eq.{email}&select=id,email,full_name,password_hash",
                headers=get_supabase_headers()
            )

            if response.ok and response.json():
                users = response.json()
                if users and len(users) > 0:
                    user = users[0]

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

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password requests"""
    if request.method == 'POST':
        email = request.form.get('email')

        try:
            # Check if user exists
            response = http_session.get(
                f"{SUPABASE_REST_URL}/profiles?email=eq.{email}&select=id,email,full_name",
                headers=get_supabase_headers()
            )

            if response.ok and response.json():
                users = response.json()
                if users and len(users) > 0:
                    user = users[0]

                    # Generate secure reset token
                    reset_token = secrets.token_urlsafe(32)

                    # Calculate expiration (1 hour from now)
                    from datetime import datetime, timedelta
                    expires_at = (datetime.utcnow() + timedelta(hours=1)).isoformat()

                    # Store token in database
                    token_data = {
                        'user_id': user['id'],
                        'token': reset_token,
                        'expires_at': expires_at,
                        'used': False
                    }

                    token_response = http_session.post(
                        f"{SUPABASE_REST_URL}/password_reset_tokens",
                        headers=get_supabase_headers(),
                        json=token_data
                    )

                    if token_response.ok:
                        # Generate reset link
                        reset_url = url_for('reset_password', token=reset_token, _external=True)

                        # TODO: Send email with reset link
                        # For now, we'll just flash it (you'll need to configure email service)
                        print(f"Password reset link for {email}: {reset_url}")

                        # Try to send email (if configured)
                        try:
                            send_password_reset_email(email, user.get('full_name', ''), reset_url)
                            flash('Password reset link has been sent to your email.', 'success')
                        except Exception as email_error:
                            # Email not configured yet, show link in console
                            print(f"Email not sent (service not configured): {email_error}")
                            flash('Password reset link sent! Check your email.', 'success')
                            # In development, also show in flash for testing
                            if os.getenv('FLASK_ENV') == 'development':
                                flash(f'DEV MODE - Reset link: {reset_url}', 'info')
                    else:
                        flash('Error creating reset token. Please try again.', 'danger')
                else:
                    # Don't reveal if email exists or not (security best practice)
                    flash('If that email exists, a reset link has been sent.', 'info')
            else:
                flash('If that email exists, a reset link has been sent.', 'info')

        except Exception as e:
            print(f"Forgot password error: {str(e)}")
            flash('An error occurred. Please try again.', 'danger')

    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with token"""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('reset_password.html', token=token)

        # Validate password strength
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('reset_password.html', token=token)

        try:
            # Look up token
            token_response = http_session.get(
                f"{SUPABASE_REST_URL}/password_reset_tokens?token=eq.{token}&used=eq.false",
                headers=get_supabase_headers()
            )

            if token_response.ok and token_response.json():
                tokens = token_response.json()
                if tokens and len(tokens) > 0:
                    token_data = tokens[0]

                    # Check if token is expired
                    from datetime import datetime
                    expires_at = datetime.fromisoformat(token_data['expires_at'].replace('Z', '+00:00'))

                    if datetime.utcnow().replace(tzinfo=expires_at.tzinfo) > expires_at:
                        flash('This reset link has expired. Please request a new one.', 'danger')
                        return redirect(url_for('forgot_password'))

                    # Update user password
                    password_hash = generate_password_hash(password)

                    update_response = http_session.patch(
                        f"{SUPABASE_REST_URL}/profiles?id=eq.{token_data['user_id']}",
                        headers=get_supabase_headers(),
                        json={'password_hash': password_hash}
                    )

                    if update_response.ok:
                        # Mark token as used
                        http_session.patch(
                            f"{SUPABASE_REST_URL}/password_reset_tokens?id=eq.{token_data['id']}",
                            headers=get_supabase_headers(),
                            json={'used': True}
                        )

                        flash('Password successfully reset! You can now log in.', 'success')
                        return redirect(url_for('login'))
                    else:
                        flash('Error updating password. Please try again.', 'danger')
                else:
                    flash('Invalid or expired reset link.', 'danger')
                    return redirect(url_for('forgot_password'))
            else:
                flash('Invalid or expired reset link.', 'danger')
                return redirect(url_for('forgot_password'))

        except Exception as e:
            print(f"Reset password error: {str(e)}")
            flash('An error occurred. Please try again.', 'danger')

    return render_template('reset_password.html', token=token)

def send_password_reset_email(to_email, user_name, reset_url):
    """Send password reset email (requires email service configuration)"""
    # Check if email service is configured
    email_service = os.getenv('EMAIL_SERVICE', 'none')

    if email_service == 'none':
        raise Exception("Email service not configured")

    # You can add SendGrid, Mailgun, or SMTP configuration here
    # Example for SendGrid:
    # sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    # if sendgrid_api_key:
    #     import sendgrid
    #     from sendgrid.helpers.mail import Mail, Email, To, Content
    #
    #     sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    #     from_email = Email(os.getenv('FROM_EMAIL', 'noreply@metabomaxpro.com'))
    #     to_email = To(to_email)
    #     subject = "Reset Your MetaboMaxPro Password"
    #     content = Content("text/html", f"""
    #         <p>Hi {user_name},</p>
    #         <p>You requested to reset your password. Click the link below to reset it:</p>
    #         <p><a href="{reset_url}">Reset Password</a></p>
    #         <p>This link will expire in 1 hour.</p>
    #         <p>If you didn't request this, please ignore this email.</p>
    #     """)
    #     mail = Mail(from_email, to_email, subject, content)
    #     response = sg.client.mail.send.post(request_body=mail.get())

    raise Exception("Email service not configured - add SendGrid, Mailgun, or SMTP settings")

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing report history"""
    user_id = session['user']['id']

    try:
        # Get user's profile
        profile_response = http_session.get(
            f"{SUPABASE_REST_URL}/profiles?id=eq.{user_id}",
            headers=get_supabase_headers()
        )
        profile = profile_response.json()[0] if profile_response.ok and profile_response.json() else None

        # Get user's reports (simplified - without nested joins)
        reports_response = http_session.get(
            f"{SUPABASE_REST_URL}/reports?user_id=eq.{user_id}&order=created_at.desc",
            headers=get_supabase_headers()
        )
        reports = reports_response.json() if reports_response.ok else []

        # Get user's subscription
        sub_response = http_session.get(
            f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
            headers=get_supabase_headers()
        )
        subscription = sub_response.json()[0] if sub_response.ok and sub_response.json() else None

        return render_template('dashboard.html',
                             profile=profile,
                             reports=reports,
                             subscription=subscription)
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

            test_response = http_session.post(
                f"{SUPABASE_REST_URL}/metabolic_tests",
                headers=get_supabase_headers(),
                json=test_data
            )
            test_id = test_response.json()[0]['id'] if test_response.ok and test_response.json() else None
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

        test_response = http_session.post(
            f"{SUPABASE_REST_URL}/metabolic_tests",
            headers=get_supabase_headers(),
            json=test_data
        )
        test_id = test_response.json()[0]['id'] if test_response.ok and test_response.json() else None
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
    """
    WRAPPER: Call the proper calculate_biological_age from utils/calculate_scores.py
    This wrapper converts the old function signature to the new one
    """
    # Convert old signature to new signature
    # Old: calculate_biological_age(core_scores, chronological_age, metabolic_data, hr_data, patient_info)
    # New: calculate_biological_age(patient_info, core_scores, metabolic_data)

    print(f"\n[APP.PY WRAPPER] Converting old bio age call to new proper function...")
    print(f"[APP.PY WRAPPER] Chronological age: {chronological_age}")

    # Ensure patient_info has age
    if patient_info and 'age' not in patient_info:
        patient_info['age'] = chronological_age

    # Call the PROPER function from utils/calculate_scores.py (NO DEFAULTS!)
    biological_age = calculate_bio_age_proper(patient_info, core_scores, metabolic_data)

    print(f"[APP.PY WRAPPER] Proper function returned: {biological_age}")

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

    # CHECK REPORT LIMIT
    can_generate, message = can_generate_basic_report(user_id)
    if not can_generate:
        return jsonify({
            'error': message,
            'upgrade_required': True,
            'pricing_url': '/pricing'
        }), 403

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
            'file_id': file_id,  # IMPORTANT: Save file_id for My Reports feature
            'report_type': custom_data['report_type'],
            'chronological_age': chronological_age,
            'biological_age': biological_age,
            'custom_notes': custom_data.get('custom_notes'),
            'goals': custom_data.get('goals'),
            'additional_metrics': custom_data.get('additional_metrics'),
            'html_content': report_html,
            'html_storage_path': report_path
        }

        print(f"[SAVE REPORT] Saving report with data: {report_data.keys()}")
        print(f"[SAVE REPORT] file_id={file_id}, user_id={user_id}")

        report_response = http_session.post(
            f"{SUPABASE_REST_URL}/reports",
            headers=get_supabase_headers(),
            json=report_data
        )

        print(f"[SAVE REPORT] Response status: {report_response.status_code}")
        print(f"[SAVE REPORT] Response: {report_response.text[:500]}")

        db_report_id = report_response.json()[0]['id'] if report_response.ok and report_response.json() else None
        print(f"[SAVE REPORT] Saved report with DB ID: {db_report_id}")

        # Update subscription reports_used counter
        subscription_response = http_session.get(
            f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}&select=reports_used",
            headers=get_supabase_headers()
        )
        if subscription_response.ok and subscription_response.json():
            subscription_data = subscription_response.json()[0]
            new_count = subscription_data['reports_used'] + 1
            http_session.patch(
                f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
                headers=get_supabase_headers(),
                json={'reports_used': new_count}
            )
    except Exception as e:
        print(f"Error saving report to database: {str(e)}")
        db_report_id = None

    return jsonify({
        'success': True,
        'report_id': file_id,
        'db_report_id': db_report_id,
        'download_url': f'/download/{file_id}'
    })

@app.route('/generate-with-ai', methods=['POST'])
@login_required
def generate_report_with_ai():
    """Generate report with AI recommendations appended"""
    data = request.json
    file_id = data.get('file_id')
    ai_recommendations = data.get('ai_recommendations', {})  # {subject: recommendation_text}

    print(f"[DEBUG /generate-with-ai] Received request")
    print(f"[DEBUG] file_id: {file_id}")
    print(f"[DEBUG] ai_recommendations keys: {list(ai_recommendations.keys())}")

    if not file_id:
        print("[ERROR] No file_id provided")
        return jsonify({'error': 'No file ID provided'}), 400

    # Check if user has AI access
    user_id = session['user']['id']
    has_access, message = can_use_ai_recommendations(user_id)

    if not has_access:
        print(f"[ERROR] User {user_id} does not have AI access: {message}")
        return jsonify({
            'error': message,
            'upgrade_required': True,
            'upgrade_url': '/pricing'
        }), 403

    print(f"[DEBUG] User has AI access: {message}")

    # Get the basic report first
    basic_report_path = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}_report.html")
    print(f"[DEBUG] Looking for basic report at: {basic_report_path}")
    print(f"[DEBUG] Basic report exists: {os.path.exists(basic_report_path)}")

    if not os.path.exists(basic_report_path):
        print("[ERROR] Basic report not found")
        return jsonify({'error': 'Basic report not found. Please generate basic report first.'}), 404

    # Read the basic report
    with open(basic_report_path, 'r') as f:
        report_html = f.read()

    # Build AI recommendations HTML section
    ai_section_html = """
    <div class="container" style="margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 20px;">
        <h2 style="color: white; text-align: center; margin-bottom: 2rem; font-size: 2.5rem;">
            🤖 AI-Powered Personalized Recommendations
        </h2>
        <p style="color: rgba(255,255,255,0.9); text-align: center; margin-bottom: 2rem; font-size: 1.1rem;">
            Based on your metabolic data and health goals
        </p>

        <!-- AI Disclaimer -->
        <div style="background: rgba(255,255,255,0.15); border-radius: 15px; padding: 2rem; backdrop-filter: blur(10px); margin-bottom: 2rem; border: 2px solid rgba(255,255,255,0.3);">
            <div style="background: rgba(255,255,255,0.15); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
                <p style="margin: 0 0 0.5rem 0; font-weight: 600; font-size: 1.1rem; color: white;">
                    ✅ First, the good news:
                </p>
                <p style="margin: 0; line-height: 1.7; color: rgba(255,255,255,0.95);">
                    Your core metabolic data (VO2 max, RMR, heart rate zones, substrate utilization) uses <strong>well-established, medically-approved algorithms</strong>—the same ones testing facilities use. No AI. No guesswork. Just proven math.
                </p>
            </div>

            <p style="font-size: 1.05rem; line-height: 1.7; margin-bottom: 1.5rem; color: rgba(255,255,255,0.95);">
                <strong>The recommendations below?</strong> That's where AI comes in. AI is incredibly smart, but it's also an overachiever that really wants you to like it.
            </p>

            <div style="background: rgba(255,255,255,0.1); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0;">
                <p style="margin: 0 0 1rem 0; font-weight: 600; color: white;">AI has a few quirks you should know about:</p>
                <ul style="margin: 0; padding-left: 1.5rem; line-height: 2; color: rgba(255,255,255,0.95);">
                    <li><strong>It can hallucinate</strong> - occasionally making up facts with complete confidence</li>
                    <li><strong>It's a people-pleaser</strong> - wants to tell you what you want to hear</li>
                    <li><strong>It lacks clinical context</strong> - doesn't know your complete medical history</li>
                </ul>
            </div>

            <div style="background: rgba(255,255,255,0.2); border-left: 4px solid white; padding: 1.25rem; border-radius: 8px; margin: 1.5rem 0;">
                <p style="margin: 0; font-size: 1.05rem; line-height: 1.7; color: white;">
                    💡 <strong>That's why every recommendation below should be reviewed with a healthcare professional</strong>—specifically one experienced with VO2 max testing, metabolic optimization, and performance physiology.
                </p>
            </div>

            <p style="margin: 0; font-size: 1rem; text-align: center; opacity: 0.95; color: white; font-weight: 600;">
                Think of these as homework to bring to your doctor, not medical advice to follow blindly.
            </p>
        </div>
    """

    # Add each subject's recommendations
    for subject, recommendation_text in ai_recommendations.items():
        ai_section_html += f"""
        <div style="background: white; padding: 2.5rem; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <h3 style="color: #10b981; font-size: 2rem; margin-bottom: 1.5rem; text-transform: capitalize; border-bottom: 3px solid #10b981; padding-bottom: 1rem;">
                {subject} Recommendations
            </h3>
            <div style="white-space: pre-wrap; line-height: 1.8; color: #334155; font-size: 1.05rem;">
                {recommendation_text}
            </div>
        </div>
        """

    ai_section_html += """
    </div>
    """

    # Insert AI section before closing body tag
    report_with_ai = report_html.replace('</body>', f'{ai_section_html}</body>')

    # Save new report with AI
    ai_report_filename = f"{file_id}_report_with_ai.html"
    ai_report_path = os.path.join(app.config['REPORTS_FOLDER'], ai_report_filename)
    with open(ai_report_path, 'w') as f:
        f.write(report_with_ai)

    print(f"[SUCCESS] AI report saved to: {ai_report_path}")

    # Decrement AI credit if user has limited credits
    use_ai_credit(user_id)
    print(f"[DEBUG] AI credit decremented for user {user_id}")

    print(f"[SUCCESS] Returning download URL: /download-ai/{file_id}")

    return jsonify({
        'success': True,
        'download_url': f'/download-ai/{file_id}'
    })

@app.route('/download/<file_id>')
@app.route('/download/<file_id>/<format>')
def download_report(file_id, format='html'):
    """Download generated report in HTML or PDF format"""
    report_path = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}_report.html")

    if not os.path.exists(report_path):
        return "Report not found", 404

    # If PDF format requested, convert HTML to PDF
    if format.lower() == 'pdf':
        try:
            pdf_path = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}_report.pdf")

            # Read HTML and ensure styles are embedded
            with open(report_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Convert HTML to PDF using WeasyPrint with better settings
            from weasyprint import CSS
            from weasyprint.text.fonts import FontConfiguration

            font_config = FontConfiguration()

            # Create HTML object with base URL for resolving relative resources
            html_doc = HTML(string=html_content, base_url=os.path.dirname(report_path))

            # Professional PNOE-style PDF formatting
            pdf_css = CSS(string='''
                @page {
                    size: letter;
                    margin: 0.5in 0.5in;
                }
                body {
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    font-size: 10pt;
                    line-height: 1.4;
                    color: #1F2937;
                }
                /* Ensure all styles from HTML are preserved */
                * {
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
                /* Page break control */
                .page-break {
                    page-break-before: always;
                }
                .executive-summary,
                .bio-age-section,
                .patient-info,
                .metrics-list,
                .zones-list,
                .action-list,
                .protocol-list,
                .interventions-grid {
                    page-break-inside: avoid;
                }
            ''', font_config=font_config)

            # Write PDF with optimized settings
            html_doc.write_pdf(
                pdf_path,
                stylesheets=[pdf_css],
                font_config=font_config,
                presentational_hints=True,
                optimize_size=('fonts', 'images')
            )

            return send_file(
                pdf_path,
                as_attachment=True,
                download_name='pnoe_report.pdf',
                mimetype='application/pdf'
            )
        except Exception as e:
            print(f"PDF generation error: {e}")
            import traceback
            traceback.print_exc()
            return f"Error generating PDF: {str(e)}", 500

    # Default: return HTML
    return send_file(
        report_path,
        as_attachment=True,
        download_name='pnoe_report.html',
        mimetype='text/html'
    )

@app.route('/download-ai/<file_id>')
@app.route('/download-ai/<file_id>/<format>')
def download_ai_report(file_id, format='html'):
    """Download report with AI recommendations in HTML or PDF format"""
    report_path = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}_report_with_ai.html")

    if not os.path.exists(report_path):
        return "Report with AI not found", 404

    # If PDF format requested, convert HTML to PDF
    if format.lower() == 'pdf':
        try:
            pdf_path = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}_report_with_ai.pdf")

            # Read HTML and ensure styles are embedded
            with open(report_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Convert HTML to PDF using WeasyPrint with better settings
            from weasyprint import CSS
            from weasyprint.text.fonts import FontConfiguration

            font_config = FontConfiguration()

            # Create HTML object with base URL for resolving relative resources
            html_doc = HTML(string=html_content, base_url=os.path.dirname(report_path))

            # Professional PNOE-style PDF formatting
            pdf_css = CSS(string='''
                @page {
                    size: letter;
                    margin: 0.5in 0.5in;
                }
                body {
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    font-size: 10pt;
                    line-height: 1.4;
                    color: #1F2937;
                }
                /* Ensure all styles from HTML are preserved */
                * {
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
                /* Page break control */
                .page-break {
                    page-break-before: always;
                }
                .executive-summary,
                .bio-age-section,
                .patient-info,
                .metrics-list,
                .zones-list,
                .action-list,
                .protocol-list,
                .interventions-grid {
                    page-break-inside: avoid;
                }
            ''', font_config=font_config)

            # Write PDF with optimized settings
            html_doc.write_pdf(
                pdf_path,
                stylesheets=[pdf_css],
                font_config=font_config,
                presentational_hints=True,
                optimize_size=('fonts', 'images')
            )

            return send_file(
                pdf_path,
                as_attachment=True,
                download_name='pnoe_report_with_ai.pdf',
                mimetype='application/pdf'
            )
        except Exception as e:
            print(f"PDF generation error: {e}")
            import traceback
            traceback.print_exc()
            return f"Error generating PDF: {str(e)}", 500

    # Default: return HTML
    try:
        return send_file(
            report_path,
            as_attachment=True,
            download_name='pnoe_report_with_ai.html',
            mimetype='text/html',
            max_age=0,
            conditional=True
        )
    except Exception as e:
        print(f"[DOWNLOAD ERROR] Failed to send file: {e}")
        return f"Download error: {str(e)}", 500

@app.route('/view/<file_id>')
def view_report(file_id):
    """View generated report in browser with download button"""

    # First try to get from database
    try:
        response = supabase.table('reports').select('html_content').eq('file_id', file_id).execute()
        if response.data and len(response.data) > 0:
            report_html = response.data[0]['html_content']
            print(f"[VIEW] Fetched report {file_id} from database")
        else:
            # Fallback to file system
            report_path = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}_report.html")
            if not os.path.exists(report_path):
                return "Report not found", 404
            with open(report_path, 'r') as f:
                report_html = f.read()
            print(f"[VIEW] Fetched report {file_id} from file system")
    except Exception as e:
        # Fallback to file system if database fails
        print(f"[VIEW] Database error: {e}, falling back to file system")
        report_path = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}_report.html")
        if not os.path.exists(report_path):
            return "Report not found", 404
        with open(report_path, 'r') as f:
            report_html = f.read()

    # Add navigation buttons at the top of the report
    nav_buttons = f'''
    <div style="position: fixed; top: 20px; right: 20px; z-index: 10000; display: flex; gap: 10px; flex-wrap: wrap;">
        <a href="/dashboard"
           style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                  color: white; padding: 15px 30px; border-radius: 12px; text-decoration: none;
                  font-weight: bold; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                  transition: all 0.3s ease;">
            ← Back to Dashboard
        </a>
        <a href="/download/{file_id}/html"
           style="display: inline-block; background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                  color: white; padding: 15px 30px; border-radius: 12px; text-decoration: none;
                  font-weight: bold; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
                  transition: all 0.3s ease;">
            📥 Download HTML
        </a>
        <a href="/download/{file_id}/pdf"
           style="display: inline-block; background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                  color: white; padding: 15px 30px; border-radius: 12px; text-decoration: none;
                  font-weight: bold; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
                  transition: all 0.3s ease;">
            📄 Download PDF
        </a>
    </div>
    '''

    # Insert navigation buttons after body tag
    report_with_nav = report_html.replace('<body>', f'<body>{nav_buttons}')

    return report_with_nav

@app.route('/view-ai/<file_id>')
def view_ai_report(file_id):
    """View report with AI recommendations in browser with download button"""

    # First try to get from database
    try:
        response = supabase.table('reports').select('html_content').eq('file_id', file_id).execute()
        if response.data and len(response.data) > 0:
            report_html = response.data[0]['html_content']
            print(f"[VIEW-AI] Fetched report {file_id} from database")
        else:
            # Fallback to file system
            report_path = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}_report_with_ai.html")
            if not os.path.exists(report_path):
                return "Report with AI not found", 404
            with open(report_path, 'r') as f:
                report_html = f.read()
            print(f"[VIEW-AI] Fetched report {file_id} from file system")
    except Exception as e:
        # Fallback to file system if database fails
        print(f"[VIEW-AI] Database error: {e}, falling back to file system")
        report_path = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}_report_with_ai.html")
        if not os.path.exists(report_path):
            return "Report with AI not found", 404
        with open(report_path, 'r') as f:
            report_html = f.read()

    # Add navigation buttons at the top of the report
    nav_buttons = f'''
    <div style="position: fixed; top: 20px; right: 20px; z-index: 10000; display: flex; gap: 10px; flex-wrap: wrap;">
        <a href="/dashboard"
           style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                  color: white; padding: 15px 30px; border-radius: 12px; text-decoration: none;
                  font-weight: bold; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                  transition: all 0.3s ease;">
            ← Back to Dashboard
        </a>
        <a href="/download-ai/{file_id}/html"
           style="display: inline-block; background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                  color: white; padding: 15px 30px; border-radius: 12px; text-decoration: none;
                  font-weight: bold; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
                  transition: all 0.3s ease;">
            📥 Download HTML
        </a>
        <a href="/download-ai/{file_id}/pdf"
           style="display: inline-block; background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                  color: white; padding: 15px 30px; border-radius: 12px; text-decoration: none;
                  font-weight: bold; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
                  transition: all 0.3s ease;">
            📄 Download PDF
        </a>
    </div>
    '''

    # Insert navigation buttons after body tag
    report_with_nav = report_html.replace('<body>', f'<body>{nav_buttons}')

    return report_with_nav

@app.route('/api/my-reports', methods=['GET'])
@login_required
def get_my_reports():
    """Get all reports for the current user"""
    user_id = session['user']['id']
    print(f"[MY REPORTS] Fetching reports for user_id: {user_id}")

    try:
        # Fetch reports from Supabase
        url = f"{SUPABASE_REST_URL}/reports?user_id=eq.{user_id}&order=created_at.desc&select=id,created_at,report_type,chronological_age,biological_age,file_id"
        print(f"[MY REPORTS] Request URL: {url}")

        response = http_session.get(url, headers=get_supabase_headers())

        print(f"[MY REPORTS] Response status: {response.status_code}")
        print(f"[MY REPORTS] Response body: {response.text[:500]}")

        if response.ok:
            reports = response.json()
            print(f"[MY REPORTS] Found {len(reports)} reports")
            for report in reports:
                print(f"[MY REPORTS] Report ID: {report.get('id')}, file_id: {report.get('file_id')}, created: {report.get('created_at')}")
            return jsonify({'success': True, 'reports': reports})
        else:
            print(f"[MY REPORTS] ERROR - Status: {response.status_code}, Body: {response.text}")
            return jsonify({'success': False, 'error': 'Failed to fetch reports'}), 500
    except Exception as e:
        print(f"[MY REPORTS] EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/delete-old-reports', methods=['POST'])
@login_required
def delete_old_reports():
    """Delete all reports without file_id (old reports that don't have HTML files)"""
    user_id = session['user']['id']
    print(f"[DELETE OLD] Starting bulk delete for user_id: {user_id}")

    try:
        # Get all reports without file_id for this user
        url = f"{SUPABASE_REST_URL}/reports?user_id=eq.{user_id}&file_id=is.null&select=id"
        print(f"[DELETE OLD] Request URL: {url}")

        response = http_session.get(url, headers=get_supabase_headers())

        if not response.ok:
            print(f"[DELETE OLD] Failed to fetch reports: {response.text}")
            return jsonify({'success': False, 'error': 'Failed to fetch old reports'}), 500

        old_reports = response.json()
        count = len(old_reports)
        print(f"[DELETE OLD] Found {count} old reports to delete")

        if count == 0:
            return jsonify({'success': True, 'deleted_count': 0, 'message': 'No old reports found'})

        # Delete all old reports
        delete_headers = get_supabase_headers()
        delete_headers['Prefer'] = 'return=minimal'

        delete_response = http_session.delete(
            f"{SUPABASE_REST_URL}/reports?user_id=eq.{user_id}&file_id=is.null",
            headers=delete_headers
        )

        if delete_response.ok or delete_response.status_code == 204:
            print(f"[DELETE OLD] Successfully deleted {count} reports")
            return jsonify({'success': True, 'deleted_count': count})
        else:
            print(f"[DELETE OLD] Delete failed: {delete_response.status_code} - {delete_response.text}")
            return jsonify({'success': False, 'error': f'Failed to delete reports: {delete_response.text}'}), 500

    except Exception as e:
        print(f"[DELETE OLD] EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/delete-report/<report_id>', methods=['DELETE'])
@login_required
def delete_report(report_id):
    """Delete a specific report"""
    user_id = session['user']['id']
    print(f"[DELETE REPORT] Starting delete for report_id={report_id}, user_id={user_id}")

    try:
        # First, verify the report belongs to this user
        url = f"{SUPABASE_REST_URL}/reports?id=eq.{report_id}&user_id=eq.{user_id}&select=id,html_storage_path,file_id"
        print(f"[DELETE REPORT] Check URL: {url}")

        check_response = http_session.get(url, headers=get_supabase_headers())

        print(f"[DELETE REPORT] Check response status: {check_response.status_code}")
        print(f"[DELETE REPORT] Check response body: {check_response.text[:500]}")

        if not check_response.ok:
            print(f"[DELETE REPORT] Check failed with status {check_response.status_code}: {check_response.text}")
            return jsonify({'success': False, 'error': 'Report not found or unauthorized'}), 404

        reports = check_response.json()
        if not reports or len(reports) == 0:
            print(f"[DELETE REPORT] No report found with id={report_id} for user_id={user_id}")
            return jsonify({'success': False, 'error': 'Report not found or unauthorized'}), 404

        report_data = reports[0]
        print(f"[DELETE REPORT] Found report: {report_data}")

        # Delete the HTML files from disk if they exist
        # Try using file_id field first (new reports), then fall back to parsing html_storage_path (old reports)
        file_id = report_data.get('file_id')

        if not file_id:
            # Fall back to extracting from html_storage_path for old reports
            file_id_pattern = report_data.get('html_storage_path', '')
            if file_id_pattern:
                import re
                match = re.search(r'/([a-f0-9\-]+)_report\.html', file_id_pattern)
                if match:
                    file_id = match.group(1)

        if file_id:
            print(f"[DELETE REPORT] Deleting files for file_id={file_id}")
            basic_report = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}_report.html")
            ai_report = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}_report_with_ai.html")

            # Delete files if they exist
            if os.path.exists(basic_report):
                print(f"[DELETE REPORT] Deleting {basic_report}")
                os.remove(basic_report)
            if os.path.exists(ai_report):
                print(f"[DELETE REPORT] Deleting {ai_report}")
                os.remove(ai_report)
        else:
            print(f"[DELETE REPORT] No file_id found, skipping file deletion")

        # Delete from database
        delete_headers = get_supabase_headers()
        delete_headers['Prefer'] = 'return=minimal'  # Required for DELETE operations

        delete_url = f"{SUPABASE_REST_URL}/reports?id=eq.{report_id}"
        print(f"[DELETE REPORT] Deleting from database: {delete_url}")

        delete_response = http_session.delete(delete_url, headers=delete_headers)

        print(f"[DELETE REPORT] Delete response status: {delete_response.status_code}")
        print(f"[DELETE REPORT] Delete response body: {delete_response.text[:200] if delete_response.text else 'empty'}")

        if delete_response.ok or delete_response.status_code == 204:
            print(f"[DELETE REPORT] Successfully deleted report_id={report_id}")
            return jsonify({'success': True})
        else:
            print(f"[DELETE REPORT] Delete failed with status {delete_response.status_code}: {delete_response.text}")
            return jsonify({'success': False, 'error': f'Failed to delete report: {delete_response.text}'}), 500
    except Exception as e:
        print(f"[DELETE REPORT] EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

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
            subscription_response = http_session.get(
                f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}&select=stripe_customer_id",
                headers=get_supabase_headers()
            )
            stripe_customer_id = None
            if subscription_response.ok and subscription_response.json():
                subscription_data = subscription_response.json()[0]
                stripe_customer_id = subscription_data.get('stripe_customer_id')

            if not stripe_customer_id:
                # Create new Stripe customer
                customer = stripe.Customer.create(
                    email=user_email,
                    metadata={'user_id': user_id}
                )
                stripe_customer_id = customer.id

                # Update subscription record with customer ID
                http_session.patch(
                    f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
                    headers=get_supabase_headers(),
                    json={'stripe_customer_id': stripe_customer_id}
                )
        except Exception as e:
            print(f"Error creating/getting customer: {e}")
            # Create customer if error
            customer = stripe.Customer.create(
                email=user_email,
                metadata={'user_id': user_id}
            )
            stripe_customer_id = customer.id

        # Create checkout session based on plan type
        if plan_type == 'unlimited_basic':
            # Unlimited Basic - $69 one-time
            checkout_session = stripe.checkout.Session.create(
                customer=stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{'price': STRIPE_PRICE_UNLIMITED_BASIC, 'quantity': 1}],
                mode='payment',
                success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_for('payment_cancel', _external=True),
                metadata={'user_id': user_id}
            )
        elif plan_type == 'ai_package':
            # AI-Enhanced Package - $99 one-time
            checkout_session = stripe.checkout.Session.create(
                customer=stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{'price': STRIPE_PRICE_AI_PACKAGE, 'quantity': 1}],
                mode='payment',
                success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_for('payment_cancel', _external=True),
                metadata={'user_id': user_id}
            )
        elif plan_type == 'subscription':
            # Monthly Subscription - $39/month
            checkout_session = stripe.checkout.Session.create(
                customer=stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{'price': STRIPE_PRICE_SUBSCRIPTION, 'quantity': 1}],
                mode='subscription',
                success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_for('payment_cancel', _external=True),
                metadata={'user_id': user_id}
            )
        else:
            return jsonify({'error': 'Invalid plan type'}), 400

        return jsonify({'checkout_url': checkout_session.url})

    except stripe.error.InvalidRequestError as e:
        print(f"Stripe Invalid Request Error: {e}")
        print(f"  - Plan type: {plan_type}")
        print(f"  - Price IDs configured:")
        print(f"    UNLIMITED_BASIC: {STRIPE_PRICE_UNLIMITED_BASIC}")
        print(f"    AI_PACKAGE: {STRIPE_PRICE_AI_PACKAGE}")
        print(f"    SUBSCRIPTION: {STRIPE_PRICE_SUBSCRIPTION}")
        return jsonify({'error': f'Stripe error: {str(e)}'}), 400
    except Exception as e:
        print(f"Error creating checkout session: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
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
        user_id = session_data['metadata'].get('user_id')

        if not user_id:
            print("Error: No user_id in session metadata")
            return jsonify({'error': 'No user_id'}), 400

        try:
            # Get the line items to determine which product was purchased
            session_id = session_data['id']
            session = stripe.checkout.Session.retrieve(session_id, expand=['line_items'])

            if session.line_items and len(session.line_items.data) > 0:
                price_id = session.line_items.data[0].price.id

                # Determine which plan based on price ID
                if price_id == STRIPE_PRICE_UNLIMITED_BASIC:
                    # Unlimited Basic ($69) - unlimited reports, no AI
                    http_session.patch(
                        f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
                        headers=get_supabase_headers(),
                        json={
                            'plan_name': 'unlimited_basic',
                            'status': 'active',
                            'reports_limit': 9999,
                            'ai_credits': 0
                        }
                    )
                    print(f"✅ User {user_id} upgraded to Unlimited Basic")

                elif price_id == STRIPE_PRICE_AI_PACKAGE:
                    # AI-Enhanced Package ($99) - unlimited reports + 10 AI credits
                    http_session.patch(
                        f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
                        headers=get_supabase_headers(),
                        json={
                            'plan_name': 'ai_package',
                            'status': 'active',
                            'reports_limit': 9999,
                            'ai_credits': 10
                        }
                    )
                    print(f"✅ User {user_id} upgraded to AI-Enhanced Package")

                elif price_id == STRIPE_PRICE_SUBSCRIPTION:
                    # Monthly Subscription ($39/mo) - unlimited everything
                    stripe_subscription_id = session_data.get('subscription')
                    http_session.patch(
                        f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
                        headers=get_supabase_headers(),
                        json={
                            'stripe_subscription_id': stripe_subscription_id,
                            'plan_name': 'subscription',
                            'status': 'active',
                            'reports_limit': 9999,
                            'ai_credits': 9999,
                            'period_start': datetime.utcnow().isoformat(),
                        }
                    )
                    print(f"✅ User {user_id} subscribed to Monthly plan")

                else:
                    print(f"⚠️ Unknown price ID: {price_id}")

        except Exception as e:
            print(f"❌ Error updating subscription: {e}")

    elif event['type'] == 'customer.subscription.deleted':
        # Subscription cancelled - downgrade to free tier
        subscription_data = event['data']['object']
        customer_id = subscription_data['customer']

        try:
            # Find user by customer ID and downgrade to free tier
            sub_response = http_session.get(
                f"{SUPABASE_REST_URL}/subscriptions?stripe_customer_id=eq.{customer_id}&select=user_id",
                headers=get_supabase_headers()
            )
            if sub_response.ok and sub_response.json():
                http_session.patch(
                    f"{SUPABASE_REST_URL}/subscriptions?stripe_customer_id=eq.{customer_id}",
                    headers=get_supabase_headers(),
                    json={
                        'plan_name': 'free',
                        'status': 'active',
                        'reports_limit': 2,  # New free tier limit
                        'ai_credits': 0,
                        'stripe_subscription_id': None
                    }
                )
                print(f"✅ Subscription cancelled - user downgraded to free tier (2 reports)")
        except Exception as e:
            print(f"❌ Error handling subscription deletion: {e}")

    return jsonify({'status': 'success'}), 200

@app.route('/payment-success')
@login_required
def payment_success():
    """Payment success page - also handles subscription update for localhost testing"""
    session_id = request.args.get('session_id')
    user_id = session['user']['id']

    print(f"[PAYMENT SUCCESS] Starting - session_id={session_id}, user_id={user_id}")

    try:
        if session_id:
            print(f"[PAYMENT SUCCESS] Retrieving Stripe session: {session_id}")
            # Retrieve the checkout session from Stripe
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            print(f"[PAYMENT SUCCESS] Checkout session mode: {checkout_session.mode}")

            # Get the price ID to determine what was purchased
            if checkout_session.mode == 'payment':
                print(f"[PAYMENT SUCCESS] Processing one-time payment")
                # One-time payment
                line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
                if line_items.data:
                    price_id = line_items.data[0].price.id

                    # Update subscription based on price
                    if price_id == STRIPE_PRICE_UNLIMITED_BASIC:
                        # $69 Unlimited Basic - Set unlimited reports
                        print(f"[PAYMENT SUCCESS] Granting unlimited reports to user {user_id}")
                        http_session.patch(
                            f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
                            headers=get_supabase_headers(),
                            json={
                                'plan_name': 'unlimited_basic',
                                'reports_limit': 999999,
                                'ai_credits': 0
                            }
                        )
                    elif price_id == STRIPE_PRICE_AI_PACKAGE:
                        # $99 AI Package - Add 10 AI credits
                        print(f"[PAYMENT SUCCESS] Granting 10 AI credits to user {user_id}")
                        http_session.patch(
                            f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
                            headers=get_supabase_headers(),
                            json={
                                'plan_name': 'ai_package',
                                'reports_limit': 999999,
                                'ai_credits': 10
                            }
                        )
            elif checkout_session.mode == 'subscription':
                # Monthly subscription - $39/month unlimited
                print(f"[PAYMENT SUCCESS] Activating subscription for user {user_id}")
                http_session.patch(
                    f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
                    headers=get_supabase_headers(),
                    json={
                        'plan_name': 'subscription',
                        'reports_limit': 999999,
                        'ai_credits': 999999,
                        'stripe_subscription_id': checkout_session.subscription
                    }
                )

            print(f"[PAYMENT SUCCESS] Subscription updated successfully for user {user_id}")
    except Exception as e:
        print(f"[PAYMENT SUCCESS] Error updating subscription: {e}")
        import traceback
        traceback.print_exc()

    return render_template('payment_success.html', session_id=session_id)

@app.route('/payment-cancel')
@login_required
def payment_cancel():
    """Payment cancelled page"""
    return render_template('payment_cancel.html')

# ========================================
# AI RECOMMENDATIONS SYSTEM
# ========================================

@app.route('/ai-recommendations')
@login_required
def ai_recommendations_page():
    """AI-powered recommendations page"""
    try:
        # Initialize AI system
        ai = UniversalRecommendationAI()
        available_subjects = ai.get_available_subjects()
    except Exception as e:
        # If AI system fails to initialize (e.g., missing API key), use defaults
        print(f"AI system initialization error: {e}")
        available_subjects = ['peptides', 'supplements', 'training', 'nutrition', 'recovery', 'longevity']

    return render_template('ai_recommendations.html',
                         subjects=available_subjects)

@app.route('/ai-examples')
def ai_examples():
    """AI recommendations examples and tutorial page"""
    return render_template('ai_examples.html')

@app.route('/api/check-ai-status')
def check_ai_status():
    """Check if AI API keys are configured"""
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')

    # Determine which provider will be used
    active_provider = None
    if anthropic_key:
        active_provider = 'claude'
    elif openai_key:
        active_provider = 'openai'

    # Test OpenAI connectivity if that's what will be used
    openai_test = "not tested"
    if openai_key:
        try:
            import socket
            socket.setdefaulttimeout(5)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("api.openai.com", 443))
            openai_test = "success"
        except Exception as e:
            openai_test = f"failed: {str(e)}"

    return jsonify({
        'ai_configured': bool(anthropic_key or openai_key),
        'active_provider': active_provider,
        'anthropic_api_key': {
            'configured': bool(anthropic_key),
            'length': len(anthropic_key) if anthropic_key else 0,
            'prefix': anthropic_key[:10] + '...' if anthropic_key else None
        },
        'openai_api_key': {
            'configured': bool(openai_key),
            'length': len(openai_key) if openai_key else 0,
            'prefix': openai_key[:7] + '...' if openai_key else None
        },
        'openai_connectivity': openai_test
    })

@app.route('/api/ai-recommend', methods=['POST'])
@login_required
def generate_ai_recommendation():
    """Generate AI-powered recommendations for any subject"""
    try:
        data = request.get_json()
        subject = data.get('subject', 'peptides')
        user_goals = data.get('goals', [])
        custom_context = data.get('custom_context', '')

        user_id = session['user']['id']
        user_email = session['user']['email']

        print(f"[AI RECOMMEND] user_id: {user_id}")
        print(f"[AI RECOMMEND] user_email: {user_email}")
        print(f"[AI RECOMMEND] subject: {subject}")

        # CHECK AI CREDITS
        can_use_ai, message = can_use_ai_recommendations(user_id)
        if not can_use_ai:
            return jsonify({
                'error': message,
                'upgrade_required': True,
                'pricing_url': '/pricing'
            }), 403

        # Get user's metabolic data from their latest report
        metabolic_data = get_user_metabolic_data(user_email)

        if not metabolic_data:
            return jsonify({
                'error': 'No metabolic data found. Please upload a test first.'
            }), 400

        # Initialize AI system
        ai = UniversalRecommendationAI()

        # Generate recommendations
        recommendations = ai.get_recommendations(
            subject=subject,
            metabolic_data=metabolic_data,
            user_goals=user_goals,
            custom_context=custom_context
        )

        print(f"[AI RECOMMEND] Recommendations generated: {recommendations.keys()}")
        print(f"[AI RECOMMEND] Has error: {'error' in recommendations}")

        # USE AI CREDIT (decrement counter)
        use_ai_credit(user_id)

        # Store recommendation in database
        save_recommendation_to_db(user_email, subject, recommendations)

        return jsonify(recommendations)

    except Exception as e:
        print(f"Error generating AI recommendations: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# INTERVIEW ANALYZER API (Public - for bigoil.net)
# ============================================================================

def add_cors_headers(response):
    """Add CORS headers to response"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    return response

def save_interview_report(transcript, job_description, candidate_name, job_title, result, request_obj):
    """Save interview report to Supabase database"""
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY', '').strip()

        if not supabase_url or not supabase_key:
            print("[INTERVIEW] Supabase not configured, skipping save")
            return None

        report_data = {
            'candidate_name': candidate_name or 'Unknown Candidate',
            'job_title': job_title or 'Unknown Position',
            'transcript': transcript[:10000],  # Limit size
            'job_description': job_description[:5000],
            'fit_score': result.get('fit_score'),
            'strengths': json.dumps(result.get('strengths', [])),
            'matching_skills': json.dumps(result.get('matching_skills', [])),
            'concerns': json.dumps(result.get('concerns', [])),
            'notable_quotes': json.dumps(result.get('notable_quotes', [])),
            'summary': result.get('summary', ''),
            'full_response': json.dumps(result),
            'ip_address': request_obj.remote_addr,
            'user_agent': request_obj.headers.get('User-Agent', '')[:500]
        }

        response = requests.post(
            f"{supabase_url}/rest/v1/interview_reports",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            },
            json=report_data
        )

        if response.status_code in [200, 201]:
            saved = response.json()
            report_id = saved[0]['id'] if saved else None
            print(f"[INTERVIEW] Report saved with ID: {report_id}")
            return report_id
        else:
            print(f"[INTERVIEW] Failed to save report: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"[INTERVIEW] Error saving report: {e}")
        return None

# ============================================================================
# JOB DESCRIPTIONS API
# ============================================================================

@app.route('/api/job-descriptions', methods=['GET', 'POST', 'OPTIONS'])
def job_descriptions():
    """List or create job descriptions"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return add_cors_headers(response)

    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY', '').strip()

    if not supabase_url or not supabase_key:
        response = jsonify({'error': 'Database not configured'})
        return add_cors_headers(response), 500

    if request.method == 'POST':
        try:
            data = request.get_json()
            title = data.get('title', '').strip()
            description = data.get('description', '').strip()

            if not title or not description:
                response = jsonify({'error': 'Title and description are required'})
                return add_cors_headers(response), 400

            job_data = {
                'title': title,
                'description': description[:10000],
                'company': data.get('company', ''),
                'department': data.get('department', '')
            }

            db_response = requests.post(
                f"{supabase_url}/rest/v1/job_descriptions",
                headers={
                    "apikey": supabase_key,
                    "Authorization": f"Bearer {supabase_key}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                },
                json=job_data
            )

            if db_response.status_code in [200, 201]:
                saved = db_response.json()
                response = jsonify({'success': True, 'job': saved[0] if saved else None})
                return add_cors_headers(response)
            else:
                print(f"[JOB] Failed to save: {db_response.status_code} - {db_response.text}")
                response = jsonify({'error': f'Failed to save job description: {db_response.status_code}'})
                return add_cors_headers(response), 500

        except Exception as e:
            print(f"Error saving job description: {e}")
            response = jsonify({'error': str(e)})
            return add_cors_headers(response), 500

    else:  # GET
        try:
            db_response = requests.get(
                f"{supabase_url}/rest/v1/job_descriptions",
                headers={
                    "apikey": supabase_key,
                    "Authorization": f"Bearer {supabase_key}",
                    "Content-Type": "application/json"
                },
                params={
                    "select": "id,created_at,title,company,department",
                    "order": "created_at.desc"
                }
            )

            if db_response.status_code == 200:
                response = jsonify({'jobs': db_response.json()})
                return add_cors_headers(response)
            else:
                print(f"[JOB] Failed to fetch: {db_response.status_code} - {db_response.text}")
                response = jsonify({'error': f'Failed to fetch job descriptions: {db_response.status_code}'})
                return add_cors_headers(response), 500

        except Exception as e:
            print(f"Error listing job descriptions: {e}")
            response = jsonify({'error': str(e)})
            return add_cors_headers(response), 500


@app.route('/api/job-descriptions/<job_id>', methods=['GET', 'DELETE', 'OPTIONS'])
def job_description_detail(job_id):
    """Get or delete a job description"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return add_cors_headers(response)

    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY', '').strip()

    if request.method == 'DELETE':
        db_response = requests.delete(
            f"{supabase_url}/rest/v1/job_descriptions",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json"
            },
            params={"id": f"eq.{job_id}"}
        )
        if db_response.status_code in [200, 204]:
            response = jsonify({'success': True})
            return add_cors_headers(response)
        else:
            response = jsonify({'error': 'Failed to delete'})
            return add_cors_headers(response), 500
    else:  # GET
        db_response = requests.get(
            f"{supabase_url}/rest/v1/job_descriptions",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json"
            },
            params={"id": f"eq.{job_id}", "select": "*"}
        )
        if db_response.status_code == 200 and db_response.json():
            response = jsonify(db_response.json()[0])
            return add_cors_headers(response)
        else:
            response = jsonify({'error': 'Not found'})
            return add_cors_headers(response), 404


@app.route('/api/batch-analyze', methods=['POST', 'OPTIONS'])
def batch_analyze():
    """
    Analyze multiple drafts against a single job description.
    """
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return add_cors_headers(response)

    try:
        data = request.get_json()
        draft_ids = data.get('draft_ids', [])
        job_id = data.get('job_id')

        if not draft_ids or not job_id:
            response = jsonify({'error': 'draft_ids and job_id are required'})
            return add_cors_headers(response), 400

        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY', '').strip()
        openai_key = os.getenv('OPENAI_API_KEY')

        if not openai_key:
            response = jsonify({'error': 'AI service not configured'})
            return add_cors_headers(response), 500

        # Fetch job description
        job_response = requests.get(
            f"{supabase_url}/rest/v1/job_descriptions",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json"
            },
            params={"id": f"eq.{job_id}", "select": "*"}
        )

        if job_response.status_code != 200 or not job_response.json():
            response = jsonify({'error': 'Job description not found'})
            return add_cors_headers(response), 404

        job = job_response.json()[0]
        job_description = job['description']
        job_title = job['title']

        results = []
        import openai
        client = openai.OpenAI(api_key=openai_key)

        for draft_id in draft_ids:
            try:
                # Fetch draft
                draft_response = requests.get(
                    f"{supabase_url}/rest/v1/interview_reports",
                    headers={
                        "apikey": supabase_key,
                        "Authorization": f"Bearer {supabase_key}",
                        "Content-Type": "application/json"
                    },
                    params={"id": f"eq.{draft_id}", "select": "*"}
                )

                if draft_response.status_code != 200 or not draft_response.json():
                    results.append({'draft_id': draft_id, 'success': False, 'error': 'Draft not found'})
                    continue

                draft = draft_response.json()[0]
                transcript = draft.get('transcript', '')
                candidate_name = draft.get('candidate_name', '')

                if not transcript:
                    results.append({'draft_id': draft_id, 'success': False, 'error': 'No transcript'})
                    continue

                # Build prompt
                prompt = f"""You are an expert HR analyst and interview coach. Analyze this interview transcript against the job description and provide a detailed candidate fit report.

JOB DESCRIPTION:
{job_description}

INTERVIEW TRANSCRIPT:
{transcript}

INSTRUCTIONS:
1. First, identify who is the interviewer vs the candidate (the candidate is the one answering questions, sharing their experience, etc.)
2. Focus ONLY on what the candidate said - ignore interviewer questions
3. Compare the candidate's responses against the job requirements
4. Be objective and evidence-based - cite specific things the candidate said

Provide your analysis in this exact JSON format:
{{
    "fit_score": <number 0-100>,
    "strengths": ["Strength 1", "Strength 2", "Strength 3"],
    "matching_skills": ["Skill 1", "Skill 2", "Skill 3"],
    "concerns": ["Concern 1", "Concern 2"],
    "notable_quotes": [{{"quote": "Quote text", "context": "Why significant"}}],
    "summary": "2-3 paragraph summary."
}}

Return ONLY valid JSON, no additional text."""

                ai_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert HR analyst. Always respond with valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )

                result_text = ai_response.choices[0].message.content.strip()
                if result_text.startswith('```'):
                    result_text = result_text.split('```')[1]
                    if result_text.startswith('json'):
                        result_text = result_text[4:]
                result_text = result_text.strip()

                analysis = json.loads(result_text)

                # Update draft with results
                update_data = {
                    'job_description': job_description[:5000],
                    'job_title': job_title,
                    'fit_score': analysis.get('fit_score'),
                    'strengths': json.dumps(analysis.get('strengths', [])),
                    'matching_skills': json.dumps(analysis.get('matching_skills', [])),
                    'concerns': json.dumps(analysis.get('concerns', [])),
                    'notable_quotes': json.dumps(analysis.get('notable_quotes', [])),
                    'summary': analysis.get('summary', ''),
                    'full_response': json.dumps(analysis)
                }

                requests.patch(
                    f"{supabase_url}/rest/v1/interview_reports",
                    headers={
                        "apikey": supabase_key,
                        "Authorization": f"Bearer {supabase_key}",
                        "Content-Type": "application/json"
                    },
                    params={"id": f"eq.{draft_id}"},
                    json=update_data
                )

                results.append({
                    'draft_id': draft_id,
                    'success': True,
                    'candidate_name': candidate_name,
                    'fit_score': analysis.get('fit_score')
                })

            except Exception as e:
                print(f"Error analyzing draft {draft_id}: {e}")
                results.append({'draft_id': draft_id, 'success': False, 'error': str(e)})

        response = jsonify({'results': results})
        return add_cors_headers(response)

    except Exception as e:
        print(f"Error in batch analyze: {e}")
        import traceback
        traceback.print_exc()
        response = jsonify({'error': str(e)})
        return add_cors_headers(response), 500


@app.route('/api/interview-drafts', methods=['POST', 'OPTIONS'])
def save_interview_draft():
    """
    Save a draft interview transcript without running analysis.
    Used for bulk uploading transcripts before adding job descriptions.
    """
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return add_cors_headers(response)

    try:
        data = request.get_json()
        transcript = data.get('transcript', '')
        candidate_name = data.get('candidate_name', '')

        if not transcript:
            response = jsonify({'error': 'Transcript is required'})
            return add_cors_headers(response), 400

        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY', '').strip()

        if not supabase_url or not supabase_key:
            response = jsonify({'error': 'Database not configured'})
            return add_cors_headers(response), 500

        # Save as draft (no job description, no analysis)
        draft_data = {
            'candidate_name': candidate_name or 'Unknown Candidate',
            'job_title': '',
            'transcript': transcript[:10000],
            'job_description': '',
            'fit_score': None,
            'strengths': None,
            'matching_skills': None,
            'concerns': None,
            'notable_quotes': None,
            'summary': None,
            'full_response': None,
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', '')[:500]
        }

        db_response = requests.post(
            f"{supabase_url}/rest/v1/interview_reports",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            },
            json=draft_data
        )

        if db_response.status_code in [200, 201]:
            saved = db_response.json()
            draft_id = saved[0]['id'] if saved else None
            print(f"[INTERVIEW] Draft saved with ID: {draft_id}")
            response = jsonify({'success': True, 'draft_id': draft_id, 'candidate_name': candidate_name})
            return add_cors_headers(response)
        else:
            print(f"[INTERVIEW] Failed to save draft: {db_response.status_code} - {db_response.text}")
            response = jsonify({'error': 'Failed to save draft'})
            return add_cors_headers(response), 500

    except Exception as e:
        print(f"Error saving interview draft: {e}")
        response = jsonify({'error': str(e)})
        return add_cors_headers(response), 500


@app.route('/api/interview-reports/<report_id>/analyze', methods=['POST', 'OPTIONS'])
def analyze_existing_draft(report_id):
    """
    Run analysis on an existing draft by adding job description.
    """
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return add_cors_headers(response)

    try:
        data = request.get_json()
        job_description = data.get('job_description', '')
        job_title = data.get('job_title', '')

        if not job_description:
            response = jsonify({'error': 'Job description is required'})
            return add_cors_headers(response), 400

        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY', '').strip()

        # Fetch the draft
        db_response = requests.get(
            f"{supabase_url}/rest/v1/interview_reports",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json"
            },
            params={"id": f"eq.{report_id}", "select": "*"}
        )

        if db_response.status_code != 200 or not db_response.json():
            response = jsonify({'error': 'Draft not found'})
            return add_cors_headers(response), 404

        draft = db_response.json()[0]
        transcript = draft.get('transcript', '')
        candidate_name = draft.get('candidate_name', '')

        if not transcript:
            response = jsonify({'error': 'Draft has no transcript'})
            return add_cors_headers(response), 400

        # Get OpenAI API key
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            response = jsonify({'error': 'AI service not configured'})
            return add_cors_headers(response), 500

        # Build the analysis prompt
        prompt = f"""You are an expert HR analyst and interview coach. Analyze this interview transcript against the job description and provide a detailed candidate fit report.

JOB DESCRIPTION:
{job_description}

INTERVIEW TRANSCRIPT:
{transcript}

INSTRUCTIONS:
1. First, identify who is the interviewer vs the candidate (the candidate is the one answering questions, sharing their experience, etc.)
2. Focus ONLY on what the candidate said - ignore interviewer questions
3. Compare the candidate's responses against the job requirements
4. Be objective and evidence-based - cite specific things the candidate said

Provide your analysis in this exact JSON format:
{{
    "fit_score": <number 0-100>,
    "strengths": [
        "Strength 1 with specific evidence from transcript",
        "Strength 2 with specific evidence",
        "Strength 3 with specific evidence"
    ],
    "matching_skills": [
        "Skill/experience that matches job requirement 1",
        "Skill/experience that matches job requirement 2",
        "Skill/experience that matches job requirement 3"
    ],
    "concerns": [
        "Potential gap or area to explore further 1",
        "Potential gap or area to explore further 2"
    ],
    "notable_quotes": [
        {{"quote": "Exact quote from candidate", "context": "Why this quote is significant"}},
        {{"quote": "Another notable quote", "context": "Why significant"}}
    ],
    "summary": "2-3 paragraph summary of why this candidate would or would not be a good fit, with specific evidence from the interview."
}}

Return ONLY valid JSON, no additional text."""

        # Call OpenAI API
        import openai
        client = openai.OpenAI(api_key=openai_key)

        ai_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert HR analyst. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        result_text = ai_response.choices[0].message.content.strip()

        if result_text.startswith('```'):
            result_text = result_text.split('```')[1]
            if result_text.startswith('json'):
                result_text = result_text[4:]
        result_text = result_text.strip()

        result = json.loads(result_text)

        # Update the draft with analysis results
        update_data = {
            'job_description': job_description[:5000],
            'job_title': job_title or '',
            'fit_score': result.get('fit_score'),
            'strengths': json.dumps(result.get('strengths', [])),
            'matching_skills': json.dumps(result.get('matching_skills', [])),
            'concerns': json.dumps(result.get('concerns', [])),
            'notable_quotes': json.dumps(result.get('notable_quotes', [])),
            'summary': result.get('summary', ''),
            'full_response': json.dumps(result)
        }

        db_update = requests.patch(
            f"{supabase_url}/rest/v1/interview_reports",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json"
            },
            params={"id": f"eq.{report_id}"},
            json=update_data
        )

        if db_update.status_code not in [200, 204]:
            print(f"[INTERVIEW] Failed to update draft: {db_update.status_code}")

        result['report_id'] = report_id
        result['candidate_name'] = candidate_name
        result['job_title'] = job_title

        response = jsonify(result)
        return add_cors_headers(response)

    except json.JSONDecodeError as e:
        print(f"JSON parse error in draft analysis: {e}")
        response = jsonify({'error': 'Failed to parse AI response'})
        return add_cors_headers(response), 500
    except Exception as e:
        print(f"Error analyzing draft: {e}")
        import traceback
        traceback.print_exc()
        response = jsonify({'error': str(e)})
        return add_cors_headers(response), 500


@app.route('/api/analyze-interview', methods=['POST', 'OPTIONS'])
def analyze_interview():
    """
    Analyze an interview transcript against a job description.
    Public API endpoint for bigoil.net interview analyzer tool.
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return add_cors_headers(response)

    try:
        data = request.get_json()
        transcript = data.get('transcript', '')
        job_description = data.get('job_description', '')
        candidate_name = data.get('candidate_name', '')
        job_title = data.get('job_title', '')

        if not transcript or not job_description:
            response = jsonify({'error': 'Both transcript and job_description are required'})
            return add_cors_headers(response), 400

        # Get OpenAI API key
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            return jsonify({'error': 'AI service not configured'}), 500

        # Build the analysis prompt
        prompt = f"""You are an expert HR analyst and interview coach. Analyze this interview transcript against the job description and provide a detailed candidate fit report.

JOB DESCRIPTION:
{job_description}

INTERVIEW TRANSCRIPT:
{transcript}

INSTRUCTIONS:
1. First, identify who is the interviewer vs the candidate (the candidate is the one answering questions, sharing their experience, etc.)
2. Focus ONLY on what the candidate said - ignore interviewer questions
3. Compare the candidate's responses against the job requirements
4. Be objective and evidence-based - cite specific things the candidate said

Provide your analysis in this exact JSON format:
{{
    "fit_score": <number 0-100>,
    "strengths": [
        "Strength 1 with specific evidence from transcript",
        "Strength 2 with specific evidence",
        "Strength 3 with specific evidence"
    ],
    "matching_skills": [
        "Skill/experience that matches job requirement 1",
        "Skill/experience that matches job requirement 2",
        "Skill/experience that matches job requirement 3"
    ],
    "concerns": [
        "Potential gap or area to explore further 1",
        "Potential gap or area to explore further 2"
    ],
    "notable_quotes": [
        {{"quote": "Exact quote from candidate", "context": "Why this quote is significant"}},
        {{"quote": "Another notable quote", "context": "Why significant"}}
    ],
    "summary": "2-3 paragraph summary of why this candidate would or would not be a good fit, with specific evidence from the interview."
}}

Return ONLY valid JSON, no additional text."""

        # Call OpenAI API
        import openai
        client = openai.OpenAI(api_key=openai_key)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert HR analyst. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        # Parse the response
        result_text = response.choices[0].message.content.strip()

        # Clean up potential markdown code blocks
        if result_text.startswith('```'):
            result_text = result_text.split('```')[1]
            if result_text.startswith('json'):
                result_text = result_text[4:]
        result_text = result_text.strip()

        result = json.loads(result_text)

        # Save report to database
        report_id = save_interview_report(
            transcript, job_description, candidate_name, job_title, result, request
        )

        # Add report_id to result
        result['report_id'] = report_id

        # Add CORS header to response
        response = jsonify(result)
        return add_cors_headers(response)

    except json.JSONDecodeError as e:
        print(f"JSON parse error in interview analysis: {e}")
        print(f"Raw response: {result_text[:500] if 'result_text' in dir() else 'N/A'}")
        response = jsonify({'error': 'Failed to parse AI response'})
        return add_cors_headers(response), 500
    except Exception as e:
        print(f"Error in interview analysis: {e}")
        import traceback
        traceback.print_exc()
        response = jsonify({'error': str(e)})
        return add_cors_headers(response), 500


@app.route('/api/interview-reports', methods=['GET', 'OPTIONS'])
def list_interview_reports():
    """List all saved interview reports"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return add_cors_headers(response)

    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY', '').strip()

        if not supabase_url or not supabase_key:
            response = jsonify({'error': 'Database not configured'})
            return add_cors_headers(response), 500

        # Get reports, most recent first
        db_response = requests.get(
            f"{supabase_url}/rest/v1/interview_reports",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json"
            },
            params={
                "select": "id,created_at,candidate_name,job_title,fit_score",
                "order": "created_at.desc",
                "limit": "50"
            }
        )

        if db_response.status_code == 200:
            reports = db_response.json()
            response = jsonify({'reports': reports})
            return add_cors_headers(response)
        else:
            response = jsonify({'error': 'Failed to fetch reports'})
            return add_cors_headers(response), 500

    except Exception as e:
        print(f"Error listing interview reports: {e}")
        response = jsonify({'error': str(e)})
        return add_cors_headers(response), 500


@app.route('/api/interview-reports/<report_id>', methods=['GET', 'DELETE', 'PATCH', 'OPTIONS'])
def get_or_delete_interview_report(report_id):
    """Get, update, or delete a specific interview report"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return add_cors_headers(response)

    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY', '').strip()

        if not supabase_url or not supabase_key:
            response = jsonify({'error': 'Database not configured'})
            return add_cors_headers(response), 500

        if request.method == 'DELETE':
            # Delete report
            db_response = requests.delete(
                f"{supabase_url}/rest/v1/interview_reports",
                headers={
                    "apikey": supabase_key,
                    "Authorization": f"Bearer {supabase_key}",
                    "Content-Type": "application/json"
                },
                params={"id": f"eq.{report_id}"}
            )

            if db_response.status_code in [200, 204]:
                response = jsonify({'success': True})
                return add_cors_headers(response)
            else:
                response = jsonify({'error': 'Failed to delete report'})
                return add_cors_headers(response), 500

        elif request.method == 'PATCH':
            # Update report (candidate_name, job_title)
            data = request.get_json()
            update_data = {}

            # Only allow updating specific fields
            if 'candidate_name' in data:
                update_data['candidate_name'] = data['candidate_name']
            if 'job_title' in data:
                update_data['job_title'] = data['job_title']

            if not update_data:
                response = jsonify({'error': 'No valid fields to update'})
                return add_cors_headers(response), 400

            db_response = requests.patch(
                f"{supabase_url}/rest/v1/interview_reports",
                headers={
                    "apikey": supabase_key,
                    "Authorization": f"Bearer {supabase_key}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                },
                params={"id": f"eq.{report_id}"},
                json=update_data
            )

            if db_response.status_code in [200, 204]:
                response = jsonify({'success': True, 'updated': update_data})
                return add_cors_headers(response)
            else:
                print(f"[INTERVIEW] Update failed: {db_response.status_code} - {db_response.text}")
                response = jsonify({'error': 'Failed to update report'})
                return add_cors_headers(response), 500

        else:
            # GET - fetch full report
            db_response = requests.get(
                f"{supabase_url}/rest/v1/interview_reports",
                headers={
                    "apikey": supabase_key,
                    "Authorization": f"Bearer {supabase_key}",
                    "Content-Type": "application/json"
                },
                params={
                    "id": f"eq.{report_id}",
                    "select": "*"
                }
            )

            if db_response.status_code == 200:
                reports = db_response.json()
                if reports:
                    report = reports[0]
                    # Parse JSON fields
                    for field in ['strengths', 'matching_skills', 'concerns', 'notable_quotes', 'full_response']:
                        if report.get(field) and isinstance(report[field], str):
                            try:
                                report[field] = json.loads(report[field])
                            except:
                                pass
                    response = jsonify(report)
                    return add_cors_headers(response)
                else:
                    response = jsonify({'error': 'Report not found'})
                    return add_cors_headers(response), 404
            else:
                response = jsonify({'error': 'Failed to fetch report'})
                return add_cors_headers(response), 500

    except Exception as e:
        print(f"Error with interview report {report_id}: {e}")
        response = jsonify({'error': str(e)})
        return add_cors_headers(response), 500


def get_user_metabolic_data(email):
    """Extract metabolic data from user's latest report"""
    try:
        # Connect to Supabase
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')

        if not supabase_url or not supabase_key:
            print("Warning: Supabase credentials not found, using sample data")
            return get_sample_metabolic_data()

        # Fetch user's latest report from Supabase
        response = requests.get(
            f"{supabase_url}/rest/v1/reports",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json"
            },
            params={
                "user_email": f"eq.{email}",
                "select": "*",
                "order": "created_at.desc",
                "limit": "1"
            }
        )

        if response.status_code == 200 and response.json():
            report = response.json()[0]
            # Extract metabolic metrics from report
            return extract_metabolic_metrics(report)
        else:
            print(f"No report found for user {email}, using sample data")
            return get_sample_metabolic_data()

    except Exception as e:
        print(f"Error fetching metabolic data: {e}")
        return get_sample_metabolic_data()

def extract_metabolic_metrics(report):
    """Extract key metrics from report data"""
    # Parse report data (adjust based on your actual data structure)
    return {
        'vo2_max': report.get('vo2_max', 45),
        'rmr': report.get('rmr', 1800),
        'max_hr': report.get('max_hr', 180),
        'resting_hr': report.get('resting_hr', 60),
        'fat_oxidation': report.get('fat_oxidation', 0.5),
        'carb_oxidation': report.get('carb_oxidation', 2.0),
        'rer': report.get('rer', 0.85),
        'age': report.get('age', 35),
        'gender': report.get('gender', 'Male'),
        'weight': report.get('weight', 75),
        'height': report.get('height', 180),
        'biological_age': report.get('biological_age', 33),
        'metabolic_score': report.get('metabolic_score', 75)
    }

def get_sample_metabolic_data():
    """Sample data for testing"""
    return {
        'vo2_max': 45,
        'rmr': 1800,
        'max_hr': 180,
        'resting_hr': 60,
        'fat_oxidation': 0.5,
        'carb_oxidation': 2.0,
        'rer': 0.85,
        'age': 35,
        'gender': 'Male',
        'weight': 75,
        'height': 180,
        'biological_age': 33,
        'metabolic_score': 75
    }

def save_recommendation_to_db(email, subject, recommendations):
    """Save AI recommendation to database"""
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')

        if not supabase_url or not supabase_key:
            print("Supabase credentials not found, skipping save")
            return

        # Save to database
        response = requests.post(
            f"{supabase_url}/rest/v1/ai_recommendations",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            },
            json={
                "user_email": email,
                "subject": subject,
                "recommendations": recommendations['recommendations'],
                "created_at": datetime.now().isoformat()
            }
        )

        if response.status_code != 201:
            print(f"Warning: Failed to save recommendation: {response.text}")

    except Exception as e:
        print(f"Error saving recommendation: {e}")

# Global error handlers for AJAX requests
@app.errorhandler(404)
def not_found_error(error):
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'error': 'Resource not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'error': 'Internal server error. Please try again.'}), 500
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_exception(error):
    # Log the error
    print(f"Unhandled exception: {error}")
    import traceback
    traceback.print_exc()

    # Return JSON for AJAX requests
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'error': f'An error occurred: {str(error)}'}), 500

    # Otherwise return HTML error page
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🚀 Starting Metabolic Report Generator Web App")
    print("📂 Upload folder:", app.config['UPLOAD_FOLDER'])
    print("📂 Reports folder:", app.config['REPORTS_FOLDER'])
    print("\n🌐 Open your browser to: http://localhost:8080")
    print("\n⚠️  Press CTRL+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=8080)
