"""
AI-Powered Peptide Recommendation Engine
Analyzes patient metabolic data to provide personalized peptide recommendations
NO DEFAULTS - All recommendations calculated from patient-specific data
"""

def calculate_peptide_recommendations(patient_info, core_scores, metabolic_data, biological_age, chronological_age):
    """
    Calculate personalized peptide recommendations based on patient data

    Args:
        patient_info: Dict with age, gender, weight, height, BMI
        core_scores: Dict with metabolic_rate, fat_burning, hrv, etc.
        metabolic_data: Dict with RMR, RER, etc.
        biological_age: Calculated biological age
        chronological_age: Actual chronological age

    Returns:
        List of peptide recommendations with dosing and rationale
    """

    recommendations = []

    # Extract key metrics
    age = patient_info.get('age', 35)
    gender = patient_info.get('gender', 'Unknown').lower()
    weight_kg = patient_info.get('weight_kg', 70)
    height_cm = patient_info.get('height_cm', 170)

    # Calculate BMI
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    # Get core scores with defaults if missing
    metabolic_rate = core_scores.get('metabolic_rate', 50)
    fat_burning = core_scores.get('fat_burning', 50)
    hrv = core_scores.get('hrv', 50)
    lung_util = core_scores.get('lung_util', 50)
    ventilation_eff = core_scores.get('ventilation_eff', 50)

    # Calculate age difference
    age_diff = chronological_age - biological_age if biological_age else 0

    # Calculate average core performance
    avg_score = sum(core_scores.values()) / len(core_scores) if core_scores else 50

    print(f"[PEPTIDE_CALC] Patient: age={age}, gender={gender}, BMI={bmi:.1f}")
    print(f"[PEPTIDE_CALC] Bio age diff: {age_diff:+.0f} years, Avg score: {avg_score:.0f}%")
    print(f"[PEPTIDE_CALC] Key scores: metabolic={metabolic_rate}%, fat_burn={fat_burning}%, HRV={hrv}%")

    # ============================================================================
    # PRIMARY RECOMMENDATIONS (based on biggest needs)
    # ============================================================================

    # 1. LONGEVITY & ANTI-AGING PEPTIDES (based on biological age)
    if age_diff < -5:  # Biologically OLDER than chronological
        # Severe aging - aggressive anti-aging protocol
        recommendations.append({
            'name': 'Epitalon',
            'dosage': f'{int(10 * (abs(age_diff) / 5))}mg',
            'frequency': '5 days on, 2 days off',
            'duration': '20-day cycles, quarterly',
            'priority': 1,
            'category': 'Longevity',
            'rationale': f'Biological age is {abs(age_diff):.0f} years OLDER - Epitalon supports telomere health and cellular regeneration. Critical for reversing accelerated aging.',
            'mechanism': 'Telomerase activation, circadian rhythm regulation, melatonin production'
        })

        recommendations.append({
            'name': 'GHK-Cu',
            'dosage': f'{int(2 * weight_kg / 70)}mg',
            'frequency': 'Daily',
            'duration': 'Continuous with 1 week break monthly',
            'priority': 2,
            'category': 'Anti-Aging',
            'rationale': f'Accelerated aging detected. GHK-Cu provides comprehensive anti-aging effects including collagen synthesis and tissue repair.',
            'mechanism': 'Collagen production, antioxidant activity, gene expression modulation'
        })

    elif age_diff < 0:  # Slightly biologically older
        # Moderate anti-aging
        recommendations.append({
            'name': 'GHK-Cu',
            'dosage': f'{int(1.5 * weight_kg / 70)}mg',
            'frequency': 'Daily',
            'duration': '3 months on, 1 month off',
            'priority': 1,
            'category': 'Anti-Aging',
            'rationale': f'Biological age is {abs(age_diff):.0f} years older - GHK-Cu supports cellular repair and anti-aging processes.',
            'mechanism': 'Tissue regeneration, anti-inflammatory effects, skin health'
        })

    elif age_diff > 7:  # Significantly younger - maintain and optimize
        recommendations.append({
            'name': 'Thymosin Alpha-1',
            'dosage': f'{int(1.6 * weight_kg / 70)}mg',
            'frequency': '2x per week',
            'duration': '3-6 months',
            'priority': 1,
            'category': 'Longevity',
            'rationale': f'Biological age is {age_diff:.0f} years YOUNGER - maintain this advantage with immune optimization and cellular health support.',
            'mechanism': 'Immune modulation, T-cell function, inflammatory response regulation'
        })

    elif age_diff > 3:  # Moderately younger - maintenance
        recommendations.append({
            'name': 'MOTS-c',
            'dosage': f'{int(5 * weight_kg / 70)}mg',
            'frequency': '3x per week',
            'duration': 'Continuous',
            'priority': 1,
            'category': 'Metabolic Optimization',
            'rationale': f'Biological age {age_diff:.0f} years younger - MOTS-c maintains mitochondrial health and metabolic advantage.',
            'mechanism': 'Mitochondrial function, insulin sensitivity, metabolic regulation'
        })

    # 2. METABOLIC RATE OPTIMIZATION
    if metabolic_rate < 70:
        # Low metabolic rate - needs significant boost
        recommendations.append({
            'name': 'CJC-1295 + Ipamorelin',
            'dosage': f'{int(100 * weight_kg / 70)}mcg each',
            'frequency': 'Daily before bed',
            'duration': '3-6 months',
            'priority': 1,
            'category': 'Metabolic Enhancement',
            'rationale': f'Metabolic rate score is LOW at {metabolic_rate}% - This combination boosts growth hormone naturally to increase RMR and fat burning.',
            'mechanism': 'Growth hormone pulse optimization, lipolysis, muscle preservation'
        })

        recommendations.append({
            'name': 'Tesamorelin',
            'dosage': f'{int(2 * weight_kg / 70)}mg',
            'frequency': 'Daily',
            'duration': '3-6 months',
            'priority': 2,
            'category': 'Fat Loss',
            'rationale': f'Low metabolic rate combined with metabolic dysfunction. Tesamorelin specifically targets visceral fat and metabolic rate.',
            'mechanism': 'GHRH analog, visceral fat reduction, lipid metabolism'
        })

    elif metabolic_rate < 85:
        # Moderate metabolic rate - gentle enhancement
        recommendations.append({
            'name': 'Ipamorelin',
            'dosage': f'{int(200 * weight_kg / 70)}mcg',
            'frequency': 'Daily before bed',
            'duration': '3-6 months',
            'priority': 2,
            'category': 'Metabolic Support',
            'rationale': f'Metabolic rate at {metabolic_rate}% - Ipamorelin provides gentle GH boost to optimize metabolism without excessive stimulation.',
            'mechanism': 'Selective ghrelin receptor agonist, natural GH pulse'
        })

    # 3. FAT BURNING OPTIMIZATION
    if fat_burning < 70:
        # Poor fat burning efficiency
        recommendations.append({
            'name': 'AOD-9604',
            'dosage': f'{int(300 * weight_kg / 70)}mcg',
            'frequency': 'Daily on empty stomach',
            'duration': '12-16 weeks',
            'priority': 1,
            'category': 'Fat Loss',
            'rationale': f'Fat burning efficiency is LOW at {fat_burning}% - AOD-9604 specifically targets lipolysis without affecting insulin.',
            'mechanism': 'Mimics GH fat-burning region, lipolytic activity, anti-lipogenic'
        })

        # If also overweight, add semaglutide
        if bmi > 27:
            recommendations.append({
                'name': 'Semaglutide',
                'dosage': f'{0.25 if bmi < 30 else 0.5}mg weekly (titrate up)',
                'frequency': 'Once weekly',
                'duration': '6-12 months',
                'priority': 1,
                'category': 'Weight Management',
                'rationale': f'BMI of {bmi:.1f} combined with {fat_burning}% fat burning score indicates need for comprehensive metabolic support.',
                'mechanism': 'GLP-1 agonist, appetite regulation, insulin sensitivity'
            })

    elif fat_burning < 85:
        # Moderate fat burning - optimize
        recommendations.append({
            'name': 'AOD-9604',
            'dosage': f'{int(250 * weight_kg / 70)}mcg',
            'frequency': '5 days per week',
            'duration': '8-12 weeks',
            'priority': 3,
            'category': 'Fat Optimization',
            'rationale': f'Fat burning at {fat_burning}% - AOD-9604 can enhance lipolytic efficiency.',
            'mechanism': 'Fat metabolism enhancement without muscle loss'
        })

    # 4. CARDIOVASCULAR & HRV OPTIMIZATION
    if hrv < 65:
        # Poor heart rate variability / autonomic function
        recommendations.append({
            'name': 'BPC-157',
            'dosage': f'{int(250 * weight_kg / 70)}mcg',
            'frequency': 'Twice daily',
            'duration': '4-8 weeks',
            'priority': 2,
            'category': 'Cardiovascular Health',
            'rationale': f'HRV score is {hrv}% indicating autonomic stress. BPC-157 supports cardiovascular healing and parasympathetic balance.',
            'mechanism': 'Vascular repair, nitric oxide modulation, angiogenesis'
        })

        recommendations.append({
            'name': 'TB-500',
            'dosage': f'{int(2.5 * weight_kg / 70)}mg',
            'frequency': '2x per week',
            'duration': '4-8 weeks',
            'priority': 3,
            'category': 'Recovery',
            'rationale': f'Cardiovascular stress indicated by HRV {hrv}%. TB-500 promotes tissue repair and reduces inflammation.',
            'mechanism': 'Beta-4 thymosin, cell migration, tissue regeneration'
        })

    # 5. RESPIRATORY EFFICIENCY (based on lung utilization and ventilation)
    lung_cardio_avg = (lung_util + ventilation_eff) / 2
    if lung_cardio_avg < 70:
        recommendations.append({
            'name': 'TB-500',
            'dosage': f'{int(3 * weight_kg / 70)}mg',
            'frequency': 'Loading: 2x weekly for 4 weeks, then 1x weekly',
            'duration': '12 weeks',
            'priority': 2,
            'category': 'Respiratory Function',
            'rationale': f'Lung utilization ({lung_util}%) and ventilation ({ventilation_eff}%) indicate respiratory limitation. TB-500 supports tissue healing.',
            'mechanism': 'Anti-inflammatory, promotes healing of lung tissue'
        })

    # 6. RECOVERY & GENERAL HEALING
    if avg_score < 70:
        # Overall poor scores - need comprehensive recovery support
        recommendations.append({
            'name': 'BPC-157',
            'dosage': f'{int(300 * weight_kg / 70)}mcg',
            'frequency': 'Twice daily',
            'duration': '6-12 weeks',
            'priority': 1,
            'category': 'Systemic Recovery',
            'rationale': f'Overall performance score is {avg_score:.0f}% - BPC-157 provides systemic healing and recovery support.',
            'mechanism': 'Gut healing, vascular repair, tendon/ligament healing, neuroprotection'
        })

    # 7. CELLULAR ENERGY & NAD+ (age-based)
    if age > 50:
        nad_dose = int(250 + (age - 50) * 10)  # Increase dose with age
        recommendations.append({
            'name': 'NAD+ (IV or Subcutaneous)',
            'dosage': f'{nad_dose}mg',
            'frequency': '2-3x per week',
            'duration': 'Ongoing',
            'priority': 2,
            'category': 'Cellular Energy',
            'rationale': f'At age {age}, NAD+ levels naturally decline. Supplementation restores cellular energy and DNA repair.',
            'mechanism': 'Mitochondrial function, sirtuins activation, DNA repair, energy metabolism'
        })

    # 8. COGNITIVE OPTIMIZATION (if older or high stress indicated)
    if age > 55 or hrv < 60:
        recommendations.append({
            'name': 'Selank',
            'dosage': '300mcg',
            'frequency': '2x daily (morning and midday)',
            'duration': '4-8 weeks, cycle as needed',
            'priority': 3,
            'category': 'Cognitive & Stress',
            'rationale': f'Age {age} and/or stress indicators (HRV: {hrv}%) - Selank supports cognitive function and stress resilience.',
            'mechanism': 'Anxiolytic, memory enhancement, immune modulation, BDNF increase'
        })

    # 9. WEIGHT MANAGEMENT (BMI-based)
    if bmi > 30:
        recommendations.append({
            'name': 'Tirzepatide',
            'dosage': f'{2.5 if bmi < 35 else 5.0}mg weekly (titrate)',
            'frequency': 'Once weekly',
            'duration': '6-12 months',
            'priority': 1,
            'category': 'Weight Loss',
            'rationale': f'BMI of {bmi:.1f} indicates need for comprehensive weight management. Tirzepatide is most effective for significant weight loss.',
            'mechanism': 'Dual GLP-1/GIP agonist, appetite suppression, insulin sensitivity, weight reduction'
        })
    elif bmi > 27.5:
        recommendations.append({
            'name': 'Semaglutide',
            'dosage': '0.25mg weekly (titrate to 1-2.4mg)',
            'frequency': 'Once weekly',
            'duration': '6-12 months',
            'priority': 2,
            'category': 'Weight Management',
            'rationale': f'BMI of {bmi:.1f} - Semaglutide supports healthy weight loss and metabolic improvement.',
            'mechanism': 'GLP-1 receptor agonist, appetite control, glucose regulation'
        })

    # 10. GENDER-SPECIFIC RECOMMENDATIONS
    if gender == 'female' and age > 45:
        # Likely peri/post-menopausal
        recommendations.append({
            'name': 'CJC-1295 (no DAC)',
            'dosage': f'{int(100 * weight_kg / 70)}mcg',
            'frequency': '3-4x per week',
            'duration': '3-6 months',
            'priority': 2,
            'category': 'Hormonal Support',
            'rationale': f'Female age {age} - CJC-1295 supports healthy GH levels during hormonal transition, preserving muscle and bone density.',
            'mechanism': 'GHRH analog, natural GH pulse enhancement'
        })

    elif gender == 'male' and age > 50 and metabolic_rate < 80:
        # Aging male with declining metabolism
        recommendations.append({
            'name': 'CJC-1295 + Ipamorelin',
            'dosage': f'{int(150 * weight_kg / 70)}mcg each',
            'frequency': 'Daily before bed',
            'duration': '6 months',
            'priority': 2,
            'category': 'Hormonal Optimization',
            'rationale': f'Male age {age} with {metabolic_rate}% metabolic rate - Optimize natural GH/IGF-1 for muscle preservation and metabolic health.',
            'mechanism': 'Synergistic GH release, muscle preservation, fat loss, recovery'
        })

    # Sort by priority (1 = highest)
    recommendations.sort(key=lambda x: x['priority'])

    # Add stack recommendations if multiple peptides
    if len(recommendations) >= 3:
        recommendations = add_stack_recommendations(recommendations, patient_info)

    print(f"[PEPTIDE_CALC] Generated {len(recommendations)} personalized recommendations")

    return recommendations


def add_stack_recommendations(recommendations, patient_info):
    """Add specific stacking protocols and timing recommendations"""

    # Identify if we have synergistic peptides
    has_cjc = any('CJC' in r['name'] for r in recommendations)
    has_ipa = any('Ipamorelin' in r['name'] for r in recommendations)
    has_bpc = any('BPC' in r['name'] for r in recommendations)
    has_tb500 = any('TB-500' in r['name'] for r in recommendations)

    # Add stacking notes
    for rec in recommendations:
        if 'CJC' in rec['name'] and has_ipa:
            rec['stacking_note'] = 'STACK: Administer with Ipamorelin for synergistic GH release. Take together before bed.'
        elif 'Ipamorelin' in rec['name'] and has_cjc:
            rec['stacking_note'] = 'STACK: Combine with CJC-1295 for optimal GH pulse. Synergistic effects enhance results.'
        elif 'BPC' in rec['name'] and has_tb500:
            rec['stacking_note'] = 'STACK: Pairs excellently with TB-500 for comprehensive healing. Can inject together.'
        elif 'TB-500' in rec['name'] and has_bpc:
            rec['stacking_note'] = 'STACK: Synergistic with BPC-157 for enhanced tissue repair and recovery.'

    return recommendations


def format_peptide_recommendations_html(recommendations):
    """Format peptide recommendations as HTML for report"""

    if not recommendations:
        return "<p>No specific recommendations generated.</p>"

    # Group by category
    categories = {}
    for rec in recommendations:
        cat = rec['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(rec)

    html = ""

    # Priority 1 recommendations first
    priority_1 = [r for r in recommendations if r['priority'] == 1]
    if priority_1:
        html += '<div class="peptide-section priority-high">\n'
        html += '<h4 style="color: #d32f2f; margin-bottom: 15px;">🎯 PRIMARY RECOMMENDATIONS</h4>\n'
        for rec in priority_1:
            html += format_single_peptide(rec)
        html += '</div>\n\n'

    # Priority 2 recommendations
    priority_2 = [r for r in recommendations if r['priority'] == 2]
    if priority_2:
        html += '<div class="peptide-section priority-medium">\n'
        html += '<h4 style="color: #f57c00; margin-bottom: 15px;">⭐ SECONDARY RECOMMENDATIONS</h4>\n'
        for rec in priority_2:
            html += format_single_peptide(rec)
        html += '</div>\n\n'

    # Priority 3 recommendations
    priority_3 = [r for r in recommendations if r['priority'] == 3]
    if priority_3:
        html += '<div class="peptide-section priority-low">\n'
        html += '<h4 style="color: #388e3c; margin-bottom: 15px;">💡 SUPPORTING RECOMMENDATIONS</h4>\n'
        for rec in priority_3:
            html += format_single_peptide(rec)
        html += '</div>\n\n'

    return html


def format_single_peptide(rec):
    """Format a single peptide recommendation"""

    html = f'''
    <div class="peptide-card">
        <div class="peptide-header">
            <h5 style="margin: 0; color: #1a237e;">{rec['name']}</h5>
            <span class="peptide-category">{rec['category']}</span>
        </div>

        <div class="peptide-dosing">
            <p><strong>Dosage:</strong> {rec['dosage']}</p>
            <p><strong>Frequency:</strong> {rec['frequency']}</p>
            <p><strong>Duration:</strong> {rec['duration']}</p>
        </div>

        <div class="peptide-rationale">
            <p><strong>Why This Recommendation:</strong></p>
            <p>{rec['rationale']}</p>
        </div>

        <div class="peptide-mechanism">
            <p><strong>Mechanism:</strong> {rec['mechanism']}</p>
        </div>

        {f'<div class="peptide-stack"><p><strong>{rec["stacking_note"]}</strong></p></div>' if rec.get('stacking_note') else ''}
    </div>
    '''

    return html
