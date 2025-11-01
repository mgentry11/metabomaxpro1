"""
Beautiful Report Generator
Creates comprehensive, visually stunning metabolic reports
Based on the ultimate report template
"""
from datetime import datetime
import json
import sys
import os

# Add parent directory to path to import template
sys.path.insert(0, os.path.dirname(__file__))
from ultimate_report_template import MarkGentryReport

def generate_beautiful_report(extracted_data, custom_data):
    """Generate a comprehensive, beautiful HTML report using the ultimate template"""

    # Create a modified report instance with user's data
    report = MarkGentryReport()

    # Override with extracted data
    patient_info = extracted_data.get('patient_info', {})
    if patient_info.get('name'):
        report.patient_info['name'] = patient_info['name']
    if patient_info.get('test_date'):
        report.patient_info['test_date'] = patient_info['test_date']
    if patient_info.get('weight_kg'):
        report.patient_info['weight_kg'] = patient_info['weight_kg']
    if patient_info.get('gender'):
        report.patient_info['gender'] = patient_info['gender']

    # Override core scores if extracted
    core_scores = extracted_data.get('core_scores', {})
    if core_scores:
        report.core_scores.update(core_scores)

    # Override caloric data if extracted
    caloric_data = extracted_data.get('caloric_data', {})
    if caloric_data:
        report.caloric_data.update(caloric_data)

    # Override with custom data
    if custom_data.get('chronological_age'):
        report.chronological_age = custom_data['chronological_age']
        report.patient_info['age'] = custom_data['chronological_age']
        print(f"DEBUG beautiful_report: Set chronological_age = {custom_data['chronological_age']}")

    if custom_data.get('biological_age'):
        report.biological_age = custom_data['biological_age']
        print(f"DEBUG beautiful_report: Set biological_age = {custom_data['biological_age']}")

    # Store custom notes and goals for later use
    report.custom_notes = custom_data.get('custom_notes', '')
    report.custom_goals = custom_data.get('goals', [])
    report.report_type = custom_data.get('report_type', 'Performance').title()

    # DEBUG: Verify ages before generating
    print(f"[BEAUTIFUL_REPORT DEBUG] About to call report.generate()")
    print(f"[BEAUTIFUL_REPORT DEBUG] report.chronological_age = {report.chronological_age}")
    print(f"[BEAUTIFUL_REPORT DEBUG] report.biological_age = {report.biological_age}")

    # Generate and return HTML
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmp:
        report.generate(tmp.name)
        with open(tmp.name, 'r') as f:
            html = f.read()
        os.unlink(tmp.name)

    return html

# Keep the old function as backup
def generate_beautiful_report_OLD(extracted_data, custom_data):
    """Generate a comprehensive, beautiful HTML report (OLD VERSION)"""

    # Extract data
    patient_name = extracted_data.get('patient_info', {}).get('name', 'Patient')
    test_date = extracted_data.get('patient_info', {}).get('test_date', datetime.now().strftime('%m/%d/%Y'))
    core_scores = extracted_data.get('core_scores', {})
    caloric_data = extracted_data.get('caloric_data', {})
    hr_data = extracted_data.get('heart_rate_data', {})
    metabolic_data = extracted_data.get('metabolic_data', {})

    # Custom data
    report_type = custom_data.get('report_type', 'performance').title()
    custom_notes = custom_data.get('custom_notes', '')
    goals = custom_data.get('goals', [])
    chronological_age = custom_data.get('chronological_age')
    biological_age = custom_data.get('biological_age')
    additional_metrics = custom_data.get('additional_metrics', {})

    # Calculate metrics
    if core_scores:
        avg_score = round(sum(core_scores.values()) / len(core_scores))
    else:
        avg_score = 0

    # Images
    LOGO_URL = "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=200"
    HERO_IMAGE = "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=1600"
    FITNESS_IMG = "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600"
    NUTRITION_IMG = "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600"

    # Score labels
    score_labels = {
        'symp_parasym': 'Sympathetic/Parasympathetic Balance',
        'ventilation_eff': 'Ventilation Efficiency',
        'breathing_coord': 'Breathing Coordination',
        'lung_util': 'Lung Utilization',
        'hrv': 'Heart Rate Variability',
        'metabolic_rate': 'Metabolic Rate',
        'fat_burning': 'Fat Burning Efficiency'
    }

    # Prepare chart data
    score_names = [score_labels.get(k, k.replace('_', ' ').title()) for k in core_scores.keys()]
    score_values = list(core_scores.values())

    # Calculate training zones if we have age
    training_zones = []
    if chronological_age:
        max_hr = 220 - chronological_age
        training_zones = [
            {'zone': 1, 'name': 'Recovery', 'hr_min': int(max_hr * 0.5), 'hr_max': int(max_hr * 0.6), 'color': '#10B981'},
            {'zone': 2, 'name': 'Aerobic', 'hr_min': int(max_hr * 0.6), 'hr_max': int(max_hr * 0.7), 'color': '#3B82F6'},
            {'zone': 3, 'name': 'Tempo', 'hr_min': int(max_hr * 0.7), 'hr_max': int(max_hr * 0.8), 'color': '#F59E0B'},
            {'zone': 4, 'name': 'Threshold', 'hr_min': int(max_hr * 0.8), 'hr_max': int(max_hr * 0.9), 'color': '#EF4444'},
            {'zone': 5, 'name': 'Max Effort', 'hr_min': int(max_hr * 0.9), 'hr_max': max_hr, 'color': '#991B1B'},
        ]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{patient_name} - {report_type} Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

:root {{
    --primary: #1E40AF;
    --secondary: #0D9488;
    --accent: #8B5CF6;
    --success: #10B981;
    --warning: #F59E0B;
    --danger: #EF4444;
    --dark: #0F172A;
    --light: #F8FAFC;
}}

body {{
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    color: var(--dark);
    background: var(--light);
}}

.container {{ max-width: 1400px; margin: 0 auto; background: white; }}

/* Hero Section */
.hero {{
    background: linear-gradient(135deg, rgba(30,64,175,0.95), rgba(139,92,246,0.95)),
                url('{HERO_IMAGE}');
    background-size: cover;
    background-position: center;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: white;
    padding: 80px 40px;
    position: relative;
    text-align: center;
}}

.hero::before {{
    content: '';
    position: absolute;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    border-radius: 50%;
    animation: pulse 8s ease-in-out infinite;
}}

@keyframes pulse {{
    0%, 100% {{ transform: scale(1); opacity: 0.5; }}
    50% {{ transform: scale(1.1); opacity: 0.3; }}
}}

.hero-content {{
    position: relative;
    z-index: 1;
}}

.hero h1 {{
    font-size: 4rem;
    font-weight: 800;
    margin-bottom: 1rem;
    text-shadow: 2px 4px 8px rgba(0,0,0,0.3);
}}

.hero .subtitle {{
    font-size: 1.5rem;
    font-weight: 300;
    margin-bottom: 2rem;
    opacity: 0.95;
}}

.hero-stats {{
    display: flex;
    gap: 3rem;
    margin-top: 3rem;
    justify-content: center;
}}

.hero-stat {{
    text-align: center;
}}

.hero-stat-value {{
    font-size: 3.5rem;
    font-weight: 800;
    display: block;
    line-height: 1;
}}

.hero-stat-label {{
    font-size: 0.9rem;
    opacity: 0.9;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 0.5rem;
}}

/* Section */
.section {{
    padding: 80px 40px;
}}

.section-header {{
    text-align: center;
    margin-bottom: 60px;
}}

.section-header h2 {{
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--dark);
    margin-bottom: 1rem;
}}

.section-header p {{
    font-size: 1.1rem;
    color: #64748B;
    max-width: 600px;
    margin: 0 auto;
}}

/* Metrics Grid */
.metrics-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}}

.metric-card {{
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-left: 5px solid var(--primary);
}}

.metric-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}}

.metric-icon {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

.metric-value {{
    font-size: 3rem;
    font-weight: 800;
    color: var(--primary);
    line-height: 1;
}}

.metric-label {{
    font-size: 0.9rem;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.5rem;
}}

.metric-change {{
    display: inline-block;
    margin-top: 0.5rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}}

.metric-change.positive {{
    background: #DCFCE7;
    color: #166534;
}}

/* Chart Container */
.chart-container {{
    background: white;
    border-radius: 20px;
    padding: 3rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin: 3rem 0;
}}

.chart-wrapper {{
    position: relative;
    height: 500px;
}}

/* Training Zones */
.zones-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 3rem 0;
}}

.zone-card {{
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    border-left: 5px solid;
}}

.zone-number {{
    display: inline-block;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--primary);
    color: white;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
}}

.zone-name {{
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.zone-hr {{
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
}}

/* Goals */
.goals-list {{
    list-style: none;
    padding: 0;
}}

.goal-item {{
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    border-left: 5px solid var(--success);
    display: flex;
    align-items: center;
}}

.goal-item::before {{
    content: "🎯";
    font-size: 2rem;
    margin-right: 1.5rem;
}}

/* Notes */
.notes-box {{
    background: #FEF3C7;
    border-left: 5px solid var(--warning);
    border-radius: 15px;
    padding: 2rem;
    margin: 3rem 0;
}}

.notes-box h3 {{
    font-size: 1.3rem;
    margin-bottom: 1rem;
    color: #92400E;
}}

.notes-box p {{
    color: #78350F;
    line-height: 1.8;
}}

/* Action Plan */
.action-plan {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 20px;
    padding: 3rem;
    margin: 3rem 0;
}}

.action-plan h3 {{
    font-size: 2rem;
    margin-bottom: 2rem;
}}

.action-steps {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}}

.action-step {{
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 2rem;
    border: 2px solid rgba(255,255,255,0.2);
}}

.step-number {{
    display: inline-block;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: white;
    color: var(--primary);
    font-weight: 800;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
}}

.step-title {{
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

/* Images */
.image-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}}

.image-card {{
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}}

.image-card img {{
    width: 100%;
    height: 300px;
    object-fit: cover;
}}

/* Footer */
.footer {{
    background: var(--dark);
    color: white;
    text-align: center;
    padding: 3rem;
}}

.footer-content {{
    max-width: 800px;
    margin: 0 auto;
}}

/* Responsive */
@media (max-width: 768px) {{
    .hero h1 {{ font-size: 2.5rem; }}
    .hero-stats {{ flex-direction: column; gap: 2rem; }}
    .section {{ padding: 60px 20px; }}
    .metrics-grid {{ grid-template-columns: 1fr; }}
}}

/* Print */
@media print {{
    .hero {{ page-break-after: always; }}
    .section {{ page-break-inside: avoid; }}
}}
    </style>
</head>
<body>
    <div class="container">
        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-content">
                <h1>{patient_name}</h1>
                <div class="subtitle">{report_type} Metabolic Report | {test_date}</div>
                <div class="hero-stats">
                    <div class="hero-stat">
                        <span class="hero-stat-value">{avg_score}%</span>
                        <span class="hero-stat-label">Overall Score</span>
                    </div>
"""

    # Add biological age if provided
    if biological_age and chronological_age:
        age_diff = chronological_age - biological_age
        html += f"""
                    <div class="hero-stat">
                        <span class="hero-stat-value">{biological_age}</span>
                        <span class="hero-stat-label">Biological Age</span>
                    </div>
                    <div class="hero-stat">
                        <span class="hero-stat-value">{age_diff}</span>
                        <span class="hero-stat-label">Years Younger</span>
                    </div>
"""

    html += """
                </div>
            </div>
        </section>

        <!-- Core Metrics Section -->
        <section class="section">
            <div class="section-header">
                <h2>📊 Core Performance Metrics</h2>
                <p>Your metabolic performance across key indicators</p>
            </div>
            <div class="metrics-grid">
"""

    # Add metric cards
    icons = ['💓', '🫁', '⚡', '💪', '❤️', '🔥', '⚖️']
    for idx, (key, value) in enumerate(core_scores.items()):
        label = score_labels.get(key, key.replace('_', ' ').title())
        icon = icons[idx] if idx < len(icons) else '📈'
        status = "Excellent" if value >= 80 else "Good" if value >= 60 else "Needs Work"
        html += f"""
                <div class="metric-card">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-value">{value}%</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-change positive">{status}</div>
                </div>
"""

    html += """
            </div>

            <!-- Radar Chart -->
            <div class="chart-container">
                <h3 style="text-align: center; margin-bottom: 2rem; font-size: 1.8rem;">Performance Profile</h3>
                <div class="chart-wrapper">
                    <canvas id="radarChart"></canvas>
                </div>
            </div>
        </section>
"""

    # Training Zones
    if training_zones:
        html += """
        <!-- Training Zones Section -->
        <section class="section" style="background: #F8FAFC;">
            <div class="section-header">
                <h2>🎯 Training Zones</h2>
                <p>Heart rate zones for optimal training</p>
            </div>
            <div class="zones-grid">
"""
        for zone in training_zones:
            html += f"""
                <div class="zone-card" style="border-left-color: {zone['color']};">
                    <div class="zone-number" style="background: {zone['color']};">{zone['zone']}</div>
                    <div class="zone-name">{zone['name']}</div>
                    <div class="zone-hr">{zone['hr_min']}-{zone['hr_max']} bpm</div>
                </div>
"""
        html += """
            </div>
        </section>
"""

    # Goals
    if goals:
        html += """
        <!-- Goals Section -->
        <section class="section">
            <div class="section-header">
                <h2>🎯 Your Goals</h2>
                <p>Objectives and targets for your fitness journey</p>
            </div>
            <ul class="goals-list">
"""
        for goal in goals:
            html += f"""
                <li class="goal-item">{goal}</li>
"""
        html += """
            </ul>
        </section>
"""

    # Custom Notes
    if custom_notes:
        html += f"""
        <!-- Notes Section -->
        <section class="section" style="background: #F8FAFC;">
            <div class="section-header">
                <h2>📝 Custom Notes</h2>
            </div>
            <div class="notes-box">
                <h3>Observations & Recommendations</h3>
                <p>{custom_notes.replace(chr(10), '<br>')}</p>
            </div>
        </section>
"""

    # Action Plan
    html += """
        <!-- Action Plan -->
        <section class="section">
            <div class="action-plan">
                <h3>🚀 Your Action Plan</h3>
                <div class="action-steps">
                    <div class="action-step">
                        <div class="step-number">1</div>
                        <div class="step-title">Consistency</div>
                        <p>Train in your target zones 4-5 times per week</p>
                    </div>
                    <div class="action-step">
                        <div class="step-number">2</div>
                        <div class="step-title">Nutrition</div>
                        <p>Fuel your body with proper macronutrient balance</p>
                    </div>
                    <div class="action-step">
                        <div class="step-number">3</div>
                        <div class="step-title">Recovery</div>
                        <p>Prioritize sleep and active recovery sessions</p>
                    </div>
                    <div class="action-step">
                        <div class="step-number">4</div>
                        <div class="step-title">Monitor</div>
                        <p>Track progress and retest in 12 weeks</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Images -->
        <section class="section" style="background: #F8FAFC;">
            <div class="image-grid">
                <div class="image-card">
                    <img src="{FITNESS_IMG}" alt="Fitness">
                </div>
                <div class="image-card">
                    <img src="{NUTRITION_IMG}" alt="Nutrition">
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-content">
                <p style="font-size: 1.2rem; margin-bottom: 1rem;">Generated on """ + datetime.now().strftime('%B %d, %Y at %I:%M %p') + """</p>
                <p style="opacity: 0.7;">🤖 Powered by Metabolic Report Generator</p>
            </div>
        </footer>
    </div>

    <script>
        // Radar Chart
        const ctx = document.getElementById('radarChart').getContext('2d');
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: """ + json.dumps(score_names) + """,
                datasets: [{
                    label: 'Your Scores',
                    data: """ + json.dumps(score_values) + """,
                    backgroundColor: 'rgba(30, 64, 175, 0.2)',
                    borderColor: 'rgba(30, 64, 175, 1)',
                    borderWidth: 3,
                    pointBackgroundColor: 'rgba(30, 64, 175, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(30, 64, 175, 1)',
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 20,
                            font: {
                                size: 14
                            }
                        },
                        pointLabels: {
                            font: {
                                size: 14,
                                weight: '600'
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: {
                                size: 16,
                                weight: '600'
                            }
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
"""

    return html
