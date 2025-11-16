#!/usr/bin/env python3
"""
Script to update the CSS in ultimate_report_template.py with ultra-condensed format
"""

# Read the ultra-condensed CSS
ultra_condensed_css = """
* { margin: 0; padding: 0; box-sizing: border-box; }

@page {
    size: letter;
    margin-left: 1.5in;
    margin-right: 1.5in;
    margin-top: 0.3in;
    margin-bottom: 0.3in;
}

:root {
    --primary: #1E40AF;
    --secondary: #0D9488;
    --success: #10B981;
    --warning: #F59E0B;
    --danger: #EF4444;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    line-height: 1.2;
    color: #0F172A;
    font-size: 6pt;
    background: white;
}

.page-wrapper,. container {
    width: 100%;
}

@media screen {
    .page-wrapper, .container {
        padding-left: 1.5in;
        padding-right: 1.5in;
        padding-top: 0.3in;
        padding-bottom: 0.3in;
    }
}

/* Ultra Condensed Hero */
.hero {
    background: linear-gradient(135deg, #1E40AF, #8B5CF6);
    color: white;
    padding: 15px 12px;
    text-align: center;
    margin-left: -1.5in;
    margin-right: -1.5in;
    margin-top: -0.3in;
}

.hero-title { font-size: 16pt; font-weight: 700; margin-bottom: 4px; }
.hero-subtitle { font-size: 6pt; margin-bottom: 8px; opacity: 0.95; }
.patient-card { background: rgba(255,255,255,0.15); padding: 8px; border-radius: 8px; margin-top: 8px; }
.patient-name { font-size: 12pt; font-weight: 700; }
.patient-details { font-size: 5pt; opacity: 0.9; margin-top: 3px; }

/* Sections */
.section, .page { margin: 10px 0; padding: 0; }
.section-title { font-size: 10pt; font-weight: 700; color: var(--primary); margin-bottom: 4px; border-bottom: 1.5px solid var(--primary); padding-bottom: 2px; }
.section-subtitle { font-size: 5pt; color: #64748B; margin-bottom: 6px; text-align: center; }

/* Exec Summary */
.exec-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 8px; }
.exec-card { background: white; padding: 8px; border-radius: 6px; border-left: 2px solid var(--primary); box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.exec-label { font-size: 5pt; text-transform: uppercase; color: #64748B; margin-bottom: 3px; font-weight: 600; }
.exec-value { font-size: 14pt; font-weight: 700; color: var(--primary); line-height: 1; }
.exec-unit { font-size: 4.5pt; color: #64748B; margin-top: 2px; }

/* Bio Age */
.bio-age-box, .bio-age-mega { background: linear-gradient(135deg, var(--primary), var(--secondary)); color: white; padding: 10px; border-radius: 8px; margin: 8px 0; }
.age-grid { display: grid; grid-template-columns: 1fr auto 1fr; gap: 10px; align-items: center; }
.age-box { text-align: center; padding: 8px; background: rgba(255,255,255,0.15); border-radius: 6px; }
.age-label { font-size: 4.5pt; text-transform: uppercase; margin-bottom: 3px; }
.age-number { font-size: 18pt; font-weight: 700; line-height: 1; }
.age-text { font-size: 4.5pt; margin-top: 2px; }
.age-arrow { font-size: 14pt; }
.age-insight, .insight-text { margin-top: 6px; padding: 6px; background: rgba(255,255,255,0.2); border-radius: 6px; text-align: center; font-size: 6pt; font-weight: 600; }

/* Metrics */
.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; margin: 8px 0; }
.metric-card { background: white; padding: 6px; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); border-top: 2px solid var(--primary); }
.metric-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 3px; }
.metric-name { font-size: 5pt; font-weight: 600; line-height: 1.1; }
.metric-score { font-size: 11pt; font-weight: 700; color: var(--primary); line-height: 1; }
.metric-badge { display: inline-block; padding: 1px 4px; border-radius: 4px; font-size: 4pt; font-weight: 700; text-transform: uppercase; }
.badge-excellent { background: rgba(16,185,129,0.15); color: var(--success); }
.badge-good { background: rgba(30,64,175,0.15); color: var(--primary); }
.badge-neutral { background: rgba(245,158,11,0.15); color: var(--warning); }
.progress-bar { width: 100%; height: 3px; background: #E2E8F0; border-radius: 3px; overflow: hidden; margin-top: 3px; }
.progress-fill { height: 100%; background: linear-gradient(90deg, var(--primary), var(--secondary)); transition: width 1s ease; }

/* Charts */
.chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 8px 0; }
.chart-container { position: relative; height: 120px; }

/* Caloric */
.caloric-box { background: linear-gradient(135deg, #10B981, #059669); color: white; padding: 10px; border-radius: 8px; margin: 8px 0; }
.caloric-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.caloric-section { background: rgba(255,255,255,0.15); padding: 6px; border-radius: 6px; text-align: center; }
.caloric-label { font-size: 4.5pt; text-transform: uppercase; margin-bottom: 4px; }
.caloric-value { font-size: 14pt; font-weight: 700; line-height: 1; }
.caloric-unit { font-size: 4.5pt; margin-top: 2px; }
.fuel-bar { display: flex; height: 18px; border-radius: 6px; overflow: hidden; margin: 6px 0; }
.fuel-section { display: flex; align-items: center; justify-content: center; color: white; font-size: 5.5pt; font-weight: 700; }

/* Zones */
.zone-card { background: white; padding: 6px; margin: 3px 0; border-radius: 6px; border-left: 2px solid; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.zone-card.zone-1 { border-left-color: #10B981; }
.zone-card.zone-2 { border-left-color: #3B82F6; }
.zone-card.zone-3 { border-left-color: #F59E0B; }
.zone-card.zone-4 { border-left-color: #EF4444; }
.zone-card.zone-5 { border-left-color: #DC2626; }
.zone-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px; }
.zone-name { font-size: 6pt; font-weight: 700; }
.zone-hr { font-size: 7pt; font-weight: 700; color: var(--primary); }
.zone-desc { font-size: 5pt; line-height: 1.3; color: #64748B; }

/* Training Plan */
.training-plan { background: white; padding: 8px; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); margin: 6px 0; }
.training-plan h3 { font-size: 7pt; margin-bottom: 4px; text-align: center; }
.training-plan p { font-size: 5pt; line-height: 1.4; text-align: center; }

/* Interventions */
.intervention-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; margin: 8px 0; }
.intervention-card { background: white; padding: 6px; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.intervention-title { font-size: 6pt; font-weight: 700; margin-bottom: 3px; }
.intervention-text { font-size: 4.5pt; line-height: 1.3; color: #64748B; }
.benefit-tag { display: inline-block; padding: 1px 4px; background: rgba(30,64,175,0.1); color: var(--primary); border-radius: 4px; font-size: 4pt; font-weight: 600; margin: 1px; }

/* Action Plan */
.action-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; margin: 8px 0; }
.action-card { background: white; padding: 8px; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.action-icon { width: 20px; height: 20px; background: linear-gradient(135deg, var(--primary), var(--secondary)); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 10pt; margin-bottom: 4px; }
.action-title { font-size: 6pt; font-weight: 700; margin-bottom: 3px; }
.action-desc { font-size: 4.5pt; line-height: 1.3; color: #64748B; margin-bottom: 4px; }
.action-priority { display: inline-block; padding: 2px 5px; border-radius: 4px; font-size: 4pt; font-weight: 700; text-transform: uppercase; }
.action-priority.high { background: rgba(239,68,68,0.1); color: var(--danger); }
.action-priority.medium { background: rgba(245,158,11,0.1); color: var(--warning); }
.action-priority.low { background: rgba(16,185,129,0.1); color: var(--success); }

/* Timeline / Progress Tracker */
.timeline, .progress-tracker { background: white; padding: 10px; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); margin: 8px 0; }
.timeline-item, .week-plan { display: grid; grid-template-columns: 60px 1fr; gap: 8px; margin-bottom: 6px; padding-bottom: 6px; border-bottom: 1px solid #E2E8F0; }
.timeline-item:last-child, .week-plan:last-child { border-bottom: none; margin-bottom: 0; }
.timeline-week, .week-number { font-size: 5.5pt; font-weight: 700; color: var(--primary); }
.timeline-content h4, .week-goals h4 { font-size: 6pt; font-weight: 700; margin-bottom: 2px; }
.timeline-content p, .week-goals ul li, .week-goals p { font-size: 4.5pt; line-height: 1.3; color: #64748B; }
.week-goals ul { padding-left: 10px; margin: 3px 0; }

/* AI Section */
.ai-section { background: linear-gradient(135deg, #10b981, #059669); padding: 10px; border-radius: 8px; margin: 8px 0; color: white; }
.ai-section h2 { color: white; font-size: 9pt; margin-bottom: 5px; text-align: center; }
.ai-disclaimer { background: rgba(255,255,255,0.15); padding: 6px; border-radius: 6px; margin: 6px 0; font-size: 4.5pt; line-height: 1.4; }
.ai-disclaimer ul { margin: 3px 0; padding-left: 10px; }
.ai-disclaimer li { margin: 2px 0; }
.ai-content { background: white; padding: 8px; border-radius: 6px; margin: 6px 0; color: #334155; }
.ai-content h3 { color: #10b981; font-size: 7pt; margin: 6px 0 3px 0; }
.ai-content p, .ai-content li { font-size: 4.5pt; line-height: 1.4; margin: 2px 0; }
.ai-content ul, .ai-content ol { padding-left: 10px; margin: 3px 0; }

.page-break { page-break-before: always; }

@media print {
    .page-wrapper, .container { padding: 0; }
    .hero { margin-left: 0; margin-right: 0; margin-top: 0; }
}
"""

# Read current template file
with open('utils/ultimate_report_template.py', 'r') as f:
    lines = f.readlines()

# Find the _get_styles method and replace its return value
output = []
in_get_styles = False
skip_until_next_method = False

for i, line in enumerate(lines):
    if '    def _get_styles(self):' in line:
        in_get_styles = True
        output.append(line)
        output.append('        """CSS styles - Ultra Condensed Format"""\n')
        output.append('        return """\n')
        output.append(ultra_condensed_css)
        output.append('        """\n')
        skip_until_next_method = True
        continue

    if skip_until_next_method:
        # Skip lines until we hit the next method definition
        if i > 122 and line.strip().startswith('def _'):
            skip_until_next_method = False
            output.append(line)
        continue

    output.append(line)

# Write updated file
with open('utils/ultimate_report_template.py', 'w') as f:
    f.writelines(output)

print("✅ Successfully updated CSS in ultimate_report_template.py to ultra-condensed format!")
