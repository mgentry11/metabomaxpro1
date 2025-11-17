"""
PNOE Professional Metabolic Blueprint Template - COMPACT ALGORITHM
Following the complete formatting algorithm for 3-4 page compact reports
with circular progress, visual bars, timeline, and gradients
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
        """Get status label, emoji, and color for a score"""
        if score >= 80:
            return ('EXCELLENT', '✓', '#00cc00', 'excellent')
        elif score >= 60:
            return ('GOOD', '●', '#0066cc', 'good')
        else:
            return ('NEUTRAL', '-', '#999999', 'neutral')

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
        """Return compact algorithm CSS with all features"""
        return """
* { box-sizing: border-box; }
body { max-width: 880px; margin: 0 auto; padding: 20px 40px; font-family: Arial, sans-serif;
       line-height: 1.2; background: linear-gradient(135deg, #f8fbff 0%, #ffffff 100%); font-size: 0.85em; }

/* HEADER */
.header { text-align: center; margin-bottom: 15px; background: linear-gradient(135deg, #0066cc 0%, #4da6ff 100%);
          color: white; padding: 12px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,102,204,0.2); }
.brand { font-size: 1.1em; margin-bottom: 4px; }
h1 { color: white; font-size: 1.8em; margin: 8px 0; font-weight: bold; }
.subtitle { margin: 4px 0; font-size: 0.9em; opacity: 0.95; }

/* SECTION HEADERS */
h2 { color: #0066cc; font-size: 1.2em; margin: 12px 0 6px 0; border-bottom: 2px solid #4da6ff;
     padding: 5px; background: linear-gradient(90deg, #f0f8ff 0%, transparent 100%); border-radius: 5px; }
h3 { color: #0066cc; font-size: 1.05em; margin: 10px 0 5px 0; }

/* PATIENT INFO TABLE */
.patient-info { background: #f0f8ff; border: 2px solid #4da6ff; border-radius: 8px; padding: 8px; margin: 8px 0; }
table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 0.9em; background: white;
        border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
th, td { border: 1px solid #ddd; padding: 4px 8px; }
th { background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%); font-weight: bold; color: #003366; }

/* EXECUTIVE SUMMARY - 3 CARD GRID */
.executive-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin: 10px 0; }
.metric-card { background: white; border: 2px solid #ddd; border-radius: 8px; padding: 10px;
               text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
.metric-card.excellent { border-color: #00cc00; }
.metric-card.good { border-color: #0066cc; }

/* CIRCULAR PROGRESS */
.circular-progress { display: flex; justify-content: center; margin: 8px 0; }
.circular-progress-inner { width: 90px; height: 90px; border-radius: 50%;
                            display: flex; align-items: center; justify-content: center;
                            position: relative; }
.circular-progress-inner::before { content: ''; position: absolute; width: 70px; height: 70px;
                                    background: white; border-radius: 50%; z-index: 0; }
.score-text { font-size: 1.6em; font-weight: bold; color: #0066cc; text-align: center; line-height: 1;
              z-index: 1; position: relative; }
.score-text small { font-size: 0.5em; display: block; margin-top: 2px; }

/* HERO IMAGE */
.hero-img { text-align: center; margin: 10px 0; }
.hero-img img { max-width: 450px; width: 100%; height: auto; border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.15); border: 2px solid #0066cc; }

/* BIOLOGICAL AGE */
.age-comparison-visual { background: linear-gradient(135deg, #e6f3ff 0%, #ffffff 100%);
                         border: 2px solid #00cc00; border-radius: 10px; padding: 12px;
                         text-align: center; box-shadow: 0 3px 8px rgba(0,204,0,0.2); margin: 10px 0; }
.age-arrow { font-size: 2em; color: #00cc00; font-weight: bold; margin: 5px 0; }

/* CORE METRICS - VISUAL PROGRESS BARS */
.metrics-visual { margin: 10px 0; }
.metric-row { display: flex; align-items: center; margin: 4px 0; padding: 5px;
              background: white; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.metric-icon { width: 25px; text-align: center; font-size: 1.1em; }
.metric-name { flex: 0 0 180px; font-size: 0.95em; }
.progress-container { flex: 1; height: 18px; background: #e0e0e0; border-radius: 10px;
                       margin: 0 8px; overflow: hidden; }
.progress-bar { height: 100%; border-radius: 10px; transition: width 0.3s; }
.progress-bar.excellent { background: linear-gradient(90deg, #00cc00 0%, #66ff66 100%); }
.progress-bar.good { background: linear-gradient(90deg, #0066cc 0%, #66b3ff 100%); }
.progress-bar.neutral { background: linear-gradient(90deg, #999999 0%, #cccccc 100%); }
.metric-score { flex: 0 0 45px; font-weight: bold; text-align: right; }
.metric-label { flex: 0 0 85px; font-weight: bold; font-size: 0.85em; }

/* CALORIC BALANCE */
.caloric-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 10px 0; }
.caloric-card { background: white; border: 2px solid; border-radius: 8px; padding: 12px;
                text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
.caloric-card.burn { border-color: #ff6600; }
.caloric-card.eat { border-color: #00cc00; }
.caloric-icon { font-size: 2.5em; margin-bottom: 5px; }
.caloric-card h3 { margin: 5px 0; color: #003366; }
.caloric-card p { margin: 3px 0; font-size: 0.95em; }

/* FUEL SOURCES BAR */
.fuel-sources { background: white; border: 2px solid #0066cc; border-radius: 8px; padding: 10px; margin: 10px 0; }
.fuel-bar { display: flex; height: 30px; border-radius: 8px; overflow: hidden; margin-top: 8px; }
.fuel-fats, .fuel-carbs { display: flex; align-items: center; justify-content: center;
                          color: white; font-weight: bold; font-size: 0.9em; }
.fuel-fats { background: linear-gradient(90deg, #ff6600 0%, #ffaa66 100%); }
.fuel-carbs { background: linear-gradient(90deg, #0066cc 0%, #66b3ff 100%); }

/* TRAINING ZONES */
.zone-cards { margin: 10px 0; }
.zone-card { padding: 8px; border-radius: 8px; border: 2px solid; display: flex;
             align-items: center; margin-bottom: 6px; background: white; }
.zone-card.zone1 { border-color: #999999; }
.zone-card.zone2 { border-color: #0066cc; border-width: 3px; box-shadow: 0 4px 12px rgba(0,102,204,0.3); }
.zone-card.zone3 { border-color: #ffaa00; }
.zone-card.zone4 { border-color: #ff6600; }
.zone-card.zone5 { border-color: #cc0000; }
.zone-icon { font-size: 1.5em; margin-right: 10px; width: 35px; text-align: center; }
.zone-info { flex: 1; }
.zone-name { font-weight: bold; color: #003366; margin-bottom: 2px; }
.zone-hr { color: #0066cc; font-weight: bold; font-size: 1.05em; margin: 2px 0; }
.zone-description { font-size: 0.85em; color: #666; }
.primary-badge { background: #ffaa00; color: white; padding: 2px 8px; border-radius: 10px;
                 font-size: 0.7em; margin-left: 6px; }

/* WEEKLY TRAINING PLAN */
.training-plan { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 10px 0; }
.training-card { background: white; border: 2px solid #0066cc; border-radius: 8px;
                 padding: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
.training-card.priority-high { border-color: #cc0000; }
.training-icon { font-size: 1.3em; margin-right: 6px; }
.priority-badge { padding: 4px 8px; border-radius: 15px; font-size: 0.75em;
                  font-weight: bold; color: white; display: inline-block; margin: 4px 0; }
.priority-badge.high { background: #cc0000; }
.priority-badge.medium { background: #ff6600; }
.priority-badge.low { background: #999999; }

/* INTERVENTIONS GRID */
.interventions-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 10px 0; }
.intervention-card { background: white; border: 2px solid #0066cc; border-radius: 8px;
                      padding: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); text-align: center; }
.intervention-card img { width: 100%; height: 120px; object-fit: cover; border-radius: 8px;
                         margin-bottom: 8px; }
.intervention-icon { font-size: 2.5em; margin-bottom: 8px; }
.evidence-badge { background: linear-gradient(90deg, #00cc00 0%, #66ff66 100%);
                  color: white; padding: 3px 8px; border-radius: 10px; font-size: 0.7em;
                  display: inline-block; margin-top: 6px; }

/* ACTION PLAN - AUTO NUMBERED */
.action-plan { counter-reset: action-counter; margin: 10px 0; }
.action-item { counter-increment: action-counter; display: flex; margin: 6px 0; padding: 8px;
               border-left: 4px solid #0066cc; background: #f8fbff; border-radius: 5px; }
.action-number { background: #0066cc; color: white; width: 30px; height: 30px;
                 border-radius: 50%; display: flex; align-items: center; justify-content: center;
                 font-weight: bold; margin-right: 10px; flex-shrink: 0; }
.action-number::before { content: counter(action-counter); }

/* 90-DAY PROTOCOL - TIMELINE */
.timeline-visual { position: relative; margin: 15px 0; padding-left: 40px; }
.timeline-line { position: absolute; left: 24px; top: 0; bottom: 0; width: 3px;
                 background: linear-gradient(180deg, #0066cc 0%, #4da6ff 100%); }
.timeline-phase { position: relative; margin: 8px 0; padding: 8px 8px 8px 30px;
                  border: 2px solid #4da6ff; border-radius: 8px; background: white; }
.timeline-phase::before { content: ''; position: absolute; left: -28px; top: 15px;
                          width: 12px; height: 12px; background: #0066cc; border-radius: 50%;
                          border: 2px solid white; box-shadow: 0 0 0 2px #0066cc; z-index: 1; }
.timeline-phase.retest { border-color: #00cc00; background: linear-gradient(135deg, #f0fff0 0%, #ffffff 100%); }
.timeline-phase.retest::before { background: #00cc00; box-shadow: 0 0 0 2px #00cc00; }
.phase-weeks { font-weight: bold; color: #0066cc; margin-bottom: 4px; }
.timeline-phase.retest .phase-weeks { color: #00cc00; }

/* DISCLAIMERS */
.disclaimer { background: linear-gradient(135deg, #fff3cd 0%, #ffffff 100%);
              border: 2px solid #ffc107; padding: 15px; border-radius: 10px; margin: 10px 0; }
.peptide-section { background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
                   border: 2px solid #ff6b6b; padding: 20px; border-radius: 10px; margin: 10px 0; }
.warning-box { text-align: center; margin-top: 30px; font-size: 1em; color: #cc0000;
               font-weight: bold; border: 2px solid #cc0000; padding: 15px; border-radius: 10px;
               background: #ffe6e6; }

/* UTILITIES */
.text-center { text-align: center; }
strong { font-weight: bold; }
"""

    def _generate_header(self):
        """Generate compact header"""
        return f"""
<div class="header">
    <div class="brand">Optimal Vitality ⚡</div>
    <h1>PERFORMANCE METABOLIC BLUEPRINT 2025</h1>
    <p class="subtitle">Comprehensive metabolic testing, training zones, and performance optimization powered by PNOE technology</p>
</div>
"""

    def _generate_patient_info(self):
        """Generate patient info table"""
        weight_lbs = round(self.patient_info['weight_kg'] * 2.20462, 1)
        height_ft = self.patient_info['height_cm'] // 30.48
        height_in = round((self.patient_info['height_cm'] % 30.48) / 2.54)

        return f"""
<div class="patient-info">
<h2>📋 Patient Information</h2>
<table>
<tr><th>Name</th><td>{self.patient_info['name']}</td><th>Test Date</th><td>{self.patient_info['test_date']}</td></tr>
<tr><th>Age</th><td>{self.patient_info['age']} years</td><th>Gender</th><td>{self.patient_info['gender']}</td></tr>
<tr><th>Weight</th><td>{weight_lbs} lbs ({self.patient_info['weight_kg']} kg)</td><th>Height</th><td>{height_ft}'{height_in}" ({self.patient_info['height_cm']} cm)</td></tr>
<tr><th>Test Type</th><td>{self.patient_info.get('test_type', 'Performance')}</td><th>Facility</th><td>{self.patient_info.get('facility', 'Optimal Vitality')}</td></tr>
</table>
</div>
"""

    def _generate_executive_summary(self):
        """Generate executive summary with circular progress"""
        overall_score = self._calculate_overall_score()
        excellent, good_plus = self._count_excellent_good()

        # Calculate degrees for circular progress (score/100 * 360)
        degrees = (overall_score / 100) * 360

        return f"""
<h2>📊 Executive Summary</h2>
<div class="executive-grid">
    <div class="metric-card">
        <div class="circular-progress">
            <div class="circular-progress-inner" style="background: conic-gradient(#0066cc 0deg, #0066cc {degrees}deg, #e0e0e0 {degrees}deg, #e0e0e0 360deg);">
                <div class="score-text">{overall_score}<br/><small>/100</small></div>
            </div>
        </div>
        <strong>Overall Health Score</strong>
    </div>
    <div class="metric-card excellent">
        <div style="font-size:2.5em;color:#00cc00">✓</div>
        <strong>{excellent} of {len(self.core_scores)}</strong><br/><small>Excellent Metrics</small>
    </div>
    <div class="metric-card good">
        <div style="font-size:2.5em;color:#0066cc">●</div>
        <strong>{good_plus} of {len(self.core_scores)}</strong><br/><small>Good+ Metrics</small>
    </div>
</div>
"""

    def _generate_hero_image(self):
        """Generate hero image"""
        return f"""
<div class="hero-img">
    <img src="{self.HERO_IMAGE}" alt="Performance Training">
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

        return f"""
<div class="age-comparison-visual">
    <h3>🧬 Biological Age Analysis</h3>
    <div class="age-arrow">{self.chronological_age} → {self.biological_age}</div>
    <div style="font-size:1.2em;font-weight:bold;color:#00cc00">{message}</div>
    <p>Your excellent performance metrics indicate superior metabolic health and cellular function.</p>
</div>
"""

    def _generate_core_metrics(self):
        """Generate core metrics with visual progress bars"""
        labels = {
            'symp_parasym': 'Sympathetic/Parasympathetic',
            'ventilation_eff': 'Ventilation Efficiency',
            'breathing_coord': 'Breathing Coordination',
            'lung_util': 'Lung Utilization',
            'hrv': 'Heart Rate Variability (HRV)',
            'metabolic_rate': 'Metabolic Rate',
            'fat_burning': 'Fat-Burning Efficiency'
        }

        html = "<h2>📈 Core Performance Metrics</h2>\n<div class=\"metrics-visual\">\n"

        for key, score in self.core_scores.items():
            label = labels.get(key, key.replace('_', ' ').title())
            status, emoji, color, css_class = self._get_score_status(score)

            html += f"""
    <div class="metric-row">
        <div class="metric-icon">{emoji}</div>
        <div class="metric-name">{label}</div>
        <div class="progress-container">
            <div class="progress-bar {css_class}" style="width:{score}%"></div>
        </div>
        <div class="metric-score" style="color:{color}">{score}%</div>
        <div class="metric-label" style="color:{color}">{status}</div>
    </div>
"""

        html += "</div>\n"
        return html

    def _generate_caloric_balance(self):
        """Generate caloric balance with fuel bar"""
        return f"""
<h2>🔥 Caloric Balance & Fuel Strategy</h2>
<div class="caloric-cards">
    <div class="caloric-card burn">
        <div class="caloric-icon">🔥</div>
        <h3>YOU BURN</h3>
        <p><strong>Rest Days:</strong> {self.caloric_data['burn_rest']:,} kcal/day</p>
        <p><strong>Workout Days:</strong> {self.caloric_data['burn_workout']:,} kcal/day</p>
    </div>
    <div class="caloric-card eat">
        <div class="caloric-icon">🍽️</div>
        <h3>YOU SHOULD EAT</h3>
        <p><strong>Rest Days:</strong> {self.caloric_data['eat_rest']:,} kcal/day</p>
        <p><strong>Workout Days:</strong> {self.caloric_data['eat_workout']:,} kcal/day</p>
    </div>
</div>
<div class="fuel-sources">
    <h3>⛽ Fuel Sources at Rest</h3>
    <div class="fuel-bar">
        <div class="fuel-fats" style="width:{self.caloric_data['fat_percent']}%">Fats {self.caloric_data['fat_percent']}%</div>
        <div class="fuel-carbs" style="width:{self.caloric_data['cho_percent']}%">Carbs {self.caloric_data['cho_percent']}%</div>
    </div>
</div>
"""

    def _generate_training_zones(self):
        """Generate training zones with special zone 2 highlighting"""
        max_hr = 220 - self.chronological_age

        zones = [
            {'num': 1, 'icon': '💤', 'name': 'Zone 1: Recovery', 'min': int(max_hr * 0.5), 'max': int(max_hr * 0.6),
             'desc': 'Active recovery, warm-up, cool-down. Very easy conversational pace.', 'class': 'zone1', 'primary': False},
            {'num': 2, 'icon': '🏃', 'name': 'Zone 2: Endurance Base', 'min': int(max_hr * 0.6), 'max': int(max_hr * 0.7),
             'desc': 'THE most important zone for improving metabolic rate and fat-burning. 3-4 sessions weekly, 45-60 minutes.', 'class': 'zone2', 'primary': True},
            {'num': 3, 'icon': '🚴', 'name': 'Zone 3: Tempo', 'min': int(max_hr * 0.7), 'max': int(max_hr * 0.8),
             'desc': 'Moderate-hard pace, improves lactate threshold. Use sparingly.', 'class': 'zone3', 'primary': False},
            {'num': 4, 'icon': '🏋', 'name': 'Zone 4: Lactate Threshold', 'min': int(max_hr * 0.8), 'max': int(max_hr * 0.9),
             'desc': 'Hard pace, 1-2 sessions weekly for strength development.', 'class': 'zone4', 'primary': False},
            {'num': 5, 'icon': '⚡', 'name': 'Zone 5: VO2 Max', 'min': int(max_hr * 0.9), 'max': max_hr,
             'desc': 'Maximum effort intervals only. Short bursts (30sec - 5min).', 'class': 'zone5', 'primary': False}
        ]

        html = "<h2>💓 Training Zones</h2>\n<div class=\"zone-cards\">\n"

        for zone in zones:
            primary_badge = '<span class="primary-badge">⭐ PRIMARY ZONE</span>' if zone['primary'] else ''
            html += f"""
    <div class="zone-card {zone['class']}">
        <div class="zone-icon">{zone['icon']}</div>
        <div class="zone-info">
            <div class="zone-name">{zone['name']}{primary_badge}</div>
            <div class="zone-hr">{zone['min']}-{zone['max']} bpm</div>
            <div class="zone-description">{zone['desc']}</div>
        </div>
    </div>
"""

        html += "</div>\n"
        return html

    def _generate_weekly_training_plan(self):
        """Generate weekly training plan grid"""
        return """
<h2>📅 Weekly Training Plan</h2>
<div class="training-plan">
    <div class="training-card priority-high">
        <div><span class="training-icon">🏃</span><strong>Zone 2 Endurance</strong></div>
        <div>3-4 sessions × 45-60 min</div>
        <span class="priority-badge high">PRIORITY #1</span>
        <div style="font-size:0.9em;margin-top:5px">Improve metabolic rate and fat-burning</div>
    </div>
    <div class="training-card">
        <div><span class="training-icon">💪</span><strong>Resistance Training</strong></div>
        <div>3 sessions × 45-60 min</div>
        <span class="priority-badge high">HIGH</span>
        <div style="font-size:0.9em;margin-top:5px">Maintain strength development focus</div>
    </div>
    <div class="training-card">
        <div><span class="training-icon">🏋</span><strong>Zone 4 Threshold</strong></div>
        <div>1-2 sessions × 20-30 min</div>
        <span class="priority-badge medium">MEDIUM</span>
        <div style="font-size:0.9em;margin-top:5px">Support strength development goals</div>
    </div>
    <div class="training-card">
        <div><span class="training-icon">😴</span><strong>Rest/Recovery</strong></div>
        <div>1-2 days per week</div>
        <span class="priority-badge low">LOW</span>
        <div style="font-size:0.9em;margin-top:5px">Zone 1 activity</div>
    </div>
</div>
"""

    def _generate_interventions(self):
        """Generate interventions grid"""
        return f"""
<h2>🎯 Recommended Interventions</h2>
<p class="text-center" style="font-style:italic;color:#666;font-size:0.95em;margin:5px 0">Targeted strategies for your specific needs</p>
<div class="interventions-grid">
    <div class="intervention-card">
        <div class="intervention-icon">🏃</div>
        <strong>Zone 2 Training</strong>
        <div style="margin:6px 0;font-size:0.85em">Primary intervention for metabolic rate & fat-burning</div>
        <span class="evidence-badge">Evidence-Based</span>
    </div>
    <div class="intervention-card">
        <img src="{self.ARX_IMAGE}" alt="ARX Training">
        <strong>ARX Omni</strong>
        <div style="margin:6px 0;font-size:0.85em">Efficient resistance training for strength goals</div>
        <span class="evidence-badge">Evidence-Based</span>
    </div>
    <div class="intervention-card">
        <img src="{self.COLD_PLUNGE_IMAGE}" alt="Cold Plunge">
        <strong>Cold Plunge</strong>
        <div style="margin:6px 0;font-size:0.85em">Boost fat-burning 15-37%, accelerate recovery</div>
        <span class="evidence-badge">Evidence-Based</span>
    </div>
    <div class="intervention-card">
        <img src="{self.NUTRITION_IMAGE}" alt="Nutrition">
        <strong>Nutrition Protocol</strong>
        <div style="margin:6px 0;font-size:0.85em">High protein (1.6-2.2g/kg) for muscle & metabolism</div>
        <span class="evidence-badge">Evidence-Based</span>
    </div>
    <div class="intervention-card">
        <img src="{self.BREATHWORK_IMAGE}" alt="Breathwork">
        <strong>Breathwork Training</strong>
        <div style="margin:6px 0;font-size:0.85em">Optimize breathing coordination (currently {self.core_scores.get('breathing_coord', 67)}%)</div>
        <span class="evidence-badge">Evidence-Based</span>
    </div>
    <div class="intervention-card">
        <div class="intervention-icon">♨️</div>
        <strong>Sauna Recovery</strong>
        <div style="margin:6px 0;font-size:0.85em">Improve HRV and parasympathetic activation</div>
        <span class="evidence-badge">Evidence-Based</span>
    </div>
</div>
"""

    def _generate_action_plan(self):
        """Generate auto-numbered action plan"""
        return """
<h2>✅ Action Plan - Prioritized Roadmap</h2>
<div class="action-plan">
    <div class="action-item">
        <div class="action-number"></div>
        <div>
            <strong>Zone 2 Endurance Training</strong> <span class="priority-badge high">HIGH</span>
            <div style="margin-top:5px">3-4 sessions, 45-60 min at appropriate heart rate. Most powerful intervention for improving metabolic rate and fat-burning.</div>
        </div>
    </div>
    <div class="action-item">
        <div class="action-number"></div>
        <div>
            <strong>Strength Training</strong> <span class="priority-badge high">HIGH</span>
            <div style="margin-top:5px">Continue 3x weekly resistance work for strength development. Add compound movements to support metabolic rate increase.</div>
        </div>
    </div>
    <div class="action-item">
        <div class="action-number"></div>
        <div>
            <strong>Performance Nutrition</strong> <span class="priority-badge medium">MEDIUM</span>
            <div style="margin-top:5px">High protein intake, omega-3 rich fish 3x/week. Time carbs around workouts for performance.</div>
        </div>
    </div>
    <div class="action-item">
        <div class="action-number"></div>
        <div>
            <strong>Recovery Optimization</strong> <span class="priority-badge medium">MEDIUM</span>
            <div style="margin-top:5px">7-9 hours nightly sleep. Consistent schedule. Maintain excellent HRV through proper recovery.</div>
        </div>
    </div>
    <div class="action-item">
        <div class="action-number"></div>
        <div>
            <strong>Cold Exposure</strong> <span class="priority-badge low">LOW</span>
            <div style="margin-top:5px">Cold plunges 3-5 min, 2-3x weekly. Can boost fat-burning by 15-37%.</div>
        </div>
    </div>
    <div class="action-item">
        <div class="action-number"></div>
        <div>
            <strong>Breathwork Practice</strong> <span class="priority-badge low">LOW</span>
            <div style="margin-top:5px">10 min daily box breathing to optimize breathing coordination.</div>
        </div>
    </div>
</div>
"""

    def _generate_90day_protocol(self):
        """Generate 90-day protocol with timeline visualization"""
        return """
<h2>📅 90-Day Performance Protocol</h2>
<div class="timeline-visual">
    <div class="timeline-line"></div>
    <div class="timeline-phase">
        <div class="phase-weeks">Weeks 1-4: Base Building Phase</div>
        <p>Add 2-3 Zone 2 sessions (45 min) alongside strength training. Monitor heart rate compliance. Focus on easy conversational pace.</p>
    </div>
    <div class="timeline-phase">
        <div class="phase-weeks">Weeks 5-8: Development Phase</div>
        <p>Increase to 3-4 Zone 2 sessions (60 min). Continue strength training 3x/week. Add cold plunges 2x/week. Implement performance nutrition timing.</p>
    </div>
    <div class="timeline-phase">
        <div class="phase-weeks">Weeks 9-12: Integration Phase</div>
        <p>Maintain 4x Zone 2 sessions. Add 1x Zone 4 threshold session. Continue all protocols. Monitor performance gains in strength training.</p>
    </div>
    <div class="timeline-phase retest">
        <div class="phase-weeks">Week 13: Retest & Reassess</div>
        <p><strong>Expected Results:</strong> Metabolic Rate: 46% → 70%+ | Fat-Burning: 58% → 75%+ | Overall Score: 73% → 80%+ | Strength gains + improved endurance capacity</p>
    </div>
</div>
"""

    def generate(self, output_path):
        """Generate the complete compact report"""
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
</body>
</html>
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
