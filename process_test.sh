#!/bin/bash
# Simple wrapper to process metabolic test PDFs
# Usage: ./process_test.sh /path/to/test.pdf

if [ $# -eq 0 ]; then
    echo "Usage: ./process_test.sh /path/to/test.pdf [report_type] [biological_age]"
    echo ""
    echo "Examples:"
    echo "  ./process_test.sh test.pdf"
    echo "  ./process_test.sh test.pdf Performance"
    echo "  ./process_test.sh test.pdf Longevity 45"
    echo ""
    echo "Report types: Performance, Longevity, Health"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the upload script
python3 upload_report.py "$@"

# Open the report if successful
if [ $? -eq 0 ]; then
    # Find the most recent HTML file
    REPORT=$(ls -t uploads/*.html 2>/dev/null | head -1)
    if [ -n "$REPORT" ]; then
        echo "Opening report in browser..."
        open "$REPORT" 2>/dev/null || xdg-open "$REPORT" 2>/dev/null || echo "Please open: $REPORT"
    fi
fi
