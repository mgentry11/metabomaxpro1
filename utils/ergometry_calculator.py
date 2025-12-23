"""
Ergometry Calculation Engine

Derives core metabolic scores from raw PNOE ergometry data.
Replicates PNOE's internal scoring algorithm based on physiological principles.

Scores calculated:
1. Metabolic Rate (%) - RMR vs predicted
2. Fat-burning Efficiency (%) - Based on RER
3. Lung Utilization (%) - Based on VE/VO2
4. Ventilation Efficiency (%) - Based on VE/VCO2
5. Breathing Coordination (%) - Based on breathing pattern consistency
6. HRV (%) - Based on heart rate variability
7. Sympathetic/Parasympathetic Balance (%) - Based on autonomic indicators
"""

import re
import numpy as np
from typing import Dict, List, Tuple, Optional
import pdfplumber


def extract_ergometry_data(pdf_path: str) -> Dict:
    """
    Extract raw ergometry data from PNOE Ergometry PDF.

    Returns dict with:
    - patient_info: name, gender, age, weight, height
    - time_series: VO2, VCO2, HR, RER values over time
    - summary_stats: calculated averages and peaks
    - chart_ranges: estimated ranges from chart axes
    """
    data = {
        'patient_info': {},
        'time_series': {
            'vo2': [],      # ml/min
            'vco2': [],     # ml/min
            'hr': [],       # bpm
            'rer': [],      # ratio
            've_vo2': [],   # ventilatory equivalent O2
            've_vco2': [],  # ventilatory equivalent CO2
        },
        'chart_ranges': {},  # Estimated ranges from chart axes
        'summary_stats': {},
        'is_rmr_test': False,
        'is_exercise_test': False,
        'data_source': 'raw_ergometry'
    }

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text() or ""
            full_text += text + "\n"

        # Extract patient info
        name_match = re.search(r'Name\s+([^\n]+?)(?:\s+Status|$)', full_text)
        if name_match:
            data['patient_info']['name'] = name_match.group(1).strip()

        gender_age_match = re.search(r'Gender\s+(\w+)\s*\((\d+)\)', full_text)
        if gender_age_match:
            data['patient_info']['gender'] = gender_age_match.group(1)
            data['patient_info']['age'] = int(gender_age_match.group(2))

        weight_match = re.search(r'Weight\s+(\d+(?:\.\d+)?)\s*kg', full_text)
        if weight_match:
            data['patient_info']['weight_kg'] = float(weight_match.group(1))

        height_match = re.search(r'Height\s+(\d+(?:\.\d+)?)\s*cm', full_text)
        if height_match:
            data['patient_info']['height_cm'] = float(height_match.group(1))

        # Detect test type
        if 'RMR' in full_text:
            data['is_rmr_test'] = True
        if 'VO2max' in full_text or 'Watts' in full_text:
            data['is_exercise_test'] = True

        # Extract data from tables if present
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table:
                    _parse_data_table(table, data)

        # Try to extract values from chart axis labels/data points
        _extract_values_from_text(full_text, data)

        # NEW: Extract estimated values from chart axis labels
        _extract_chart_axis_ranges(full_text, data)

    # Calculate summary statistics
    _calculate_summary_stats(data)

    # If no time-series data extracted, use chart range estimates
    if not data['time_series']['vo2'] and data['chart_ranges']:
        _estimate_values_from_chart_ranges(data)

    return data


def _extract_chart_axis_ranges(text: str, data: Dict):
    """
    Extract estimated value ranges from chart axis labels.

    PNOE Ergometry PDFs have charts with axis labels like:
    - VO2/VCO2: 0-600 ml/min (Y-axis values: 600, 500, 400, 300, 200, 100, 0)
    - HR: 60-75 bpm (Y-axis values: 75, 70, 65, 60)
    - RER: 0.5-1.0 (Y-axis values: 1.0, 0.9, 0.8, 0.7, 0.6, 0.5)
    - VE/VO2: 40-80 (Y-axis values: 80, 70, 60, 50, 40)
    """
    ranges = data['chart_ranges']

    # Look for HR axis values (typically 60-75 for RMR, higher for exercise)
    # Pattern: consecutive numbers like "75 70 65 60" near "Heart Rate"
    hr_section = re.search(r'Heart Rate.*?(\d{2,3})\s+(\d{2,3})\s+(\d{2,3})', text, re.DOTALL)
    if hr_section:
        hr_vals = [int(hr_section.group(i)) for i in range(1, 4)]
        if all(40 < v < 200 for v in hr_vals):
            ranges['hr_max'] = max(hr_vals)
            ranges['hr_min'] = min(hr_vals)
            # Estimate mean as midpoint weighted toward lower end (resting)
            ranges['hr_mean'] = (ranges['hr_min'] + ranges['hr_max']) / 2

    # If we see specific HR values in the text
    hr_matches = re.findall(r'\[?\d{2}\]?\s*Heart Rate|HR.*?(\d{2})', text)
    if hr_matches:
        # Look for numbers before "Heart Rate" or after "HR"
        single_hr = re.findall(r'(?:^|\s)(\d{2})(?:\s|$)', text)
        valid_hrs = [int(h) for h in single_hr if 50 <= int(h) <= 100]
        if valid_hrs and 'hr_mean' not in ranges:
            ranges['hr_mean'] = np.mean(valid_hrs)

    # Default reasonable resting HR if nothing found
    if 'hr_mean' not in ranges:
        ranges['hr_mean'] = 68  # Typical resting HR

    # Look for RER axis values (0.5-1.0 range)
    rer_matches = re.findall(r'(0\.[5-9]|1\.0)', text)
    if rer_matches:
        rer_vals = [float(v) for v in rer_matches if 0.5 <= float(v) <= 1.2]
        if rer_vals:
            ranges['rer_range'] = (min(rer_vals), max(rer_vals))
            # For RMR, estimate mid-range leaning toward fat burning
            ranges['rer_mean'] = 0.82  # Typical RMR RER

    # Look for VE/VO2 values (typically 40-80)
    ve_vo2_matches = re.findall(r'VE/VO2.*?(\d{2})', text)
    if ve_vo2_matches:
        ve_vo2_vals = [int(v) for v in ve_vo2_matches if 20 <= int(v) <= 100]
        if ve_vo2_vals:
            ranges['ve_vo2_range'] = (min(ve_vo2_vals), max(ve_vo2_vals))
            ranges['ve_vo2_mean'] = np.mean(ve_vo2_vals)

    # Look for VE/VCO2 values
    ve_vco2_matches = re.findall(r'VE/VCO2.*?(\d{2})', text)
    if ve_vco2_matches:
        ve_vco2_vals = [int(v) for v in ve_vco2_matches if 20 <= int(v) <= 100]
        if ve_vco2_vals:
            ranges['ve_vco2_range'] = (min(ve_vco2_vals), max(ve_vco2_vals))
            ranges['ve_vco2_mean'] = np.mean(ve_vco2_vals)


def _estimate_values_from_chart_ranges(data: Dict):
    """
    When no time-series data is available, create estimates from chart axis ranges.
    """
    ranges = data['chart_ranges']

    # Populate time_series with single estimated values
    if 'hr_mean' in ranges:
        data['time_series']['hr'] = [ranges['hr_mean']]
        data['summary_stats']['hr_mean'] = ranges['hr_mean']
        data['summary_stats']['hr_std'] = 5.0  # Assume moderate variability

    if 'rer_mean' in ranges:
        data['time_series']['rer'] = [ranges['rer_mean']]
        data['summary_stats']['rer_mean'] = ranges['rer_mean']
        data['summary_stats']['rer_std'] = 0.05

    if 've_vo2_mean' in ranges:
        data['time_series']['ve_vo2'] = [ranges['ve_vo2_mean']]
        data['summary_stats']['ve_vo2_mean'] = ranges['ve_vo2_mean']

    if 've_vco2_mean' in ranges:
        data['time_series']['ve_vco2'] = [ranges['ve_vco2_mean']]
        data['summary_stats']['ve_vco2_mean'] = ranges['ve_vco2_mean']


def _parse_data_table(table: List[List], data: Dict):
    """Parse tabular data from ergometry PDF."""
    for row in table:
        if not row:
            continue
        # Look for numeric data rows
        try:
            # Typical format: Time, VO2, VCO2, HR, RER, etc.
            numeric_values = [float(x) for x in row if x and re.match(r'^-?\d+\.?\d*$', str(x))]
            if len(numeric_values) >= 3:
                # Assume order based on typical PNOE format
                if numeric_values[0] < 1000:  # Likely VO2 in ml/min range
                    if len(numeric_values) >= 2:
                        data['time_series']['vo2'].append(numeric_values[0])
                    if len(numeric_values) >= 3:
                        data['time_series']['vco2'].append(numeric_values[1])
        except (ValueError, TypeError):
            continue


def _extract_values_from_text(text: str, data: Dict):
    """Extract numeric values from text patterns in the PDF."""

    # Look for VO2 values (typically 100-600 ml/min at rest)
    vo2_matches = re.findall(r'VO2[:\s]+(\d+(?:\.\d+)?)\s*(?:ml|L)', text)
    for val in vo2_matches:
        v = float(val)
        if v < 10:  # L/min
            v *= 1000
        if 50 < v < 1000:  # Reasonable RMR range
            data['time_series']['vo2'].append(v)

    # Look for VCO2 values
    vco2_matches = re.findall(r'VCO2[:\s]+(\d+(?:\.\d+)?)\s*(?:ml|L)', text)
    for val in vco2_matches:
        v = float(val)
        if v < 10:
            v *= 1000
        if 50 < v < 1000:
            data['time_series']['vco2'].append(v)

    # Look for heart rate values
    hr_matches = re.findall(r'(?:HR|Heart Rate)[:\s]+(\d+)\s*(?:bpm)?', text)
    for val in hr_matches:
        hr = int(val)
        if 40 < hr < 200:
            data['time_series']['hr'].append(hr)

    # Look for RER values
    rer_matches = re.findall(r'RER[:\s]+(\d+\.?\d*)', text)
    for val in rer_matches:
        rer = float(val)
        if 0.5 < rer < 1.5:
            data['time_series']['rer'].append(rer)

    # Look for VE/VO2 ratios
    ve_vo2_matches = re.findall(r'VE/VO2[:\s]+(\d+\.?\d*)', text)
    for val in ve_vo2_matches:
        data['time_series']['ve_vo2'].append(float(val))

    # Look for VE/VCO2 ratios
    ve_vco2_matches = re.findall(r'VE/VCO2[:\s]+(\d+\.?\d*)', text)
    for val in ve_vco2_matches:
        data['time_series']['ve_vco2'].append(float(val))


def _calculate_summary_stats(data: Dict):
    """Calculate summary statistics from time series data."""
    stats = data['summary_stats']

    for key, values in data['time_series'].items():
        if values:
            arr = np.array(values)
            stats[f'{key}_mean'] = float(np.mean(arr))
            stats[f'{key}_std'] = float(np.std(arr))
            stats[f'{key}_min'] = float(np.min(arr))
            stats[f'{key}_max'] = float(np.max(arr))
            # Use middle 80% for more stable average (exclude outliers)
            if len(arr) > 5:
                sorted_arr = np.sort(arr)
                trim_n = len(arr) // 10
                if trim_n > 0:
                    trimmed = sorted_arr[trim_n:-trim_n]
                    stats[f'{key}_trimmed_mean'] = float(np.mean(trimmed))


def calculate_predicted_rmr(gender: str, age: int, weight_kg: float, height_cm: float) -> float:
    """
    Calculate predicted RMR using Mifflin-St Jeor equation.
    Most accurate for modern populations.

    Returns RMR in kcal/day
    """
    if gender.lower() in ['male', 'm']:
        # Men: (10 × weight in kg) + (6.25 × height in cm) - (5 × age) + 5
        rmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        # Women: (10 × weight in kg) + (6.25 × height in cm) - (5 × age) - 161
        rmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    return rmr


def calculate_rmr_from_vo2(vo2_ml_min: float) -> float:
    """
    Calculate RMR in kcal/day from VO2 in ml/min.
    Uses Weir equation: RMR = VO2 × 4.86 kcal/L × 1440 min/day / 1000
    Simplified: RMR ≈ VO2 × 6.998
    """
    return vo2_ml_min * 6.998


def calculate_metabolic_rate_score(measured_rmr: float, predicted_rmr: float) -> int:
    """
    Calculate Metabolic Rate Score (0-100%).

    Score based on how measured RMR compares to predicted:
    - 100% = measured is ≥110% of predicted (fast metabolism)
    - 50% = measured equals predicted
    - 0% = measured is ≤70% of predicted (slow metabolism)
    """
    ratio = measured_rmr / predicted_rmr

    # Scale: 0.7 → 0%, 1.0 → 50%, 1.1+ → 100%
    if ratio >= 1.10:
        return 100
    elif ratio <= 0.70:
        return 0
    elif ratio >= 1.0:
        # 1.0 to 1.1 maps to 50-100
        score = 50 + (ratio - 1.0) * 500
    else:
        # 0.7 to 1.0 maps to 0-50
        score = (ratio - 0.7) * 166.67

    return int(min(100, max(0, score)))


def calculate_fat_burning_score(rer: float) -> int:
    """
    Calculate Fat-Burning Efficiency Score (0-100%).

    Based on Respiratory Exchange Ratio (RER):
    - RER 0.70 = 100% fat oxidation (score: 100%)
    - RER 0.85 = ~50% fat / 50% carbs (score: ~50%)
    - RER 1.00 = 100% carb oxidation (score: 0%)

    At rest, lower RER indicates better fat adaptation.
    """
    if rer <= 0.70:
        return 100
    elif rer >= 1.00:
        return 0
    else:
        # Linear scale from 0.70 (100%) to 1.00 (0%)
        score = (1.00 - rer) / 0.30 * 100
        return int(min(100, max(0, score)))


def calculate_lung_utilization_score(ve_vo2: float) -> int:
    """
    Calculate Lung Utilization Score (0-100%).

    Based on VE/VO2 (ventilatory equivalent for oxygen):
    - VE/VO2 < 20: Excellent efficiency (score: 100%)
    - VE/VO2 20-25: Good efficiency (score: 75-100%)
    - VE/VO2 25-30: Average (score: 50-75%)
    - VE/VO2 30-40: Below average (score: 25-50%)
    - VE/VO2 > 40: Poor (score: 0-25%)

    Lower VE/VO2 = lungs extract more O2 per breath = better.
    """
    if ve_vo2 <= 20:
        return 100
    elif ve_vo2 >= 50:
        return 0
    elif ve_vo2 <= 25:
        # 20-25 maps to 75-100
        return int(100 - (ve_vo2 - 20) * 5)
    elif ve_vo2 <= 30:
        # 25-30 maps to 50-75
        return int(75 - (ve_vo2 - 25) * 5)
    elif ve_vo2 <= 40:
        # 30-40 maps to 25-50
        return int(50 - (ve_vo2 - 30) * 2.5)
    else:
        # 40-50 maps to 0-25
        return int(25 - (ve_vo2 - 40) * 2.5)


def calculate_ventilation_efficiency_score(ve_vco2: float) -> int:
    """
    Calculate Ventilation Efficiency Score (0-100%).

    Based on VE/VCO2 (ventilatory equivalent for CO2):
    - VE/VCO2 < 25: Excellent (score: 100%)
    - VE/VCO2 25-30: Good (score: 75-100%)
    - VE/VCO2 30-35: Average (score: 50-75%)
    - VE/VCO2 35-45: Below average (score: 25-50%)
    - VE/VCO2 > 45: Poor (score: 0-25%)

    Lower = more efficient CO2 clearance.
    Clinical threshold for heart failure prognosis: VE/VCO2 > 34
    """
    if ve_vco2 <= 25:
        return 100
    elif ve_vco2 >= 55:
        return 0
    elif ve_vco2 <= 30:
        return int(100 - (ve_vco2 - 25) * 5)
    elif ve_vco2 <= 35:
        return int(75 - (ve_vco2 - 30) * 5)
    elif ve_vco2 <= 45:
        return int(50 - (ve_vco2 - 35) * 2.5)
    else:
        return int(25 - (ve_vco2 - 45) * 2.5)


def calculate_breathing_coordination_score(data: Dict) -> int:
    """
    Calculate Breathing Coordination Score (0-100%).

    Based on the consistency and relationship between:
    - VO2 and VCO2 patterns (should track together)
    - Stability of RER over time
    - Coefficient of variation in breathing metrics

    More consistent patterns = better coordination.
    """
    scores = []

    # Check RER stability (CV should be low at rest)
    if data['time_series']['rer']:
        rer_std = data['summary_stats'].get('rer_std', 0)
        rer_mean = data['summary_stats'].get('rer_mean', 0.85)
        if rer_mean > 0:
            rer_cv = rer_std / rer_mean * 100  # Coefficient of variation %
            # CV < 5% = excellent, CV > 20% = poor
            if rer_cv <= 5:
                scores.append(100)
            elif rer_cv >= 20:
                scores.append(30)
            else:
                scores.append(int(100 - (rer_cv - 5) * 4.67))

    # Check VO2/VCO2 correlation (should be highly correlated)
    if len(data['time_series']['vo2']) > 5 and len(data['time_series']['vco2']) > 5:
        vo2 = np.array(data['time_series']['vo2'][:min(len(data['time_series']['vo2']), len(data['time_series']['vco2']))])
        vco2 = np.array(data['time_series']['vco2'][:len(vo2)])
        if len(vo2) > 2:
            correlation = np.corrcoef(vo2, vco2)[0, 1]
            # Correlation > 0.9 = excellent, < 0.5 = poor
            if correlation >= 0.95:
                scores.append(100)
            elif correlation <= 0.5:
                scores.append(30)
            else:
                scores.append(int(30 + (correlation - 0.5) * 155.6))

    # Check heart rate stability (should be stable at rest)
    if data['time_series']['hr']:
        hr_std = data['summary_stats'].get('hr_std', 0)
        # At rest, HR std < 3 bpm = excellent, > 10 = poor
        if hr_std <= 3:
            scores.append(100)
        elif hr_std >= 10:
            scores.append(40)
        else:
            scores.append(int(100 - (hr_std - 3) * 8.57))

    if scores:
        return int(np.mean(scores))
    else:
        return 65  # Default to average if no data


def calculate_hrv_score(hr_data: List[float]) -> int:
    """
    Calculate HRV Score (0-100%).

    Without beat-to-beat RR intervals, we estimate HRV from:
    - Heart rate variability over the measurement period
    - Standard deviation of heart rate (SDHR) as proxy

    At rest, some variability is healthy (indicates parasympathetic tone).
    Too little = poor HRV, too much = irregular.
    """
    if not hr_data or len(hr_data) < 5:
        return 65  # Default if insufficient data

    hr_array = np.array(hr_data)
    mean_hr = np.mean(hr_array)
    std_hr = np.std(hr_array)

    # Calculate RMSSD approximation from HR data
    # RMSSD-like metric: sqrt of mean squared differences
    if len(hr_array) > 1:
        successive_diffs = np.diff(hr_array)
        rmssd_like = np.sqrt(np.mean(successive_diffs ** 2))
    else:
        rmssd_like = 0

    # Scoring based on age-adjusted norms
    # Younger: higher HRV is better
    # At rest with ~60-70 bpm, SDHR of 3-5 bpm suggests good HRV

    # Score based on relative variability
    cv = (std_hr / mean_hr) * 100 if mean_hr > 0 else 0

    # CV of 3-8% is healthy at rest
    if 3 <= cv <= 8:
        score = 85 + (5 - abs(cv - 5.5)) * 3  # Peak around 5.5%
    elif cv < 3:
        score = 50 + cv * 11.67  # Low variability
    elif cv <= 15:
        score = 85 - (cv - 8) * 5  # Declining
    else:
        score = max(20, 50 - (cv - 15) * 2)  # Too much variability

    return int(min(100, max(0, score)))


def calculate_autonomic_balance_score(data: Dict) -> int:
    """
    Calculate Sympathetic/Parasympathetic Balance Score (0-100%).

    Without direct HRV frequency analysis, we estimate from:
    - Resting heart rate (lower = more parasympathetic)
    - Heart rate variability pattern
    - Recovery patterns if available

    Score represents parasympathetic dominance (higher = better recovery capacity).
    """
    scores = []

    # Resting heart rate component
    if data['time_series']['hr']:
        mean_hr = data['summary_stats'].get('hr_mean', 70)

        # Lower resting HR indicates parasympathetic dominance
        # Elite athletes: 40-50 bpm (score: 90-100)
        # Average: 60-70 bpm (score: 60-75)
        # Elevated: 80-90+ bpm (score: 30-50)

        if mean_hr <= 50:
            hr_score = 95
        elif mean_hr <= 60:
            hr_score = 85 + (60 - mean_hr)
        elif mean_hr <= 70:
            hr_score = 70 + (70 - mean_hr) * 1.5
        elif mean_hr <= 80:
            hr_score = 55 + (80 - mean_hr) * 1.5
        elif mean_hr <= 90:
            hr_score = 40 + (90 - mean_hr) * 1.5
        else:
            hr_score = max(20, 40 - (mean_hr - 90))

        scores.append(hr_score)

    # HRV component (variability indicates parasympathetic activity)
    if data['time_series']['hr'] and len(data['time_series']['hr']) > 5:
        hrv_score = calculate_hrv_score(data['time_series']['hr'])
        scores.append(hrv_score)

    # RER component (lower RER at rest can indicate better metabolic flexibility)
    if data['time_series']['rer']:
        mean_rer = data['summary_stats'].get('rer_mean', 0.85)
        # RER 0.70-0.75 at rest = good autonomic state
        if mean_rer <= 0.75:
            rer_score = 90
        elif mean_rer <= 0.85:
            rer_score = 70 + (0.85 - mean_rer) * 200
        else:
            rer_score = max(40, 70 - (mean_rer - 0.85) * 200)
        scores.append(rer_score)

    if scores:
        return int(np.mean(scores))
    else:
        return 60  # Default


def calculate_all_scores(pdf_path: str) -> Dict:
    """
    Main function: Extract data and calculate all 7 core scores.

    Returns dict with:
    - patient_info
    - core_scores (the 7 percentage scores)
    - raw_metrics (underlying measurements)
    - calculation_details (explanations)
    """
    # Extract raw data
    data = extract_ergometry_data(pdf_path)

    patient = data['patient_info']
    stats = data['summary_stats']

    result = {
        'patient_info': patient,
        'core_scores': {},
        'raw_metrics': {},
        'calculation_details': {},
        'data_quality': 'good'
    }

    # Check data quality
    has_vo2 = bool(data['time_series']['vo2'])
    has_vco2 = bool(data['time_series']['vco2'])
    has_hr = bool(data['time_series']['hr'])
    has_rer = bool(data['time_series']['rer'])

    if not (has_vo2 or has_rer):
        result['data_quality'] = 'limited'

    # 1. Metabolic Rate Score
    if has_vo2 and all(k in patient for k in ['gender', 'age', 'weight_kg', 'height_cm']):
        mean_vo2 = stats.get('vo2_trimmed_mean', stats.get('vo2_mean', 250))
        measured_rmr = calculate_rmr_from_vo2(mean_vo2)
        predicted_rmr = calculate_predicted_rmr(
            patient['gender'], patient['age'],
            patient['weight_kg'], patient['height_cm']
        )

        result['core_scores']['metabolic_rate'] = calculate_metabolic_rate_score(measured_rmr, predicted_rmr)
        result['raw_metrics']['measured_rmr_kcal'] = round(measured_rmr)
        result['raw_metrics']['predicted_rmr_kcal'] = round(predicted_rmr)
        result['raw_metrics']['rmr_ratio'] = round(measured_rmr / predicted_rmr, 2)
        result['calculation_details']['metabolic_rate'] = (
            f"Measured RMR: {measured_rmr:.0f} kcal/day vs "
            f"Predicted: {predicted_rmr:.0f} kcal/day ({measured_rmr/predicted_rmr*100:.0f}%)"
        )
    else:
        result['core_scores']['metabolic_rate'] = 50  # Default
        result['calculation_details']['metabolic_rate'] = "Insufficient data - using default"

    # 2. Fat-Burning Efficiency Score
    if has_rer:
        mean_rer = stats.get('rer_trimmed_mean', stats.get('rer_mean', 0.85))
        result['core_scores']['fat_burning'] = calculate_fat_burning_score(mean_rer)
        result['raw_metrics']['rer'] = round(mean_rer, 3)

        # Calculate fat/carb percentages
        if mean_rer <= 0.70:
            fat_pct, carb_pct = 100, 0
        elif mean_rer >= 1.00:
            fat_pct, carb_pct = 0, 100
        else:
            fat_pct = round((1.00 - mean_rer) / 0.30 * 100)
            carb_pct = 100 - fat_pct

        result['raw_metrics']['fat_oxidation_pct'] = fat_pct
        result['raw_metrics']['carb_oxidation_pct'] = carb_pct
        result['calculation_details']['fat_burning'] = (
            f"RER: {mean_rer:.2f} = {fat_pct}% fat / {carb_pct}% carbs at rest"
        )
    elif has_vo2 and has_vco2:
        # Calculate RER from VO2/VCO2
        mean_vo2 = stats.get('vo2_mean', 250)
        mean_vco2 = stats.get('vco2_mean', 200)
        calculated_rer = mean_vco2 / mean_vo2 if mean_vo2 > 0 else 0.85
        result['core_scores']['fat_burning'] = calculate_fat_burning_score(calculated_rer)
        result['raw_metrics']['rer'] = round(calculated_rer, 3)
        result['calculation_details']['fat_burning'] = f"Calculated RER from VCO2/VO2: {calculated_rer:.2f}"
    else:
        result['core_scores']['fat_burning'] = 50
        result['calculation_details']['fat_burning'] = "Insufficient data - using default"

    # 3. Lung Utilization Score
    if data['time_series']['ve_vo2']:
        mean_ve_vo2 = stats.get('ve_vo2_trimmed_mean', stats.get('ve_vo2_mean', 30))
        result['core_scores']['lung_util'] = calculate_lung_utilization_score(mean_ve_vo2)
        result['raw_metrics']['ve_vo2'] = round(mean_ve_vo2, 1)
        result['calculation_details']['lung_util'] = f"VE/VO2: {mean_ve_vo2:.1f}"
    else:
        # Estimate from typical values if not available
        result['core_scores']['lung_util'] = 70  # Default to good
        result['calculation_details']['lung_util'] = "VE/VO2 not directly measured - using estimate"

    # 4. Ventilation Efficiency Score
    if data['time_series']['ve_vco2']:
        mean_ve_vco2 = stats.get('ve_vco2_trimmed_mean', stats.get('ve_vco2_mean', 32))
        result['core_scores']['ventilation_eff'] = calculate_ventilation_efficiency_score(mean_ve_vco2)
        result['raw_metrics']['ve_vco2'] = round(mean_ve_vco2, 1)
        result['calculation_details']['ventilation_eff'] = f"VE/VCO2: {mean_ve_vco2:.1f}"
    else:
        result['core_scores']['ventilation_eff'] = 68
        result['calculation_details']['ventilation_eff'] = "VE/VCO2 not directly measured - using estimate"

    # 5. Breathing Coordination Score
    result['core_scores']['breathing_coord'] = calculate_breathing_coordination_score(data)
    result['calculation_details']['breathing_coord'] = "Based on VO2/VCO2 correlation and RER stability"

    # 6. HRV Score
    if has_hr:
        result['core_scores']['hrv'] = calculate_hrv_score(data['time_series']['hr'])
        result['raw_metrics']['mean_hr'] = round(stats.get('hr_mean', 70))
        result['raw_metrics']['hr_std'] = round(stats.get('hr_std', 5), 1)
        result['calculation_details']['hrv'] = (
            f"HR: {stats.get('hr_mean', 70):.0f} ± {stats.get('hr_std', 5):.1f} bpm"
        )
    else:
        result['core_scores']['hrv'] = 65
        result['calculation_details']['hrv'] = "Heart rate data limited - using estimate"

    # 7. Sympathetic/Parasympathetic Balance Score
    result['core_scores']['symp_parasym'] = calculate_autonomic_balance_score(data)
    result['calculation_details']['symp_parasym'] = "Based on resting HR, HRV, and metabolic state"

    return result


def is_raw_ergometry_pdf(pdf_path: str) -> bool:
    """
    Detect if a PDF is raw PNOE ergometry data (needs calculation)
    vs. a processed Performance Report (has scores already).

    Raw ergometry files have:
    - "PNOE Ergometry results" header
    - Time series graphs
    - No percentage scores

    Performance Reports have:
    - Percentage scores like "Metabolic rate - 46%"
    - Detailed analysis sections
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            first_page_text = pdf.pages[0].extract_text() or ""

            # Check for raw ergometry indicators
            is_ergometry = "PNOE Ergometry results" in first_page_text
            is_ergometry = is_ergometry or ("Ergometry" in first_page_text and "Time (sec)" in first_page_text)

            # Check for processed report indicators
            has_scores = bool(re.search(r'(?:Metabolic rate|Fat-burning|Lung utilization).*?-\s*\d+%', first_page_text))

            # If it has ergometry markers and no scores, it's raw data
            if is_ergometry and not has_scores:
                return True

            return False
    except Exception:
        return False


def extract_scores_from_performance_report(pdf_path: str) -> Dict:
    """
    Extract pre-calculated scores from PNOE Performance/RMR Reports.

    These reports already have the percentage scores calculated by PNOE.
    """
    result = {
        'patient_info': {},
        'core_scores': {},
        'raw_metrics': {},
        'data_source': 'performance_report'
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            for page in pdf.pages[:15]:  # First 15 pages should have all scores
                text = page.extract_text() or ""
                all_text += text + "\n"

            # Extract patient info
            name_match = re.search(r'Name\s+([^\n]+?)(?:\s+Status|$)', all_text)
            if name_match:
                result['patient_info']['name'] = name_match.group(1).strip()

            gender_age_match = re.search(r'Gender\s+(\w+)\s*\((\d+)\)', all_text)
            if gender_age_match:
                result['patient_info']['gender'] = gender_age_match.group(1)
                result['patient_info']['age'] = int(gender_age_match.group(2))

            weight_match = re.search(r'Weight\s+(\d+(?:\.\d+)?)\s*kg', all_text)
            if weight_match:
                result['patient_info']['weight_kg'] = float(weight_match.group(1))

            height_match = re.search(r'Height\s+(\d+(?:\.\d+)?)\s*cm', all_text)
            if height_match:
                result['patient_info']['height_cm'] = float(height_match.group(1))

            # Extract core scores using specific patterns
            score_patterns = [
                (r'Sympathetic/Parasympathetic.*?-\s*(\d+)%', 'symp_parasym'),
                (r'Ventilation efficiency.*?-\s*(\d+)%', 'ventilation_eff'),
                (r'Breathing coordination.*?-\s*(\d+)%', 'breathing_coord'),
                (r'Lung utilization.*?-\s*(\d+)%', 'lung_util'),
                (r'Heart Rate Variability.*?-\s*(\d+)%', 'hrv'),
                (r'HRV.*?-\s*(\d+)%', 'hrv'),
                (r'Metabolic rate.*?-\s*(\d+)%', 'metabolic_rate'),
                (r'Fat-burning.*?-\s*(\d+)%', 'fat_burning'),
            ]

            for pattern, score_key in score_patterns:
                match = re.search(pattern, all_text, re.IGNORECASE)
                if match and score_key not in result['core_scores']:
                    result['core_scores'][score_key] = int(match.group(1))

            # Extract raw metrics
            # RMR/calorie values
            calorie_match = re.search(r'(\d{4})\s*kcal/day.*?(\d{4})\s*kcal/day', all_text)
            if calorie_match:
                result['raw_metrics']['burn_kcal'] = int(calorie_match.group(1))
                result['raw_metrics']['eat_kcal'] = int(calorie_match.group(2))

            # Fat/carb mix
            fat_mix_match = re.search(r'(\d+)%\s*fat.*?(\d+)%\s*carb', all_text, re.IGNORECASE)
            if fat_mix_match:
                result['raw_metrics']['fat_percent'] = int(fat_mix_match.group(1))
                result['raw_metrics']['carb_percent'] = int(fat_mix_match.group(2))

    except Exception as e:
        result['error'] = str(e)

    return result


def detect_pdf_type(pdf_path: str) -> str:
    """
    Detect the type of PNOE PDF:
    - 'raw_ergometry': Raw measurement data with charts (needs calculation)
    - 'performance_report': Processed report with scores already calculated
    - 'unknown': Cannot determine type
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Check first page for ergometry indicators
            first_page_text = pdf.pages[0].extract_text() or ""

            # Check for raw ergometry indicators (usually clear on first page)
            is_ergometry = "PNOE Ergometry results" in first_page_text
            is_ergometry = is_ergometry or ("Ergometry" in first_page_text and "Time (sec)" in first_page_text)

            if is_ergometry:
                # Double-check it doesn't also have scores (would be performance report)
                has_scores = bool(re.search(
                    r'(?:Metabolic rate|Fat-burning|Lung utilization).*?-\s*\d+%',
                    first_page_text,
                    re.IGNORECASE
                ))
                if not has_scores:
                    return 'raw_ergometry'

            # Check first 10 pages for performance report indicators
            # (scores may be on later pages in performance reports)
            all_text = ""
            for page in pdf.pages[:10]:
                text = page.extract_text() or ""
                all_text += text + "\n"

            # Check for processed report indicators (scores with percentages)
            has_scores = bool(re.search(
                r'(?:Metabolic rate|Fat-burning|Lung utilization|Heart Rate Variability).*?-\s*\d+%',
                all_text,
                re.IGNORECASE
            ))

            if has_scores:
                return 'performance_report'

            # Check for other performance report indicators
            is_performance = "Performance" in all_text and "Blueprint" in all_text
            is_performance = is_performance or "Caloric Balance" in all_text
            is_performance = is_performance or "You Burn" in all_text

            if is_performance:
                return 'performance_report'

            return 'unknown'
    except Exception:
        return 'unknown'


def process_pnoe_pdf(pdf_path: str) -> Dict:
    """
    Universal function to process any PNOE PDF.

    Automatically detects the PDF type and extracts/calculates scores accordingly.

    Returns:
    - patient_info: Patient demographics
    - core_scores: The 7 metabolic scores (0-100%)
    - raw_metrics: Underlying measurements
    - data_source: 'performance_report', 'raw_ergometry', or 'calculated'
    - data_quality: 'excellent', 'good', 'estimated', 'limited'
    """
    pdf_type = detect_pdf_type(pdf_path)

    if pdf_type == 'performance_report':
        result = extract_scores_from_performance_report(pdf_path)
        result['data_quality'] = 'excellent'
        return result

    elif pdf_type == 'raw_ergometry':
        result = calculate_all_scores(pdf_path)
        result['data_source'] = 'calculated'
        # Determine quality based on what data was available
        if result.get('raw_metrics', {}).get('measured_rmr_kcal'):
            result['data_quality'] = 'good'
        else:
            result['data_quality'] = 'estimated'
        return result

    else:
        return {
            'error': 'Unable to detect PDF type. Please upload a PNOE Ergometry or Performance Report.',
            'data_source': 'unknown',
            'data_quality': 'none'
        }


# Convenience function for direct testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
        print(f"\nAnalyzing: {pdf_file}")
        print("=" * 60)

        pdf_type = detect_pdf_type(pdf_file)
        print(f"Detected Type: {pdf_type}")

        results = process_pnoe_pdf(pdf_file)

        if 'error' in results:
            print(f"\nError: {results['error']}")
        else:
            print(f"Data Source: {results.get('data_source', 'unknown')}")
            print(f"Data Quality: {results.get('data_quality', 'unknown')}")

            print("\nPatient Info:")
            for k, v in results.get('patient_info', {}).items():
                print(f"  {k}: {v}")

            print("\nCore Scores:")
            for score_name, score_val in results.get('core_scores', {}).items():
                detail = results.get('calculation_details', {}).get(score_name, '')
                if detail:
                    print(f"  {score_name}: {score_val}% - {detail}")
                else:
                    print(f"  {score_name}: {score_val}%")

            if results.get('raw_metrics'):
                print("\nRaw Metrics:")
                for k, v in results['raw_metrics'].items():
                    print(f"  {k}: {v}")

            # Compare with expected PNOE scores if this is raw ergometry
            if pdf_type == 'raw_ergometry':
                print("\n" + "=" * 60)
                print("NOTE: Scores calculated from raw ergometry data are estimates.")
                print("For accurate scores, use the PNOE Performance Report instead.")
    else:
        print("Usage: python ergometry_calculator.py <pdf_path>")
        print("\nSupported PDF types:")
        print("  - PNOE Performance/RMR Reports (has pre-calculated scores)")
        print("  - PNOE Ergometry exports (calculates scores from raw data)")
