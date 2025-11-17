"""
SP Comprehensive Metabolic Blueprint Template
Matches the format from SP_PNOE Comprehensive Metabolic Blueprint 2025.pdf
Single-page comprehensive report with all details
"""
from datetime import datetime

class SPComprehensiveBlueprintReport:
    """Generate SP-style comprehensive metabolic blueprint reports"""

    def __init__(self):
        """Initialize with default data"""
        self.patient_info = {
            'name': 'Patient Name',
            'test_date': datetime.now().strftime('%m/%d/%Y'),
            'age': 35,
            'gender': 'Male',
            'weight_kg': 77,
            'height_cm': 188,
            'test_type': 'Performance',
            'facility': 'Optimal Vitality'
        }

        self.core_scores = {}
        self.caloric_data = {}
        self.chronological_age = None
        self.biological_age = None
        self.report_type = 'Performance'
        self.peptide_recommendations = []
        self.peptide_html = ''

    def _get_score_status(self, score):
        """Get status label and color for a score"""
        if score >= 80:
            return ('EXCELLENT', '#00cc00')
        elif score >= 60:
            return ('GOOD', '#0066cc')
        else:
            return ('NEUTRAL', '#999999')

    def _calculate_overall_score(self):
        """Calculate overall health score"""
        if not self.core_scores:
            return 0
        return round(sum(self.core_scores.values()) / len(self.core_scores))

    def _count_excellent_good_neutral(self):
        """Count metrics by category"""
        excellent = sum(1 for score in self.core_scores.values() if score >= 80)
        good = sum(1 for score in self.core_scores.values() if 60 <= score < 80)
        neutral = sum(1 for score in self.core_scores.values() if score < 60)
        return excellent, good, neutral

    def _get_styles(self):
        """Return SP Comprehensive Blueprint CSS"""
        return """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    max-width: 900px;
    margin: 0 auto;
    padding: 30px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    line-height: 1.6;
    background: #ffffff;
    color: #333;
    font-size: 14px;
}

/* HEADER */
.header {
    text-align: center;
    margin-bottom: 30px;
    padding: 25px;
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    color: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(30, 58, 138, 0.3);
}
.brand {
    font-size: 1.3em;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}
h1 {
    color: white;
    font-size: 2em;
    margin: 12px 0;
    font-weight: 700;
    letter-spacing: -0.5px;
}
.subtitle {
    margin: 8px 0 0 0;
    font-size: 0.95em;
    opacity: 0.95;
    font-weight: 300;
}

/* SECTION HEADERS */
h2 {
    color: #1e3a8a;
    font-size: 1.4em;
    margin: 30px 0 15px 0;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 10px;
}

h3 {
    color: #3b82f6;
    font-size: 1.1em;
    margin: 20px 0 10px 0;
    font-weight: 600;
}

/* PATIENT INFO */
.patient-info {
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.info-label {
    font-weight: 600;
    color: #64748b;
    font-size: 0.85em;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.info-value {
    font-size: 1.1em;
    color: #1e293b;
    font-weight: 500;
}

/* EXECUTIVE SUMMARY */
.executive-summary {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin: 25px 0;
}

.summary-card {
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.score-circle {
    width: 100px;
    height: 100px;
    margin: 0 auto 15px auto;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5em;
    font-weight: 700;
    color: #1e3a8a;
    position: relative;
}

.score-label {
    font-size: 0.9em;
    color: #64748b;
    font-weight: 600;
}

/* BIOLOGICAL AGE */
.bio-age-section {
    background: linear-gradient(135deg, #dcfce7 0%, #f0fdf4 100%);
    border: 3px solid #16a34a;
    border-radius: 12px;
    padding: 25px;
    text-align: center;
    margin: 25px 0;
}

.age-display {
    font-size: 3em;
    font-weight: 700;
    color: #15803d;
    margin: 15px 0;
    letter-spacing: -1px;
}

.age-message {
    font-size: 1.2em;
    font-weight: 600;
    color: #166534;
    margin: 10px 0;
}

/* METRICS LIST */
.metrics-list {
    margin: 20px 0;
}

.metric-item {
    display: flex;
    align-items: center;
    padding: 12px 15px;
    margin: 8px 0;
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.metric-name {
    flex: 1;
    font-weight: 600;
    color: #334155;
}

.metric-score {
    font-size: 1.3em;
    font-weight: 700;
    margin: 0 15px;
    min-width: 50px;
    text-align: center;
}

.metric-badge {
    padding: 6px 14px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.85em;
    min-width: 90px;
    text-align: center;
}

.badge-excellent {
    background: #dcfce7;
    color: #166534;
}

.badge-good {
    background: #dbeafe;
    color: #1e40af;
}

.badge-neutral {
    background: #f1f5f9;
    color: #64748b;
}

/* CALORIC DISPLAY */
.caloric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin: 20px 0;
}

.caloric-card {
    background: white;
    border: 3px solid #e2e8f0;
    border-radius: 12px;
    padding: 25px;
    text-align: center;
}

.caloric-card.burn {
    border-color: #f97316;
}

.caloric-card.eat {
    border-color: #16a34a;
}

.caloric-icon {
    font-size: 3em;
    margin-bottom: 10px;
}

.caloric-value {
    font-size: 2em;
    font-weight: 700;
    color: #1e293b;
    margin: 8px 0;
}

.caloric-label {
    font-size: 0.9em;
    color: #64748b;
    font-weight: 600;
}

/* FUEL BAR */
.fuel-bar {
    display: flex;
    height: 40px;
    border-radius: 8px;
    overflow: hidden;
    margin: 15px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.fuel-segment {
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 1.1em;
}

.fuel-fat {
    background: linear-gradient(90deg, #f97316 0%, #fb923c 100%);
}

.fuel-carb {
    background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%);
}

/* TRAINING ZONES */
.zone-card {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px 20px;
    margin: 12px 0;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    background: white;
}

.zone-icon {
    font-size: 2em;
    min-width: 50px;
    text-align: center;
}

.zone-info {
    flex: 1;
}

.zone-name {
    font-weight: 700;
    color: #1e293b;
    font-size: 1.1em;
    margin-bottom: 4px;
}

.zone-hr {
    color: #3b82f6;
    font-weight: 700;
    font-size: 1.2em;
    margin: 4px 0;
}

.zone-description {
    color: #64748b;
    font-size: 0.9em;
    margin-top: 6px;
}

.primary-badge {
    background: linear-gradient(90deg, #fbbf24 0%, #f59e0b 100%);
    color: white;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.75em;
    font-weight: 700;
    margin-left: 8px;
}

/* INTERVENTIONS */
.interventions-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin: 20px 0;
}

.intervention-card {
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.intervention-title {
    font-weight: 700;
    font-size: 1.1em;
    color: #1e293b;
    margin: 10px 0;
}

.evidence-badge {
    background: linear-gradient(90deg, #16a34a 0%, #22c55e 100%);
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.75em;
    font-weight: 700;
    display: inline-block;
    margin-top: 10px;
}

/* ACTION PLAN */
.action-plan {
    counter-reset: action-counter;
    margin: 20px 0;
}

.action-item {
    counter-increment: action-counter;
    display: flex;
    gap: 15px;
    margin: 15px 0;
    padding: 15px;
    background: white;
    border-left: 4px solid #3b82f6;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.action-number {
    background: #3b82f6;
    color: white;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.2em;
    flex-shrink: 0;
}

.action-number::before {
    content: counter(action-counter);
}

.action-content {
    flex: 1;
}

.action-title {
    font-weight: 700;
    font-size: 1.1em;
    color: #1e293b;
    margin-bottom: 8px;
}

.priority-badge {
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.75em;
    margin-left: 10px;
}

.priority-high {
    background: #fee2e2;
    color: #991b1b;
}

.priority-medium {
    background: #fed7aa;
    color: #9a3412;
}

.priority-low {
    background: #e0e7ff;
    color: #3730a3;
}

/* 90-DAY PROTOCOL */
.protocol-timeline {
    margin: 25px 0;
}

.protocol-phase {
    padding: 20px;
    margin: 15px 0;
    border: 2px solid #e2e8f0;
    border-left: 6px solid #3b82f6;
    border-radius: 8px;
    background: white;
}

.phase-title {
    font-weight: 700;
    font-size: 1.2em;
    color: #1e3a8a;
    margin-bottom: 10px;
}

.phase-retest {
    border-left-color: #16a34a;
    background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
}

/* PEPTIDE SECTION */
.peptide-section {
    background: linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%);
    border: 3px solid #f59e0b;
    border-radius: 12px;
    padding: 25px;
    margin: 30px 0;
}

.disclaimer {
    background: linear-gradient(135deg, #fef2f2 0%, #fff5f5 100%);
    border: 2px solid #f87171;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
    color: #991b1b;
    font-weight: 500;
}

/* Utilities */
.text-center { text-align: center; }
.mt-20 { margin-top: 20px; }
.mb-20 { margin-bottom: 20px; }
"""

    def generate(self):
        """Generate the complete SP Comprehensive Blueprint HTML"""

        overall_score = self._calculate_overall_score()
        excellent, good, neutral = self._count_excellent_good_neutral()

        # Calculate age difference
        age_diff = self.chronological_age - self.biological_age if (self.chronological_age and self.biological_age) else 0
        age_direction = "younger" if age_diff > 0 else ("older" if age_diff < 0 else "same as")
        age_abs_diff = abs(age_diff)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Metabolic Blueprint 2025</title>
    <style>
{self._get_styles()}
    </style>
</head>
<body>

<div class="header">
    <div class="brand">Optimal Vitality ⚡</div>
    <h1>COMPREHENSIVE METABOLIC BLUEPRINT 2025</h1>
    <p class="subtitle">Complete Performance & Longevity Analysis powered by PNOE technology</p>
</div>

<div class="patient-info">
    <h2>📋 Patient Information</h2>
    <div class="info-grid">
        <div class="info-item">
            <span class="info-label">Name</span>
            <span class="info-value">{self.patient_info.get('name', 'N/A')}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Age</span>
            <span class="info-value">{self.patient_info.get('age', 'N/A')} years</span>
        </div>
        <div class="info-item">
            <span class="info-label">Gender</span>
            <span class="info-value">{self.patient_info.get('gender', 'N/A')}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Facility</span>
            <span class="info-value">{self.patient_info.get('facility', 'Optimal Vitality')}</span>
        </div>
        <div class="info-item">
            <span class="info-label">{self.report_type} Test</span>
            <span class="info-value">{self.patient_info.get('test_date', 'N/A')}</span>
        </div>
    </div>
</div>

<h2>📊 Executive Summary</h2>
<div class="executive-summary">
    <div class="summary-card">
        <div class="score-circle" style="background: conic-gradient(#3b82f6 0deg, #3b82f6 {overall_score * 3.6}deg, #e2e8f0 {overall_score * 3.6}deg);">
            <div style="position: absolute; width: 70px; height: 70px; background: white; border-radius: 50%;"></div>
            <span style="position: relative; z-index: 1;">{overall_score}</span>
        </div>
        <div class="score-label">Overall Health Score</div>
    </div>
    <div class="summary-card">
        <div class="score-circle" style="font-size: 2em; color: #16a34a;">✓</div>
        <div class="score-label"><strong>{excellent}</strong> Excellent Metrics</div>
    </div>
    <div class="summary-card">
        <div class="score-circle" style="font-size: 2em; color: #3b82f6;">●</div>
        <div class="score-label"><strong>{good}</strong> Good Metrics</div>
    </div>
</div>
"""

        # Biological Age Section
        if self.chronological_age and self.biological_age:
            html += f"""
<div class="bio-age-section">
    <h2 style="color: #166534; border: none;">🧬 Biological Age Analysis</h2>
    <div class="age-display">{self.chronological_age} → {self.biological_age}</div>
    <div class="age-message">{"Outstanding!" if age_diff > 0 else "Good progress!"} {age_abs_diff} years {age_direction} chronological age!</div>
    <p style="color: #166534; margin-top: 15px;">Your {"excellent" if age_diff > 2 else "good"} performance metrics indicate {"superior" if age_diff > 2 else "healthy"} metabolic health and cellular function.</p>
</div>
"""

        # Core Metrics Section
        if self.core_scores:
            html += """
<h2>🔵 Performance Test Results</h2>
<div class="metrics-list">
"""
            for metric_key, score in self.core_scores.items():
                status, color = self._get_score_status(score)
                badge_class = f"badge-{status.lower()}"

                # Format metric name
                metric_names = {
                    'symp_parasym': 'Sympathetic/Parasympathetic',
                    'ventilation_eff': 'Ventilation Efficiency',
                    'breathing_coord': 'Breathing Coordination',
                    'lung_util': 'Lung Utilization',
                    'hrv': 'Heart Rate Variability (HRV)',
                    'metabolic_rate': 'Metabolic Rate',
                    'fat_burning': 'Fat-Burning Efficiency'
                }
                metric_name = metric_names.get(metric_key, metric_key.replace('_', ' ').title())

                html += f"""
    <div class="metric-item">
        <div class="metric-name">{metric_name}</div>
        <div class="metric-score" style="color: {color};">{score}%</div>
        <div class="metric-badge {badge_class}">{status}</div>
    </div>
"""
            html += "</div>\n"

        # Caloric Recommendations
        if self.caloric_data:
            burn_rest = self.caloric_data.get('burn_rest', 0)
            burn_workout = self.caloric_data.get('burn_workout', 0)
            eat_rest = self.caloric_data.get('eat_rest', 0)
            eat_workout = self.caloric_data.get('eat_workout', 0)
            fat_percent = self.caloric_data.get('fat_percent', 0)
            cho_percent = self.caloric_data.get('cho_percent', 0)

            html += f"""
<h2>🔥 Caloric Recommendations</h2>
<div class="caloric-grid">
    <div class="caloric-card burn">
        <div class="caloric-icon">🔥</div>
        <h3>YOU BURN</h3>
        <div class="caloric-value">{burn_rest:,}</div>
        <div class="caloric-label">kcal/day (Rest)</div>
        <div class="caloric-value" style="font-size: 1.5em; margin-top: 10px;">{burn_workout:,}</div>
        <div class="caloric-label">kcal/day (Workout)</div>
    </div>
    <div class="caloric-card eat">
        <div class="caloric-icon">🍽️</div>
        <h3>YOU SHOULD EAT</h3>
        <div class="caloric-value">{eat_rest:,}</div>
        <div class="caloric-label">kcal/day (Rest)</div>
        <div class="caloric-value" style="font-size: 1.5em; margin-top: 10px;">{eat_workout:,}</div>
        <div class="caloric-label">kcal/day (Workout)</div>
    </div>
</div>

<h3>⛽ Fuel Sources</h3>
<div class="fuel-bar">
    <div class="fuel-segment fuel-fat" style="width: {fat_percent}%;">Fats {fat_percent}%</div>
    <div class="fuel-segment fuel-carb" style="width: {cho_percent}%;">Carbs {cho_percent}%</div>
</div>
"""

        # Training Zones
        age = self.patient_info.get('age', 35)
        max_hr = 220 - age

        html += f"""
<h2>💓 Training Zones</h2>
<div class="zone-card">
    <div class="zone-icon">💤</div>
    <div class="zone-info">
        <div class="zone-name">Zone 1: Recovery</div>
        <div class="zone-hr">{int(max_hr * 0.50)}-{int(max_hr * 0.60)} bpm</div>
        <div class="zone-description">Active recovery, warm-up, cool-down. Very easy conversational pace.</div>
    </div>
</div>

<div class="zone-card" style="border: 3px solid #3b82f6;">
    <div class="zone-icon">🏃</div>
    <div class="zone-info">
        <div class="zone-name">Zone 2: Endurance Base <span class="primary-badge">⭐ PRIMARY ZONE</span></div>
        <div class="zone-hr">{int(max_hr * 0.60)}-{int(max_hr * 0.70)} bpm</div>
        <div class="zone-description">YOUR PRIMARY ZONE for improving metabolic rate & fat-burning. 3-4 sessions weekly, 45-60 minutes.</div>
    </div>
</div>

<div class="zone-card">
    <div class="zone-icon">🚴</div>
    <div class="zone-info">
        <div class="zone-name">Zone 3: Tempo</div>
        <div class="zone-hr">{int(max_hr * 0.70)}-{int(max_hr * 0.80)} bpm</div>
        <div class="zone-description">Moderate-hard pace, improves lactate threshold. Use sparingly.</div>
    </div>
</div>

<div class="zone-card">
    <div class="zone-icon">🏋</div>
    <div class="zone-info">
        <div class="zone-name">Zone 4: Lactate Threshold</div>
        <div class="zone-hr">{int(max_hr * 0.80)}-{int(max_hr * 0.90)} bpm</div>
        <div class="zone-description">Hard pace, 1-2 sessions weekly for strength development.</div>
    </div>
</div>

<div class="zone-card">
    <div class="zone-icon">⚡</div>
    <div class="zone-info">
        <div class="zone-name">Zone 5: VO2 Max</div>
        <div class="zone-hr">{int(max_hr * 0.90)}-{max_hr} bpm</div>
        <div class="zone-description">Maximum effort intervals only. Short bursts (30sec - 5min).</div>
    </div>
</div>

<h2>🎯 Recommended Interventions</h2>
<div class="interventions-grid">
    <div class="intervention-card">
        <div style="font-size: 3em;">🏃</div>
        <div class="intervention-title">Zone 2 Training</div>
        <p>Primary intervention for metabolic rate & fat-burning</p>
        <span class="evidence-badge">Evidence-Based</span>
    </div>
    <div class="intervention-card">
        <div style="font-size: 3em;">🏋️</div>
        <div class="intervention-title">ARX Omni</div>
        <p>Efficient resistance training for strength goals</p>
        <span class="evidence-badge">Evidence-Based</span>
    </div>
    <div class="intervention-card">
        <div style="font-size: 3em;">🧊</div>
        <div class="intervention-title">Cold Plunge</div>
        <p>Boost fat-burning 15-37%, accelerate recovery</p>
        <span class="evidence-badge">Evidence-Based</span>
    </div>
    <div class="intervention-card">
        <div style="font-size: 3em;">🥗</div>
        <div class="intervention-title">Nutrition Protocol</div>
        <p>High protein (1.6-2.2g/kg) for muscle & metabolism</p>
        <span class="evidence-badge">Evidence-Based</span>
    </div>
</div>

<h2>✅ Action Plan - Prioritized Roadmap</h2>
<div class="action-plan">
    <div class="action-item">
        <div class="action-number"></div>
        <div class="action-content">
            <div class="action-title">Zone 2 Endurance Training <span class="priority-badge priority-high">HIGH</span></div>
            <p>3-4 weekly sessions, 45-60 min at {int(max_hr * 0.60)}-{int(max_hr * 0.70)} bpm. THE most powerful intervention for improving metabolic rate and fat-burning.</p>
        </div>
    </div>
    <div class="action-item">
        <div class="action-number"></div>
        <div class="action-content">
            <div class="action-title">Strength Training <span class="priority-badge priority-high">HIGH</span></div>
            <p>Continue 3x weekly resistance work for strength development. Add compound movements to support metabolic rate increase.</p>
        </div>
    </div>
    <div class="action-item">
        <div class="action-number"></div>
        <div class="action-content">
            <div class="action-title">Performance Nutrition <span class="priority-badge priority-medium">MEDIUM</span></div>
            <p>High protein (1.6-2.2g/kg), omega-3 rich fish 3x/week. Time carbs around workouts for performance.</p>
        </div>
    </div>
    <div class="action-item">
        <div class="action-number"></div>
        <div class="action-content">
            <div class="action-title">Recovery Optimization <span class="priority-badge priority-medium">MEDIUM</span></div>
            <p>7-9 hours nightly sleep. Consistent schedule. Maintain excellent HRV through proper recovery.</p>
        </div>
    </div>
    <div class="action-item">
        <div class="action-number"></div>
        <div class="action-content">
            <div class="action-title">Cold Exposure <span class="priority-badge priority-low">LOW</span></div>
            <p>Cold plunges 3-5 min, 2-3x weekly. Can boost fat-burning by 15-37%.</p>
        </div>
    </div>
</div>

<h2>📅 90-Day Performance Protocol</h2>
<div class="protocol-timeline">
    <div class="protocol-phase">
        <div class="phase-title">WEEKS 1-4: Base Building Phase</div>
        <p>Add 2-3 Zone 2 sessions (45 min) alongside strength training. Monitor heart rate compliance. Focus on easy conversational pace. Track recovery and energy levels.</p>
    </div>
    <div class="protocol-phase">
        <div class="phase-title">WEEKS 5-8: Development Phase</div>
        <p>Increase to 3-4 Zone 2 sessions (60 min). Continue strength training 3x/week. Add cold plunges 2x/week. Implement performance nutrition timing around workouts.</p>
    </div>
    <div class="protocol-phase">
        <div class="phase-title">WEEKS 9-12: Integration Phase</div>
        <p>Maintain 4x Zone 2 sessions. Add 1x Zone 4 threshold session. Continue all protocols. Monitor performance gains in strength training. Prepare for retest.</p>
    </div>
    <div class="protocol-phase phase-retest">
        <div class="phase-title" style="color: #16a34a;">WEEK 13: Retest & Reassess</div>
        <p><strong>Expected Results:</strong> Improved metabolic rate, enhanced fat-burning efficiency, increased overall health score, strength gains with improved endurance capacity.</p>
    </div>
</div>
"""

        # Peptide Section
        if self.peptide_html:
            html += f"""
<div class="peptide-section">
    <h2 style="color: #92400e; border: none;">🤖 AI-Powered Personalized Recommendations</h2>
    <div class="disclaimer">
        <strong>Important Disclaimer:</strong> AI recommendations should be reviewed with a healthcare professional. Think of these as homework to bring to your doctor, not medical advice to follow blindly.
    </div>
    {self.peptide_html}
</div>
"""

        html += """
</body>
</html>
"""
        return html
