
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