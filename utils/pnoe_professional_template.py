"""
PNOE Professional Metabolic Blueprint Template - PDF OPTIMIZED 2025
Professional "Medical Tech" Styling
Color Palette: Deep Emerald (Primary), Indigo (Performance), Teal (Longevity)
Optimized for Print/PDF with CSS-only visualizations (no JS dependency for core visuals)
"""
import json
from datetime import datetime

class PNOEProfessionalReport:
    """Generate professional PNOE-style metabolic blueprint reports"""

    # Stock images for professional appearance (High Res)
    HERO_IMAGE = "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=1600&h=600&fit=crop&q=80"
    TRAINING_IMAGE = "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800&q=80"
    ARX_IMAGE = "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800&q=80"
    COLD_PLUNGE_IMAGE = "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&q=80"
    NUTRITION_IMAGE = "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800&q=80"
    BREATHWORK_IMAGE = "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&q=80"

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
        self.peptide_recommendations = []
        self.peptide_html = ''
        self.longevity_score = None

    def _get_score_status(self, score):
        """Get status label and color for a score"""
        if score >= 80:
            return ('EXCELLENT', '#059669', 'excellent') # Emerald-600
        elif score >= 60:
            return ('GOOD', '#2563EB', 'good')      # Blue-600
        else:
            return ('NEUTRAL', '#64748B', 'neutral')   # Slate-500

    def _count_limitations(self):
        distribution = [0, 0, 0, 0, 0] # [Severe, Poor, Limited, Good, Excellent]
        for score in self.core_scores.values():
            if score < 20: distribution[0] += 1
            elif score < 40: distribution[1] += 1
            elif score < 60: distribution[2] += 1
            elif score < 80: distribution[3] += 1
            else: distribution[4] += 1
        return distribution

    def _calculate_overall_score(self):
        if not self.core_scores: return 0
        return round(sum(self.core_scores.values()) / len(self.core_scores))
    
    def _calculate_longevity_score(self):
        if not self.core_scores: return 0
        weights = {'hrv': 1.5, 'metabolic_rate': 1.5, 'fat_burning': 1.2}
        total_score = 0
        total_weight = 0
        for key, score in self.core_scores.items():
            w = weights.get(key, 1.0)
            total_score += score * w
            total_weight += w
        return round(total_score / total_weight)

    def _get_styles(self):
        """Return PDF-Optimized CSS"""
        return """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #0F766E; /* Deep Teal */
    --secondary: #4338CA; /* Indigo */
    --accent: #0D9488; /* Teal */
    --bg-light: #F8FAFC;
    --text-dark: #1E293B;
    --text-light: #64748B;
    --border: #E2E8F0;
    --white: #FFFFFF;
}

* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }

body { 
    max-width: 900px; 
    margin: 0 auto; 
    padding: 0; 
    font-family: 'Inter', sans-serif;
    line-height: 1.5; 
    background: var(--bg-light); 
    font-size: 14px; 
    color: var(--text-dark);
}

/* Page Break & Layout Control */
@page { margin: 0.5in; size: letter; }
.page-break { page-break-before: always; }
.no-break { page-break-inside: avoid; }

/* CONTAINERS */
.container { padding: 40px; }
.card { 
    background: var(--white); 
    border-radius: 12px; 
    padding: 25px; 
    margin-bottom: 25px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); 
    border: 1px solid var(--border);
}

/* HEADER - Professional Medical Style */
.header { 
    background: linear-gradient(135deg, #0F766E 0%, #115E59 100%);
    color: white;
    padding: 40px;
    border-radius: 0 0 20px 20px;
    margin-bottom: 40px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.header-top { display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 20px; margin-bottom: 20px; }
.brand { font-size: 1.5em; font-weight: 800; letter-spacing: -0.02em; display: flex; align-items: center; gap: 10px; }
.report-meta { text-align: right; font-size: 0.9em; opacity: 0.9; }
.main-title { font-size: 2.5em; font-weight: 800; margin: 0; line-height: 1.1; }
.subtitle { font-size: 1.1em; opacity: 0.9; margin-top: 10px; font-weight: 300; }

/* TYPOGRAPHY */
h2 { 
    color: var(--primary); 
    font-size: 1.5em; 
    margin: 30px 0 15px 0; 
    font-weight: 700; 
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 10px;
}
h2 svg { width: 24px; height: 24px; stroke: currentColor; }

h3 { color: var(--secondary); font-size: 1.1em; margin: 0 0 10px 0; font-weight: 600; }

/* PATIENT INFO GRID */
.patient-grid { 
    display: grid; 
    grid-template-columns: repeat(4, 1fr); 
    gap: 15px; 
    margin-bottom: 30px; 
}
.info-item { 
    background: white; 
    padding: 15px; 
    border-radius: 8px; 
    border: 1px solid var(--border);
    border-left: 4px solid var(--primary);
}
.info-label { font-size: 0.75em; text-transform: uppercase; color: var(--text-light); letter-spacing: 0.05em; font-weight: 600; }
.info-value { font-size: 1.1em; font-weight: 700; color: var(--text-dark); margin-top: 4px; }

/* DUAL SCORE CARDS */
.score-container { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 30px; }
.score-box { 
    background: white; 
    border-radius: 16px; 
    padding: 30px; 
    text-align: center; 
    border: 1px solid var(--border);
    position: relative;
    overflow: hidden;
}
.score-box.perf { border-top: 6px solid #4F46E5; }
.score-box.long { border-top: 6px solid #0F766E; }

/* CSS-ONLY CIRCULAR CHART (Print Friendly) */
.css-pie {
    width: 140px; height: 140px;
    border-radius: 50%;
    background: conic-gradient(var(--c) calc(var(--p)*1%), #F1F5F9 0);
    margin: 0 auto 15px;
    display: flex; align-items: center; justify-content: center;
    position: relative;
}
.css-pie::before {
    content: ''; position: absolute;
    width: 110px; height: 110px;
    background: white; border-radius: 50%;
}
.pie-value { position: relative; font-size: 3em; font-weight: 800; line-height: 1; z-index: 10; }
.pie-label { font-size: 0.9em; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }

/* BIOLOGICAL AGE - Modern Timeline */
.bio-age-card { 
    background: linear-gradient(to right, #FFF1F2, #FFFFFF); 
    border: 1px solid #FECDD3; 
    border-left: 6px solid #E11D48;
}
.bio-timeline { 
    display: flex; 
    align-items: center; 
    justify-content: space-between; 
    margin: 20px 0; 
    position: relative; 
    padding: 0 40px;
}
.bio-timeline::before {
    content: ''; position: absolute; left: 50px; right: 50px; top: 50%; height: 2px;
    background: #E2E8F0; z-index: 0;
}
.bio-point { 
    position: relative; 
    z-index: 1; 
    background: white; 
    padding: 10px 20px; 
    border-radius: 30px; 
    border: 2px solid #E2E8F0; 
    text-align: center;
    min-width: 120px;
}
.bio-point.current { border-color: #E11D48; box-shadow: 0 4px 12px rgba(225, 29, 72, 0.15); }
.bio-num { font-size: 1.8em; font-weight: 800; display: block; line-height: 1; }
.bio-txt { font-size: 0.8em; font-weight: 600; text-transform: uppercase; color: var(--text-light); }
.bio-arrow { font-size: 1.5em; color: #E11D48; z-index: 1; background: white; padding: 0 10px; }

/* SUMMARY SQUARES */
.summary-squares { display: flex; gap: 8px; margin-top: 15px; }
.sq-box { 
    flex: 1; 
    height: 45px; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    color: white; 
    font-weight: 700; 
    font-size: 1.2em; 
    border-radius: 6px; 
    position: relative;
}
.sq-label {
    position: absolute; bottom: -20px; left: 0; right: 0;
    text-align: center; font-size: 0.7em; color: var(--text-light); font-weight: 500;
}

/* METRIC BARS - Clean & Flat */
.metric-item { margin-bottom: 18px; }
.metric-top { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 0.95em; font-weight: 600; }
.bar-bg { height: 10px; background: #F1F5F9; border-radius: 5px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 5px; }

/* PILLARS & ZONES - Grid Layouts */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
.grid-4 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }

.icon-card { 
    background: white; border: 1px solid var(--border); 
    border-radius: 10px; padding: 20px; 
    transition: transform 0.2s;
}
.icon-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; color: var(--primary); font-weight: 700; font-size: 1.1em; }
.icon-body { font-size: 0.9em; color: var(--text-light); line-height: 1.4; }

/* ZONES */
.zone-box { text-align: center; padding: 15px; border-radius: 10px; background: white; border: 1px solid var(--border); }
.zone-box.primary { border: 2px solid #10B981; background: #ECFDF5; }
.zone-bpm { font-size: 1.4em; font-weight: 800; color: var(--text-dark); margin: 5px 0; }
.zone-name { font-size: 0.8em; text-transform: uppercase; font-weight: 700; color: var(--text-light); }

/* CALORIC VISUALS */
.caloric-visual { display: flex; align-items: flex-end; gap: 20px; height: 150px; padding-bottom: 20px; border-bottom: 1px solid var(--border); }
.c-bar-group { flex: 1; display: flex; flex-direction: column; justify-content: flex-end; gap: 5px; height: 100%; }
.c-bar { width: 100%; border-radius: 4px 4px 0 0; position: relative; min-height: 20px; transition: height 0.5s; }
.c-val { position: absolute; top: -25px; left: 0; right: 0; text-align: center; font-weight: 700; font-size: 0.9em; }
.c-label { text-align: center; font-size: 0.8em; font-weight: 600; margin-top: 10px; color: var(--text-light); }

/* FUEL DONUT (CSS Only) */
.fuel-donut { 
    width: 120px; height: 120px; border-radius: 50%; margin: 0 auto;
    background: conic-gradient(#10B981 0% var(--fat), #3B82F6 var(--fat) 100%);
    position: relative;
    display: flex; align-items: center; justify-content: center;
}
.fuel-donut::before { content: ''; position: absolute; width: 80px; height: 80px; background: white; border-radius: 50%; }
.fuel-legend { display: flex; justify-content: center; gap: 20px; margin-top: 15px; font-size: 0.9em; }
.dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 5px; }

/* ACTION PLAN */
.roadmap { position: relative; padding-left: 30px; border-left: 2px solid #E2E8F0; margin-left: 15px; }
.road-item { position: relative; margin-bottom: 30px; }
.road-dot { 
    position: absolute; left: -39px; top: 0; 
    width: 16px; height: 16px; 
    background: var(--primary); border: 4px solid white; 
    border-radius: 50%; box-shadow: 0 0 0 1px #E2E8F0; 
}
.road-content { background: white; border: 1px solid var(--border); border-radius: 8px; padding: 15px; }
.tag { font-size: 0.7em; padding: 3px 8px; border-radius: 12px; font-weight: 700; text-transform: uppercase; float: right; }
.tag.high { background: #FEE2E2; color: #BE123C; }
.tag.med { background: #FEF3C7; color: #B45309; }

/* UTILS */
.text-center { text-align: center; }
.mb-20 { margin-bottom: 20px; }
.text-primary { color: var(--primary); }
"""

    def _generate_header(self):
        return f"""
<div class="header">
    <div class="header-top">
        <div class="brand">
            <span style="font-size:1.8em;">⚡</span>
            <div>OPTIMAL VITALITY<br><span style="font-size:0.6em;font-weight:400;opacity:0.8;letter-spacing:1px;">PERFORMANCE MEDICINE</span></div>
        </div>
        <div class="report-meta">
            DATE: {self.patient_info['test_date']}<br>
            ID: {self.patient_info.get('name', '').replace(' ','').upper()[:8]}
        </div>
    </div>
    <h1 class="main-title">Complete Metabolic Blueprint</h1>
    <div class="subtitle">Advanced Physiology & Longevity Analysis</div>
</div>
"""

    def _generate_patient_info(self):
        weight_lbs = round(self.patient_info['weight_kg'] * 2.20462, 1)
        height_ft = self.patient_info['height_cm'] // 30.48
        height_in = round((self.patient_info['height_cm'] % 30.48) / 2.54)
        
        return f"""
<div class="patient-grid">
    <div class="info-item">
        <div class="info-label">Patient Name</div>
        <div class="info-value">{self.patient_info['name']}</div>
    </div>
    <div class="info-item">
        <div class="info-label">Age / Gender</div>
        <div class="info-value">{self.patient_info['age']} / {self.patient_info['gender']}</div>
    </div>
    <div class="info-item">
        <div class="info-label">Body Metrics</div>
        <div class="info-value">{weight_lbs} lbs / {height_ft}'{height_in}"</div>
    </div>
    <div class="info-item">
        <div class="info-label">Facility</div>
        <div class="info-value">{self.patient_info.get('facility', 'Optimal Vitality')}</div>
    </div>
</div>
"""

    def _generate_executive_summary(self):
        perf_score = self._calculate_overall_score()
        long_score = self.longevity_score if self.longevity_score else self._calculate_longevity_score()
        
        return f"""
<div class="score-container">
    <div class="score-box perf">
        <h3>Performance Score</h3>
        <div class="css-pie" style="--p:{perf_score}; --c:#4F46E5">
            <span class="pie-value" style="color:#4F46E5">{perf_score}</span>
        </div>
        <div class="pie-label" style="color:#4F46E5">Excellent</div>
    </div>
    <div class="score-box long">
        <h3>Longevity Score</h3>
        <div class="css-pie" style="--p:{long_score}; --c:#0F766E">
            <span class="pie-value" style="color:#0F766E">{long_score}</span>
        </div>
        <div class="pie-label" style="color:#0F766E">Good</div>
    </div>
</div>
"""

    def _generate_biological_age(self):
        age_diff = self.biological_age - self.chronological_age
        status_color = "#E11D48" if age_diff > 0 else "#10B981"
        arrow = "→"

        # Calculate VO2 max potential scenarios
        chrono = self.chronological_age
        scenarios = [
            {"vo2": "Average", "percentile": "50th", "bio_age": chrono, "diff": 0},
            {"vo2": "Good", "percentile": "75th", "bio_age": max(20, chrono - 6), "diff": -6},
            {"vo2": "Excellent", "percentile": "90th", "bio_age": max(20, chrono - 11), "diff": -11},
            {"vo2": "Elite", "percentile": "95th+", "bio_age": max(20, chrono - 16), "diff": -16},
        ]

        return f"""
<div class="card bio-age-card no-break">
    <h2 style="margin-top:0; color:#BE123C">🧬 Biological Age Analysis</h2>
    <div class="bio-timeline">
        <div class="bio-point">
            <span class="bio-num" style="color:#64748B">{self.chronological_age}</span>
            <span class="bio-txt">Chronological</span>
        </div>
        <div class="bio-arrow">{arrow}</div>
        <div class="bio-point current" style="border-color:{status_color}">
            <span class="bio-num" style="color:{status_color}">{self.biological_age}</span>
            <span class="bio-txt">Biological Age</span>
        </div>
    </div>
    <div class="text-center" style="font-weight:600; color:{status_color}; margin-bottom:15px;">
        {f"{age_diff} years older" if age_diff > 0 else f"{abs(age_diff)} years younger"} than your calendar age.
    </div>

    <div style="background:#F8FAFC; border-radius:8px; padding:15px; margin-top:15px;">
        <h3 style="margin:0 0 10px 0; font-size:1em; color:#475569;">📊 How We Calculate Biological Age</h3>
        <p style="font-size:0.85em; color:#64748B; margin:0 0 12px 0; line-height:1.5;">
            Your biological age is calculated using a methodology aligned with the <strong>American Heart Association</strong> research.
            The primary factor is <strong>VO2 max</strong> (cardiorespiratory fitness) - the single best predictor of longevity.
            Secondary factors include fat-burning efficiency, metabolic rate, and your core performance scores.
        </p>

        <h4 style="margin:15px 0 8px 0; font-size:0.9em; color:#475569;">🎯 Your VO2 Max Potential</h4>
        <p style="font-size:0.8em; color:#64748B; margin:0 0 10px 0;">
            A VO2 max exercise test would give you the most accurate biological age. Here's what different fitness levels mean for your age:
        </p>

        <table style="width:100%; border-collapse:collapse; font-size:0.8em;">
            <thead>
                <tr style="background:#E2E8F0;">
                    <th style="padding:8px; text-align:left; border-radius:4px 0 0 0;">Fitness Level</th>
                    <th style="padding:8px; text-align:center;">Percentile</th>
                    <th style="padding:8px; text-align:center;">Bio Age</th>
                    <th style="padding:8px; text-align:right; border-radius:0 4px 0 0;">Difference</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background:#FEE2E2;">
                    <td style="padding:8px;">Below Average</td>
                    <td style="padding:8px; text-align:center;">&lt;50th</td>
                    <td style="padding:8px; text-align:center; color:#E11D48;">{chrono + 5}+</td>
                    <td style="padding:8px; text-align:right; color:#E11D48;">5+ years older</td>
                </tr>
                <tr>
                    <td style="padding:8px;">Average</td>
                    <td style="padding:8px; text-align:center;">50th</td>
                    <td style="padding:8px; text-align:center;">{chrono}</td>
                    <td style="padding:8px; text-align:right;">Same as calendar</td>
                </tr>
                <tr style="background:#DBEAFE;">
                    <td style="padding:8px;">Good</td>
                    <td style="padding:8px; text-align:center;">75th</td>
                    <td style="padding:8px; text-align:center; color:#3B82F6;">{max(20, chrono - 6)}</td>
                    <td style="padding:8px; text-align:right; color:#3B82F6;">6 years younger</td>
                </tr>
                <tr style="background:#D1FAE5;">
                    <td style="padding:8px;">Excellent</td>
                    <td style="padding:8px; text-align:center;">90th</td>
                    <td style="padding:8px; text-align:center; color:#10B981;">{max(20, chrono - 11)}</td>
                    <td style="padding:8px; text-align:right; color:#10B981;">11 years younger</td>
                </tr>
                <tr style="background:#BBF7D0;">
                    <td style="padding:8px; font-weight:600;">Elite Athlete</td>
                    <td style="padding:8px; text-align:center;">95th+</td>
                    <td style="padding:8px; text-align:center; color:#059669; font-weight:600;">{max(20, chrono - 16)}</td>
                    <td style="padding:8px; text-align:right; color:#059669; font-weight:600;">16+ years younger</td>
                </tr>
            </tbody>
        </table>

        <p style="font-size:0.75em; color:#94A3B8; margin:10px 0 0 0; font-style:italic;">
            💡 Tip: To improve your biological age, focus on Zone 2 cardio training (3-4x/week, 45-60 min) and strength training.
            A VO2 max test will give you the most accurate measurement.
        </p>
    </div>
</div>
"""

    def _generate_overview_summary(self):
        dist = self._count_limitations()
        return f"""
<div class="card no-break">
    <h2>📊 Overview Summary</h2>
    <p class="subtitle" style="margin-bottom:20px">Distribution of metabolic limitations across core systems.</p>
    <div class="summary-squares">
        <div class="sq-box" style="background:#EF4444">{dist[0]}<div class="sq-label">Severe</div></div>
        <div class="sq-box" style="background:#F97316">{dist[1]}<div class="sq-label">Poor</div></div>
        <div class="sq-box" style="background:#F59E0B">{dist[2]}<div class="sq-label">Limited</div></div>
        <div class="sq-box" style="background:#3B82F6">{dist[3]}<div class="sq-label">Good</div></div>
        <div class="sq-box" style="background:#10B981">{dist[4]}<div class="sq-label">Excellent</div></div>
    </div>
</div>
"""

    def _generate_core_metrics(self):
        labels = {
            'symp_parasym': 'Nervous System Balance',
            'ventilation_eff': 'Ventilation Efficiency',
            'breathing_coord': 'Breathing Coordination',
            'lung_util': 'Lung Utilization',
            'hrv': 'Heart Rate Variability',
            'metabolic_rate': 'Metabolic Rate',
            'fat_burning': 'Fat Burning Efficiency'
        }
        
        html = """
<div class="card no-break">
    <h2>📈 Core Metrics Analysis</h2>
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:30px;">
        <div>
"""
        # Split metrics into two columns
        items = list(self.core_scores.items())
        mid = (len(items) + 1) // 2
        
        for i, (key, score) in enumerate(items):
            if i == mid:
                html += "</div><div>"
                
            label = labels.get(key, key.replace('_', ' ').title())
            color = self._get_score_status(score)[1]
            
            html += f"""
            <div class="metric-item">
                <div class="metric-top">
                    <span>{label}</span>
                    <span style="color:{color}">{score}%</span>
                </div>
                <div class="bar-bg">
                    <div class="bar-fill" style="width:{score}%; background:{color}"></div>
                </div>
            </div>
            """
            
        html += "</div></div></div>"
        return html

    def _generate_pillars_of_longevity(self):
        return f"""
<div class="card no-break">
    <h2>🏛️ Pillars of Longevity</h2>
    <div class="grid-2">
        <div class="icon-card">
            <div class="icon-header">🧠 Mental Status</div>
            <div class="icon-body">Fundamental pillar of wellness; healthy mind drives healthy choices.</div>
        </div>
        <div class="icon-card">
            <div class="icon-header">❤️ Heart Fitness</div>
            <div class="icon-body">Critical for wellness; CV dysfunction is a major mortality risk.</div>
        </div>
        <div class="icon-card">
            <div class="icon-header">🫁 Lung Fitness</div>
            <div class="icon-body">High lung fitness is essential for oxygen delivery and longevity.</div>
        </div>
        <div class="icon-card">
            <div class="icon-header">🦴 Posture</div>
            <div class="icon-body">Spinal health drives quality of life and breathing mechanics.</div>
        </div>
    </div>
</div>
"""

    def _generate_training_zones(self):
        max_hr = 220 - self.chronological_age
        zones = [
            {'name': 'Zone 1', 'desc': 'Recovery', 'range': f"{int(max_hr*0.5)}-{int(max_hr*0.6)}", 'class': ''},
            {'name': 'Zone 2', 'desc': 'Endurance', 'range': f"{int(max_hr*0.6)}-{int(max_hr*0.7)}", 'class': 'primary'},
            {'name': 'Zone 3', 'desc': 'Tempo', 'range': f"{int(max_hr*0.7)}-{int(max_hr*0.8)}", 'class': ''},
            {'name': 'Zone 4', 'desc': 'Threshold', 'range': f"{int(max_hr*0.8)}-{int(max_hr*0.9)}", 'class': ''},
            {'name': 'Zone 5', 'desc': 'VO2 Max', 'range': f"{int(max_hr*0.9)}-{max_hr}", 'class': ''}
        ]
        
        html = f"""
<div class="card no-break">
    <h2>🏃 Training Zones</h2>
    <div class="grid-3" style="grid-template-columns: repeat(5, 1fr);">
"""
        for z in zones:
            html += f"""
        <div class="zone-box {z['class']}">
            <div class="zone-name" style="color:{'#10B981' if z['class'] else '#64748B'}">{z['name']}</div>
            <div class="zone-bpm">{z['range']}</div>
            <div style="font-size:0.7em; font-weight:600;">{z['desc']}</div>
        </div>
"""
        html += "</div></div>"
        return html

    def _generate_caloric_balance(self):
        # Scale for visual bars (max value)
        max_val = max(self.caloric_data['eat_workout'], 3000)
        
        def get_h(val):
            return int((val / max_val) * 100)
            
        return f"""
<div class="card no-break">
    <h2>🔥 Metabolism & Fuel</h2>
    <div class="grid-2">
        <div>
            <h3>Daily Energy Balance</h3>
            <div class="caloric-visual">
                <div class="c-bar-group">
                    <div class="c-val" style="color:#F97316">{self.caloric_data['burn_rest']}</div>
                    <div class="c-bar" style="height:{get_h(self.caloric_data['burn_rest'])}%; background:#F97316"></div>
                    <div class="c-label">Burn<br>(Rest)</div>
                </div>
                <div class="c-bar-group">
                    <div class="c-val" style="color:#F59E0B">{self.caloric_data['eat_rest']}</div>
                    <div class="c-bar" style="height:{get_h(self.caloric_data['eat_rest'])}%; background:#F59E0B"></div>
                    <div class="c-label">Eat<br>(Rest)</div>
                </div>
                <div class="c-bar-group">
                    <div class="c-val" style="color:#10B981">{self.caloric_data['eat_workout']}</div>
                    <div class="c-bar" style="height:{get_h(self.caloric_data['eat_workout'])}%; background:#10B981"></div>
                    <div class="c-label">Eat<br>(Workout)</div>
                </div>
            </div>
        </div>
        <div>
            <h3>Fuel Efficiency</h3>
            <div class="fuel-donut" style="--fat:{self.caloric_data['fat_percent']}%;">
                <div class="text-center">
                    <div style="font-size:0.8em; color:#64748B">FAT BURN</div>
                    <div style="font-size:1.5em; font-weight:800; color:#10B981">{self.caloric_data['fat_percent']}%</div>
                </div>
            </div>
            <div class="fuel-legend">
                <div><span class="dot" style="background:#10B981"></span>Fats</div>
                <div><span class="dot" style="background:#3B82F6"></span>Carbs</div>
            </div>
        </div>
    </div>
</div>
"""

    def _generate_interventions(self):
        return f"""
<div class="card no-break page-break">
    <h2>💪 Recommended Interventions</h2>
    <div class="grid-3">
        <div class="int-card">
            <img src="{self.TRAINING_IMAGE}" class="int-img" style="width:100%; height:120px; object-fit:cover; border-radius:8px; margin-bottom:10px;">
            <div style="font-weight:700; color:#0F766E">Zone 2 Training</div>
            <div style="font-size:0.85em">3-4 sessions/week</div>
        </div>
        <div class="int-card">
            <img src="{self.COLD_PLUNGE_IMAGE}" class="int-img" style="width:100%; height:120px; object-fit:cover; border-radius:8px; margin-bottom:10px;">
            <div style="font-weight:700; color:#0F766E">Cold Plunge</div>
            <div style="font-size:0.85em">Metabolic activation</div>
        </div>
        <div class="int-card">
            <img src="{self.NUTRITION_IMAGE}" class="int-img" style="width:100%; height:120px; object-fit:cover; border-radius:8px; margin-bottom:10px;">
            <div style="font-weight:700; color:#0F766E">High Protein</div>
            <div style="font-size:0.85em">1.6-2.2g/kg bodyweight</div>
        </div>
    </div>
</div>
"""

    def _generate_action_roadmap(self):
        return """
<div class="card no-break">
    <h2>✅ 90-Day Action Roadmap</h2>
    <div class="roadmap">
        <div class="road-item">
            <div class="road-dot"></div>
            <div class="road-content">
                <span class="tag high">High Priority</span>
                <h3>Zone 2 Endurance Base</h3>
                <p style="font-size:0.9em; color:#4B5563">Establish 3-4 weekly sessions of 45-60 mins. This is the primary driver for mitochondrial efficiency.</p>
            </div>
        </div>
        <div class="road-item">
            <div class="road-dot"></div>
            <div class="road-content">
                <span class="tag high">High Priority</span>
                <h3>Strength Protocol</h3>
                <p style="font-size:0.9em; color:#4B5563">Maintain 3x weekly resistance training to support metabolic rate and glucose disposal.</p>
            </div>
        </div>
        <div class="road-item">
            <div class="road-dot"></div>
            <div class="road-content">
                <span class="tag med">Medium Priority</span>
                <h3>Recovery & Sleep</h3>
                <p style="font-size:0.9em; color:#4B5563">Optimize circadian rhythm with morning sunlight and consistent sleep schedule to boost HRV.</p>
            </div>
        </div>
    </div>
</div>
"""

    def _generate_disclaimer(self):
        return """
<div style="font-size:0.8em; color:#94A3B8; text-align:center; padding:20px; border-top:1px solid #E2E8F0; margin-top:40px;">
    <strong>MEDICAL DISCLAIMER:</strong> This report is for informational purposes only and does not constitute medical advice, diagnosis, or treatment. 
    Always consult with a qualified healthcare provider before initiating any new exercise or nutrition program.
    <br><br>
    © 2025 Optimal Vitality. Powered by PNOE.
</div>
"""

    def generate(self, output_path):
        """Generate the complete compact report"""
        if not self.longevity_score:
            self.longevity_score = self._calculate_longevity_score()
            
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metabolic Blueprint - {self.patient_info.get('name', 'Patient')}</title>
    <style>
{self._get_styles()}
    </style>
</head>
<body>
{self._generate_header()}
{self._generate_patient_info()}
{self._generate_executive_summary()}
{self._generate_biological_age()}
{self._generate_overview_summary()}
{self._generate_core_metrics()}
{self._generate_pillars_of_longevity()}
<div class="page-break"></div>
{self._generate_training_zones()}
{self._generate_caloric_balance()}
{self._generate_interventions()}
{self._generate_action_roadmap()}
{self.peptide_html if self.peptide_html else ''}
{self._generate_disclaimer()}
</body>
</html>
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
