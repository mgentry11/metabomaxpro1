#!/usr/bin/env python3
"""
Batch Reprocess Reports

Reprocesses all PNOE test PDFs using the updated ergometry calculation engine
and regenerates the HTML reports.
"""

import os
import sys
import json
import re
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.ergometry_calculator import (
    detect_pdf_type,
    process_pnoe_pdf,
    calculate_all_scores,
    extract_scores_from_performance_report
)

# Configuration
TEST_PDF_DIR = "/Users/markgentry/temp_pnoe_tests"
UPLOADS_DIR = "/Users/markgentry/metabomaxpro1/uploads"

# Mapping of patient names to JSON file IDs (based on current data)
# This maps patient names (lowercase) to their existing data file IDs
KNOWN_MAPPINGS = {
    "gentry mark": "08e2dca0470c86b9",
    "kurtzer john": "27fb28f5b1063aa7",
    "littlefield bradlely": "30613bcfda61f388",
    "franco jessica": "42a0b062ee57676d",
    "alexander eric": "97035e366eb67d7c",
    "alexander denelle": "98eaff0843aacd7c",
    "robison debra": "a1ab331e4cf69470",
    "dee jay": "f06d8887e0409458",
}


def find_pdf_files(directory):
    """Find all PDF files in directory."""
    pdfs = []
    for f in os.listdir(directory):
        if f.endswith('.pdf') and not f.startswith('._'):
            pdfs.append(os.path.join(directory, f))

    # Also check subdirectories
    for subdir in os.listdir(directory):
        subpath = os.path.join(directory, subdir)
        if os.path.isdir(subpath) and not subdir.startswith('_'):
            for f in os.listdir(subpath):
                if f.endswith('.pdf') and not f.startswith('._'):
                    pdfs.append(os.path.join(subpath, f))

    return pdfs


def extract_patient_name(pdf_path):
    """Extract patient name from PDF."""
    import pdfplumber
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = pdf.pages[0].extract_text() or ""
            # Try different name patterns
            name_match = re.search(r'Name\s+([^\n]+?)(?:\s+Status|\s+Date|$)', text)
            if name_match:
                name = name_match.group(1).strip()
                # Clean up name (remove "Test" suffix sometimes added)
                name = re.sub(r'\s+Test$', '', name)
                return name.lower()
    except Exception:
        pass
    return None


def load_existing_data(json_path):
    """Load existing JSON data file."""
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except Exception:
        return None


def save_data(json_path, data):
    """Save data to JSON file."""
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)


def process_pdf(pdf_path, existing_data=None):
    """Process a PDF and return updated data structure."""
    pdf_type = detect_pdf_type(pdf_path)
    print(f"  PDF Type: {pdf_type}")

    # Process based on type
    if pdf_type == 'raw_ergometry':
        result = calculate_all_scores(pdf_path)
    elif pdf_type == 'performance_report':
        result = extract_scores_from_performance_report(pdf_path)
    else:
        result = process_pnoe_pdf(pdf_path)

    # Build updated data structure
    data = existing_data.copy() if existing_data else {}

    # Update patient info
    if 'patient_info' not in data:
        data['patient_info'] = {}

    data['patient_info'].update(result.get('patient_info', {}))
    data['patient_info']['test_source'] = 'PNOE'
    data['patient_info']['data_quality'] = result.get('data_quality', 'estimated')
    data['patient_info']['reprocessed_at'] = datetime.now().isoformat()

    # Update core scores with new calculated values
    data['core_scores'] = result.get('core_scores', {})

    # Update raw metrics
    raw_metrics = result.get('raw_metrics', {})

    if 'caloric_data' not in data:
        data['caloric_data'] = {}
    if 'metabolic_data' not in data:
        data['metabolic_data'] = {}
    if 'heart_rate_data' not in data:
        data['heart_rate_data'] = {}

    if 'measured_rmr_kcal' in raw_metrics:
        data['metabolic_data']['rmr'] = raw_metrics['measured_rmr_kcal']
    elif 'estimated_rmr_kcal' in raw_metrics:
        data['metabolic_data']['rmr'] = raw_metrics['estimated_rmr_kcal']

    if 'predicted_rmr_kcal' in raw_metrics:
        data['metabolic_data']['predicted_rmr'] = raw_metrics['predicted_rmr_kcal']

    if 'rer' in raw_metrics:
        data['metabolic_data']['rer'] = raw_metrics['rer']

    if 'mean_hr' in raw_metrics:
        data['heart_rate_data']['resting_hr'] = raw_metrics['mean_hr']

    if 'fat_oxidation_pct' in raw_metrics:
        data['caloric_data']['fat_percent'] = raw_metrics['fat_oxidation_pct']
        data['caloric_data']['cho_percent'] = raw_metrics['carb_oxidation_pct']

    # Store calculation details
    data['calculation_details'] = result.get('calculation_details', {})
    data['raw_metrics'] = raw_metrics

    return data


def reprocess_all():
    """Main function to reprocess all reports."""
    print("=" * 60)
    print("BATCH REPORT REPROCESSING")
    print("Using updated ergometry calculation engine")
    print("=" * 60)

    # Find all PDFs
    pdf_files = find_pdf_files(TEST_PDF_DIR)
    print(f"\nFound {len(pdf_files)} PDF files to process\n")

    results = {
        'processed': [],
        'skipped': [],
        'errors': []
    }

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        print(f"\nProcessing: {filename}")

        try:
            # Extract patient name
            patient_name = extract_patient_name(pdf_path)
            print(f"  Patient: {patient_name or 'Unknown'}")

            # Find existing data file
            json_id = None
            existing_data = None

            if patient_name and patient_name in KNOWN_MAPPINGS:
                json_id = KNOWN_MAPPINGS[patient_name]
                json_path = os.path.join(UPLOADS_DIR, f"{json_id}_data.json")
                if os.path.exists(json_path):
                    existing_data = load_existing_data(json_path)
                    print(f"  Found existing data: {json_id}")

            # Process the PDF
            updated_data = process_pdf(pdf_path, existing_data)

            # Print new scores
            scores = updated_data.get('core_scores', {})
            print(f"  New Scores:")
            for score_name, score_val in sorted(scores.items()):
                print(f"    {score_name}: {score_val}%")

            # Save updated data
            if json_id:
                json_path = os.path.join(UPLOADS_DIR, f"{json_id}_data.json")
                save_data(json_path, updated_data)
                print(f"  Saved: {json_path}")
                results['processed'].append({
                    'pdf': filename,
                    'patient': patient_name,
                    'json_id': json_id,
                    'scores': scores
                })
            else:
                # No existing file - create new one
                import hashlib
                new_id = hashlib.md5(filename.encode()).hexdigest()[:16]
                json_path = os.path.join(UPLOADS_DIR, f"{new_id}_data.json")
                save_data(json_path, updated_data)
                print(f"  Created new: {json_path}")
                results['processed'].append({
                    'pdf': filename,
                    'patient': patient_name,
                    'json_id': new_id,
                    'scores': scores,
                    'new': True
                })

        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            results['errors'].append({
                'pdf': filename,
                'error': str(e)
            })

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Processed: {len(results['processed'])}")
    print(f"Errors: {len(results['errors'])}")

    if results['errors']:
        print("\nErrors:")
        for err in results['errors']:
            print(f"  - {err['pdf']}: {err['error']}")

    return results


if __name__ == "__main__":
    reprocess_all()
