#!/usr/bin/env python3
"""
Script to redact PNOE branding from the sample PDF
"""
import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_redaction_overlay(text_positions):
    """Create a PDF overlay with white rectangles to cover text"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Draw white rectangles over PNOE text positions
    can.setFillColorRGB(1, 1, 1)  # White color

    for x, y, width, height in text_positions:
        can.rect(x, y, width, height, fill=1, stroke=0)

    can.save()
    packet.seek(0)
    return PdfReader(packet)

def redact_pdf(input_path, output_path):
    """Redact PNOE references from PDF"""
    # Read the original PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Positions where PNOE text appears (x, y, width, height)
    # These are approximate positions - may need adjustment
    redaction_positions_page1 = [
        # PNOE logo at top (approximate position)
        (40, 720, 100, 40),  # Top left logo area
        # Device name in test info section
        (150, 650, 200, 15),  # "PNOE 2516-338 / Ambient" in device field
    ]

    # Process each page
    for page_num, page in enumerate(reader.pages):
        if page_num == 0:  # First page typically has the branding
            # Create redaction overlay
            overlay_pdf = create_redaction_overlay(redaction_positions_page1)
            overlay_page = overlay_pdf.pages[0]

            # Merge overlay onto original page
            page.merge_page(overlay_page)

        writer.add_page(page)

    # Write the redacted PDF
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

    print(f"Redacted PDF saved to: {output_path}")

if __name__ == "__main__":
    input_pdf = "static/samples/Sample_Metabolic_Test_Data.pdf"
    output_pdf = "static/samples/Sample_Metabolic_Test_Data_redacted.pdf"

    redact_pdf(input_pdf, output_pdf)
