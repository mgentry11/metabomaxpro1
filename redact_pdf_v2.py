#!/usr/bin/env python3
"""
Script to redact PNOE branding from the sample PDF using PyMuPDF
"""
import fitz  # PyMuPDF

def redact_pdf(input_path, output_path):
    """Redact PNOE references from PDF"""
    # Open the PDF
    doc = fitz.open(input_path)

    # Terms to redact
    search_terms = ["PNOE", "2516-338", "pnoe"]

    print(f"Processing {len(doc)} pages...")

    # Process each page
    for page_num in range(len(doc)):
        page = doc[page_num]
        print(f"\nPage {page_num + 1}:")

        # Search for each term and add redaction annotations
        for term in search_terms:
            text_instances = page.search_for(term)

            if text_instances:
                print(f"  Found '{term}' {len(text_instances)} time(s)")

                for inst in text_instances:
                    # Add a redaction annotation (white rectangle)
                    # Expand the rectangle slightly to cover the text fully
                    rect = fitz.Rect(inst.x0 - 2, inst.y0 - 2, inst.x1 + 2, inst.y1 + 2)
                    annot = page.add_redact_annot(rect, fill=(1, 1, 1))  # White fill

        # Apply all redactions on this page
        page.apply_redactions()

    # Save the redacted PDF
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()

    print(f"\n✓ Redacted PDF saved to: {output_path}")

if __name__ == "__main__":
    input_pdf = "static/samples/Sample_Metabolic_Test_Data.pdf"

    # First backup the original
    import shutil
    backup_pdf = "static/samples/Sample_Metabolic_Test_Data_ORIGINAL.pdf"
    shutil.copy(input_pdf, backup_pdf)
    print(f"✓ Backup created: {backup_pdf}")

    # Redact and replace original
    output_pdf = "static/samples/Sample_Metabolic_Test_Data_temp.pdf"
    redact_pdf(input_pdf, output_pdf)

    # Replace original with redacted version
    shutil.move(output_pdf, input_pdf)
    print(f"\n✓ Original PDF has been replaced with redacted version")
    print(f"✓ Original backed up to: {backup_pdf}")
