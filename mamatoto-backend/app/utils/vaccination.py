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