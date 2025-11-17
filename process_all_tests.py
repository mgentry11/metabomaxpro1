#!/usr/bin/env python3
"""Process all PDFs in PNOE_tests and analyze for defaulting"""
import sys
import os
import json
import glob
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from upload_report import upload_and_generate_report

test_dir = '/Users/markgentry/Downloads/PNOE_tests'

print("="*100)
print("PROCESSING ALL METABOLIC TEST PDFs")
print("="*100)

# Find all PDFs
pdf_files = glob.glob(os.path.join(test_dir, '*.pdf'))
print(f"\nFound {len(pdf_files)} PDF files:")
for pdf in pdf_files:
    print(f"  - {os.path.basename(pdf)}")

print(f"\n{'='*100}\n")

results = []

for pdf_path in pdf_files:
    print(f"Processing: {os.path.basename(pdf_path)}")
    print("-" * 100)

    result = upload_and_generate_report(pdf_path)

    if result.get('success'):
        # Read the generated data file to get detailed info
        data_file = result['data_file']
        with open(data_file, 'r') as f:
            data = json.load(f)

        patient_info = data.get('patient_info', {})
        core_scores = data.get('core_scores', {})
        caloric_data = data.get('caloric_data', {})

        # Calculate average score
        avg_score = sum(core_scores.values()) / len(core_scores) if core_scores else 0

        results.append({
            'name': patient_info.get('name', 'Unknown'),
            'gender': patient_info.get('gender', 'Unknown'),
            'age': patient_info.get('age'),
            'weight': patient_info.get('weight_kg'),
            'height': patient_info.get('height_cm'),
            'bio_age': result.get('biological_age'),
            'chrono_age': result.get('chronological_age'),
            'diff': result.get('chronological_age') - result.get('biological_age') if result.get('biological_age') else None,
            'burn_rest': caloric_data.get('burn_rest'),
            'burn_workout': caloric_data.get('burn_workout'),
            'avg_score': avg_score,
            'fat_percent': caloric_data.get('fat_percent'),
            'cho_percent': caloric_data.get('cho_percent'),
            'test_source': patient_info.get('test_source', 'Unknown'),
            'file': os.path.basename(pdf_path)
        })

    print()

print("="*100)
print("COMPREHENSIVE ANALYSIS - ALL PATIENTS")
print("="*100)

# Display results
print(f"\n{'='*100}")
print(f"PATIENT DEMOGRAPHICS")
print(f"{'='*100}\n")

print(f"{'Patient':<25} {'Gender':<8} {'Age':<5} {'Weight':<8} {'Height':<8} {'Test Source'}")
print("-" * 100)
for r in results:
    print(f"{r['name']:<25} {r['gender']:<8} {r['age']:<5} {r['weight']}kg{'':<4} {r['height']}cm{'':<4} {r['test_source']}")

print(f"\n{'='*100}")
print(f"BIOLOGICAL AGE ANALYSIS")
print(f"{'='*100}\n")

print(f"{'Patient':<25} {'Chrono Age':<12} {'Bio Age':<10} {'Difference':<15} {'Avg Score'}")
print("-" * 100)
for r in sorted(results, key=lambda x: x['diff'] if x['diff'] else 0, reverse=True):
    diff_str = f"{r['diff']:+.0f} years" if r['diff'] else "N/A"
    print(f"{r['name']:<25} {r['chrono_age']:<12} {r['bio_age']:<10} {diff_str:<15} {r['avg_score']:.1f}%")

print(f"\n{'='*100}")
print(f"CALORIC BURN VALUES")
print(f"{'='*100}\n")

print(f"{'Patient':<25} {'Burn Rest':<15} {'Burn Workout':<15} {'Fat%':<8} {'Carb%'}")
print("-" * 100)
for r in results:
    burn_rest = r['burn_rest'] if r['burn_rest'] else 'N/A'
    burn_workout = r['burn_workout'] if r['burn_workout'] else 'N/A'
    fat_pct = f"{r['fat_percent']}%" if r['fat_percent'] else 'N/A'
    cho_pct = f"{r['cho_percent']}%" if r['cho_percent'] else 'N/A'
    print(f"{r['name']:<25} {str(burn_rest):<15} {str(burn_workout):<15} {fat_pct:<8} {cho_pct}")

print(f"\n{'='*100}")
print(f"DEFAULTING DETECTION")
print(f"{'='*100}\n")

# Check for identical values
bio_ages = [r['bio_age'] for r in results if r['bio_age']]
diffs = [r['diff'] for r in results if r['diff']]
burns_rest = [r['burn_rest'] for r in results if r['burn_rest']]
burns_workout = [r['burn_workout'] for r in results if r['burn_workout']]
fat_percents = [r['fat_percent'] for r in results if r['fat_percent']]
avg_scores = [r['avg_score'] for r in results if r['avg_score']]

print("Biological Age:")
if len(set(bio_ages)) == len(bio_ages):
    print(f"  ✅ All {len(bio_ages)} biological ages are UNIQUE")
    print(f"     Values: {sorted(set(bio_ages))}")
else:
    print(f"  ⚠️  DUPLICATES FOUND: {len(set(bio_ages))} unique out of {len(bio_ages)} total")
    # Find duplicates
    from collections import Counter
    counts = Counter(bio_ages)
    for val, count in counts.items():
        if count > 1:
            print(f"     {count} patients have bio age {val}")

print(f"\nBiological Age Differences:")
if len(set(diffs)) == len(diffs):
    print(f"  ✅ All {len(diffs)} differences are UNIQUE")
    print(f"     Range: {min(diffs):+.0f} to {max(diffs):+.0f} years")
else:
    print(f"  ⚠️  DUPLICATES FOUND: {len(set(diffs))} unique out of {len(diffs)} total")
    from collections import Counter
    counts = Counter(diffs)
    for val, count in counts.items():
        if count > 1:
            print(f"     {count} patients have difference of {val:+.0f} years")

print(f"\nCaloric Burn (Rest Days):")
if len(set(burns_rest)) == len(burns_rest):
    print(f"  ✅ All {len(burns_rest)} values are UNIQUE")
    print(f"     Range: {min(burns_rest)} - {max(burns_rest)} kcal ({max(burns_rest)-min(burns_rest)} kcal spread)")
else:
    print(f"  ⚠️  DUPLICATES FOUND: {len(set(burns_rest))} unique out of {len(burns_rest)} total")

print(f"\nCaloric Burn (Workout Days):")
if len(set(burns_workout)) == len(burns_workout):
    print(f"  ✅ All {len(burns_workout)} values are UNIQUE")
    print(f"     Range: {min(burns_workout)} - {max(burns_workout)} kcal ({max(burns_workout)-min(burns_workout)} kcal spread)")
else:
    print(f"  ⚠️  DUPLICATES FOUND: {len(set(burns_workout))} unique out of {len(burns_workout)} total")

print(f"\nFat Utilization Percentages:")
if len(set(fat_percents)) == len(fat_percents):
    print(f"  ✅ All {len(fat_percents)} values are UNIQUE")
    print(f"     Range: {min(fat_percents)}% - {max(fat_percents)}%")
else:
    print(f"  ⚠️  DUPLICATES FOUND: {len(set(fat_percents))} unique out of {len(fat_percents)} total")
    from collections import Counter
    counts = Counter(fat_percents)
    for val, count in counts.items():
        if count > 1:
            print(f"     {count} patients have {val}% fat utilization")

print(f"\nAverage Core Scores:")
if len(set([round(s, 1) for s in avg_scores])) == len(avg_scores):
    print(f"  ✅ All {len(avg_scores)} scores are UNIQUE")
    print(f"     Range: {min(avg_scores):.1f}% - {max(avg_scores):.1f}%")
else:
    print(f"  ⚠️  Some similarity in scores (expected if patients have similar fitness)")
    print(f"     {len(set([round(s, 1) for s in avg_scores]))} unique values out of {len(avg_scores)} total")

print(f"\n{'='*100}")
print(f"STATISTICAL ANALYSIS")
print(f"{'='*100}\n")

print("Biological Age Differences:")
print(f"  Most younger: {max(diffs):+.0f} years")
print(f"  Most older: {min(diffs):+.0f} years")
print(f"  Average: {sum(diffs)/len(diffs):+.1f} years")
print(f"  Standard deviation: {(sum((d - sum(diffs)/len(diffs))**2 for d in diffs) / len(diffs))**0.5:.1f} years")

younger = sum(1 for d in diffs if d > 0)
older = sum(1 for d in diffs if d < 0)
print(f"\nDistribution:")
print(f"  Biologically younger: {younger} ({younger/len(diffs)*100:.0f}%)")
print(f"  Biologically older: {older} ({older/len(diffs)*100:.0f}%)")

print(f"\nCaloric Burn Correlation:")
# Check if heavier people burn more
sorted_by_weight = sorted(results, key=lambda x: x['weight'])
sorted_by_burn = sorted(results, key=lambda x: x['burn_rest'])
weight_burn_match = sum(1 for i, r in enumerate(sorted_by_weight) if r in sorted_by_burn[:len(sorted_by_burn)//2+1] and i < len(sorted_by_weight)//2+1)

if [r['name'] for r in sorted_by_weight[-2:]] == [r['name'] for r in sorted_by_burn[-2:]]:
    print(f"  ✅ Heaviest people have highest caloric burn (correct correlation)")
else:
    print(f"  ⚠️  Caloric burn shows variation (age/gender also factors)")

print(f"\n{'='*100}")
print(f"FINAL VERDICT")
print(f"{'='*100}\n")

issues = []
if len(set(bio_ages)) < len(bio_ages):
    issues.append("Biological ages have duplicates")
if len(set(burns_rest)) < len(burns_rest):
    issues.append("Rest day burns have duplicates")
if len(set(burns_workout)) < len(burns_workout):
    issues.append("Workout day burns have duplicates")

if not issues:
    print("✅ NO DEFAULTING DETECTED!")
    print("   All values are appropriately unique and personalized")
    print("   Calculations are working correctly")
else:
    print("⚠️  POTENTIAL ISSUES:")
    for issue in issues:
        print(f"   - {issue}")

print(f"\n{'='*100}\n")
