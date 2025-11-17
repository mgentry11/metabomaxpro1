#!/usr/bin/env python3
"""
CLI tool to upload metabolic test PDFs and generate reports
Usage: python3 upload_report.py /path/to/test.pdf
"""
import sys
import os
import json
import hashlib
from datetime import datetime

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

def upload_and_generate_report(pdf_path, user_id='admin', report_type='Performance', biological_age_override=None, premium=False):
    """
    Upload a PDF, extract data, generate report, and save to database

    Args:
        pdf_path: Path to PDF file
        user_id: User ID (default: 'admin')
        report_type: Report type (default: 'Performance')
        biological_age_override: Optional manual biological age
        premium: Generate premium report (default: False = basic report)

    Returns:
        dict with report_id, file_id, and download info
    """

    # Check if file exists
    if not os.path.exists(pdf_path):
        return {'error': f'File not found: {pdf_path}'}

    print(f"\n{'='*80}")
    print(f"PROCESSING METABOLIC TEST REPORT")
    print(f"{'='*80}\n")
    print(f"File: {pdf_path}")
    print(f"User: {user_id}")
    print(f"Report Type: {report_type}\n")

    # Import app functions
    from app import extract_pnoe_data
    from ai_basic_report import generate_beautiful_report as generate_basic_report
    from ai_premium_report import generate_premium_report
    from calculate_scores import calculate_biological_age

    # Select report generator
    generate_report = generate_premium_report if premium else generate_basic_report
    report_label = "PREMIUM" if premium else "BASIC"

    # Read PDF file
    with open(pdf_path, 'rb') as f:
        pdf_content = f.read()

    # Generate file ID
    file_id = hashlib.md5(pdf_content).hexdigest()[:16]

    print(f"File ID: {file_id}")
    print(f"\nExtracting patient data from PDF...")

    # Extract data from PDF
    extracted_data = extract_pnoe_data(pdf_path)

    if not extracted_data or not extracted_data.get('patient_info'):
        return {'error': 'Failed to extract patient data from PDF'}

    patient_info = extracted_data['patient_info']
    print(f"\n✅ Patient identified: {patient_info.get('name', 'Unknown')}")
    print(f"   Age: {patient_info.get('age', 'N/A')}, Gender: {patient_info.get('gender', 'N/A')}")
    print(f"   Weight: {patient_info.get('weight_kg', 'N/A')}kg, Height: {patient_info.get('height_cm', 'N/A')}cm")

    # Save initial extracted data
    uploads_dir = 'uploads'
    os.makedirs(uploads_dir, exist_ok=True)

    data_file = os.path.join(uploads_dir, f'{file_id}_data.json')
    # Note: Will update this file later with calculated data

    # Calculate biological age if not overridden
    chronological_age = patient_info.get('age')

    if biological_age_override:
        biological_age = biological_age_override
        print(f"\n📝 Using manual biological age override: {biological_age}")
    elif chronological_age:
        print(f"\n🧬 Calculating biological age...")
        biological_age = calculate_biological_age(
            patient_info,
            extracted_data.get('core_scores', {}),
            extracted_data.get('metabolic_data', {})
        )
        print(f"✅ Calculated biological age: {biological_age} (chronological: {chronological_age})")
    else:
        biological_age = None
        print(f"\n⚠️  Could not calculate biological age (missing chronological age)")

    # Generate HTML report (this also enhances extracted_data with calculations)
    print(f"\n📄 Generating {report_label} HTML report...")

    custom_data = {
        'chronological_age': chronological_age,
        'biological_age': biological_age,
        'report_type': report_type,
        'custom_notes': '',
        'goals': []
    }

    try:
        html_content = generate_report(extracted_data, custom_data)

        # Save HTML report
        html_file = os.path.join(uploads_dir, f'{file_id}_report.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ HTML report generated: {html_file}")

        # Now save the ENHANCED extracted_data (with calculated scores and caloric data)
        # The generate_beautiful_report function enhances the data in-place
        with open(data_file, 'w') as f:
            json.dump(extracted_data, f, indent=2)

        print(f"✅ Enhanced data saved to: {data_file}")

        # Also save a copy with patient name for easy access
        patient_name = patient_info.get('name', 'Unknown').replace(' ', '_').replace('/', '_')
        friendly_name = f"{patient_name}_{datetime.now().strftime('%Y%m%d')}.html"
        friendly_file = os.path.join(uploads_dir, friendly_name)

        with open(friendly_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Friendly copy saved: {friendly_file}")

    except Exception as e:
        print(f"❌ Error generating report: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'error': f'Report generation failed: {str(e)}'}

    # Prepare result
    result = {
        'success': True,
        'file_id': file_id,
        'patient_name': patient_info.get('name'),
        'chronological_age': chronological_age,
        'biological_age': biological_age,
        'html_file': html_file,
        'friendly_file': friendly_file,
        'data_file': data_file
    }

    print(f"\n{'='*80}")
    print(f"✅ SUCCESS - Report Generated")
    print(f"{'='*80}\n")
    print(f"Patient: {result['patient_name']}")
    print(f"Age: {result['chronological_age']} (Biological: {result['biological_age']})")
    print(f"\nReport files:")
    print(f"  📄 HTML Report: {result['friendly_file']}")
    print(f"  📄 Technical:   {result['html_file']}")
    print(f"  📊 Data:        {result['data_file']}")
    print(f"\nTo view the report:")
    print(f"  open {result['friendly_file']}")
    print(f"\n{'='*80}\n")

    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 upload_report.py /path/to/test.pdf [report_type] [biological_age] [--premium]")
        print("\nExamples:")
        print("  # Basic report")
        print("  python3 upload_report.py test.pdf")
        print("  python3 upload_report.py test.pdf Performance")
        print("  python3 upload_report.py test.pdf Longevity 45")
        print()
        print("  # Premium report (30+ pages)")
        print("  python3 upload_report.py test.pdf Performance --premium")
        print("  python3 upload_report.py test.pdf Longevity 45 --premium")
        sys.exit(1)

    pdf_path = sys.argv[1]
    report_type = 'Performance'
    bio_age = None
    premium = '--premium' in sys.argv

    # Parse arguments
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--premium':
            continue
        elif arg.isdigit():
            bio_age = int(arg)
        else:
            report_type = arg

    result = upload_and_generate_report(pdf_path, report_type=report_type, biological_age_override=bio_age, premium=premium)

    if result.get('error'):
        print(f"\n❌ ERROR: {result['error']}\n")
        sys.exit(1)
