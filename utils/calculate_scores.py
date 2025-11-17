"""
Calculate core performance scores from available metabolic data
Since PNOE PDFs don't include these scores, we calculate them from raw metabolic data
"""
import math

def calculate_core_scores_from_metabolic_data(patient_info, metabolic_data, caloric_data):
    """
    Calculate 7 core performance scores from available metabolic data

    Args:
        patient_info: dict with name, age, gender, weight_kg, height_cm
        metabolic_data: dict with rmr, rer, vo2max, etc.
        caloric_data: dict with rmr, fat_percent, cho_percent

    Returns:
        dict with 7 core scores (each 0-100)
    """

    # Extract data
    age = patient_info.get('age', 35)
    weight_kg = patient_info.get('weight_kg', 77)
    height_cm = patient_info.get('height_cm', 180)
    gender = patient_info.get('gender', 'Male').lower()

    rmr = metabolic_data.get('rmr') or caloric_data.get('rmr', 1700)
    rer = metabolic_data.get('rer', 0.85)
    fat_percent = caloric_data.get('fat_percent', 50)

    # 1. METABOLIC RATE SCORE
    # Calculate expected RMR using Mifflin-St Jeor equation
    if gender == 'male':
        expected_rmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        expected_rmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    # Score based on actual vs expected (100 = actual matches expected, higher/lower varies)
    rmr_ratio = (rmr / expected_rmr) if expected_rmr > 0 else 1.0
    metabolic_rate = min(100, max(30, int(rmr_ratio * 70 + 15)))

    # 2. FAT-BURNING EFFICIENCY SCORE
    # Based on fat utilization percentage (higher fat% = better fat burning)
    # 70%+ fat = excellent (90-100), 50-69% = good (70-89), <50% = needs work (40-69)
    if fat_percent >= 70:
        fat_burning = min(100, 85 + (fat_percent - 70) // 2)
    elif fat_percent >= 50:
        fat_burning = 65 + (fat_percent - 50)
    else:
        fat_burning = max(35, 40 + fat_percent // 3)

    # 3. LUNG UTILIZATION SCORE
    # Estimate based on age and fitness (younger = better potential)
    # Start with age-based score, modified by metabolic efficiency
    lung_base = max(60, 100 - (age - 25) * 0.5)
    lung_modifier = (rmr_ratio - 0.9) * 20  # Adjust based on metabolic rate
    lung_util = min(100, max(50, int(lung_base + lung_modifier)))

    # 4. HRV (Heart Rate Variability) SCORE
    # Estimate based on age and metabolic health
    # Younger age + good metabolism = higher HRV
    hrv_base = max(40, 95 - (age - 25) * 0.8)
    hrv_metabolic_bonus = (rmr_ratio - 0.85) * 15
    hrv = min(100, max(35, int(hrv_base + hrv_metabolic_bonus)))

    # 5. SYMPATHETIC/PARASYMPATHETIC BALANCE
    # Balance is better with good fat burning and appropriate metabolic rate
    # RER closer to 0.85 = better balance
    rer_balance = max(0, 1 - abs(rer - 0.85) / 0.3) if rer else 0.5
    symp_parasym = min(100, max(40, int(60 + rer_balance * 30 + (fat_burning - 60) * 0.3)))

    # 6. VENTILATION EFFICIENCY
    # Correlates with lung utilization and age
    vent_base = lung_util * 0.8
    vent_age_factor = max(0, (50 - age) * 0.3)
    ventilation_eff = min(100, max(40, int(vent_base + vent_age_factor)))

    # 7. BREATHING COORDINATION
    # Related to ventilation efficiency but with more variation
    # Good metabolic rate suggests good breathing
    breath_base = ventilation_eff * 0.85
    breath_metabolic = (rmr_ratio - 0.85) * 20
    breathing_coord = min(100, max(30, int(breath_base + breath_metabolic)))

    scores = {
        'metabolic_rate': metabolic_rate,
        'fat_burning': fat_burning,
        'lung_util': lung_util,
        'hrv': hrv,
        'symp_parasym': symp_parasym,
        'ventilation_eff': ventilation_eff,
        'breathing_coord': breathing_coord
    }

    # Debug output
    print(f"\n[CALCULATE_SCORES] Input data:")
    print(f"  Age: {age}, Weight: {weight_kg}kg, Height: {height_cm}cm, Gender: {gender}")
    print(f"  RMR: {rmr} (expected: {expected_rmr:.0f}, ratio: {rmr_ratio:.2f})")
    print(f"  Fat%: {fat_percent}%, RER: {rer}")
    print(f"\n[CALCULATE_SCORES] Calculated scores:")
    for key, value in scores.items():
        print(f"  {key}: {value}%")
    print()

    return scores


def enhance_extracted_data_with_calculated_scores(extracted_data):
    """
    If core_scores is empty, calculate them from available data

    Args:
        extracted_data: The data extracted from PDF

    Returns:
        extracted_data with core_scores filled in if they were empty
    """
    core_scores = extracted_data.get('core_scores', {})

    # Only calculate if scores are missing
    if not core_scores or len(core_scores) == 0:
        print("[ENHANCE_DATA] No core scores found in PDF, calculating from metabolic data...")

        patient_info = extracted_data.get('patient_info', {})
        metabolic_data = extracted_data.get('metabolic_data', {})
        caloric_data = extracted_data.get('caloric_data', {})

        calculated_scores = calculate_core_scores_from_metabolic_data(
            patient_info,
            metabolic_data,
            caloric_data
        )

        extracted_data['core_scores'] = calculated_scores
        print(f"[ENHANCE_DATA] Added {len(calculated_scores)} calculated core scores")
    else:
        print(f"[ENHANCE_DATA] Using {len(core_scores)} core scores from PDF extraction")

    return extracted_data
