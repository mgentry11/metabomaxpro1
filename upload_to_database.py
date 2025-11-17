#!/usr/bin/env python3
"""
CLI tool to upload locally generated reports to the website database
Usage: python3 upload_to_database.py <report_html_file> <user_email>
"""
import sys
import os
import json
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERROR: Missing Supabase credentials in .env file")
    print("   Need: SUPABASE_URL and SUPABASE_KEY")
    sys.exit(1)

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def find_user_by_email(email):
    """Find user ID by email"""
    try:
        # Query profiles table
        response = supabase.table('profiles').select('id').eq('email', email).execute()

        if response.data and len(response.data) > 0:
            return response.data[0]['id']
        else:
            print(f"❌ User not found: {email}")
            print("   Available users:")
            # List available users
            all_users = supabase.table('profiles').select('email').execute()
            for user in all_users.data:
                print(f"     - {user['email']}")
            return None
    except Exception as e:
        print(f"❌ Error finding user: {e}")
        return None

def upload_report_to_database(html_file, user_email, report_type='AI_basic_report'):
    """
    Upload a generated HTML report to the database

    Args:
        html_file: Path to HTML report file
        user_email: User's email address
        report_type: Type of report (AI_basic_report or AI_premium_report)

    Returns:
        Report ID if successful, None otherwise
    """

    # Check if file exists
    if not os.path.exists(html_file):
        print(f"❌ File not found: {html_file}")
        return None

    # Load corresponding data file
    data_file = html_file.replace('_report.html', '_data.json')
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        print(f"   Expected: {data_file}")
        return None

    print(f"\n{'='*80}")
    print(f"UPLOADING REPORT TO DATABASE")
    print(f"{'='*80}\n")
    print(f"Report: {os.path.basename(html_file)}")
    print(f"User: {user_email}")
    print(f"Type: {report_type}\n")

    # Find user ID
    user_id = find_user_by_email(user_email)
    if not user_id:
        return None

    print(f"✅ Found user ID: {user_id}\n")

    # Load data file
    with open(data_file, 'r') as f:
        extracted_data = json.load(f)

    patient_info = extracted_data.get('patient_info', {})

    print(f"Patient: {patient_info.get('name', 'Unknown')}")
    print(f"Age: {patient_info.get('age', 'N/A')}")
    print(f"Gender: {patient_info.get('gender', 'N/A')}\n")

    # Read HTML content
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Create metabolic test record
    print("📤 Creating metabolic test record...")
    test_data = {
        'user_id': user_id,
        'test_date': patient_info.get('test_date', datetime.now().strftime('%Y-%m-%d')),
        'pdf_filename': None,  # CLI generated, no PDF
        'pdf_storage_path': None,
        'extracted_data': extracted_data,
        'patient_name': patient_info.get('name'),
        'patient_age': patient_info.get('age'),
        'patient_gender': patient_info.get('gender'),
        'patient_weight_kg': patient_info.get('weight_kg')
    }

    try:
        test_response = supabase.table('metabolic_tests').insert(test_data).execute()
        test_id = test_response.data[0]['id']
        print(f"✅ Test record created: {test_id}")
    except Exception as e:
        print(f"❌ Error creating test record: {e}")
        return None

    # Create report record
    print("📤 Creating report record...")

    # Get biological age from data
    caloric_data = extracted_data.get('caloric_data', {})
    chronological_age = patient_info.get('age')
    biological_age = extracted_data.get('biological_age', chronological_age)

    report_data = {
        'user_id': user_id,
        'test_id': test_id,
        'report_type': report_type,
        'chronological_age': chronological_age,
        'biological_age': biological_age,
        'custom_notes': '',
        'goals': [],
        'additional_metrics': {
            'core_scores': extracted_data.get('core_scores', {}),
            'caloric_data': caloric_data,
            'metabolic_data': extracted_data.get('metabolic_data', {})
        },
        'html_content': html_content,
        'html_storage_path': os.path.basename(html_file)
    }

    try:
        report_response = supabase.table('reports').insert(report_data).execute()
        report_id = report_response.data[0]['id']
        print(f"✅ Report record created: {report_id}")
    except Exception as e:
        print(f"❌ Error creating report record: {e}")
        return None

    print(f"\n{'='*80}")
    print(f"✅ SUCCESS - Report Uploaded to Database")
    print(f"{'='*80}\n")
    print(f"Report ID: {report_id}")
    print(f"Test ID: {test_id}")
    print(f"User: {user_email}")
    print(f"\nView on website:")
    print(f"  https://metabomaxpro1.onrender.com/dashboard")
    print(f"\n{'='*80}\n")

    return report_id

def upload_all_reports(user_email, uploads_dir='uploads'):
    """Upload all reports in uploads directory to database"""

    print(f"\n{'='*80}")
    print(f"BATCH UPLOAD - ALL REPORTS")
    print(f"{'='*80}\n")

    # Find all report HTML files (excluding friendly named ones)
    import glob
    report_files = glob.glob(os.path.join(uploads_dir, '*_report.html'))

    print(f"Found {len(report_files)} reports to upload\n")

    uploaded = []
    failed = []

    for report_file in report_files:
        try:
            report_id = upload_report_to_database(report_file, user_email)
            if report_id:
                uploaded.append(report_file)
            else:
                failed.append(report_file)
        except Exception as e:
            print(f"❌ Error uploading {report_file}: {e}")
            failed.append(report_file)

    print(f"\n{'='*80}")
    print(f"BATCH UPLOAD SUMMARY")
    print(f"{'='*80}\n")
    print(f"✅ Uploaded: {len(uploaded)}")
    print(f"❌ Failed: {len(failed)}")

    if failed:
        print("\nFailed uploads:")
        for f in failed:
            print(f"  - {os.path.basename(f)}")

    print(f"\n{'='*80}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 upload_to_database.py <user_email> [report_file]")
        print("\nExamples:")
        print("  # Upload all reports in uploads/ directory")
        print("  python3 upload_to_database.py your@email.com")
        print()
        print("  # Upload specific report")
        print("  python3 upload_to_database.py your@email.com uploads/abc123_report.html")
        print()
        sys.exit(1)

    user_email = sys.argv[1]

    if len(sys.argv) >= 3:
        # Upload specific file
        report_file = sys.argv[2]
        upload_report_to_database(report_file, user_email)
    else:
        # Upload all reports
        upload_all_reports(user_email)
