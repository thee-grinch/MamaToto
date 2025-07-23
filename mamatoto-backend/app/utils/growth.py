# app/utils/growth.py
from typing import Dict, Optional
import math

def calculate_percentiles(age_months: int, weight: Optional[float], 
                         height: Optional[float], gender: str) -> Dict:
    """
    Calculate growth percentiles using simplified WHO standards
    Note: In production, use the actual WHO growth standards tables
    """
    percentiles = {}
    
    # Simplified calculation - replace with actual WHO standards
    if weight and age_months >= 0:
        # Weight percentiles (simplified)
        if gender.lower() == "male":
            expected_weight = 3.3 + (age_months * 0.6)  # Simplified formula
        else:
            expected_weight = 3.2 + (age_months * 0.55)  # Simplified formula
        
        weight_z_score = (weight - expected_weight) / (expected_weight * 0.15)
        percentiles["weight_percentile"] = norm_cdf(weight_z_score) * 100
    
    if height and age_months >= 0:
        # Height percentiles (simplified)
        if gender.lower() == "male":
            expected_height = 50 + (age_months * 1.8)  # Simplified formula
        else:
            expected_height = 49.5 + (age_months * 1.75)  # Simplified formula
        
        height_z_score = (height - expected_height) / (expected_height * 0.1)
        percentiles["height_percentile"] = norm_cdf(height_z_score) * 100
    
    # Calculate BMI if both weight and height available
    if weight and height:
        height_m = height / 100  # Convert cm to meters
        bmi = weight / (height_m ** 2)
        percentiles["bmi"] = round(bmi, 2)
    
    return percentiles

def norm_cdf(x):
    """Approximation of normal cumulative distribution function"""
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def get_growth_alerts(child_age_months: int, weight_percentile: Optional[float], 
                     height_percentile: Optional[float]) -> list:
    """Generate growth-related alerts"""
    alerts = []
    
    if weight_percentile is not None:
        if weight_percentile < 3:
            alerts.append("Weight below 3rd percentile - consider nutritional assessment")
        elif weight_percentile > 97:
            alerts.append("Weight above 97th percentile - monitor for obesity risk")
    
    if height_percentile is not None:
        if height_percentile < 3:
            alerts.append("Height below 3rd percentile - consider growth assessment")
    
    return alerts