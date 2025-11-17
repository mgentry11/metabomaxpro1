"""
Calculate core performance scores from available metabolic data
Since PNOE PDFs don't include these scores, we calculate them from raw metabolic data
"""
import math

def calculate_fuel_percentages_from_rer(rer):
    """
    Calculate fat and carb utilization percentages from RER

    RER (Respiratory Exchange Ratio) = VCO2 / VO2
    - RER 0.7 = 100% fat oxidation
    - RER 0.85 = ~50/50 fat/carb
    - RER 1.0 = 100% carb oxidation

    Args:
        rer: Respiratory Exchange Ratio (0.7-1.0)

    Returns:
        tuple: (fat_percent, cho_percent)
    """
    # Clamp RER to valid range
    rer = max(0.7, min(1.0, rer))

    # Linear interpolation between 0.7 and 1.0
    # At 0.7: 100% fat, 0% carbs
    # At 1.0: 0% fat, 100% carbs
    carb_percent = int(((rer - 0.7) / 0.3) * 100)
    fat_percent = 100 - carb_percent

    return fat_percent, carb_percent

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

    # DON'T trust extracted RMR - it's often wrong (PDF extracts VO2 ml/min instead)
    # Calculate proper RMR from patient data
    if gender == 'male':
        calculated_rmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        calculated_rmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    # Use extracted RMR only if it's realistic (within 50% of calculated)
    extracted_rmr = metabolic_data.get('rmr') or caloric_data.get('rmr')
    if extracted_rmr and 0.5 < (extracted_rmr / calculated_rmr) < 1.5:
        rmr = extracted_rmr
        print(f"[CALCULATE_SCORES] Using extracted RMR: {rmr} kcal (validated against calculated: {calculated_rmr:.0f})")
    else:
        rmr = calculated_rmr
        if extracted_rmr:
            print(f"[CALCULATE_SCORES] Rejected extracted RMR ({extracted_rmr}) - using calculated: {rmr:.0f} kcal")
        else:
            print(f"[CALCULATE_SCORES] No extracted RMR - using calculated: {rmr:.0f} kcal")
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
    # Correlates with lung utilization, age, and BMI
    bmi = weight_kg / ((height_cm / 100) ** 2)
    bmi_factor = max(-5, min(5, (25 - bmi) * 0.5))  # Optimal BMI ~25, ±5 points

    vent_base = lung_util * 0.8
    vent_age_factor = max(0, (50 - age) * 0.3)
    ventilation_eff = min(100, max(40, int(vent_base + vent_age_factor + bmi_factor)))

    # 7. BREATHING COORDINATION
    # Related to ventilation efficiency but with more variation
    # Good metabolic rate + weight management suggest good breathing
    breath_base = ventilation_eff * 0.85
    breath_metabolic = (rmr_ratio - 0.85) * 20
    # Add weight-based factor: lighter/optimal weight = better coordination
    weight_factor = max(-3, min(3, (80 - weight_kg) * 0.05))  # Optimal ~80kg
    breathing_coord = min(100, max(30, int(breath_base + breath_metabolic + weight_factor)))

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
    Also calculate fuel percentages if missing

    Args:
        extracted_data: The data extracted from PDF

    Returns:
        extracted_data with core_scores and fuel percentages filled in if they were empty
    """
    # STEP 1: Calculate fuel percentages if missing
    caloric_data = extracted_data.get('caloric_data', {})
    metabolic_data = extracted_data.get('metabolic_data', {})

    if 'fat_percent' not in caloric_data or 'cho_percent' not in caloric_data:
        print("[ENHANCE_DATA] Fuel percentages not found in PDF, calculating from metabolic data...")

        # Get RER value
        rer = metabolic_data.get('rer')

        # Fix invalid RER values (sometimes extraction gets wrong numbers)
        if not rer or rer < 0.7 or rer > 1.0:
            # Estimate RER based on metabolic efficiency
            # Better metabolic rate = lower RER (more fat burning)
            patient_info = extracted_data.get('patient_info', {})
            age = patient_info.get('age', 35)
            weight_kg = patient_info.get('weight_kg', 77)
            height_cm = patient_info.get('height_cm', 180)
            gender = patient_info.get('gender', 'Male').lower()

            rmr = caloric_data.get('rmr', 1700)

            # Calculate expected RMR
            if gender == 'male':
                expected_rmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
            else:
                expected_rmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

            # RMR ratio: higher ratio = better metabolism = more fat burning = lower RER
            rmr_ratio = (rmr / expected_rmr) if expected_rmr > 0 else 1.0

            # Estimate RER on a continuous scale based on RMR ratio
            # Use age as a secondary factor (younger = better fat burning potential)
            age_factor = max(0, (50 - age) * 0.002)  # Bonus for being younger than 50

            # Map RMR ratio to RER:
            # - ratio 0.3-0.5 (very low) -> RER 0.90-0.95 (carb dependent)
            # - ratio 0.5-0.8 (low) -> RER 0.87-0.90 (carb leaning)
            # - ratio 0.8-1.0 (normal low) -> RER 0.83-0.87 (mixed)
            # - ratio 1.0-1.2 (normal high) -> RER 0.78-0.83 (fat leaning)
            # - ratio >1.2 (high) -> RER 0.70-0.78 (fat burner)

            if rmr_ratio < 0.5:
                # Very low metabolism
                rer = 0.95 - (rmr_ratio * 0.1)  # Scale between 0.90-0.95
            elif rmr_ratio < 0.8:
                # Low metabolism
                rer = 0.90 - ((rmr_ratio - 0.5) / 0.3) * 0.03  # Scale between 0.87-0.90
            elif rmr_ratio < 1.0:
                # Below normal
                rer = 0.87 - ((rmr_ratio - 0.8) / 0.2) * 0.04  # Scale between 0.83-0.87
            elif rmr_ratio < 1.2:
                # Above normal
                rer = 0.83 - ((rmr_ratio - 1.0) / 0.2) * 0.05  # Scale between 0.78-0.83
            else:
                # High metabolism
                rer = max(0.70, 0.78 - (rmr_ratio - 1.2) * 0.04)  # Scale down from 0.78

            # Apply age bonus (younger = lower RER)
            rer = max(0.70, rer - age_factor)

            print(f"[ENHANCE_DATA] Invalid/missing RER, estimated from RMR ratio ({rmr_ratio:.2f}) + age ({age}): {rer:.3f}")
        else:
            print(f"[ENHANCE_DATA] Using extracted RER: {rer}")

        # Calculate fuel percentages from RER
        fat_pct, cho_pct = calculate_fuel_percentages_from_rer(rer)

        extracted_data['caloric_data']['fat_percent'] = fat_pct
        extracted_data['caloric_data']['cho_percent'] = cho_pct

        print(f"[ENHANCE_DATA] Calculated fuel percentages: Fat {fat_pct}%, Carbs {cho_pct}%")

    # STEP 2: Calculate core scores if missing
    core_scores = extracted_data.get('core_scores', {})

    if not core_scores or len(core_scores) == 0:
        print("[ENHANCE_DATA] No core scores found in PDF, calculating from metabolic data...")

        patient_info = extracted_data.get('patient_info', {})
        caloric_data = extracted_data.get('caloric_data', {})  # Use updated caloric_data

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
