import pdfplumber
import json

pdf_path = "/Users/markgentry/Downloads/Genspark - Metabolic Performance Blueprint for Bradley Littlefield.pdf"

# Extract text from PDF
with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}\n")
    print("="*80)

    all_text = []
    for i, page in enumerate(pdf.pages):
        print(f"\n{'='*80}")
        print(f"PAGE {i+1}")
        print(f"{'='*80}\n")

        text = page.extract_text()
        if text:
            print(text)
            all_text.append({
                'page': i+1,
                'text': text
            })

        # Also extract tables if present
        tables = page.extract_tables()
        if tables:
            print(f"\n[TABLES FOUND ON PAGE {i+1}]")
            for j, table in enumerate(tables):
                print(f"\nTable {j+1}:")
                for row in table:
                    print(row)

    print("\n" + "="*80)
    print("EXTRACTION COMPLETE")
    print("="*80)
