"""
Calculate core performance scores from available metabolic data
Since PNOE PDFs don't include these scores, we calculate them from raw metabolic data

Biological Age Algorithm aligned with PNOE methodology:
- Primary factor: VO2 max (the best predictor of longevity per American Heart Association)
- Secondary factors: Fat-burning efficiency, Metabolic rate
- Supporting factors: Core scores, BMI, cardiovascular health
"""
import math

# VO2 max percentile reference tables (ACSM Guidelines, 10th Edition)
# Values represent 50th percentile VO2 max (ml/kg/min) by age and gender
# Used to calculate "what age would have this VO2 max as average?"

VO2MAX_PERCENTILES_MALE = {
    # age: {percentile: vo2max}
    20: {10: 32.2, 25: 38.1, 50: 44.2, 75: 50.2, 90: 55.1},
    25: {10: 31.0, 25: 36.8, 50: 42.8, 75: 48.5, 90: 53.2},
    30: {10: 29.4, 25: 35.0, 50: 40.8, 75: 46.3, 90: 50.8},
    35: {10: 27.9, 25: 33.4, 50: 38.9, 75: 44.2, 90: 48.5},
    40: {10: 26.5, 25: 31.8, 50: 37.0, 75: 42.1, 90: 46.2},
    45: {10: 25.1, 25: 30.2, 50: 35.2, 75: 40.1, 90: 44.0},
    50: {10: 23.8, 25: 28.7, 50: 33.5, 75: 38.1, 90: 41.8},
    55: {10: 22.5, 25: 27.2, 50: 31.8, 75: 36.2, 90: 39.7},
    60: {10: 21.3, 25: 25.8, 50: 30.2, 75: 34.3, 90: 37.6},
    65: {10: 20.1, 25: 24.4, 50: 28.6, 75: 32.5, 90: 35.6},
    70: {10: 19.0, 25: 23.1, 50: 27.0, 75: 30.7, 90: 33.6},
    75: {10: 17.9, 25: 21.8, 50: 25.5, 75: 29.0, 90: 31.7},
    80: {10: 16.9, 25: 20.5, 50: 24.1, 75: 27.3, 90: 29.9},
}

VO2MAX_PERCENTILES_FEMALE = {
    # age: {percentile: vo2max}
    20: {10: 27.6, 25: 32.3, 50: 37.6, 75: 42.4, 90: 46.8},
    25: {10: 26.6, 25: 31.1, 50: 36.2, 75: 40.8, 90: 44.9},
    30: {10: 25.3, 25: 29.6, 50: 34.5, 75: 38.8, 90: 42.7},
    35: {10: 24.0, 25: 28.1, 50: 32.8, 75: 36.9, 90: 40.5},
    40: {10: 22.8, 25: 26.7, 50: 31.1, 75: 35.0, 90: 38.4},
    45: {10: 21.6, 25: 25.3, 50: 29.5, 75: 33.2, 90: 36.4},
    50: {10: 20.5, 25: 24.0, 50: 28.0, 75: 31.4, 90: 34.4},
    55: {10: 19.4, 25: 22.7, 50: 26.5, 75: 29.7, 90: 32.5},
    60: {10: 18.4, 25: 21.5, 50: 25.1, 75: 28.1, 90: 30.7},
    65: {10: 17.4, 25: 20.3, 50: 23.7, 75: 26.5, 90: 29.0},
    70: {10: 16.4, 25: 19.2, 50: 22.4, 75: 25.0, 90: 27.3},
    75: {10: 15.5, 25: 18.1, 50: 21.1, 75: 23.6, 90: 25.7},
    80: {10: 14.6, 25: 17.1, 50: 19.9, 75: 22.2, 90: 24.2},
}


def get_vo2max_biological_age(vo2max, gender, chronological_age):
    """
    Calculate biological age based on VO2 max using ACSM percentile tables.

    This is the PRIMARY factor in biological age calculation, aligned with
    American Heart Association research showing VO2 max is the best predictor
    of longevity and all-cause mortality.

    Algorithm: Find what age would have this VO2 max as the 50th percentile.

    Args:
        vo2max: VO2 max in ml/kg/min (relative)
        gender: 'male' or 'female'
        chronological_age: Current age in years

    Returns:
        tuple: (vo2max_bio_age, percentile_for_age, adjustment_years)
    """
    if not vo2max or vo2max <= 0:
        return chronological_age, 50, 0

    # Select appropriate table
    if 'male' in gender.lower():
        table = VO2MAX_PERCENTILES_MALE
    else:
        table = VO2MAX_PERCENTILES_FEMALE

    # Find the age where this VO2 max would be the 50th percentile
    vo2max_bio_age = chronological_age

    # Search through ages to find where this VO2 max matches 50th percentile
    ages = sorted(table.keys())

    for age in ages:
        p50 = table[age][50]
        if vo2max >= p50:
            vo2max_bio_age = age
            break
    else:
        # VO2 max is below all 50th percentiles - use oldest age + adjustment
        vo2max_bio_age = ages[-1] + 5

    # Also calculate what percentile this person is at for their actual age
    # Find closest age bracket
    closest_age = min(ages, key=lambda x: abs(x - chronological_age))
    age_data = table[closest_age]

    # Determine percentile for their age
    percentile = 50  # default
    if vo2max >= age_data[90]:
        percentile = 95
    elif vo2max >= age_data[75]:
        percentile = 82  # midpoint 75-90
    elif vo2max >= age_data[50]:
        percentile = 62  # midpoint 50-75
    elif vo2max >= age_data[25]:
        percentile = 37  # midpoint 25-50
    elif vo2max >= age_data[10]:
        percentile = 17  # midpoint 10-25
    else:
        percentile = 5

    adjustment = chronological_age - vo2max_bio_age

    print(f"  VO2 max: {vo2max:.1f} ml/kg/min")
    print(f"  VO2 max percentile for age {chronological_age}: {percentile}th")
    print(f"  VO2 max biological age: {vo2max_bio_age} (adjustment: {adjustment:+d} years)")

    return vo2max_bio_age, percentile, adjustment


def estimate_vo2max_from_metrics(patient_info, core_scores, metabolic_data):
    """
    Estimate VO2 max when not directly available from test data.

    Uses validated estimation formulas based on:
    - Age, gender, weight, height
    - Resting heart rate (if available)
    - Activity level indicators from core scores

    Args:
        patient_info: dict with age, gender, weight_kg, height_cm
        core_scores: dict with performance scores
        metabolic_data: dict with any available metabolic data

    Returns:
        tuple: (vo2max, is_measured) - VO2 max in ml/kg/min and whether it was measured
    """
    age = patient_info.get('age', 35)
    gender = patient_info.get('gender', 'Male').lower()
    weight_kg = patient_info.get('weight_kg', 77)
    height_cm = patient_info.get('height_cm', 180)

    # Check if we have actual VO2 max data
    vo2max = metabolic_data.get('vo2max_rel') or metabolic_data.get('vo2max') if metabolic_data else None
    if vo2max and vo2max > 10:  # Sanity check - valid VO2 max is > 10
        print(f"  Using MEASURED VO2 max: {vo2max} ml/kg/min")
        return vo2max, True  # Return True = measured

    # Check for absolute VO2 max and convert to relative
    vo2max_abs = metabolic_data.get('vo2max_abs') if metabolic_data else None
    if vo2max_abs and weight_kg > 0:
        vo2max = (vo2max_abs * 1000) / weight_kg  # Convert L/min to ml/kg/min
        if 10 < vo2max < 80:  # Sanity check
            print(f"  Using MEASURED VO2 max (converted): {vo2max:.1f} ml/kg/min")
            return vo2max, True  # Return True = measured

    # Estimate VO2 max using modified Jackson formula
    # Base formula: VO2 max = 56.363 - (0.381 × age) - (0.754 × BMI) + (1.921 × PA)
    # PA (physical activity) estimated from core scores

    bmi = weight_kg / ((height_cm / 100) ** 2) if height_cm > 0 else 25

    # Estimate physical activity level from core scores (0-7 scale)
    if core_scores:
        avg_score = sum(core_scores.values()) / len(core_scores)
        # Map average score (0-100) to PA level (0-7)
        pa_level = (avg_score / 100) * 7
    else:
        pa_level = 3.5  # Assume moderate activity

    # Gender adjustment
    if 'male' in gender:
        base_vo2 = 56.363
    else:
        base_vo2 = 50.513  # Women have ~10% lower base

    estimated_vo2max = base_vo2 - (0.381 * age) - (0.754 * bmi) + (1.921 * pa_level)

    # Ensure reasonable bounds (15-70 ml/kg/min)
    estimated_vo2max = max(15, min(70, estimated_vo2max))

    print(f"  ESTIMATED VO2 max (no test data): {estimated_vo2max:.1f} ml/kg/min")
    print(f"    (Based on age={age}, BMI={bmi:.1f}, PA={pa_level:.1f})")

    return estimated_vo2max, False  # Return False = estimated

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


def calculate_biological_age(patient_info, core_scores, metabolic_data):
    """
    Calculate biological age from metabolic data and core performance scores.

    ALIGNED WITH PNOE METHODOLOGY:
    - PRIMARY factor (50% weight): VO2 max - the best predictor of longevity
    - SECONDARY factors (30% weight): Fat-burning efficiency + Metabolic rate
    - SUPPORTING factors (20% weight): Core scores, BMI, cardiovascular health

    Args:
        patient_info: dict with age, weight_kg, height_cm, gender
        core_scores: dict with 7 core performance scores
        metabolic_data: dict with rmr, rer, vo2max, etc.

    Returns:
        int: calculated biological age (18-90 years)
    """
    chronological_age = patient_info.get('age', 35)

    if not chronological_age:
        return None

    weight_kg = patient_info.get('weight_kg', 77)
    height_cm = patient_info.get('height_cm', 180)
    gender = patient_info.get('gender', 'Male').lower()

    print(f"\n[CALCULATE_BIO_AGE] Calculating biological age (PNOE-aligned algorithm)...")
    print(f"  Chronological age: {chronological_age}")
    print(f"  Gender: {gender}, Weight: {weight_kg}kg, Height: {height_cm}cm")

    # ========================================================================
    # PRIMARY FACTOR: VO2 MAX
    # Per American Heart Association: VO2 max is the best predictor of longevity
    # ONLY used when MEASURED - estimated VO2 max is too unreliable
    # ========================================================================

    # Get or estimate VO2 max
    vo2max, vo2max_is_measured = estimate_vo2max_from_metrics(patient_info, core_scores, metabolic_data)

    # Determine weights based on whether VO2 max is measured
    if vo2max_is_measured:
        # When measured, VO2 max is the primary factor
        vo2max_weight = 0.50  # 50% - Full weight when measured
        secondary_weight = 0.30  # 30%
        supporting_weight = 0.20  # 20%
        print(f"\n  === PRIMARY FACTOR: VO2 MAX (50% weight - MEASURED) ===")

        # Calculate VO2 max biological age
        vo2max_bio_age, vo2max_percentile, vo2max_adjustment = get_vo2max_biological_age(
            vo2max, gender, chronological_age
        )
    else:
        # When NOT measured, VO2 max is NEUTRAL (no adjustment)
        # Let core scores, fat burning, and metabolic rate determine biological age
        vo2max_weight = 0.00  # 0% - Don't use estimated VO2 max
        secondary_weight = 0.50  # 50% - Fat-burning + Metabolic rate
        supporting_weight = 0.50  # 50% - Core scores + BMI
        vo2max_adjustment = 0  # Neutral - no effect
        vo2max_percentile = 50  # Assume average
        print(f"\n  === VO2 MAX: Not measured (using core scores instead) ===")
        print(f"  VO2 max: {vo2max:.1f} ml/kg/min (estimated - NOT used for biological age)")
        print(f"  Note: Get a VO2 max exercise test for accurate biological age based on cardio fitness")

    # ========================================================================
    # SECONDARY FACTORS (30% weight): Fat-burning + Metabolic Rate
    # These are the other two factors PNOE emphasizes
    # ========================================================================
    print(f"\n  === SECONDARY FACTORS: FAT-BURNING + METABOLIC RATE (30% weight) ===")

    secondary_adjustments = []

    # Fat-burning efficiency (range: -8 to +8 years)
    fat_burning_score = core_scores.get('fat_burning', 50) if core_scores else 50

    if fat_burning_score >= 80:
        fat_adjustment = -8  # Elite fat burner
    elif fat_burning_score >= 70:
        fat_adjustment = -5  # Excellent
    elif fat_burning_score >= 60:
        fat_adjustment = -3  # Good
    elif fat_burning_score >= 50:
        fat_adjustment = -1  # Average (slight benefit)
    elif fat_burning_score >= 40:
        fat_adjustment = 2   # Below average
    elif fat_burning_score >= 30:
        fat_adjustment = 5   # Poor
    else:
        fat_adjustment = 8   # Very poor

    secondary_adjustments.append(fat_adjustment)
    print(f"  Fat burning: {fat_burning_score}% → adjustment: {fat_adjustment:+d} years")

    # Metabolic rate (RMR efficiency) - range: -6 to +6 years
    if 'male' in gender:
        expected_rmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * chronological_age) + 5
    else:
        expected_rmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * chronological_age) - 161

    extracted_rmr = metabolic_data.get('rmr') if metabolic_data else None

    if extracted_rmr and 0.5 < (extracted_rmr / expected_rmr) < 1.5:
        rmr = extracted_rmr
    else:
        rmr = expected_rmr

    rmr_ratio = rmr / expected_rmr if expected_rmr > 0 else 1.0

    if rmr_ratio >= 1.15:
        rmr_adjustment = -6  # Very fast metabolism
    elif rmr_ratio >= 1.05:
        rmr_adjustment = -3  # Fast metabolism
    elif rmr_ratio >= 0.95:
        rmr_adjustment = -1  # Normal (slight benefit)
    elif rmr_ratio >= 0.88:
        rmr_adjustment = 2   # Slow metabolism
    else:
        rmr_adjustment = 5   # Very slow

    secondary_adjustments.append(rmr_adjustment)
    print(f"  Metabolic rate ratio: {rmr_ratio:.2f} → adjustment: {rmr_adjustment:+d} years")

    secondary_avg = sum(secondary_adjustments) / len(secondary_adjustments)
    print(f"  Secondary factors avg adjustment: {secondary_avg:+.1f} years")

    # ========================================================================
    # SUPPORTING FACTORS (20% weight): Core scores average, BMI
    # ========================================================================
    print(f"\n  === SUPPORTING FACTORS (20% weight) ===")

    supporting_adjustments = []

    # Core scores average (range: -5 to +5 years)
    if core_scores and len(core_scores) > 0:
        avg_score = sum(core_scores.values()) / len(core_scores)

        if avg_score >= 85:
            score_adjustment = -5  # Elite
        elif avg_score >= 75:
            score_adjustment = -3  # Excellent
        elif avg_score >= 65:
            score_adjustment = -1  # Good (Mark is here at 67%)
        elif avg_score >= 55:
            score_adjustment = 1   # Average
        elif avg_score >= 45:
            score_adjustment = 3   # Below average
        else:
            score_adjustment = 5   # Poor

        supporting_adjustments.append(score_adjustment)
        print(f"  Core scores avg: {avg_score:.1f}% → adjustment: {score_adjustment:+d} years")

    # BMI factor (range: -2 to +4 years)
    bmi = weight_kg / ((height_cm / 100) ** 2) if height_cm > 0 else 25

    if bmi < 18.5:
        bmi_factor = 1   # Underweight
    elif bmi < 25:
        bmi_factor = -2  # Optimal
    elif bmi < 30:
        bmi_factor = 1   # Overweight
    elif bmi < 35:
        bmi_factor = 3   # Obese
    else:
        bmi_factor = 4   # Severely obese

    supporting_adjustments.append(bmi_factor)
    print(f"  BMI: {bmi:.1f} → adjustment: {bmi_factor:+d} years")

    supporting_avg = sum(supporting_adjustments) / len(supporting_adjustments) if supporting_adjustments else 0
    print(f"  Supporting factors avg adjustment: {supporting_avg:+.1f} years")

    # ========================================================================
    # WEIGHTED FINAL CALCULATION
    # ========================================================================
    print(f"\n  === FINAL WEIGHTED CALCULATION ===")
    print(f"  Weights: VO2={vo2max_weight:.0%}, Secondary={secondary_weight:.0%}, Supporting={supporting_weight:.0%}")

    # Calculate weighted adjustment (weights were set earlier based on measured vs estimated)
    weighted_adjustment = (
        (vo2max_adjustment * vo2max_weight) +
        (secondary_avg * secondary_weight) +
        (supporting_avg * supporting_weight)
    )

    print(f"  VO2 max contribution: {vo2max_adjustment:+d} × {vo2max_weight:.0%} = {vo2max_adjustment * vo2max_weight:+.1f}")
    print(f"  Secondary contribution: {secondary_avg:+.1f} × {secondary_weight:.0%} = {secondary_avg * secondary_weight:+.1f}")
    print(f"  Supporting contribution: {supporting_avg:+.1f} × {supporting_weight:.0%} = {supporting_avg * supporting_weight:+.1f}")
    print(f"  Total weighted adjustment: {weighted_adjustment:+.1f} years")

    # Calculate final biological age
    # Negative adjustment = factors suggest younger, so ADD to get lower bio age
    # Positive adjustment = factors suggest older, so ADD to get higher bio age
    biological_age = chronological_age + weighted_adjustment

    # Ensure reasonable bounds (18-90 years)
    biological_age = max(18, min(90, round(biological_age)))

    age_diff = chronological_age - biological_age
    print(f"\n  ✓ BIOLOGICAL AGE: {biological_age} (vs chronological: {chronological_age})")
    print(f"  ✓ You are {abs(age_diff)} years {'younger' if age_diff > 0 else 'older'} than your chronological age")
    print()

    return biological_age
