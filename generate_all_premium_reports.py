#!/usr/bin/env python3
"""
Generate PREMIUM reports for all patients
"""
import sys
import os
import glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from upload_report import upload_and_generate_report

test_dir = '/Users/markgentry/Downloads/PNOE_tests'

print("="*100)
print("GENERATING PREMIUM REPORTS FOR ALL PATIENTS")
print("="*100)

# Find all PDFs
pdf_files = glob.glob(os.path.join(test_dir, '*.pdf'))
print(f"\nFound {len(pdf_files)} PDF files\n")

for pdf_path in pdf_files:
    print(f"\n{'='*100}")
    print(f"Processing: {os.path.basename(pdf_path)}")
    print(f"{'='*100}\n")

    # Generate PREMIUM report
    result = upload_and_generate_report(pdf_path, report_type='Longevity', premium=True)

    if result.get('error'):
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Premium report generated successfully")

    print()

print("="*100)
print("✅ ALL PREMIUM REPORTS GENERATED")
print("="*100)
print(f"\nReports saved to: uploads/")
print(f"\nTo view all reports:")
print(f"  ls -lh uploads/*_20251117.html")
print()
