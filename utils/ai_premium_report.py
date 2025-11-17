"""
AI Premium Report Generator
Creates comprehensive 30+ page metabolic reports
Based on Frank Shallenberger's premium report structure
"""
from datetime import datetime
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))
from calculate_scores import enhance_extracted_data_with_calculated_scores, calculate_biological_age
from peptide_recommendations import calculate_peptide_recommendations, format_peptide_recommendations_html

class AIPremiumReportTemplate:
    """Premium metabolic report template - 30+ pages comprehensive"""

    def __init__(self):
        self.patient_info = {
            'name': 'Patient Name',
            'test_date': datetime.now().strftime('%m/%d/%Y'),
            'test_type': 'Longevity',
            'provider_email': 'provider@clinic.com',
            'age': None,
            'gender': None,
            'weight_kg': None,
            'height_cm': None
        }

        self.chronological_age = None
        self.biological_age = None

        self.core_scores = {}
        self.caloric_data = {}
        self.metabolic_data = {}

    def get_score_rating(self, score):
        """Convert score to rating text"""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Neutral"
        elif score >= 20:
            return "Limitation"
        else:
            return "Severe limitation"

    def get_score_bar_html(self, score, label):
        """Generate score bar visualization"""
        rating = self.get_score_rating(score)

        # Determine color based on score
        if score >= 80:
            color = "#10b981"  # Green
        elif score >= 60:
            color = "#3b82f6"  # Blue
        elif score >= 40:
            color = "#f59e0b"  # Orange
        elif score >= 20:
            color = "#ef4444"  # Red
        else:
            color = "#991b1b"  # Dark red

        return f"""
        <div class="score-bar-container">
            <div class="score-label">{label} - {score}% | {rating}</div>
            <div class="score-track">
                <div class="score-markers">
                    <span>0%</span>
                    <span>20%</span>
                    <span>40%</span>
                    <span>60%</span>
                    <span>80%</span>
                    <span>100%</span>
                </div>
                <div class="score-fill" style="width: {score}%; background: {color};"></div>
            </div>
            <div class="score-zones">
                <span class="zone severe">Severe limitation</span>
                <span class="zone limitation">Limitation</span>
                <span class="zone neutral">Neutral</span>
                <span class="zone good">Good</span>
                <span class="zone excellent">Excellent</span>
            </div>
        </div>
        """

    def generate_cover_page(self):
        """Generate cover page"""
        return f"""
        <div class="cover-page">
            <h1 class="cover-title">Metabolic Blueprint & Nutrition Analysis</h1>
            <h2 class="cover-subtitle">{self.patient_info['test_type']}</h2>
            <h3 class="cover-patient">{self.patient_info['name']}</h3>
            <div class="cover-details">
                <div class="detail-row">
                    <span class="detail-label">Test Type:</span>
                    <span class="detail-value">Resting</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Optimal Vitality</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Test Date:</span>
                    <span class="detail-value">{self.patient_info['test_date']}</span>
                    <span class="detail-provider">{self.patient_info['provider_email']}</span>
                </div>
            </div>
        </div>
        """

    def generate_disclaimer_page(self):
        """Generate disclaimer page"""
        return """
        <div class="disclaimer-page">
            <h2>Disclaimer</h2>
            <p>The present Assessment/Report is intended for information purposes only and under no circumstances should it be considered a substitute for professional medical advice, diagnosis or treatment. You need to consult your physician and/or family doctor prior to engaging in any exercise program and/or changing your diet and/or habits as a result of the information provided by the present Assessment/Report.</p>

            <p>Company makes no representation that the present Assessment/Report will result in any improvement of your health and fitness status. You agree that participating in any workout regimen, physical exercise or activity may result in an increased risk of physical injury based on the nature, frequency, intensity and duration of the workout regimen, physical exercise or activity.</p>

            <p>You agree that if you participate in any workout regimen, physical exercise or activity, you do so at your own risk and you assume the risk of any and all injury and/or damage you may suffer.</p>
        </div>
        """

    def generate_pillars_page(self):
        """Generate Pillars of Longevity page"""
        return """
        <div class="pillars-page">
            <h1>Pillars of Longevity</h1>
            <div class="pillars-grid">
                <div class="pillar">
                    <h3>Mental status</h3>
                    <p>Mental status is a fundamental pillar of wellness since a healthy mind is a prerequisite for healthy choices and a healthy lifestyle. A well-functioning brain is tightly linked to effective breathing since our breath drives our brain's chemistry balance. On the contrary, poor breathing is linked to anxiety and lower cognitive capacity.</p>
                </div>
                <div class="pillar">
                    <h3>Heart fitness</h3>
                    <p>A healthy heart is critical for overall wellness since cardiovascular dysfunction is the second most likely cause of mortality and one of the most common threats to the quality of life. A healthy heart is effective in pumping oxygen-rich blood into your body.</p>
                </div>
                <div class="pillar">
                    <h3>Lung fitness</h3>
                    <p>High lung fitness is critical for a long and healthy life as lung dysfunction has become one of the most common causes of mortality. Healthy lungs are effective in transferring oxygen from their surface into the bloodstream.</p>
                </div>
                <div class="pillar">
                    <h3>Posture</h3>
                    <p>Lower back pain and musculoskeletal problems are the number one driver of lower quality of life since they are a source of chronic pain and physical inactivity. Good posture is inextricably related to our breath since the way we inhale is one of the most potent regulators of our core's stability.</p>
                </div>
                <div class="pillar">
                    <h3>Cellular performance</h3>
                    <p>Cellular performance is a fundamental driver of wellness as it provides one of the most potent shields against metabolic dysfunction and obesity. Healthy cells absorb oxygen efficiently, a prerequisite for burning fat and maintaining a high metabolism.</p>
                </div>
            </div>
        </div>
        """

    def generate_overview_dashboard(self):
        """Generate overview dashboard with all scores"""
        scores = self.core_scores

        # Count scores by category
        severe = sum(1 for s in scores.values() if s < 20)
        limitation = sum(1 for s in scores.values() if 20 <= s < 40)
        neutral = sum(1 for s in scores.values() if 40 <= s < 60)
        good = sum(1 for s in scores.values() if 60 <= s < 80)
        excellent = sum(1 for s in scores.values() if s >= 80)

        return f"""
        <div class="overview-page">
            <h1>Overview</h1>
            <div class="overview-summary">
                <div class="summary-count severe">{severe}</div>
                <div class="summary-count limitation">{limitation}</div>
                <div class="summary-count neutral">{neutral}</div>
                <div class="summary-count good">{good}</div>
                <div class="summary-count excellent">{excellent}</div>
                <div class="summary-label">Core Limitations</div>
            </div>
            <div class="overview-legend">
                <span class="legend-item severe">Severe limitation</span>
                <span class="legend-item limitation">Limitation</span>
                <span class="legend-item neutral">Neutral</span>
                <span class="legend-item good">Good</span>
                <span class="legend-item excellent">Excellent</span>
            </div>
            <div class="overview-scores">
                {self._generate_all_score_bars()}
            </div>
        </div>
        """

    def _generate_all_score_bars(self):
        """Generate all score bars for overview"""
        scores = self.core_scores
        html = ""

        score_labels = {
            'symp_parasym': 'Sympathetic/Parasympathetic activation',
            'breathing_coord': 'Breathing Coordination',
            'ventilation_eff': 'Ventilation efficiency',
            'lung_util': 'Lung utilization',
            'hrv': 'Heart Rate Variability (HRV)',
            'metabolic_rate': 'Metabolic rate',
            'fat_burning': 'Fat-burning Efficiency & Mitochondrial Function'
        }

        for key, label in score_labels.items():
            if key in scores:
                html += self.get_score_bar_html(scores[key], label)

        return html

    def generate_core_metrics_intro(self):
        """Generate core metrics introduction page"""
        return """
        <div class="metrics-intro-page">
            <h1>Core Metrics</h1>
            <p class="intro-text">The following metrics are the most important for longevity. Achieving a high score maximizes the likelihood of maintaining a good quality of life.</p>
        </div>
        """

    def generate_metric_page(self, metric_name, score, what_it_shows, why_important, how_to_improve=None):
        """Generate a full page for a single metric"""
        rating = self.get_score_rating(score)

        html = f"""
        <div class="metric-page">
            <h1>{metric_name} - {score}% | {rating}</h1>
            {self.get_score_bar_html(score, metric_name)}

            <div class="metric-section">
                <h2>What it shows</h2>
                <p>{what_it_shows}</p>
            </div>

            <div class="metric-section">
                <h2>Why it's important to track</h2>
                <p>{why_important}</p>
            </div>
        """

        if how_to_improve:
            html += f"""
            <div class="metric-section">
                <h2>How to improve it</h2>
                <p>{how_to_improve}</p>
            </div>
            """

        html += "</div>"
        return html

    def generate_all_metric_pages(self):
        """Generate all metric detail pages"""
        scores = self.core_scores
        pages = []

        # Breathing Coordination
        if 'breathing_coord' in scores:
            pages.append(self.generate_metric_page(
                "Breathing Coordination",
                scores['breathing_coord'],
                "Breathing coordination shows your ability to maintain regular and efficient breathing during resting states and is a measure of how efficiently you can coordinate your respiratory muscles and diaphragm.",
                "Breathing coordination is important to track as it can regulate your nervous system activation and oxygenation levels across the entire body. How fast and deep you breathe can profoundly regulate the activation of your sympathetic and parasympathetic nervous systems.",
                "Meditation and breathwork are one of the most powerful tools for improving breathing for better brain function and reduced stress."
            ))

        # Sympathetic/Parasympathetic
        if 'symp_parasym' in scores:
            pages.append(self.generate_metric_page(
                "Sympathetic/Parasympathetic activation",
                scores['symp_parasym'],
                "Sympathetic & Parasympathetic activation shows the balance between the two main parts of the autonomic nervous system and, specifically, which one of the two is more activated.",
                "Tracking the balance between your sympathetic and parasympathetic activation is important because it indicates the level of psychosomatic stress your body has accumulated. High parasympathetic activation indicates sufficient recovery and stress management."
            ))

        # Ventilation Efficiency
        if 'ventilation_eff' in scores:
            pages.append(self.generate_metric_page(
                "Ventilation efficiency",
                scores['ventilation_eff'],
                "Ventilation efficiency indicates your lungs' ability to absorb oxygen and clear carbon dioxide. It is calculated by the ratio of the total amount of air exchange between your lungs and the environment (VE) over the exhaled carbon dioxide volume (VCO2).",
                "Ventilation efficiency is important to track, especially in individuals who cannot perform cardiopulmonary exercise testing. It provides insights into pulmonary function and gas exchange efficiency."
            ))

        # Lung Utilization
        if 'lung_util' in scores:
            pages.append(self.generate_metric_page(
                "Lung utilization",
                scores['lung_util'],
                "Lung utilization indicates how much of your lungs you use in a resting state. It is measured by evaluating your tidal volume, which is the amount of air you exhale during every breathing cycle.",
                "Lung utilization is important to track as it's a measure of your body's ability to absorb oxygen and a major contributor to a high VO2max. The more of your lungs you use, the more oxygen you can absorb and deliver across your body."
            ))

        # HRV
        if 'hrv' in scores:
            pages.append(self.generate_metric_page(
                "Heart Rate Variability (HRV)",
                scores['hrv'],
                "HRV shows your cardiovascular system function in resting conditions. It's scored based on the heart frequency ratio, which, based on its values, can be indicative of heart-related conditions, such as heart failure and arrhythmias.",
                "HRV is important to track because it reflects the function of your heart in terms of its rhythm and can demonstrate heart rhythm-related conditions such as atrial fibrillation. A high HRV equals a lower risk for such issues, while a low HRV may indicate cardiovascular stress."
            ))

        # Metabolic Rate
        if 'metabolic_rate' in scores:
            pages.append(self.generate_metric_page(
                "Metabolic rate",
                scores['metabolic_rate'],
                "Metabolic Rate shows how fast or slow your metabolism is. In other words, it shows whether your body is burning greater or fewer calories than predicted based on your weight, gender, age, and height during regular movements. The more the number of calories burned, the higher the metabolic rate score.",
                "Metabolic rate is important to track as it indicates your predisposition for weight loss or weight gain. A high metabolic rate means your body burns more calories at rest, making weight management easier."
            ))

        # Fat Burning
        if 'fat_burning' in scores:
            pages.append(self.generate_metric_page(
                "Fat-burning Efficiency & Mitochondrial Function",
                scores['fat_burning'],
                "Fat-burning Efficiency shows your cells' ability to use fat as a fuel source and is a hallmark of mitochondrial and cellular function. Our cells use a mix of fats and carbohydrates as fuel to release the energy they need to support vital functions. This is measured by analyzing the balance of carbon dioxide and oxygen in your breath. High reliance on fat as a fuel source is an indication of good mitochondrial and metabolic function.",
                "Fat-burning efficiency is important to track because it indicates metabolic flexibility and mitochondrial health. Better fat-burning capacity means improved energy levels and metabolic health."
            ))

        return "\n".join(pages)

    def generate_caloric_balance_page(self):
        """Generate caloric balance page"""
        cal_data = self.caloric_data

        burn_rest = cal_data.get('burn_rest', 2000)
        burn_workout = cal_data.get('burn_workout', 2500)
        eat_rest = cal_data.get('eat_rest', burn_rest)
        eat_workout = cal_data.get('eat_workout', burn_workout)
        fat_pct = cal_data.get('fat_percent', 35)
        cho_pct = cal_data.get('cho_percent', 65)

        return f"""
        <div class="caloric-page">
            <h1>Caloric Balance</h1>
            <div class="caloric-grid">
                <div class="caloric-box">
                    <h3>You Burn</h3>
                    <div class="cal-section">
                        <p class="cal-label">During days you don't work out</p>
                        <p class="cal-value">{burn_rest} kcal/day</p>
                    </div>
                    <div class="cal-section">
                        <p class="cal-label">During days you work out</p>
                        <p class="cal-value">{burn_workout} kcal/day</p>
                    </div>
                </div>
                <div class="caloric-box">
                    <h3>You should eat</h3>
                    <div class="cal-section">
                        <p class="cal-label">During days you don't work out</p>
                        <p class="cal-value">{eat_rest} kcal/day</p>
                    </div>
                    <div class="cal-section">
                        <p class="cal-label">During days you work out</p>
                        <p class="cal-value">{eat_workout} kcal/day</p>
                    </div>
                </div>
            </div>
            <div class="fuel-sources">
                <h2>Fuel Sources</h2>
                <div class="fuel-bars">
                    <div class="fuel-bar">
                        <div class="fuel-label">Fats</div>
                        <div class="fuel-track">
                            <div class="fuel-fill" style="width: {fat_pct}%; background: #10b981;"></div>
                        </div>
                        <div class="fuel-percent">{fat_pct}%</div>
                    </div>
                    <div class="fuel-bar">
                        <div class="fuel-label">Carbohydrates</div>
                        <div class="fuel-track">
                            <div class="fuel-fill" style="width: {cho_pct}%; background: #3b82f6;"></div>
                        </div>
                        <div class="fuel-percent">{cho_pct}%</div>
                    </div>
                </div>
                <p class="fuel-note">Your body uses a mixture of carbs and fats to produce the energy needed to sustain life and power daily activities. High reliance on fat as a fuel source is one of the most important markers of metabolic health.</p>
            </div>
        </div>
        """

    def generate_macronutrient_page(self):
        """Generate macronutrient balance page"""
        return """
        <div class="macro-page">
            <h1>Macronutrient Balance</h1>
            <p class="macro-intro">Personalized macronutrient recommendations based on your metabolic profile.</p>
            <!-- This page can be expanded with specific macro recommendations -->
        </div>
        """

    def generate_testing_schedule_page(self):
        """Generate testing schedule page"""
        return """
        <div class="schedule-page">
            <h1>Testing Schedule</h1>
            <p>Regular metabolic testing helps track progress and optimize your health journey.</p>
            <div class="schedule-recommendations">
                <h3>Recommended Testing Frequency:</h3>
                <ul>
                    <li><strong>Initial Phase:</strong> Every 4-6 weeks to establish baseline and track initial improvements</li>
                    <li><strong>Maintenance Phase:</strong> Every 3-6 months to monitor long-term progress</li>
                    <li><strong>Optimization Phase:</strong> As needed based on specific health goals</li>
                </ul>
            </div>
        </div>
        """

    def generate_supplement_recommendations(self):
        """Generate IV therapy and supplement recommendations"""
        # This will be populated with AI-generated recommendations
        return """
        <div class="supplements-section">
            <h1>Personalized Supplement & IV Therapy Recommendations</h1>
            <p>Based on your metabolic profile, the following interventions may support your health optimization goals:</p>
            <!-- AI-generated supplement recommendations will be inserted here -->
        </div>
        """

    def generate_css(self):
        """Generate comprehensive CSS for premium report"""
        return """
        <style>
            /* Premium Report Styles */
            @page {
                size: letter;
                margin: 0.5in;
            }

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #1f2937;
            }

            /* Cover Page */
            .cover-page {
                page-break-after: always;
                text-align: center;
                padding: 3in 1in;
            }

            .cover-title {
                font-size: 32pt;
                font-weight: 700;
                color: #10b981;
                margin-bottom: 0.5in;
            }

            .cover-subtitle {
                font-size: 24pt;
                font-weight: 600;
                color: #374151;
                margin-bottom: 0.3in;
            }

            .cover-patient {
                font-size: 20pt;
                font-weight: 500;
                color: #1f2937;
                margin-bottom: 1in;
            }

            .cover-details {
                text-align: left;
                max-width: 500px;
                margin: 0 auto;
            }

            .detail-row {
                display: flex;
                justify-content: space-between;
                margin-bottom: 0.2in;
                font-size: 12pt;
            }

            /* Standard Pages */
            .disclaimer-page,
            .pillars-page,
            .overview-page,
            .metrics-intro-page,
            .metric-page,
            .caloric-page,
            .macro-page,
            .schedule-page,
            .supplements-section {
                page-break-after: always;
                padding: 0.5in;
            }

            h1 {
                font-size: 24pt;
                font-weight: 700;
                color: #10b981;
                margin-bottom: 0.3in;
                border-bottom: 3px solid #10b981;
                padding-bottom: 0.1in;
            }

            h2 {
                font-size: 16pt;
                font-weight: 600;
                color: #374151;
                margin-top: 0.2in;
                margin-bottom: 0.1in;
            }

            h3 {
                font-size: 14pt;
                font-weight: 600;
                color: #1f2937;
                margin-bottom: 0.1in;
            }

            p {
                margin-bottom: 0.15in;
            }

            /* Pillars Grid */
            .pillars-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.3in;
                margin-top: 0.2in;
            }

            .pillar {
                background: #f9fafb;
                padding: 0.2in;
                border-radius: 8px;
                border-left: 4px solid #10b981;
            }

            /* Overview Dashboard */
            .overview-summary {
                display: flex;
                gap: 0.2in;
                margin: 0.3in 0;
                align-items: center;
            }

            .summary-count {
                font-size: 28pt;
                font-weight: 700;
                padding: 0.15in 0.25in;
                border-radius: 8px;
                color: white;
            }

            .summary-count.severe { background: #991b1b; }
            .summary-count.limitation { background: #ef4444; }
            .summary-count.neutral { background: #f59e0b; }
            .summary-count.good { background: #3b82f6; }
            .summary-count.excellent { background: #10b981; }

            .summary-label {
                font-size: 14pt;
                font-weight: 600;
                color: #6b7280;
            }

            .overview-legend {
                display: flex;
                gap: 0.2in;
                margin-bottom: 0.3in;
                font-size: 9pt;
            }

            .legend-item {
                padding: 0.05in 0.1in;
                border-radius: 4px;
                color: white;
                font-weight: 500;
            }

            .legend-item.severe { background: #991b1b; }
            .legend-item.limitation { background: #ef4444; }
            .legend-item.neutral { background: #f59e0b; }
            .legend-item.good { background: #3b82f6; }
            .legend-item.excellent { background: #10b981; }

            /* Score Bars */
            .score-bar-container {
                margin: 0.2in 0;
            }

            .score-label {
                font-size: 12pt;
                font-weight: 600;
                color: #1f2937;
                margin-bottom: 0.1in;
            }

            .score-track {
                height: 30px;
                background: #e5e7eb;
                border-radius: 15px;
                position: relative;
                overflow: hidden;
            }

            .score-fill {
                height: 100%;
                border-radius: 15px;
                transition: width 0.3s ease;
            }

            .score-markers {
                display: flex;
                justify-content: space-between;
                font-size: 8pt;
                color: #6b7280;
                margin-top: 0.05in;
            }

            .score-zones {
                display: flex;
                justify-content: space-between;
                margin-top: 0.1in;
                font-size: 8pt;
            }

            .zone {
                padding: 0.03in 0.08in;
                border-radius: 4px;
                color: white;
                font-weight: 500;
            }

            .zone.severe { background: #991b1b; }
            .zone.limitation { background: #ef4444; }
            .zone.neutral { background: #f59e0b; }
            .zone.good { background: #3b82f6; }
            .zone.excellent { background: #10b981; }

            /* Metric Pages */
            .metric-section {
                margin: 0.2in 0;
                background: #f9fafb;
                padding: 0.2in;
                border-radius: 8px;
            }

            /* Caloric Balance */
            .caloric-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.3in;
                margin: 0.2in 0;
            }

            .caloric-box {
                background: #f9fafb;
                padding: 0.2in;
                border-radius: 8px;
                border-top: 4px solid #10b981;
            }

            .cal-section {
                margin: 0.15in 0;
            }

            .cal-label {
                font-size: 10pt;
                color: #6b7280;
                margin-bottom: 0.05in;
            }

            .cal-value {
                font-size: 18pt;
                font-weight: 700;
                color: #10b981;
            }

            .fuel-sources {
                margin-top: 0.3in;
            }

            .fuel-bars {
                margin: 0.2in 0;
            }

            .fuel-bar {
                display: grid;
                grid-template-columns: 120px 1fr 60px;
                gap: 0.1in;
                align-items: center;
                margin-bottom: 0.15in;
            }

            .fuel-label {
                font-weight: 600;
                color: #1f2937;
            }

            .fuel-track {
                height: 24px;
                background: #e5e7eb;
                border-radius: 12px;
                overflow: hidden;
            }

            .fuel-fill {
                height: 100%;
                border-radius: 12px;
            }

            .fuel-percent {
                font-weight: 700;
                color: #1f2937;
                text-align: right;
            }

            .fuel-note {
                font-size: 9pt;
                color: #6b7280;
                font-style: italic;
                margin-top: 0.2in;
            }

            /* Print Optimization */
            @media print {
                body {
                    print-color-adjust: exact;
                    -webkit-print-color-adjust: exact;
                }
            }
        </style>
        """

    def generate(self):
        """Generate the complete premium HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Metabolic Blueprint - {self.patient_info['name']}</title>
            {self.generate_css()}
        </head>
        <body>
            {self.generate_cover_page()}
            {self.generate_disclaimer_page()}
            {self.generate_pillars_page()}
            {self.generate_overview_dashboard()}
            {self.generate_core_metrics_intro()}
            {self.generate_all_metric_pages()}
            {self.generate_caloric_balance_page()}
            {self.generate_macronutrient_page()}
            {self.generate_testing_schedule_page()}
            {self.generate_supplement_recommendations()}
        </body>
        </html>
        """
        return html


def generate_premium_report(extracted_data, custom_data):
    """
    Generate a premium 30+ page metabolic report

    Args:
        extracted_data: Patient data extracted from PDF
        custom_data: Custom settings (chronological_age, biological_age, etc.)

    Returns:
        HTML string of complete premium report
    """

    print("\n[AI_PREMIUM_REPORT] Generating premium report...")

    # Enhance data with calculated scores
    extracted_data = enhance_extracted_data_with_calculated_scores(extracted_data)

    # Create report instance
    report = AIPremiumReportTemplate()

    # Set patient info
    patient_info = extracted_data.get('patient_info', {})
    if patient_info.get('name'):
        report.patient_info['name'] = patient_info['name']
    if patient_info.get('test_date'):
        report.patient_info['test_date'] = patient_info['test_date']
    if patient_info.get('age'):
        report.patient_info['age'] = patient_info['age']
    if patient_info.get('gender'):
        report.patient_info['gender'] = patient_info['gender']
    if patient_info.get('weight_kg'):
        report.patient_info['weight_kg'] = patient_info['weight_kg']
    if patient_info.get('height_cm'):
        report.patient_info['height_cm'] = patient_info['height_cm']

    # Set ages
    report.chronological_age = custom_data.get('chronological_age', patient_info.get('age'))
    report.biological_age = custom_data.get('biological_age', report.chronological_age)

    # Set scores and data
    report.core_scores = extracted_data.get('core_scores', {})
    report.caloric_data = extracted_data.get('caloric_data', {})
    report.metabolic_data = extracted_data.get('metabolic_data', {})

    print(f"[AI_PREMIUM_REPORT] Patient: {report.patient_info['name']}")
    print(f"[AI_PREMIUM_REPORT] Chronological Age: {report.chronological_age}")
    print(f"[AI_PREMIUM_REPORT] Biological Age: {report.biological_age}")
    print(f"[AI_PREMIUM_REPORT] Core Scores: {len(report.core_scores)} metrics")

    # Generate HTML
    html = report.generate()

    print("[AI_PREMIUM_REPORT] ✅ Premium report generated successfully\n")

    return html
