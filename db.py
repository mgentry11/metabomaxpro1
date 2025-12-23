"""
Database module for MetaboMax Pro
HIPAA-compliant PostgreSQL connection to AWS RDS
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')

# Parse DATABASE_URL or use individual env vars
if DATABASE_URL:
    # Render provides DATABASE_URL in postgres:// format
    # psycopg2 needs postgresql://
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
else:
    # Build from individual env vars
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'metabomaxpro')
    DB_USER = os.getenv('DB_USER', 'metabomaxadmin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"


@contextmanager
def get_db_connection():
    """Get a database connection with automatic cleanup"""
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        yield conn
    finally:
        if conn:
            conn.close()


@contextmanager
def get_db_cursor(commit=True):
    """Get a database cursor with automatic commit/rollback"""
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()


# ============================================
# Profile/User Operations
# ============================================

def get_profile_by_email(email):
    """Get user profile by email"""
    with get_db_cursor(commit=False) as cur:
        cur.execute(
            "SELECT id, email, full_name, password_hash FROM profiles WHERE email = %s",
            (email,)
        )
        return cur.fetchone()


def get_profile_by_id(user_id):
    """Get user profile by ID"""
    with get_db_cursor(commit=False) as cur:
        cur.execute(
            "SELECT id, email, full_name FROM profiles WHERE id = %s",
            (user_id,)
        )
        return cur.fetchone()


def create_profile(email, password_hash, full_name=None, company_name=None):
    """Create a new user profile"""
    with get_db_cursor() as cur:
        cur.execute(
            """INSERT INTO profiles (email, password_hash, full_name, company_name)
               VALUES (%s, %s, %s, %s)
               RETURNING id, email, full_name""",
            (email, password_hash, full_name, company_name)
        )
        return cur.fetchone()


def update_profile(user_id, **kwargs):
    """Update user profile fields"""
    if not kwargs:
        return None

    set_clauses = []
    values = []
    for key, value in kwargs.items():
        if key in ['full_name', 'company_name', 'email']:
            set_clauses.append(f"{key} = %s")
            values.append(value)

    if not set_clauses:
        return None

    values.append(user_id)

    with get_db_cursor() as cur:
        cur.execute(
            f"UPDATE profiles SET {', '.join(set_clauses)} WHERE id = %s RETURNING *",
            tuple(values)
        )
        return cur.fetchone()


def check_email_exists(email):
    """Check if email already exists"""
    with get_db_cursor(commit=False) as cur:
        cur.execute("SELECT id FROM profiles WHERE email = %s", (email,))
        return cur.fetchone() is not None


# ============================================
# Subscription Operations
# ============================================

def get_subscription(user_id):
    """Get user subscription"""
    with get_db_cursor(commit=False) as cur:
        cur.execute(
            "SELECT * FROM subscriptions WHERE user_id = %s",
            (user_id,)
        )
        return cur.fetchone()


def create_subscription(user_id, plan_type='free', basic_reports_remaining=2, ai_credits_remaining=0):
    """Create a new subscription"""
    with get_db_cursor() as cur:
        cur.execute(
            """INSERT INTO subscriptions (user_id, plan_type, basic_reports_remaining, ai_credits_remaining)
               VALUES (%s, %s, %s, %s)
               RETURNING *""",
            (user_id, plan_type, basic_reports_remaining, ai_credits_remaining)
        )
        return cur.fetchone()


def update_subscription(user_id, **kwargs):
    """Update subscription fields"""
    if not kwargs:
        return None

    allowed_fields = ['plan_type', 'status', 'basic_reports_remaining', 'ai_credits_remaining',
                      'stripe_customer_id', 'stripe_subscription_id']

    set_clauses = []
    values = []
    for key, value in kwargs.items():
        if key in allowed_fields:
            set_clauses.append(f"{key} = %s")
            values.append(value)

    if not set_clauses:
        return None

    values.append(user_id)

    with get_db_cursor() as cur:
        cur.execute(
            f"UPDATE subscriptions SET {', '.join(set_clauses)} WHERE user_id = %s RETURNING *",
            tuple(values)
        )
        return cur.fetchone()


def decrement_basic_reports(user_id):
    """Decrement basic reports remaining"""
    with get_db_cursor() as cur:
        cur.execute(
            """UPDATE subscriptions
               SET basic_reports_remaining = basic_reports_remaining - 1
               WHERE user_id = %s AND basic_reports_remaining > 0
               RETURNING basic_reports_remaining""",
            (user_id,)
        )
        return cur.fetchone()


def decrement_ai_credits(user_id):
    """Decrement AI credits remaining"""
    with get_db_cursor() as cur:
        cur.execute(
            """UPDATE subscriptions
               SET ai_credits_remaining = ai_credits_remaining - 1
               WHERE user_id = %s AND ai_credits_remaining > 0
               RETURNING ai_credits_remaining""",
            (user_id,)
        )
        return cur.fetchone()


# ============================================
# Metabolic Test Operations
# ============================================

def create_metabolic_test(user_id, filename, test_data):
    """Create a new metabolic test record"""
    with get_db_cursor() as cur:
        cur.execute(
            """INSERT INTO metabolic_tests
               (user_id, filename, vo2_max, rmr, max_hr, resting_hr, fat_oxidation,
                carb_oxidation, rer, age, gender, weight, height, biological_age,
                metabolic_score, raw_data)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (user_id, filename,
             test_data.get('vo2_max'), test_data.get('rmr'),
             test_data.get('max_hr'), test_data.get('resting_hr'),
             test_data.get('fat_oxidation'), test_data.get('carb_oxidation'),
             test_data.get('rer'), test_data.get('age'),
             test_data.get('gender'), test_data.get('weight'),
             test_data.get('height'), test_data.get('biological_age'),
             test_data.get('metabolic_score'),
             psycopg2.extras.Json(test_data) if test_data else None)
        )
        return cur.fetchone()


def get_metabolic_tests(user_id, limit=50):
    """Get user's metabolic tests"""
    with get_db_cursor(commit=False) as cur:
        cur.execute(
            "SELECT * FROM metabolic_tests WHERE user_id = %s ORDER BY created_at DESC LIMIT %s",
            (user_id, limit)
        )
        return cur.fetchall()


def get_metabolic_test(test_id):
    """Get a specific metabolic test"""
    with get_db_cursor(commit=False) as cur:
        cur.execute("SELECT * FROM metabolic_tests WHERE id = %s", (test_id,))
        return cur.fetchone()


# ============================================
# Report Operations
# ============================================

def create_report(user_id, test_id, report_type, patient_name, report_html,
                  ai_recommendations=None, focus_areas=None):
    """Create a new report"""
    with get_db_cursor() as cur:
        cur.execute(
            """INSERT INTO reports
               (user_id, test_id, report_type, patient_name, report_html,
                ai_recommendations, focus_areas)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (user_id, test_id, report_type, patient_name, report_html,
             psycopg2.extras.Json(ai_recommendations) if ai_recommendations else None,
             psycopg2.extras.Json(focus_areas) if focus_areas else None)
        )
        return cur.fetchone()


def get_reports(user_id, limit=50):
    """Get user's reports"""
    with get_db_cursor(commit=False) as cur:
        cur.execute(
            "SELECT * FROM reports WHERE user_id = %s ORDER BY created_at DESC LIMIT %s",
            (user_id, limit)
        )
        return cur.fetchall()


def get_report(report_id):
    """Get a specific report"""
    with get_db_cursor(commit=False) as cur:
        cur.execute("SELECT * FROM reports WHERE id = %s", (report_id,))
        return cur.fetchone()


def update_report(report_id, **kwargs):
    """Update report fields"""
    allowed_fields = ['report_html', 'report_pdf_url', 'ai_recommendations', 'focus_areas']

    set_clauses = []
    values = []
    for key, value in kwargs.items():
        if key in allowed_fields:
            set_clauses.append(f"{key} = %s")
            if key in ['ai_recommendations', 'focus_areas'] and value:
                values.append(psycopg2.extras.Json(value))
            else:
                values.append(value)

    if not set_clauses:
        return None

    values.append(report_id)

    with get_db_cursor() as cur:
        cur.execute(
            f"UPDATE reports SET {', '.join(set_clauses)} WHERE id = %s RETURNING *",
            tuple(values)
        )
        return cur.fetchone()


def delete_report(report_id):
    """Delete a report"""
    with get_db_cursor() as cur:
        cur.execute("DELETE FROM reports WHERE id = %s RETURNING id", (report_id,))
        return cur.fetchone()


# ============================================
# Audit Log Operations (HIPAA Compliance)
# ============================================

def log_audit(user_id, action, resource_type, resource_id=None, ip_address=None,
              user_agent=None, details=None):
    """Log an audit event for HIPAA compliance"""
    try:
        with get_db_cursor() as cur:
            cur.execute(
                """INSERT INTO audit_logs
                   (user_id, action, resource_type, resource_id, ip_address, user_agent, details)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (str(user_id) if user_id else None, action, resource_type, resource_id,
                 ip_address, user_agent,
                 psycopg2.extras.Json(details) if details else None)
            )
    except Exception as e:
        # Don't let audit logging failures break the app
        print(f"[AUDIT] Failed to log: {e}")


def get_audit_logs(user_id=None, limit=100):
    """Get audit logs, optionally filtered by user"""
    with get_db_cursor(commit=False) as cur:
        if user_id:
            cur.execute(
                "SELECT * FROM audit_logs WHERE user_id = %s ORDER BY timestamp DESC LIMIT %s",
                (str(user_id), limit)
            )
        else:
            cur.execute(
                "SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT %s",
                (limit,)
            )
        return cur.fetchall()


# ============================================
# Utility Functions
# ============================================

def test_connection():
    """Test database connection"""
    try:
        with get_db_cursor(commit=False) as cur:
            cur.execute("SELECT 1")
            return True
    except Exception as e:
        print(f"[DB] Connection test failed: {e}")
        return False
