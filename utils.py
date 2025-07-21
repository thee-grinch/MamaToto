# app/utils/vaccination.py
from typing import List, Dict

def get_vaccination_schedule() -> List[Dict]:
    """
    Returns the WHO/Kenya vaccination schedule
    """
    return [
        # Birth vaccines
        {"name": "BCG", "code": "BCG", "days_from_birth": 0, "description": "Tuberculosis protection"},
        {"name": "OPV 0", "code": "OPV0", "days_from_birth": 0, "description": "Oral Polio Vaccine - Birth dose"},
        
        # 6 weeks
        {"name": "OPV 1", "code": "OPV1", "days_from_birth": 42, "description": "Oral Polio Vaccine - 1st dose"},
        {"name": "DPT-HepB-Hib 1", "code": "PENTA1", "days_from_birth": 42, "description": "Pentavalent vaccine - 1st dose"},
        {"name": "PCV 1", "code": "PCV1", "days_from_birth": 42, "description": "Pneumococcal Conjugate Vaccine - 1st dose"},
        {"name": "Rota 1", "code": "ROTA1", "days_from_birth": 42, "description": "Rotavirus vaccine - 1st dose"},
        
        # 10 weeks
        {"name": "OPV 2", "code": "OPV2", "days_from_birth": 70, "description": "Oral Polio Vaccine - 2nd dose"},
        {"name": "DPT-HepB-Hib 2", "code": "PENTA2", "days_from_birth": 70, "description": "Pentavalent vaccine - 2nd dose"},
        {"name": "PCV 2", "code": "PCV2", "days_from_birth": 70, "description": "Pneumococcal Conjugate Vaccine - 2nd dose"},
        {"name": "Rota 2", "code": "ROTA2", "days_from_birth": 70, "description": "Rotavirus vaccine - 2nd dose"},
        
        # 14 weeks
        {"name": "OPV 3", "code": "OPV3", "days_from_birth": 98, "description": "Oral Polio Vaccine - 3rd dose"},
        {"name": "DPT-HepB-Hib 3", "code": "PENTA3", "days_from_birth": 98, "description": "Pentavalent vaccine - 3rd dose"},
        {"name": "PCV 3", "code": "PCV3", "days_from_birth": 98, "description": "Pneumococcal Conjugate Vaccine - 3rd dose"},
        {"name": "IPV", "code": "IPV", "days_from_birth": 98, "description": "Inactivated Polio Vaccine"},
        
        # 9 months
        {"name": "Measles-Rubella 1", "code": "MR1", "days_from_birth": 270, "description": "Measles-Rubella vaccine - 1st dose"},
        {"name": "Yellow Fever", "code": "YF", "days_from_birth": 270, "description": "Yellow Fever vaccine"},
        
        # 18 months
        {"name": "Measles-Rubella 2", "code": "MR2", "days_from_birth": 540, "description": "Measles-Rubella vaccine - 2nd dose"},
        {"name": "DPT Booster", "code": "DPT_BOOSTER", "days_from_birth": 540, "description": "DPT Booster dose"},
    ]

def calculate_vaccine_status(scheduled_date, administered_date, current_date):
    """Calculate vaccination status based on dates"""
    if administered_date:
        return "completed"
    elif current_date > scheduled_date:
        days_overdue = (current_date - scheduled_date).days
        if days_overdue > 30:
            return "overdue"
        else:
            return "due"
    else:
        return "pending"

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

# app/utils/pregnancy.py
from datetime import date, timedelta
from typing import Dict, List

def calculate_pregnancy_week(due_date: date, current_date: date = None) -> int:
    """Calculate current pregnancy week based on due date"""
    if current_date is None:
        current_date = date.today()
    
    # Standard pregnancy is 280 days (40 weeks)
    conception_date = due_date - timedelta(days=280)
    days_pregnant = (current_date - conception_date).days
    weeks_pregnant = days_pregnant // 7
    
    return max(1, min(42, weeks_pregnant))  # Clamp between 1-42 weeks

def get_trimester(week: int) -> int:
    """Get trimester based on pregnancy week"""
    if week <= 12:
        return 1
    elif week <= 27:
        return 2
    else:
        return 3

def get_weekly_info(week: int) -> Dict:
    """Get pregnancy information for specific week"""
    trimester = get_trimester(week)
    
    # Simplified weekly info - expand with detailed medical information
    info = {
        "week": week,
        "trimester": trimester,
        "baby_size": get_baby_size(week),
        "symptoms": get_common_symptoms(week),
        "tips": get_pregnancy_tips(week),
        "appointments": get_recommended_appointments(week)
    }
    
    return info

def get_baby_size(week: int) -> str:
    """Get baby size comparison for the week"""
    size_comparisons = {
        4: "poppy seed", 6: "lentil", 8: "raspberry", 10: "strawberry",
        12: "lime", 16: "avocado", 20: "banana", 24: "ear of corn",
        28: "eggplant", 32: "squash", 36: "cantaloupe", 40: "watermelon"
    }
    
    for w in sorted(size_comparisons.keys(), reverse=True):
        if week >= w:
            return size_comparisons[w]
    return "tiny seed"

def get_common_symptoms(week: int) -> List[str]:
    """Get common symptoms for pregnancy week"""
    trimester = get_trimester(week)
    
    if trimester == 1:
        return ["Morning sickness", "Fatigue", "Breast tenderness", "Frequent urination"]
    elif trimester == 2:
        return ["Increased energy", "Growing belly", "Back pain", "Heartburn"]
    else:
        return ["Braxton Hicks contractions", "Shortness of breath", "Swelling", "Frequent urination"]

def get_pregnancy_tips(week: int) -> List[str]:
    """Get pregnancy tips for specific week"""
    trimester = get_trimester(week)
    
    if trimester == 1:
        return [
            "Take prenatal vitamins with folic acid",
            "Avoid alcohol, smoking, and raw foods",
            "Get plenty of rest",
            "Stay hydrated"
        ]
    elif trimester == 2:
        return [
            "Start monitoring baby movements",
            "Practice good posture",
            "Wear comfortable, supportive shoes",
            "Consider prenatal classes"
        ]
    else:
        return [
            "Practice breathing exercises",
            "Pack your hospital bag",
            "Monitor baby movements daily",
            "Watch for signs of labor"
        ]

def get_recommended_appointments(week: int) -> List[str]:
    """Get recommended appointments for pregnancy week"""
    appointments = []
    
    if week in [8, 12, 16, 20, 24, 28, 32, 36, 38, 40]:
        appointments.append("Routine prenatal checkup")
    
    if week == 20:
        appointments.append("Anatomy ultrasound")
    
    if week in [24, 28]:
        appointments.append("Glucose screening test")
    
    if week >= 36:
        appointments.append("Group B Strep test")
    
    return appointments

def get_danger_signs() -> List[Dict]:
    """Get list of pregnancy danger signs to watch for"""
    return [
        {
            "symptom": "Severe abdominal pain",
            "urgency": "high",
            "action": "Seek immediate medical attention"
        },
        {
            "symptom": "Heavy bleeding",
            "urgency": "high",
            "action": "Go to hospital immediately"
        },
        {
            "symptom": "Severe headache with vision changes",
            "urgency": "high",
            "action": "Contact healthcare provider immediately"
        },
        {
            "symptom": "Persistent vomiting",
            "urgency": "medium",
            "action": "Contact healthcare provider"
        },
        {
            "symptom": "Decreased fetal movement",
            "urgency": "high",
            "action": "Monitor for 2 hours, if no improvement seek care"
        },
        {
            "symptom": "Signs of preterm labor",
            "urgency": "high",
            "action": "Go to hospital immediately"
        }
    ]