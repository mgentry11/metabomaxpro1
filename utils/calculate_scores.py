"""
Calculate Scores - Biological age and other metrics
This is a minimal implementation to allow app.py to import successfully.
"""

def calculate_biological_age(vo2max, age, gender):
    """
    Calculate biological age based on VO2max

    Args:
        vo2max: VO2max value in ml/kg/min
        age: Chronological age in years
        gender: 'Male' or 'Female'

    Returns:
        dict: Dictionary containing biological age and percentile data
    """
    # This is a simplified stub implementation
    # In production, this would use actual VO2max percentile tables

    # Default to chronological age if no valid vo2max
    if not vo2max or vo2max <= 0:
        return {
            'biological_age': age,
            'percentile': 50,
            'years_younger': 0,
            'fitness_level': 'Average'
        }

    # Simplified calculation - higher VO2max = younger biological age
    # This is placeholder logic
    percentile = min(95, max(5, (vo2max / 60.0) * 100))
    years_difference = int((percentile - 50) / 10)
    biological_age = max(20, age - years_difference)

    if percentile >= 80:
        fitness_level = 'Excellent'
    elif percentile >= 60:
        fitness_level = 'Good'
    elif percentile >= 40:
        fitness_level = 'Average'
    elif percentile >= 20:
        fitness_level = 'Below Average'
    else:
        fitness_level = 'Poor'

    return {
        'biological_age': biological_age,
        'percentile': int(percentile),
        'years_younger': age - biological_age,
        'fitness_level': fitness_level
    }
