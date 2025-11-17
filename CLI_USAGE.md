# CLI Tool - Quick PDF Processing

## Overview

Process metabolic test PDFs directly from the command line without using the web interface. The system automatically detects the test type (PNOE, CorSense, or generic) and brands the report accordingly.

## Quick Start

### Simple Usage (Recommended)

```bash
./process_test.sh /path/to/test.pdf
```

This will:
1. Extract patient data from the PDF
2. Calculate biological age automatically
3. Generate a professional HTML report
4. Save files to the `uploads/` directory
5. Open the report in your browser

### Examples

**Process a PNOE test:**
```bash
./process_test.sh ~/Downloads/patient_test.pdf
```

**Process with specific report type:**
```bash
./process_test.sh ~/Downloads/test.pdf Performance
```

**Override biological age manually:**
```bash
./process_test.sh ~/Downloads/test.pdf Longevity 45
```

## Report Types

- `Performance` - For athletes and performance optimization (default)
- `Longevity` - For health and longevity focus
- `Health` - For general health assessment

## Output Files

All files are saved to `uploads/`:

- **`PatientName_YYYYMMDD.html`** - Main report (easy to find)
- **`<file_id>_report.html`** - Technical reference
- **`<file_id>_data.json`** - Extracted data

## Advanced Usage

### Python Script Directly

```bash
python3 upload_report.py /path/to/test.pdf [report_type] [biological_age]
```

### Process Multiple Files

```bash
for file in ~/Downloads/PNOE_tests/*.pdf; do
    ./process_test.sh "$file"
done
```

### Custom Biological Age

If you want to manually set the biological age:
```bash
./process_test.sh patient.pdf Performance 38
```

## Automatic Test Detection

The system automatically detects the test source:

- **PNOE tests** → Shows "powered by PNOE technology"
- **CorSense tests** → Shows "powered by CorSense technology"
- **Other tests** → Generic branding (no vendor mention)

Detection is based on PDF content, so it works automatically!

## Troubleshooting

**"File not found" error:**
- Check the path to your PDF
- Use quotes around paths with spaces: `"~/My Files/test.pdf"`

**Report doesn't open automatically:**
- Open manually: `open uploads/PatientName_YYYYMMDD.html`
- Or find it in Finder: `uploads/` directory

**Missing biological age:**
- Add it manually as third argument
- Or edit the generated report data file

## Integration with Web Interface

These reports are compatible with the web interface:
1. Upload the generated HTML files through the dashboard
2. All data is preserved and can be downloaded
3. Reports are linked to your user account

## Files Reference

- `process_test.sh` - Simple bash wrapper (recommended)
- `upload_report.py` - Python processing script
- `uploads/` - Output directory for all generated files

## Tips

1. **Batch Processing**: Process multiple PDFs at once using a loop
2. **File Naming**: Reports use patient name + date for easy identification
3. **Backup Data**: Keep the `_data.json` files for future reference
4. **Custom Branding**: Edit `utils/pnoe_professional_template.py` to customize

---

**Questions or Issues?**
Check the main README.md or contact support.
