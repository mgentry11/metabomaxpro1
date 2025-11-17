import pdfplumber
import re

pdf_path = "/Users/markgentry/Downloads/Genspark - Metabolic Performance Blueprint for Bradley Littlefield.pdf"

# Let's look at specific pages to understand the actual content structure
# Skip the first few pages which appear to be metadata/navigation

with pdfplumber.open(pdf_path) as pdf:
    print("=" * 80)
    print("DETAILED CONTENT EXTRACTION")
    print("=" * 80)

    # Extract from middle pages to find actual report content
    target_pages = [20, 30, 40, 50, 60, 70, 80]

    for page_num in target_pages:
        if page_num < len(pdf.pages):
            print(f"\n{'=' * 80}")
            print(f"PAGE {page_num + 1} FULL CONTENT")
            print(f"{'=' * 80}\n")

            text = pdf.pages[page_num].extract_text()
            if text:
                # Clean up the text a bit
                lines = text.split('\n')
                # Skip header/footer with timestamps
                filtered_lines = [line for line in lines if not line.startswith('11/17/25')]
                cleaned_text = '\n'.join(filtered_lines)
                print(cleaned_text)

            # Also show tables
            tables = pdf.pages[page_num].extract_tables()
            if tables:
                print(f"\n--- TABLES ON THIS PAGE ---")
                for i, table in enumerate(tables):
                    print(f"\nTable {i+1}:")
                    for row in table:
                        if row and any(cell for cell in row if cell):
                            print(row)

    # Now let's search for pages with specific content markers
    print("\n\n" + "=" * 80)
    print("SEARCHING FOR KEY CONTENT SECTIONS")
    print("=" * 80)

    content_markers = {
        'Patient Info': ['bradley', 'littlefield', 'age:', 'weight:', 'height:'],
        'Metabolic Score': ['metabolic', 'score', '/100', 'percentile'],
        'Performance Metrics': ['vo2 max', 'resting metabolic', 'fat burning', 'aerobic'],
        'Training Zones': ['zone 1', 'zone 2', 'zone 3', 'bpm', 'heart rate'],
        'Recommendations': ['intervention', 'evidence-based', 'weekly plan'],
        'Biological Age': ['biological age', 'chronological', 'years younger'],
        'Caloric Info': ['calories', 'should eat', 'burn', 'kcal'],
    }

    for section_name, markers in content_markers.items():
        print(f"\n--- {section_name.upper()} ---")
        found_pages = []

        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                text_lower = text.lower()
                # Check if multiple markers are present
                matches = sum(1 for marker in markers if marker in text_lower)
                if matches >= 2:  # At least 2 markers
                    found_pages.append((i+1, matches))

        if found_pages:
            # Get the page with most matches
            best_page = max(found_pages, key=lambda x: x[1])
            print(f"Found on pages: {[p[0] for p in found_pages[:5]]}")
            print(f"Best match: Page {best_page[0]} ({best_page[1]} markers)")

            # Extract content from best page
            page_text = pdf.pages[best_page[0]-1].extract_text()
            # Get relevant excerpt (500 chars)
            for marker in markers:
                if marker in page_text.lower():
                    idx = page_text.lower().find(marker)
                    excerpt = page_text[max(0, idx-100):min(len(page_text), idx+400)]
                    print(f"\nExcerpt around '{marker}':")
                    print(excerpt.replace('\n', ' ')[:300] + "...")
                    break
        else:
            print("Not found with confidence")

    # Look for actual numeric data
    print("\n\n" + "=" * 80)
    print("EXTRACTING SPECIFIC METABOLIC DATA")
    print("=" * 80)

    all_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n"

    # Extract specific metrics with patterns
    patterns = {
        'Metabolic Score': r'(\d+)/100|score[:\s]+(\d+)',
        'Heart Rate Zones': r'zone\s+\d+[:\s]+(\d+)-(\d+)\s*bpm',
        'Biological Age': r'biological age[:\s]+(\d+)|(\d+)\s+years\s+(?:younger|older)',
        'Calories': r'(\d{3,4})\s*(?:calories|cal|kcal)',
        'Percentages': r'(\d+)%\s+(fat|carb|protein)',
        'VO2 Max': r'vo2\s*max[:\s]+(\d+\.?\d*)',
        'RMR': r'rmr[:\s]+(\d{3,4})|resting.*?(\d{3,4})',
    }

    for metric_name, pattern in patterns.items():
        matches = re.findall(pattern, all_text.lower())
        if matches:
            print(f"\n{metric_name}:")
            # Flatten tuples and remove empty strings
            flat_matches = []
            for match in matches[:10]:  # First 10
                if isinstance(match, tuple):
                    flat_matches.extend([m for m in match if m])
                else:
                    flat_matches.append(match)
            print(f"  Found: {flat_matches[:10]}")
