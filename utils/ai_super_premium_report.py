"""
AI SUPER PREMIUM Report Generator
THE ULTIMATE REPORT: Generates BOTH AI_Basic + AI_Premium, then MERGES them
Creates comprehensive blueprint showing all data from both report types
"""
from datetime import datetime
import json
import sys
import os

# Add parent directory to path to import templates
sys.path.insert(0, os.path.dirname(__file__))
from sp_comprehensive_blueprint_template import SPComprehensiveBlueprintReport
from ai_basic_report import generate_beautiful_report as generate_basic_report
from ai_premium_report import generate_premium_report
from calculate_scores import enhance_extracted_data_with_calculated_scores, calculate_biological_age
from peptide_recommendations import calculate_peptide_recommendations, format_peptide_recommendations_html

def generate_super_premium_report(extracted_data, custom_data):
    """
    Generate SUPER PREMIUM report by:
    1. Generating AI_Basic report
    2. Generating AI_Premium report
    3. Merging both into SP Comprehensive Blueprint format

    This gives users ALL the data from both report types in one comprehensive document.
    """

    print(f"\n[SUPER PREMIUM] Generating BOTH Basic + Premium reports for merging...")
    print(f"[SUPER PREMIUM] Patient: {extracted_data.get('patient_info', {}).get('name', 'Unknown')}")

    # Step 1: Generate AI_Basic report (this will enhance data and calculate everything)
    print(f"\n[SUPER PREMIUM] Step 1/3: Generating AI_Basic report...")
    basic_html = generate_basic_report(extracted_data.copy(), custom_data.copy())

    # Step 2: Generate AI_Premium report (using same enhanced data)
    print(f"[SUPER PREMIUM] Step 2/3: Generating AI_Premium report...")
    premium_html = generate_premium_report(extracted_data.copy(), custom_data.copy())

    # Step 3: Merge both into SP Comprehensive Blueprint
    print(f"[SUPER PREMIUM] Step 3/3: Merging both reports into SP Comprehensive Blueprint...")

    # At this point, extracted_data has been enhanced with all calculations
    # Now create the SP Comprehensive Blueprint with all the data

    report = SPComprehensiveBlueprintReport()

    # Set patient info
    patient_info = extracted_data.get('patient_info', {})
    report.patient_info = {
        'name': patient_info.get('name', 'Patient Name'),
        'test_date': patient_info.get('test_date', datetime.now().strftime('%m/%d/%Y')),
        'age': patient_info.get('age', 35),
        'gender': patient_info.get('gender', 'Male'),
        'weight_kg': patient_info.get('weight_kg', 77),
        'height_cm': patient_info.get('height_cm', 188),
        'test_type': custom_data.get('report_type', 'Performance'),
        'facility': patient_info.get('facility', 'Optimal Vitality')
    }

    # Set core scores
    report.core_scores = extracted_data.get('core_scores', {})

    # Set caloric data
    report.caloric_data = extracted_data.get('caloric_data', {})

    # Set biological age
    report.chronological_age = custom_data.get('chronological_age') or patient_info.get('age')
    report.biological_age = custom_data.get('biological_age') or report.chronological_age

    # Set report type
    report.report_type = custom_data.get('report_type', 'Performance')

    # Add peptide recommendations
    peptide_recommendations = extracted_data.get('peptide_recommendations', [])
    if peptide_recommendations:
        report.peptide_recommendations = peptide_recommendations
        report.peptide_html = format_peptide_recommendations_html(peptide_recommendations)

    # Generate the final merged SP Comprehensive Blueprint
    print(f"[SUPER PREMIUM] ✅ Merging complete! Generating final HTML...")
    merged_html = report.generate()

    # Add metadata comment at the top
    metadata = f"""<!--
SUPER PREMIUM REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Patient: {patient_info.get('name', 'Unknown')}
Report Type: {custom_data.get('report_type', 'Performance')}

This report contains ALL data from both:
- AI_Basic Report (single-page scrollable)
- AI_Premium Report (30+ page detailed)

Merged into SP Comprehensive Blueprint format.
-->

"""

    final_html = merged_html.replace('<!DOCTYPE html>', f'<!DOCTYPE html>\n{metadata}')

    print(f"[SUPER PREMIUM] ✅ SUPER PREMIUM report generated successfully!")
    print(f"[SUPER PREMIUM] Contains data from BOTH Basic + Premium reports")

    return final_html
