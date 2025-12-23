#!/usr/bin/env python3
"""
Batch Regenerate HTML Reports

Regenerates all HTML reports from updated JSON data files using the
ai_basic_report generator.
"""

import os
import sys
import json
import glob

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.ai_basic_report import generate_beautiful_report

UPLOADS_DIR = "/Users/markgentry/metabomaxpro1/uploads"


def regenerate_all_reports():
    """Regenerate all HTML reports from JSON data files."""
    print("=" * 60)
    print("BATCH HTML REPORT REGENERATION")
    print("=" * 60)

    # Find all JSON data files
    json_files = glob.glob(os.path.join(UPLOADS_DIR, "*_data.json"))
    print(f"\nFound {len(json_files)} data files to process\n")

    results = {
        'regenerated': [],
        'skipped': [],
        'errors': []
    }

    for json_path in json_files:
        filename = os.path.basename(json_path)
        file_id = filename.replace('_data.json', '')
        html_path = os.path.join(UPLOADS_DIR, f"{file_id}_report.html")

        print(f"\nProcessing: {filename}")

        try:
            # Load JSON data
            with open(json_path, 'r') as f:
                extracted_data = json.load(f)

            patient_name = extracted_data.get('patient_info', {}).get('name', 'Unknown')
            print(f"  Patient: {patient_name}")

            # Print current scores
            scores = extracted_data.get('core_scores', {})
            print(f"  Scores: metabolic_rate={scores.get('metabolic_rate')}%, "
                  f"hrv={scores.get('hrv')}%, symp_parasym={scores.get('symp_parasym')}%")

            # Custom data for report generation
            custom_data = {
                'report_type': 'performance',
                'focus_areas': ['Peptides'],
                'chronological_age': extracted_data.get('patient_info', {}).get('age', 50)
            }

            # Generate the HTML report
            html_content = generate_beautiful_report(extracted_data, custom_data)

            # Write the HTML file
            with open(html_path, 'w') as f:
                f.write(html_content)

            print(f"  Saved: {html_path}")
            results['regenerated'].append({
                'json': filename,
                'html': f"{file_id}_report.html",
                'patient': patient_name
            })

        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            results['errors'].append({
                'json': filename,
                'error': str(e)
            })

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Regenerated: {len(results['regenerated'])}")
    print(f"Errors: {len(results['errors'])}")

    if results['errors']:
        print("\nErrors:")
        for err in results['errors']:
            print(f"  - {err['json']}: {err['error']}")

    return results


if __name__ == "__main__":
    regenerate_all_reports()
