# MetaboMax Pro - Report Types Guide

## Overview

You now have **TWO report types** available:

1. **AI_Basic_Report** - Original comprehensive report
2. **AI_Premium_Report** - 30+ page premium report (emulates Frank Shallenberger format)

Both reports use the same metabolic data and calculations, but differ in presentation and depth.

---

## Report Comparison

### AI_Basic_Report

**What it is:**
- Your original comprehensive metabolic report
- Single-page HTML with all metrics
- Interactive charts and visualizations
- AI peptide recommendations (optional)

**Page Count:** 1-2 pages (scrollable HTML)

**Best for:**
- Quick reference
- Digital viewing
- Email distribution
- Dashboard integration

**Generate with:**
```bash
python3 upload_report.py test.pdf
# OR
python3 upload_report.py test.pdf Performance
```

---

### AI_Premium_Report ⭐ NEW

**What it is:**
- 30+ page comprehensive report
- Each metric gets a full dedicated page
- Formatted like Frank Shallenberger's premium reports
- Professional print-ready PDF format

**Page Structure:**
1. **Cover Page** - Branded header with patient info
2. **Disclaimer** - Legal disclaimer page
3. **Pillars of Longevity** - 5 foundational health pillars
4. **Overview Dashboard** - Visual score summary (2-1-3-2-4-0 format)
5. **Core Metrics** (12-15 pages) - Each metric on full page:
   - Breathing Coordination
   - Sympathetic/Parasympathetic activation
   - Ventilation efficiency
   - Lung utilization
   - Heart Rate Variability (HRV)
   - Metabolic rate
   - Fat-burning Efficiency
   - M-Factor
   - C-factor
   - Lung Factor
   - Adrenal Factor
6. **Caloric Balance** - Personalized daily calories
7. **Macronutrient Balance** - Macro recommendations
8. **Testing Schedule** - Follow-up protocols
9. **Supplement Recommendations** - Personalized protocols

**Page Count:** 30-35 pages

**Best for:**
- Client presentations
- Printed reports
- High-value services
- Professional consulting

**Generate with:**
```bash
python3 upload_report.py test.pdf Longevity --premium
# OR
python3 upload_report.py test.pdf Performance --premium
```

---

## CLI Usage

### Basic Report
```bash
# Simple
python3 upload_report.py "/path/to/test.pdf"

# With report type
python3 upload_report.py "/path/to/test.pdf" Performance

# With custom biological age
python3 upload_report.py "/path/to/test.pdf" Longevity 45
```

### Premium Report
```bash
# Add --premium flag
python3 upload_report.py "/path/to/test.pdf" --premium

# With report type
python3 upload_report.py "/path/to/test.pdf" Longevity --premium

# With custom biological age
python3 upload_report.py "/path/to/test.pdf" Longevity 45 --premium
```

---

## Upload to Website Database

After generating reports, upload them to your website:

```bash
# Upload ALL reports in uploads/ directory
python3 upload_to_database.py your@email.com

# Upload specific report
python3 upload_to_database.py your@email.com uploads/abc123_report.html
```

**View on website:**
https://metabomaxpro1.onrender.com/dashboard

---

## Complete Workflow Example

### Process a batch of tests and upload to website:

```bash
# 1. Generate basic reports for all tests
python3 process_all_tests.py

# 2. Generate premium report for specific client
python3 upload_report.py "/Users/markgentry/Downloads/PNOE_tests/Brad_P N O E - View Ergometry.pdf" Longevity --premium

# 3. Upload all reports to website database
python3 upload_to_database.py drgarcia@vitalitymed.co

# 4. View on website
open https://metabomaxpro1.onrender.com/dashboard
```

---

## Pricing Suggestions

### AI_Basic_Report
**Suggested Retail:** $50-$150
- Quick turnaround
- Comprehensive data
- Digital delivery
- Good for volume clients

### AI_Premium_Report
**Suggested Retail:** $300-$500
- Premium presentation
- 30+ pages
- Print-ready
- High-value consulting
- Matches Frank Shallenberger pricing

---

## Technical Details

### Files Modified/Created:

**New Files:**
- `utils/ai_basic_report.py` - Basic report generator (copy of beautiful_report.py)
- `utils/ai_premium_report.py` - Premium report generator (new)
- `upload_to_database.py` - CLI tool to upload reports to website
- `REPORT_TYPES_GUIDE.md` - This guide

**Modified Files:**
- `upload_report.py` - Now supports `--premium` flag
- `process_all_tests.py` - Unchanged (uses basic by default)

### Data Flow:

```
PDF → extract_pnoe_data() → enhance_with_scores() → generate_report()
                                                      ↓
                                        ┌─────────────┴──────────────┐
                                        ↓                            ↓
                              ai_basic_report.py          ai_premium_report.py
                                        ↓                            ↓
                               1-2 page HTML                 30+ page HTML
                                        ↓                            ↓
                              uploads/file_id_report.html
                                        ↓
                              upload_to_database.py
                                        ↓
                          Supabase Database → Website Dashboard
```

---

## FAQs

**Q: Can I generate both reports for the same patient?**
A: Yes! Just run the command twice:
```bash
python3 upload_report.py test.pdf Performance          # Basic
python3 upload_report.py test.pdf Performance --premium  # Premium
```

**Q: Which report should I use by default?**
A:
- **Basic** for quick assessments, dashboard viewing, email distribution
- **Premium** for high-paying clients, consultations, printed reports

**Q: Do they use the same data?**
A: Yes! Both use identical metabolic calculations. Only presentation differs.

**Q: Can I customize the premium report?**
A: Yes! Edit `utils/ai_premium_report.py` to customize:
- Cover page branding
- Metric descriptions
- Page layout
- Colors and styling

**Q: How do I add my clinic branding?**
A: Edit line 20-26 in `ai_premium_report.py`:
```python
self.patient_info = {
    'name': 'Patient Name',
    'test_date': datetime.now().strftime('%m/%d/%Y'),
    'test_type': 'Longevity',
    'provider_email': 'YOUR_CLINIC@email.com',  # Change this
    'age': None,
    ...
}
```

---

## Next Steps

1. ✅ Generate test reports (both basic and premium)
2. ✅ Review output quality
3. ✅ Upload to website database
4. ✅ Test website dashboard viewing/downloading
5. Set pricing for each report type
6. Market to clients!

---

## Support

**Issues?**
- Check `upload_report.py` usage examples
- Verify virtual environment is activated: `source venv/bin/activate`
- Check file paths are correct
- Review generated HTML in uploads/ directory

**Questions?**
All algorithms are verified unique and working correctly (see `process_all_tests.py` output)
