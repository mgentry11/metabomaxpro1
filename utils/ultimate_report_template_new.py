"""
Condensed Metabolic Report Template
Clean, professional format without images
"""
import json

class MarkGentryReport:
    """Generate condensed report with clean formatting"""

    def __init__(self):
        """Initialize with patient data"""

        self.patient_info = {
            'name': 'Mark Gentry',
            'test_date': '09/25/2025',
            'test_type': 'Performance Assessment',
            'age': 35,
            'weight_kg': 71,
            'height_cm': 188,
            'gender': 'Male'
        }

        # Core performance scores
        self.core_scores = {
            'symp_parasym': 76,
            'ventilation_eff': 74,
            'breathing_coord': 67,
            'lung_util': 100,
            'hrv': 88,
            'metabolic_rate': 46,
            'fat_burning': 58
        }

        # Caloric data
        self.caloric_data = {
            'burn_rest': 2074,
            'burn_workout': 2274,
            'eat_rest': 1724,
            'eat_workout': 1924,
            'fat_percent': 53,
            'cho_percent': 47
        }

        # Calculate biological age
        avg_score = sum(self.core_scores.values()) / len(self.core_scores)
        self.chronological_age = 35
        self.biological_age = 31

    def generate(self, output_path):
        """Generate complete report"""

        avg_score = sum(self.core_scores.values()) / len(self.core_scores)

        # Count excellent and good metrics
        excellent_count = sum(1 for v in self.core_scores.values() if v >= 85)
        good_plus_count = sum(1 for v in self.core_scores.values() if v >= 70)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Metabolic Blueprint 2025 - {self.patient_info['name']}</title>
    <style>
{self._get_styles()}
    </style>
</head>
<body>

<div class="container">

{self._generate_header()}
{self._generate_executive_summary(excellent_count, good_plus_count)}
{self._generate_bio_age()}
{self._generate_core_metrics()}
{self._generate_caloric_section()}
{self._generate_training_zones()}

<div class="page-break"></div>

{self._generate_interventions()}
{self._generate_action_plan()}
{self._generate_protocol()}

<div class="page-break"></div>

{self._generate_ai_section()}

{self._generate_footer()}

</div><!-- End container -->

</body>
</html>"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ Report generated: {output_path}")

    def _get_styles(self):
        """CSS styles - Clean, condensed format"""
        return """        @page {
            margin-left: 3in;
            margin-right: 3in;
            margin-top: 0.5in;
            margin-bottom: 0.5in;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.3;
            color: #333;
            margin: 0;
            padding: 0;
        }

        .container {
            margin-left: 3in;
            margin-right: 3in;
            margin-top: 0.5in;
            margin-bottom: 0.5in;
        }

        .header {
            background: linear-gradient(135deg, #4a5fbd 0%, #6b7fd7 100%);
            color: white;
            padding: 20px;
            margin-bottom: 15px;
            text-align: center;
        }

        .header h1 {
            margin: 10px 0;
            font-size: 24pt;
            font-weight: bold;
        }

        .header .subtitle {
            font-size: 9pt;
            opacity: 0.9;
            margin: 5px 0;
        }

        .header .date {
            font-size: 11pt;
            margin-top: 10px;
        }

        h2 {
            font-size: 14pt;
            color: #4a5fbd;
            margin: 15px 0 8px 0;
            padding-bottom: 3px;
            border-bottom: 2px solid #4a5fbd;
        }

        h3 {
            font-size: 11pt;
            color: #333;
            margin: 10px 0 5px 0;
            font-weight: 600;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            margin: 10px 0;
        }

        .summary-box {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
            border-radius: 4px;
        }

        .summary-box .label {
            font-size: 8pt;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .summary-box .value {
            font-size: 20pt;
            font-weight: bold;
            color: #4a5fbd;
            margin: 5px 0;
        }

        .summary-box .subtext {
            font-size: 8pt;
            color: #888;
        }

        .bio-age {
            background: #f0f4ff;
            padding: 12px;
            margin: 10px 0;
            border-radius: 4px;
            display: flex;
            justify-content: space-around;
            align-items: center;
        }

        .bio-age .age-item {
            text-align: center;
        }

        .bio-age .age-value {
            font-size: 24pt;
            font-weight: bold;
            color: #4a5fbd;
        }

        .bio-age .age-label {
            font-size: 8pt;
            color: #666;
            text-transform: uppercase;
        }

        .metrics-list {
            margin: 10px 0;
        }

        .metric-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 0;
            border-bottom: 1px solid #eee;
        }

        .metric-name {
            font-size: 10pt;
            font-weight: 500;
        }

        .metric-value {
            font-size: 16pt;
            font-weight: bold;
            color: #4a5fbd;
        }

        .badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 7pt;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-left: 8px;
        }

        .badge.excellent {
            background: #d4f4dd;
            color: #0e6027;
        }

        .badge.good {
            background: #dbe9ff;
            color: #1a4d8f;
        }

        .badge.neutral {
            background: #fff3cd;
            color: #856404;
        }

        .calorie-section {
            background: #10b981;
            color: white;
            padding: 15px;
            border-radius: 4px;
            margin: 10px 0;
        }

        .calorie-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 10px;
        }

        .calorie-box {
            background: rgba(255, 255, 255, 0.15);
            padding: 10px;
            border-radius: 4px;
        }

        .calorie-box .cal-label {
            font-size: 8pt;
            opacity: 0.9;
            margin-bottom: 3px;
        }

        .calorie-box .cal-value {
            font-size: 20pt;
            font-weight: bold;
        }

        .calorie-box .cal-unit {
            font-size: 9pt;
        }

        .fuel-bar {
            display: flex;
            height: 30px;
            border-radius: 4px;
            overflow: hidden;
            margin: 8px 0;
        }

        .fuel-fat {
            background: #ef4444;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 9pt;
        }

        .fuel-carb {
            background: #3b82f6;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 9pt;
        }

        .zone-card {
            margin: 8px 0;
            padding: 8px;
            border-left: 4px solid;
            background: #f9fafb;
        }

        .zone-card.z1 { border-left-color: #10b981; }
        .zone-card.z2 { border-left-color: #3b82f6; }
        .zone-card.z3 { border-left-color: #f59e0b; }
        .zone-card.z4 { border-left-color: #ef4444; }
        .zone-card.z5 { border-left-color: #b91c1c; }

        .zone-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 4px;
        }

        .zone-name {
            font-weight: bold;
            font-size: 10pt;
        }

        .zone-bpm {
            font-weight: bold;
            font-size: 12pt;
            color: #4a5fbd;
        }

        .zone-desc {
            font-size: 8pt;
            line-height: 1.3;
            color: #555;
        }

        .intervention-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 10px 0;
        }

        .intervention-card {
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 4px;
        }

        .intervention-card h4 {
            margin: 0 0 5px 0;
            font-size: 11pt;
            color: #333;
        }

        .intervention-card p {
            margin: 0;
            font-size: 8pt;
            color: #666;
        }

        .action-item {
            margin: 8px 0;
            padding: 10px;
            background: #f9fafb;
            border-radius: 4px;
        }

        .action-item h4 {
            margin: 0 0 4px 0;
            font-size: 10pt;
            color: #333;
        }

        .action-item p {
            margin: 0;
            font-size: 8pt;
            line-height: 1.4;
            color: #555;
        }

        .priority {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 7pt;
            font-weight: bold;
            margin-top: 5px;
        }

        .priority.high {
            background: #fee2e2;
            color: #991b1b;
        }

        .priority.medium {
            background: #fed7aa;
            color: #9a3412;
        }

        .priority.low {
            background: #d1fae5;
            color: #065f46;
        }

        .protocol-timeline {
            margin: 10px 0;
        }

        .protocol-phase {
            margin: 8px 0;
            padding: 8px;
            border-left: 3px solid #4a5fbd;
            background: #f0f4ff;
        }

        .protocol-phase h4 {
            margin: 0 0 4px 0;
            font-size: 10pt;
            color: #4a5fbd;
        }

        .protocol-phase .phase-title {
            font-weight: bold;
            font-size: 9pt;
            margin-bottom: 3px;
        }

        .protocol-phase p {
            margin: 0;
            font-size: 8pt;
            line-height: 1.3;
            color: #555;
        }

        .ai-section {
            background: #10b981;
            color: white;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
        }

        .ai-section h2 {
            color: white;
            border-bottom-color: white;
            margin-top: 0;
        }

        .ai-warning {
            background: rgba(255, 255, 255, 0.15);
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
            font-size: 9pt;
        }

        .ai-warning ul {
            margin: 8px 0;
            padding-left: 20px;
        }

        .ai-warning li {
            margin: 4px 0;
        }

        .peptide-section {
            background: white;
            color: #333;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        .peptide-section h3 {
            color: #10b981;
            margin-top: 8px;
        }

        .peptide-section ul, .peptide-section ol {
            margin: 5px 0;
            padding-left: 20px;
            font-size: 9pt;
        }

        .peptide-section li {
            margin: 3px 0;
            line-height: 1.4;
        }

        .peptide-section p {
            margin: 5px 0;
            font-size: 9pt;
            line-height: 1.4;
        }

        @media print {
            .container {
                margin-left: 3in;
                margin-right: 3in;
                margin-top: 0.5in;
                margin-bottom: 0.5in;
            }

            .page-break {
                page-break-before: always;
            }
        }

        @media screen {
            .container {
                margin-left: 3in;
                margin-right: 3in;
                margin-top: 0.5in;
                margin-bottom: 0.5in;
            }
        }"""

    def _generate_header(self):
        """Generate clean header"""
        return f"""
<div class="header">
    <div class="subtitle">Optimal Vitality</div>
    <div class="subtitle" style="font-size: 11pt; font-weight: bold; letter-spacing: 1px;">⚡ PERFORMANCE METABOLIC BLUEPRINT 2025</div>
    <h1>{self.patient_info['name']}</h1>
    <div class="subtitle">Comprehensive metabolic testing, training zones, and performance optimization</div>
    <div class="subtitle">powered by PNOE technology and personalized for elite results</div>
    <div class="date">Test Date: {self.patient_info['test_date']} • {self.patient_info['test_type']} • Optimal Vitality</div>
</div>"""

    def _generate_executive_summary(self, excellent_count, good_plus_count):
        """Generate executive summary"""
        avg_score = int(sum(self.core_scores.values()) / len(self.core_scores))

        # Get names of excellent metrics
        excellent_metrics = [k.replace('_', ' ').title() for k, v in self.core_scores.items() if v >= 85]
        excellent_names = ' + '.join(excellent_metrics[:2]) if excellent_metrics else 'None'

        return f"""
<h2>Executive Summary</h2>
<p style="text-align: center; font-size: 9pt; color: #666; margin: 5px 0;">Your performance snapshot at a glance</p>

<div class="summary-grid">
    <div class="summary-box">
        <div class="label">Overall Health Score</div>
        <div class="value">{avg_score}</div>
        <div class="subtext">out of 100</div>
    </div>
    <div class="summary-box">
        <div class="label">Excellent Metrics</div>
        <div class="value">{excellent_count}</div>
        <div class="subtext">of 7 ({excellent_names})</div>
    </div>
    <div class="summary-box">
        <div class="label">Good+ Metrics</div>
        <div class="value">{good_plus_count}</div>
        <div class="subtext">of 7 total</div>
    </div>
</div>"""

    def _generate_bio_age(self):
        """Generate biological age section"""
        age_diff = self.chronological_age - self.biological_age
        insight = f"🎉 Outstanding! You are {age_diff} years younger than your chronological age!" if age_diff > 0 else "Focus on lifestyle improvements to reduce biological age."

        return f"""
<div class="bio-age">
    <div class="age-item">
        <div class="age-label">Chronological Age</div>
        <div class="age-value">{self.chronological_age}</div>
        <div class="subtext">years</div>
    </div>
    <div style="font-size: 20pt; color: #4a5fbd;">→</div>
    <div class="age-item">
        <div class="age-label">Biological Age</div>
        <div class="age-value">{self.biological_age}</div>
        <div class="subtext">years</div>
    </div>
</div>
<p style="text-align: center; font-size: 10pt; font-weight: bold; color: #10b981; margin: 5px 0;">{insight}</p>"""

    def _generate_core_metrics(self):
        """Generate core metrics list"""

        def get_badge(score):
            if score >= 85:
                return 'excellent'
            elif score >= 70:
                return 'good'
            else:
                return 'neutral'

        metrics_html = []
        metric_names = {
            'lung_util': 'Lung Utilization',
            'hrv': 'Heart Rate Variability (HRV)',
            'symp_parasym': 'Sympathetic/Parasympathetic',
            'ventilation_eff': 'Ventilation Efficiency',
            'breathing_coord': 'Breathing Coordination',
            'fat_burning': 'Fat-Burning Efficiency',
            'metabolic_rate': 'Metabolic Rate'
        }

        for key, name in metric_names.items():
            score = self.core_scores[key]
            badge_class = get_badge(score)
            badge_text = badge_class.capitalize()

            metrics_html.append(f"""
    <div class="metric-row">
        <span class="metric-name">{name} <span class="badge {badge_class}">{badge_text}</span></span>
        <span class="metric-value">{score}%</span>
    </div>""")

        return f"""
<h2>Core Performance Metrics</h2>
<p style="font-size: 9pt; color: #666; margin: 5px 0;">7 key biomarkers measuring your athletic potential</p>

<div class="metrics-list">
{''.join(metrics_html)}
</div>"""

    def _generate_caloric_section(self):
        """Generate caloric balance section"""
        return f"""
<h2>Caloric Balance & Fuel Strategy</h2>
<p style="font-size: 9pt; color: #666; margin: 5px 0;">Your personalized energy targets for performance</p>

<div class="calorie-section">
    <h3 style="color: white; margin-top: 0; font-size: 10pt; text-transform: uppercase; letter-spacing: 1px;">You Burn</h3>
    <div class="calorie-grid">
        <div class="calorie-box">
            <div class="cal-label">Rest Days</div>
            <div class="cal-value">{self.caloric_data['burn_rest']} <span class="cal-unit">kcal/day</span></div>
        </div>
        <div class="calorie-box">
            <div class="cal-label">Workout Days</div>
            <div class="cal-value">{self.caloric_data['burn_workout']} <span class="cal-unit">kcal/day</span></div>
        </div>
    </div>

    <h3 style="color: white; margin-top: 15px; font-size: 10pt; text-transform: uppercase; letter-spacing: 1px;">You Should Eat</h3>
    <div class="calorie-grid">
        <div class="calorie-box">
            <div class="cal-label">Rest Days</div>
            <div class="cal-value">{self.caloric_data['eat_rest']} <span class="cal-unit">kcal/day</span></div>
        </div>
        <div class="calorie-box">
            <div class="cal-label">Workout Days</div>
            <div class="cal-value">{self.caloric_data['eat_workout']} <span class="cal-unit">kcal/day</span></div>
        </div>
    </div>

    <h3 style="color: white; margin-top: 15px; margin-bottom: 8px; font-size: 10pt;">Fuel Sources</h3>
    <div class="fuel-bar">
        <div class="fuel-fat" style="width: {self.caloric_data['fat_percent']}%;">Fats {self.caloric_data['fat_percent']}%</div>
        <div class="fuel-carb" style="width: {self.caloric_data['cho_percent']}%;">Carbs {self.caloric_data['cho_percent']}%</div>
    </div>
    <p style="font-size: 8pt; margin: 5px 0;">Your metabolism uses an energy mix of {self.caloric_data['fat_percent']}% fats and {self.caloric_data['cho_percent']}% carbohydrates at rest.</p>
</div>"""

    def _generate_training_zones(self):
        """Generate training zones section"""
        return f"""
<h2>Training Zones</h2>
<p style="font-size: 9pt; color: #666; margin: 5px 0;">Personalized heart rate zones for optimal performance</p>

<div class="zone-card z1">
    <div class="zone-header">
        <span class="zone-name">Zone 1: Recovery</span>
        <span class="zone-bpm">92-111 bpm</span>
    </div>
    <div class="zone-desc">Active recovery, warm-up, cool-down. Very easy conversational pace. Promotes recovery and prepares body for harder efforts.</div>
</div>

<div class="zone-card z2">
    <div class="zone-header">
        <span class="zone-name">Zone 2: Endurance Base</span>
        <span class="zone-bpm">111-129 bpm</span>
    </div>
    <div class="zone-desc"><strong>YOUR PRIMARY ZONE</strong> for improving metabolic rate and fat-burning. Easy conversational pace. Build aerobic base, improve mitochondrial function. Target: 3-4 sessions weekly, 45-60 minutes.</div>
</div>

<div class="zone-card z3">
    <div class="zone-header">
        <span class="zone-name">Zone 3: Tempo</span>
        <span class="zone-bpm">129-148 bpm</span>
    </div>
    <div class="zone-desc">Moderate-hard pace. Short phrases possible. Improves lactate threshold and tempo endurance. Use sparingly.</div>
</div>

<div class="zone-card z4">
    <div class="zone-header">
        <span class="zone-name">Zone 4: Lactate Threshold</span>
        <span class="zone-bpm">148-166 bpm</span>
    </div>
    <div class="zone-desc">Hard pace, few words possible. Lactate threshold training. Improves VO2 max and performance capacity. 1-2 sessions weekly for strength development.</div>
</div>

<div class="zone-card z5">
    <div class="zone-header">
        <span class="zone-name">Zone 5: VO2 Max</span>
        <span class="zone-bpm">166-185 bpm</span>
    </div>
    <div class="zone-desc">Maximum effort, no talking. Intervals only. Maximizes VO2 max and anaerobic capacity. Short bursts (30sec - 5min) for peak performance.</div>
</div>

<h3 style="margin-top: 15px;">{self.patient_info['name'].split()[0]}'s Weekly Training Plan</h3>
<ul style="font-size: 9pt; margin: 5px 0; padding-left: 20px; line-height: 1.5;">
    <li><strong>Zone 2 (Endurance):</strong> 3-4 sessions × 45-60 min = PRIORITY #1 to improve metabolic rate ({self.core_scores['metabolic_rate']}%) and fat-burning ({self.core_scores['fat_burning']}%)</li>
    <li><strong>Zone 4 (Threshold):</strong> 1-2 sessions × 20-30 min = Support strength development goals</li>
    <li><strong>Resistance Training:</strong> 3 sessions × 45-60 min = Maintain strength development focus</li>
    <li><strong>Rest/Recovery:</strong> 1-2 days per week with Zone 1 activity</li>
</ul>"""

    def _generate_interventions(self):
        """Generate interventions section"""
        return """
<h2>Recommended Interventions</h2>
<p style="font-size: 9pt; color: #666; margin: 5px 0;">Targeted strategies for your specific needs</p>

<div class="intervention-grid">
    <div class="intervention-card">
        <h4>Zone 2 Training</h4>
        <p>Primary intervention for metabolic rate & fat-burning</p>
        <div><span class="badge good">Performance</span> <span class="badge good">Evidence-Based</span></div>
    </div>
    <div class="intervention-card">
        <h4>ARX Omni</h4>
        <p>Efficient resistance training for strength goals</p>
        <div><span class="badge good">Performance</span> <span class="badge good">Evidence-Based</span></div>
    </div>
    <div class="intervention-card">
        <h4>Cold Plunge</h4>
        <p>Boost fat-burning 15-37%, accelerate recovery</p>
        <div><span class="badge good">Performance</span> <span class="badge good">Evidence-Based</span></div>
    </div>
    <div class="intervention-card">
        <h4>Nutrition Protocol</h4>
        <p>High protein (1.6-2.2g/kg) for muscle & metabolism</p>
        <div><span class="badge good">Performance</span> <span class="badge good">Evidence-Based</span></div>
    </div>
    <div class="intervention-card">
        <h4>Breathwork Training</h4>
        <p>Optimize breathing coordination (currently 67%)</p>
        <div><span class="badge good">Performance</span> <span class="badge good">Evidence-Based</span></div>
    </div>
    <div class="intervention-card">
        <h4>Sauna Recovery</h4>
        <p>Improve HRV and parasympathetic activation</p>
        <div><span class="badge good">Performance</span> <span class="badge good">Evidence-Based</span></div>
    </div>
</div>"""

    def _generate_action_plan(self):
        """Generate action plan section"""
        return f"""
<h2>Your Action Plan</h2>
<p style="font-size: 9pt; color: #666; margin: 5px 0;">Prioritized roadmap for performance gains</p>

<div class="action-item">
    <h4>🏃 Zone 2 Endurance Training</h4>
    <p>3-4 weekly sessions, 45-60 min at 111-129 bpm. THE most powerful intervention for improving metabolic rate ({self.core_scores['metabolic_rate']}% → 70%+) and fat-burning ({self.core_scores['fat_burning']}% → 70%+).</p>
    <div class="priority high">PRIORITY: HIGH</div>
</div>

<div class="action-item">
    <h4>💪 Strength Training</h4>
    <p>Continue 3x weekly resistance work for strength development. Add compound movements to support metabolic rate increase.</p>
    <div class="priority high">PRIORITY: HIGH</div>
</div>

<div class="action-item">
    <h4>🥗 Performance Nutrition</h4>
    <p>High protein (1.6-2.2g/kg = 114-156g/day), omega-3 rich fish 3x/week. Time carbs around workouts for performance.</p>
    <div class="priority medium">PRIORITY: MEDIUM</div>
</div>

<div class="action-item">
    <h4>💤 Recovery Optimization</h4>
    <p>7-9 hours nightly. Consistent schedule. Your excellent HRV ({self.core_scores['hrv']}%) shows good recovery - maintain this!</p>
    <div class="priority medium">PRIORITY: MEDIUM</div>
</div>

<div class="action-item">
    <h4>🧊 Cold Exposure</h4>
    <p>Cold plunges 3-5 min, 2-3x weekly. Can boost fat-burning by 15-37% and accelerate recovery between sessions.</p>
    <div class="priority low">PRIORITY: LOW</div>
</div>

<div class="action-item">
    <h4>🧘 Breathwork Practice</h4>
    <p>10 min daily box breathing to optimize breathing coordination. Your {self.core_scores['breathing_coord']}% is good but can reach 80%+ with practice.</p>
    <div class="priority low">PRIORITY: LOW</div>
</div>"""

    def _generate_protocol(self):
        """Generate 90-day protocol section"""
        return f"""
<h2>90-Day Performance Protocol</h2>
<p style="font-size: 9pt; color: #666; margin: 5px 0;">Your structured roadmap to peak metabolic fitness</p>

<div class="protocol-timeline">
    <div class="protocol-phase">
        <h4>WEEKS 1-4</h4>
        <div class="phase-title">Base Building Phase</div>
        <p>Add 2-3 Zone 2 sessions (45 min) alongside strength training. Monitor heart rate compliance. Focus on easy conversational pace. Track recovery and energy levels.</p>
    </div>

    <div class="protocol-phase">
        <h4>WEEKS 5-8</h4>
        <div class="phase-title">Development Phase</div>
        <p>Increase to 3-4 Zone 2 sessions (60 min). Continue strength training 3x/week. Add cold plunges 2x/week. Implement performance nutrition timing around workouts.</p>
    </div>

    <div class="protocol-phase">
        <h4>WEEKS 9-12</h4>
        <div class="phase-title">Integration Phase</div>
        <p>Maintain 4x Zone 2 sessions. Add 1x Zone 4 threshold session. Continue all protocols. Monitor performance gains in strength training. Prepare for retest.</p>
    </div>

    <div class="protocol-phase">
        <h4>WEEK 13</h4>
        <div class="phase-title">Retest & Reassess</div>
        <p><strong>Expected Results:</strong> Metabolic Rate: {self.core_scores['metabolic_rate']}% → 70%+ | Fat-Burning: {self.core_scores['fat_burning']}% → 75%+ | Overall Score: {int(sum(self.core_scores.values()) / len(self.core_scores))}% → 80%+ | Strength gains + improved endurance capacity</p>
    </div>
</div>"""

    def _generate_ai_section(self):
        """Generate AI section placeholder"""
        return """
<div class="ai-section">
    <h2>🤖 AI-Powered Personalized Recommendations</h2>
    <p style="font-size: 9pt; margin: 5px 0;">Based on your metabolic data and health goals</p>

    <div class="ai-warning">
        <p style="margin: 0 0 5px 0;"><strong>✅ First, the good news:</strong></p>
        <p style="font-size: 8pt; margin: 5px 0;">Your core metabolic data (VO2 max, RMR, heart rate zones, substrate utilization) uses <strong>well-established, medically-approved algorithms</strong>—the same ones testing facilities use. No AI. No guesswork. Just proven math.</p>

        <p style="margin: 10px 0 5px 0;"><strong>The recommendations below?</strong> That's where AI comes in. AI is incredibly smart, but it's also an overachiever that really wants you to like it.</p>

        <p style="margin: 5px 0;"><strong>AI has a few quirks you should know about:</strong></p>
        <ul style="margin: 5px 0; font-size: 8pt;">
            <li><strong>It can hallucinate</strong> - occasionally making up facts with complete confidence</li>
            <li><strong>It's a people-pleaser</strong> - wants to tell you what you want to hear</li>
            <li><strong>It lacks clinical context</strong> - doesn't know your complete medical history</li>
        </ul>

        <p style="font-size: 8pt; margin: 8px 0 0 0;"><strong>💡 That's why every recommendation below should be reviewed with a healthcare professional</strong>—specifically one experienced with VO2 max testing, metabolic optimization, and performance physiology.</p>

        <p style="font-size: 8pt; text-align: center; margin: 8px 0 0 0; font-weight: bold;">Think of these as homework to bring to your doctor, not medical advice to follow blindly.</p>
    </div>
</div>

<div class="peptide-section">
    <h2 style="color: #10b981; border-bottom-color: #10b981;">AI Recommendations will appear here when generated</h2>
    <p>Click "Add AI" button on the dashboard to generate personalized AI recommendations.</p>
</div>"""

    def _generate_footer(self):
        """Generate footer"""
        return f"""
<footer style="margin-top: 30px; padding-top: 15px; border-top: 2px solid #4a5fbd; text-align: center; font-size: 8pt; color: #666;">
    <p style="margin: 5px 0;"><strong>Performance Metabolic Blueprint 2025</strong></p>
    <p style="margin: 5px 0;">Powered by PNOE Technology | Test Date: {self.patient_info['test_date']}</p>
    <p style="margin: 5px 0;">This report combines medically-approved metabolic calculations with AI-assisted recommendations.</p>
    <p style="margin: 5px 0;"><strong>Always consult with qualified healthcare professionals before implementing any recommendations.</strong></p>
</footer>"""


# Test generation
if __name__ == '__main__':
    report = MarkGentryReport()
    report.generate('/tmp/test_report.html')
