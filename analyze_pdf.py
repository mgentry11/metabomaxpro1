import pdfplumber
import json
import re

pdf_path = "/Users/markgentry/Downloads/Genspark - Metabolic Performance Blueprint for Bradley Littlefield.pdf"

def extract_sections(text):
    """Extract sections based on common headers and patterns"""
    sections = []
    lines = text.split('\n')
    current_section = None

    for line in lines:
        # Look for section headers (usually all caps or with specific formatting)
        if line.strip() and (line.isupper() or any(keyword in line.lower() for keyword in ['section', 'chapter', 'part', 'overview', 'summary', 'analysis', 'recommendations', 'metrics', 'zones', 'training', 'performance', 'metabolic'])):
            if current_section:
                sections.append(current_section)
            current_section = {'header': line.strip(), 'content': []}
        elif current_section is not None:
            current_section['content'].append(line)

    if current_section:
        sections.append(current_section)

    return sections

# Extract comprehensive analysis
with pdfplumber.open(pdf_path) as pdf:
    print("=" * 80)
    print("PDF STRUCTURE ANALYSIS")
    print("=" * 80)
    print(f"\nTotal Pages: {len(pdf.pages)}")

    # Extract all text
    all_text = ""
    page_summaries = []

    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            all_text += text + "\n\n"
            # Get first 200 chars as summary
            summary = text[:200].replace('\n', ' ')
            page_summaries.append({
                'page': i+1,
                'preview': summary
            })

    # Print page summaries
    print("\n" + "=" * 80)
    print("PAGE SUMMARIES (First 200 characters per page)")
    print("=" * 80)
    for summary in page_summaries[:20]:  # First 20 pages
        print(f"\nPage {summary['page']}:")
        print(f"  {summary['preview']}...")

    if len(page_summaries) > 20:
        print(f"\n... and {len(page_summaries) - 20} more pages")

    # Look for key sections and data
    print("\n" + "=" * 80)
    print("KEY CONTENT ANALYSIS")
    print("=" * 80)

    # Search for specific keywords
    keywords = {
        'Metabolic': all_text.lower().count('metabolic'),
        'Performance': all_text.lower().count('performance'),
        'Zone': all_text.lower().count('zone'),
        'Training': all_text.lower().count('training'),
        'Heart Rate': all_text.lower().count('heart rate'),
        'Calorie': all_text.lower().count('calorie') + all_text.lower().count('caloric'),
        'Fat': all_text.lower().count('fat'),
        'Carb': all_text.lower().count('carb'),
        'VO2': all_text.lower().count('vo2'),
        'Oxygen': all_text.lower().count('oxygen'),
        'Biological Age': all_text.lower().count('biological age'),
        'Recommendation': all_text.lower().count('recommendation'),
        'Intervention': all_text.lower().count('intervention'),
    }

    print("\nKeyword Frequency Analysis:")
    for keyword, count in sorted(keywords.items(), key=lambda x: x[1], reverse=True):
        print(f"  {keyword:20s}: {count:3d} occurrences")

    # Extract numbers and metrics
    print("\n" + "=" * 80)
    print("NUMERIC DATA PATTERNS")
    print("=" * 80)

    # Find heart rate mentions
    hr_pattern = re.findall(r'(\d+)\s*bpm', all_text.lower())
    if hr_pattern:
        print(f"\nHeart Rate values found: {len(hr_pattern)} occurrences")
        print(f"  Range: {min(map(int, hr_pattern))} - {max(map(int, hr_pattern))} bpm")

    # Find calorie mentions
    cal_pattern = re.findall(r'(\d+)\s*cal', all_text.lower())
    if cal_pattern:
        print(f"\nCalorie values found: {len(cal_pattern)} occurrences")

    # Find percentage mentions
    pct_pattern = re.findall(r'(\d+)%', all_text)
    if pct_pattern:
        print(f"\nPercentage values found: {len(pct_pattern)} occurrences")
        print(f"  Sample: {', '.join(pct_pattern[:10])}%...")

    # Look for zone information
    print("\n" + "=" * 80)
    print("TRAINING ZONES DETECTION")
    print("=" * 80)

    zone_matches = re.findall(r'zone\s+(\d+)', all_text.lower())
    if zone_matches:
        unique_zones = set(zone_matches)
        print(f"\nZones mentioned: {', '.join(sorted(unique_zones))}")
        print(f"Total zone references: {len(zone_matches)}")

    # Extract table information
    print("\n" + "=" * 80)
    print("TABLE STRUCTURE ANALYSIS")
    print("=" * 80)

    total_tables = 0
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        if tables:
            total_tables += len(tables)
            print(f"\nPage {i+1}: {len(tables)} table(s)")
            for j, table in enumerate(tables[:2]):  # Show first 2 tables per page
                if table and len(table) > 0:
                    print(f"  Table {j+1}: {len(table)} rows x {len(table[0]) if table[0] else 0} columns")

    print(f"\nTotal tables found: {total_tables}")

    # Look for structured sections
    print("\n" + "=" * 80)
    print("DOCUMENT STRUCTURE INSIGHTS")
    print("=" * 80)

    # Common section headers in metabolic reports
    section_keywords = [
        'executive summary',
        'overview',
        'patient information',
        'test results',
        'metabolic rate',
        'performance metrics',
        'training zones',
        'heart rate zones',
        'fuel utilization',
        'fat burning',
        'carbohydrate',
        'biological age',
        'recommendations',
        'interventions',
        'protocol',
        'weekly plan',
        'nutrition',
        'supplement',
        'assessment',
        'baseline',
        'goals',
    ]

    print("\nSection Detection:")
    found_sections = []
    for keyword in section_keywords:
        if keyword in all_text.lower():
            # Find context around the keyword
            idx = all_text.lower().find(keyword)
            context = all_text[max(0, idx-50):min(len(all_text), idx+len(keyword)+50)]
            context = context.replace('\n', ' ').strip()
            found_sections.append((keyword, context))

    for keyword, context in found_sections[:15]:  # Show first 15
        print(f"\n  '{keyword.upper()}':")
        print(f"    Context: ...{context}...")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
