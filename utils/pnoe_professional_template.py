"""
PNOE Professional Metabolic Blueprint Template
Matches the professional PNOE 2025 design exactly
"""
import json
from datetime import datetime

class PNOEProfessionalReport:
    """Generate professional PNOE-style metabolic blueprint reports"""

    # Stock images for professional appearance
    HERO_IMAGE = "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=1200&fit=crop"
    TRAINING_IMAGE = "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"
    ARX_IMAGE = "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"
    COLD_PLUNGE_IMAGE = "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800"
    NUTRITION_IMAGE = "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800"
    BREATHWORK_IMAGE = "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800"
    SAUNA_IMAGE = "https://images.unsplash.com/photo-1600334089648-b0d9d3028eb2?w=800"

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

        self.core_scores = {
            'symp_parasym': 76,
            'ventilation_eff': 74,
            'breathing_coord': 67,
            'lung_util': 100,
            'hrv': 88,
            'metabolic_rate': 46,
            'fat_burning': 58
        }

        self.caloric_data = {
            'burn_rest': 1724,
            'burn_workout': 1924,
            'eat_rest': 2074,
            'eat_workout': 2274,
            'fat_percent': 53,
            'cho_percent': 47
        }

        self.chronological_age = 54
        self.biological_age = 49
        self.report_type = 'Performance'
        self.custom_notes = ''
        self.custom_goals = []

    def _get_score_status(self, score):
        """Get status label and emoji for a score"""
        if score >= 80:
            return ('EXCELLENT', '✓', '#10B981')
        elif score >= 60:
            return ('GOOD', '●', '#3B82F6')
        else:
            return ('NEUTRAL', '-', '#6B7280')

    def _count_excellent_good(self):
        """Count excellent and good+ metrics"""
        excellent = sum(1 for score in self.core_scores.values() if score >= 80)
        good_plus = sum(1 for score in self.core_scores.values() if score >= 60)
        return excellent, good_plus

    def _calculate_overall_score(self):
        """Calculate overall health score"""
        if not self.core_scores:
            return 0
        return round(sum(self.core_scores.values()) / len(self.core_scores))

    def _get_styles(self):
        """Return professional PNOE-style CSS"""
        return """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-blue: #1E40AF;
    --success-green: #10B981;
    --warning-orange: #F59E0B;
    --danger-red: #EF4444;
    --gray-50: #F9FAFB;
    --gray-100: #F3F4F6;
    --gray-200: #E5E7EB;
    --gray-300: #D1D5DB;
    --gray-600: #4B5563;
    --gray-700: #374151;
    --gray-800: #1F2937;
    --gray-900: #111827;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: var(--gray-800);
    background: white;
    font-size: 14px;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    background: white;
}

/* Header Section */
.header {
    text-align: center;
    padding: 40px 30px 20px;
    background: white;
}

.header-title {
    color: var(--gray-400);
    font-size: 18px;
    font-weight: 300;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}

.header-main {
    font-size: 32px;
    font-weight: 700;
    color: var(--gray-700);
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}

.header-subtitle {
    font-size: 13px;
    color: var(--gray-600);
    line-height: 1.5;
}

/* Patient Info Table */
.patient-info {
    margin: 30px 30px 40px;
    border: 2px solid var(--primary-blue);
    border-radius: 12px;
    overflow: hidden;
}

.patient-info-header {
    background: var(--gray-50);
    padding: 12px 20px;
    border-bottom: 2px solid var(--primary-blue);
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: var(--primary-blue);
}

.patient-info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: white;
}

.patient-info-row {
    display: contents;
}

.patient-info-cell {
    padding: 14px 20px;
    border-right: 1px solid var(--gray-200);
    border-bottom: 1px solid var(--gray-200);
}

.patient-info-cell:nth-child(2n) {
    border-right: none;
}

.patient-info-label {
    font-weight: 600;
    color: var(--gray-900);
    margin-bottom: 2px;
}

.patient-info-value {
    color: var(--gray-600);
}

/* Executive Summary */
.executive-summary {
    margin: 40px 30px;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 18px;
    font-weight: 600;
    color: var(--primary-blue);
    margin-bottom: 24px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--primary-blue);
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.summary-card {
    border: 2px solid var(--gray-200);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
}

.summary-card.green {
    border-color: var(--success-green);
}

.summary-card.blue {
    border-color: var(--primary-blue);
}

.summary-score {
    font-size: 48px;
    font-weight: 800;
    color: var(--primary-blue);
    line-height: 1;
}

.summary-score-label {
    font-size: 11px;
    color: var(--gray-600);
    margin-top: 4px;
}

.summary-label {
    font-size: 13px;
    font-weight: 600;
    color: var(--gray-800);
    margin-top: 12px;
}

.summary-check {
    font-size: 64px;
    color: var(--success-green);
    line-height: 1;
}

.summary-detail {
    font-size: 18px;
    font-weight: 700;
    color: var(--gray-800);
    margin-top: 8px;
}

.summary-subtext {
    font-size: 12px;
    color: var(--gray-600);
}

.summary-dot {
    font-size: 48px;
    color: var(--primary-blue);
    line-height: 1;
}

/* Hero Image */
.hero-image-container {
    margin: 30px 30px 40px;
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid var(--primary-blue);
}

.hero-image {
    width: 100%;
    height: 400px;
    object-fit: cover;
    display: block;
}

/* Biological Age */
.bio-age-section {
    margin: 40px 30px;
    border: 3px solid var(--success-green);
    border-radius: 12px;
    padding: 30px;
    text-align: center;
    background: var(--gray-50);
}

.bio-age-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--primary-blue);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.bio-age-display {
    font-size: 48px;
    font-weight: 800;
    color: var(--success-green);
    margin: 16px 0;
}

.bio-age-arrow {
    display: inline-block;
    margin: 0 16px;
}

.bio-age-message {
    font-size: 18px;
    font-weight: 700;
    color: var(--success-green);
    margin-top: 12px;
}

.bio-age-description {
    font-size: 13px;
    color: var(--gray-700);
    margin-top: 12px;
    line-height: 1.6;
}

/* Core Metrics */
.metrics-list {
    margin: 30px 30px 40px;
}

.metric-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 0;
    border-bottom: 1px solid var(--gray-200);
}

.metric-label {
    font-size: 14px;
    color: var(--gray-900);
    display: flex;
    align-items: center;
    gap: 8px;
}

.metric-value {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 15px;
    font-weight: 700;
}

.metric-score {
    min-width: 50px;
    text-align: right;
}

.metric-status {
    min-width: 100px;
    text-align: right;
}

/* Caloric Balance */
.caloric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin: 24px 0;
}

.caloric-card {
    border: 2px solid;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
}

.caloric-card.orange {
    border-color: var(--warning-orange);
}

.caloric-card.green {
    border-color: var(--success-green);
}

.caloric-icon {
    font-size: 40px;
    margin-bottom: 12px;
}

.caloric-title {
    font-size: 16px;
    font-weight: 700;
    color: var(--gray-900);
    margin-bottom: 12px;
}

.caloric-value {
    font-size: 14px;
    color: var(--gray-700);
    margin: 8px 0;
}

.caloric-value strong {
    font-weight: 600;
}

/* Fuel Sources */
.fuel-section {
    margin: 24px 0;
    border: 2px solid var(--primary-blue);
    border-radius: 12px;
    padding: 20px;
}

.fuel-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--gray-900);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.fuel-row {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-top: 8px;
}

.fuel-item {
    text-align: center;
}

.fuel-label {
    font-size: 13px;
    color: var(--gray-600);
    font-weight: 600;
}

/* Training Zones */
.zones-list {
    margin: 24px 0;
}

.zone-card {
    border: 2px solid;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 16px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
}

.zone-icon {
    font-size: 28px;
    flex-shrink: 0;
}

.zone-content {
    flex: 1;
}

.zone-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--gray-900);
    margin-bottom: 4px;
}

.zone-hr {
    font-size: 18px;
    font-weight: 700;
    color: var(--primary-blue);
    margin: 4px 0;
}

.zone-description {
    font-size: 13px;
    color: var(--gray-700);
    line-height: 1.5;
    margin-top: 4px;
}

.zone-badge {
    display: inline-block;
    background: var(--warning-orange);
    color: white;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 700;
    margin-left: 8px;
}

/* Weekly Training Plan */
.training-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin: 24px 0;
}

.training-card {
    border: 2px solid;
    border-radius: 12px;
    padding: 20px;
}

.training-card.red {
    border-color: var(--danger-red);
}

.training-card.orange {
    border-color: var(--warning-orange);
}

.training-card.gray {
    border-color: var(--gray-300);
}

.training-icon {
    font-size: 28px;
    margin-bottom: 8px;
}

.training-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--gray-900);
    margin-bottom: 4px;
}

.training-frequency {
    font-size: 13px;
    color: var(--gray-700);
    margin-bottom: 8px;
}

.training-priority {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 12px;
    margin-bottom: 8px;
}

.training-priority.high {
    background: var(--danger-red);
    color: white;
}

.training-priority.medium {
    background: var(--warning-orange);
    color: white;
}

.training-priority.low {
    background: var(--gray-300);
    color: var(--gray-700);
}

.training-description {
    font-size: 12px;
    color: var(--gray-700);
    line-height: 1.5;
}

/* Interventions */
.interventions-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin: 24px 0;
}

.intervention-card {
    border: 2px solid var(--primary-blue);
    border-radius: 12px;
    overflow: hidden;
}

.intervention-image {
    width: 100%;
    height: 180px;
    object-fit: cover;
}

.intervention-content {
    padding: 16px;
}

.intervention-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--gray-900);
    margin-bottom: 8px;
}

.intervention-description {
    font-size: 12px;
    color: var(--gray-700);
    line-height: 1.5;
    margin-bottom: 12px;
}

.intervention-badge {
    display: inline-block;
    font-size: 10px;
    color: var(--gray-500);
    font-weight: 600;
}

/* Action Plan */
.action-list {
    margin: 24px 0;
}

.action-item {
    display: flex;
    gap: 16px;
    padding: 20px;
    border-left: 4px solid var(--primary-blue);
    background: var(--gray-50);
    margin-bottom: 12px;
    border-radius: 8px;
}

.action-number {
    font-size: 20px;
    font-weight: 800;
    color: var(--primary-blue);
    min-width: 30px;
}

.action-content {
    flex: 1;
}

.action-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--gray-900);
    margin-bottom: 4px;
}

.action-priority {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 8px;
    margin-left: 8px;
}

.action-priority.high {
    background: var(--danger-red);
    color: white;
}

.action-priority.medium {
    background: var(--warning-orange);
    color: white;
}

.action-priority.low {
    background: var(--gray-300);
    color: var(--gray-700);
}

.action-description {
    font-size: 13px;
    color: var(--gray-700);
    line-height: 1.6;
    margin-top: 4px;
}

/* 90-Day Protocol */
.protocol-list {
    margin: 24px 0;
}

.protocol-phase {
    border: 2px solid var(--primary-blue);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}

.protocol-phase.final {
    border-color: var(--success-green);
    background: var(--gray-50);
}

.protocol-header {
    font-size: 15px;
    font-weight: 700;
    color: var(--primary-blue);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.protocol-description {
    font-size: 13px;
    color: var(--gray-700);
    line-height: 1.6;
}

.protocol-results {
    font-size: 14px;
    font-weight: 600;
    color: var(--success-green);
    margin-top: 8px;
}

/* AI Disclaimer */
.disclaimer-box {
    background: #FEF3C7;
    border: 2px solid var(--warning-orange);
    border-radius: 12px;
    padding: 20px;
    margin: 30px 30px;
}

.disclaimer-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    font-weight: 700;
    color: #92400E;
    margin-bottom: 12px;
}

.disclaimer-text {
    font-size: 12px;
    color: #78350F;
    line-height: 1.6;
}

/* Peptides Section */
.peptides-section {
    margin: 30px;
    border: 2px solid var(--danger-red);
    border-radius: 12px;
    padding: 24px;
}

.peptides-header {
    font-size: 16px;
    font-weight: 700;
    color: var(--danger-red);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.peptides-disclaimer {
    background: #FEF2F2;
    border: 1px solid var(--danger-red);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 20px;
}

.peptides-disclaimer-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 700;
    color: var(--danger-red);
    margin-bottom: 8px;
}

.peptides-disclaimer-text {
    font-size: 11px;
    color: #991B1B;
    line-height: 1.5;
}

.peptides-content h3 {
    font-size: 14px;
    font-weight: 700;
    color: var(--gray-900);
    margin: 20px 0 12px;
}

.peptides-content h4 {
    font-size: 13px;
    font-weight: 700;
    color: var(--danger-red);
    margin: 16px 0 8px;
}

.peptides-content p {
    font-size: 12px;
    color: var(--gray-700);
    line-height: 1.6;
    margin-bottom: 12px;
}

.peptides-content ul {
    margin-left: 20px;
    margin-bottom: 12px;
}

.peptides-content li {
    font-size: 12px;
    color: var(--gray-700);
    line-height: 1.6;
    margin-bottom: 6px;
}

.peptides-warning {
    background: var(--danger-red);
    color: white;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
    margin-top: 20px;
    font-size: 13px;
    font-weight: 700;
}

/* Utility Classes */
.text-center {
    text-align: center;
}

.mt-20 {
    margin-top: 20px;
}

.mb-20 {
    margin-bottom: 20px;
}

.p-30 {
    padding: 30px;
}

/* Print Styles */
@media print {
    body {
        print-color-adjust: exact;
        -webkit-print-color-adjust: exact;
    }
}
"""

    def _generate_header(self):
        """Generate header section"""
        return f"""
<div class="header">
    <div class="header-title">Optimal Vitality ⚡</div>
    <div class="header-main">PERFORMANCE METABOLIC BLUEPRINT 2025</div>
    <div class="header-subtitle">Comprehensive metabolic testing, training zones, and performance optimization powered by PNOE technology</div>
</div>
"""

    def _generate_patient_info(self):
        """Generate patient information table"""
        weight_lbs = round(self.patient_info['weight_kg'] * 2.20462, 1)
        height_ft = self.patient_info['height_cm'] // 30.48
        height_in = round((self.patient_info['height_cm'] % 30.48) / 2.54)

        return f"""
<div class="patient-info">
    <div class="patient-info-header">
        📋 Patient Information
    </div>
    <div class="patient-info-grid">
        <div class="patient-info-cell">
            <div class="patient-info-label">Name</div>
            <div class="patient-info-value">{self.patient_info['name']}</div>
        </div>
        <div class="patient-info-cell">
            <div class="patient-info-label">Test Date</div>
            <div class="patient-info-value">{self.patient_info['test_date']}</div>
        </div>
        <div class="patient-info-cell">
            <div class="patient-info-label">Age</div>
            <div class="patient-info-value">{self.patient_info['age']} years</div>
        </div>
        <div class="patient-info-cell">
            <div class="patient-info-label">Gender</div>
            <div class="patient-info-value">{self.patient_info['gender']}</div>
        </div>
        <div class="patient-info-cell">
            <div class="patient-info-label">Weight</div>
            <div class="patient-info-value">{weight_lbs} lbs ({self.patient_info['weight_kg']} kg)</div>
        </div>
        <div class="patient-info-cell">
            <div class="patient-info-label">Height</div>
            <div class="patient-info-value">{height_ft}'{height_in}" ({self.patient_info['height_cm']} cm)</div>
        </div>
        <div class="patient-info-cell">
            <div class="patient-info-label">Test Type</div>
            <div class="patient-info-value">{self.patient_info.get('test_type', 'Performance')}</div>
        </div>
        <div class="patient-info-cell">
            <div class="patient-info-label">Facility</div>
            <div class="patient-info-value">{self.patient_info.get('facility', 'Optimal Vitality')}</div>
        </div>
    </div>
</div>
"""

    def _generate_executive_summary(self):
        """Generate executive summary with score cards"""
        overall_score = self._calculate_overall_score()
        excellent, good_plus = self._count_excellent_good()

        return f"""
<div class="executive-summary">
    <div class="section-title">📊 Executive Summary</div>
    <div class="summary-grid">
        <div class="summary-card">
            <div class="summary-score">{overall_score}</div>
            <div class="summary-score-label">/100</div>
            <div class="summary-label">Overall Health Score</div>
        </div>
        <div class="summary-card green">
            <div class="summary-check">✓</div>
            <div class="summary-detail">{excellent} of {len(self.core_scores)}</div>
            <div class="summary-subtext">Excellent Metrics</div>
        </div>
        <div class="summary-card blue">
            <div class="summary-dot">●</div>
            <div class="summary-detail">{good_plus} of {len(self.core_scores)}</div>
            <div class="summary-subtext">Good+ Metrics</div>
        </div>
    </div>
</div>
"""

    def _generate_hero_image(self):
        """Generate hero image section"""
        return f"""
<div class="hero-image-container">
    <img src="{self.HERO_IMAGE}" alt="Performance Training" class="hero-image">
</div>
"""

    def _generate_biological_age(self):
        """Generate biological age analysis"""
        age_diff = self.chronological_age - self.biological_age

        if age_diff > 0:
            message = f"Outstanding! {age_diff} years younger than chronological age!"
        elif age_diff < 0:
            message = f"Your biological age is {abs(age_diff)} years older than chronological age."
        else:
            message = "Your biological age matches your chronological age."

        description = "Your excellent performance metrics indicate superior metabolic health and cellular function."

        return f"""
<div class="bio-age-section">
    <div class="bio-age-title">🧬 Biological Age Analysis</div>
    <div class="bio-age-display">
        {self.chronological_age} <span class="bio-age-arrow">→</span> {self.biological_age}
    </div>
    <div class="bio-age-message">{message}</div>
    <div class="bio-age-description">{description}</div>
</div>
"""

    def _generate_core_metrics(self):
        """Generate core performance metrics list"""
        labels = {
            'symp_parasym': 'Sympathetic/Parasympathetic',
            'ventilation_eff': 'Ventilation Efficiency',
            'breathing_coord': 'Breathing Coordination',
            'lung_util': 'Lung Utilization',
            'hrv': 'Heart Rate Variability (HRV)',
            'metabolic_rate': 'Metabolic Rate',
            'fat_burning': 'Fat-Burning Efficiency'
        }

        html = """
<div class="metrics-list">
    <div class="section-title">📈 Core Performance Metrics</div>
"""

        for key, score in self.core_scores.items():
            label = labels.get(key, key.replace('_', ' ').title())
            status, emoji, color = self._get_score_status(score)

            html += f"""
    <div class="metric-item">
        <div class="metric-label">
            <span>{emoji}</span>
            <span>{label}</span>
        </div>
        <div class="metric-value">
            <span class="metric-score">{score}%</span>
            <span class="metric-status" style="color: {color};">{status}</span>
        </div>
    </div>
"""

        html += "</div>\n"
        return html

    def _generate_caloric_balance(self):
        """Generate caloric balance and fuel strategy"""
        return f"""
<div class="executive-summary">
    <div class="section-title">🔥 Caloric Balance & Fuel Strategy</div>
    <div class="caloric-grid">
        <div class="caloric-card orange">
            <div class="caloric-icon">🔥</div>
            <div class="caloric-title">YOU BURN</div>
            <div class="caloric-value"><strong>Rest Days:</strong> {self.caloric_data['burn_rest']:,} kcal/day</div>
            <div class="caloric-value"><strong>Workout Days:</strong> {self.caloric_data['burn_workout']:,} kcal/day</div>
        </div>
        <div class="caloric-card green">
            <div class="caloric-icon">🍽</div>
            <div class="caloric-title">YOU SHOULD EAT</div>
            <div class="caloric-value"><strong>Rest Days:</strong> {self.caloric_data['eat_rest']:,} kcal/day</div>
            <div class="caloric-value"><strong>Workout Days:</strong> {self.caloric_data['eat_workout']:,} kcal/day</div>
        </div>
    </div>
    <div class="fuel-section">
        <div class="fuel-title">⛽ Fuel Sources at Rest</div>
        <div class="fuel-row">
            <div class="fuel-item">
                <div class="fuel-label">Fats {self.caloric_data['fat_percent']}%</div>
            </div>
            <div class="fuel-item">
                <div class="fuel-label">Carbs {self.caloric_data['cho_percent']}%</div>
            </div>
        </div>
    </div>
</div>
"""

    def _generate_training_zones(self):
        """Generate training zones"""
        max_hr = 220 - self.chronological_age

        zones = [
            {'icon': '💤', 'name': 'Zone 1: Recovery', 'hr_min': int(max_hr * 0.5), 'hr_max': int(max_hr * 0.6),
             'desc': 'Active recovery, warm-up, cool-down. Very easy conversational pace.', 'color': 'var(--gray-300)', 'badge': ''},
            {'icon': '🏃', 'name': 'Zone 2: Endurance Base', 'hr_min': int(max_hr * 0.6), 'hr_max': int(max_hr * 0.7),
             'desc': 'THE most important zone for improving metabolic rate and fat-burning. 3-4 sessions weekly, 45-60 minutes.', 'color': 'var(--primary-blue)', 'badge': '⭐ PRIMARY ZONE'},
            {'icon': '🚴', 'name': 'Zone 3: Tempo', 'hr_min': int(max_hr * 0.7), 'hr_max': int(max_hr * 0.8),
             'desc': 'Moderate-hard pace, improves lactate threshold. Use sparingly.', 'color': 'var(--warning-orange)', 'badge': ''},
            {'icon': '🏋', 'name': 'Zone 4: Lactate Threshold', 'hr_min': int(max_hr * 0.8), 'hr_max': int(max_hr * 0.9),
             'desc': 'Hard pace, 1-2 sessions weekly for strength development.', 'color': 'var(--warning-orange)', 'badge': ''},
            {'icon': '⚡', 'name': 'Zone 5: VO2 Max', 'hr_min': int(max_hr * 0.9), 'hr_max': max_hr,
             'desc': 'Maximum effort intervals only. Short bursts (30sec - 5min).', 'color': 'var(--danger-red)', 'badge': ''}
        ]

        html = """
<div class="executive-summary">
    <div class="section-title">💓 Training Zones</div>
    <div class="zones-list">
"""

        for zone in zones:
            badge_html = f'<span class="zone-badge">{zone["badge"]}</span>' if zone['badge'] else ''
            html += f"""
        <div class="zone-card" style="border-color: {zone['color']};">
            <div class="zone-icon">{zone['icon']}</div>
            <div class="zone-content">
                <div class="zone-title">{zone['name']}{badge_html}</div>
                <div class="zone-hr">{zone['hr_min']}-{zone['hr_max']} bpm</div>
                <div class="zone-description">{zone['desc']}</div>
            </div>
        </div>
"""

        html += """
    </div>
</div>
"""
        return html

    def _generate_weekly_training_plan(self):
        """Generate weekly training plan"""
        return """
<div class="executive-summary">
    <div class="section-title">📅 Weekly Training Plan</div>
    <div class="training-grid">
        <div class="training-card red">
            <div class="training-icon">🏃</div>
            <div class="training-title">Zone 2 Endurance</div>
            <div class="training-frequency">3-4 sessions × 45-60 min</div>
            <div class="training-priority high">PRIORITY #1</div>
            <div class="training-description">Improve metabolic rate and fat-burning</div>
        </div>
        <div class="training-card">
            <div class="training-icon">💪</div>
            <div class="training-title">Resistance Training</div>
            <div class="training-frequency">3 sessions × 45-60 min</div>
            <div class="training-priority high">HIGH</div>
            <div class="training-description">Maintain strength development focus</div>
        </div>
        <div class="training-card orange">
            <div class="training-icon">🏋</div>
            <div class="training-title">Zone 4 Threshold</div>
            <div class="training-frequency">1-2 sessions × 20-30 min</div>
            <div class="training-priority medium">MEDIUM</div>
            <div class="training-description">Support strength development goals</div>
        </div>
        <div class="training-card gray">
            <div class="training-icon">😴</div>
            <div class="training-title">Rest/Recovery</div>
            <div class="training-frequency">1-2 days per week</div>
            <div class="training-priority low">LOW</div>
            <div class="training-description">Zone 1 activity</div>
        </div>
    </div>
</div>
"""

    def _generate_interventions(self):
        """Generate recommended interventions"""
        return f"""
<div class="executive-summary">
    <div class="section-title">🎯 Recommended Interventions</div>
    <div class="text-center mb-20" style="font-style: italic; color: var(--gray-600); font-size: 13px;">
        Targeted strategies for your specific needs
    </div>
    <div class="interventions-grid">
        <div class="intervention-card">
            <div class="intervention-content">
                <div class="intervention-icon" style="font-size: 40px; text-align: center; margin-bottom: 12px;">🏃</div>
                <div class="intervention-title">Zone 2 Training</div>
                <div class="intervention-description">Primary intervention for metabolic rate & fat-burning</div>
                <div class="intervention-badge">Evidence-Based</div>
            </div>
        </div>
        <div class="intervention-card">
            <img src="{self.ARX_IMAGE}" alt="ARX Training" class="intervention-image">
            <div class="intervention-content">
                <div class="intervention-title">ARX Omni</div>
                <div class="intervention-description">Efficient resistance training for strength goals</div>
                <div class="intervention-badge">Evidence-Based</div>
            </div>
        </div>
        <div class="intervention-card">
            <img src="{self.COLD_PLUNGE_IMAGE}" alt="Cold Plunge" class="intervention-image">
            <div class="intervention-content">
                <div class="intervention-title">Cold Plunge</div>
                <div class="intervention-description">Boost fat-burning 15-37%, accelerate recovery</div>
                <div class="intervention-badge">Evidence-Based</div>
            </div>
        </div>
        <div class="intervention-card">
            <img src="{self.NUTRITION_IMAGE}" alt="Nutrition" class="intervention-image">
            <div class="intervention-content">
                <div class="intervention-title">Nutrition Protocol</div>
                <div class="intervention-description">High protein (1.6-2.2g/kg) for muscle & metabolism</div>
                <div class="intervention-badge">Evidence-Based</div>
            </div>
        </div>
        <div class="intervention-card">
            <img src="{self.BREATHWORK_IMAGE}" alt="Breathwork" class="intervention-image">
            <div class="intervention-content">
                <div class="intervention-title">Breathwork Training</div>
                <div class="intervention-description">Optimize breathing coordination (currently {self.core_scores.get('breathing_coord', 67)}%)</div>
                <div class="intervention-badge">Evidence-Based</div>
            </div>
        </div>
        <div class="intervention-card">
            <div class="intervention-content">
                <div class="intervention-icon" style="font-size: 40px; text-align: center; margin-bottom: 12px;">♨️</div>
                <div class="intervention-title">Sauna Recovery</div>
                <div class="intervention-description">Improve HRV and parasympathetic activation</div>
                <div class="intervention-badge">Evidence-Based</div>
            </div>
        </div>
    </div>
</div>
"""

    def _generate_action_plan(self):
        """Generate prioritized action plan"""
        return """
<div class="executive-summary">
    <div class="section-title">✅ Action Plan - Prioritized Roadmap</div>
    <div class="action-list">
        <div class="action-item">
            <div class="action-number">1</div>
            <div class="action-content">
                <div class="action-title">Zone 2 Endurance Training<span class="action-priority high">HIGH</span></div>
                <div class="action-description">3-4 sessions, 45-60 min at appropriate heart rate. Most powerful intervention for improving metabolic rate and fat-burning.</div>
            </div>
        </div>
        <div class="action-item">
            <div class="action-number">2</div>
            <div class="action-content">
                <div class="action-title">Strength Training<span class="action-priority high">HIGH</span></div>
                <div class="action-description">Continue 3x weekly resistance work for strength development. Add compound movements to support metabolic rate increase.</div>
            </div>
        </div>
        <div class="action-item">
            <div class="action-number">3</div>
            <div class="action-content">
                <div class="action-title">Performance Nutrition<span class="action-priority medium">MEDIUM</span></div>
                <div class="action-description">High protein intake, omega-3 rich fish 3x/week. Time carbs around workouts for performance.</div>
            </div>
        </div>
        <div class="action-item">
            <div class="action-number">4</div>
            <div class="action-content">
                <div class="action-title">Recovery Optimization<span class="action-priority medium">MEDIUM</span></div>
                <div class="action-description">7-9 hours nightly sleep. Consistent schedule. Maintain excellent HRV through proper recovery.</div>
            </div>
        </div>
        <div class="action-item">
            <div class="action-number">5</div>
            <div class="action-content">
                <div class="action-title">Cold Exposure<span class="action-priority low">LOW</span></div>
                <div class="action-description">Cold plunges 3-5 min, 2-3x weekly. Can boost fat-burning by 15-37%.</div>
            </div>
        </div>
        <div class="action-item">
            <div class="action-number">6</div>
            <div class="action-content">
                <div class="action-title">Breathwork Practice<span class="action-priority low">LOW</span></div>
                <div class="action-description">10 min daily box breathing to optimize breathing coordination.</div>
            </div>
        </div>
    </div>
</div>
"""

    def _generate_90day_protocol(self):
        """Generate 90-day performance protocol"""
        return """
<div class="executive-summary">
    <div class="section-title">📅 90-Day Performance Protocol</div>
    <div class="protocol-list">
        <div class="protocol-phase">
            <div class="protocol-header">⭕ Weeks 1-4: Base Building Phase</div>
            <div class="protocol-description">Add 2-3 Zone 2 sessions (45 min) alongside strength training. Monitor heart rate compliance. Focus on easy conversational pace.</div>
        </div>
        <div class="protocol-phase">
            <div class="protocol-header">⭕ Weeks 5-8: Development Phase</div>
            <div class="protocol-description">Increase to 3-4 Zone 2 sessions (60 min). Continue strength training 3x/week. Add cold plunges 2x/week. Implement performance nutrition timing.</div>
        </div>
        <div class="protocol-phase">
            <div class="protocol-header">⭕ Weeks 9-12: Integration Phase</div>
            <div class="protocol-description">Maintain 4x Zone 2 sessions. Add 1x Zone 4 threshold session. Continue all protocols. Monitor performance gains in strength training.</div>
        </div>
        <div class="protocol-phase final">
            <div class="protocol-header" style="color: var(--success-green);">⭕ Week 13: Retest & Reassess</div>
            <div class="protocol-results">Expected Results: Metabolic Rate: 46% → 70%+ | Fat-Burning: 58% → 75%+ | Overall Score: 73% → 80%+ | Strength gains + improved endurance capacity</div>
        </div>
    </div>
</div>
"""

    def generate(self, output_path):
        """Generate the complete report"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PNOE Performance Metabolic Blueprint 2025</title>
    <style>
{self._get_styles()}
    </style>
</head>
<body>
    <div class="container">
{self._generate_header()}
{self._generate_patient_info()}
{self._generate_executive_summary()}
{self._generate_hero_image()}
{self._generate_biological_age()}
{self._generate_core_metrics()}
{self._generate_caloric_balance()}
{self._generate_training_zones()}
{self._generate_weekly_training_plan()}
{self._generate_interventions()}
{self._generate_action_plan()}
{self._generate_90day_protocol()}
    </div>
</body>
</html>
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
