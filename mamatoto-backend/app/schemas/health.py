# app/schemas/health.py
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date

from .user import UserResponse
from .pregnancy import PregnancyResponse, AppointmentResponse
from .child import ChildResponse, VaccinationResponse

class HealthRecordBase(BaseModel):
    record_type: str
    title: str
    description: Optional[str] = None
    severity: Optional[str] = None
    symptoms: Optional[List[str]] = None
    medications: Optional[List[Dict[str, Any]]] = None
    test_results: Optional[Dict[str, Any]] = None
    action_taken: Optional[str] = None
    outcome: Optional[str] = None
    recorded_date: date

class HealthRecordCreate(HealthRecordBase):
    child_id: Optional[int] = None
    pregnancy_id: Optional[int] = None

class HealthRecordResponse(HealthRecordBase):
    id: int
    user_id: int
    child_id: Optional[int]
    pregnancy_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class MentalHealthAssessmentBase(BaseModel):
    assessment_type: str
    responses: Dict[str, Any]
    assessment_date: date

class MentalHealthAssessmentCreate(MentalHealthAssessmentBase):
    pass

class MentalHealthAssessmentResponse(MentalHealthAssessmentBase):
    id: int
    user_id: int
    score: Optional[int]
    risk_level: Optional[str]
    recommendations: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class EmergencyContactBase(BaseModel):
    name: str
    relationship: Optional[str] = None
    phone: str
    email: Optional[str] = None
    is_primary: bool = False

class EmergencyContactCreate(EmergencyContactBase):
    pass

class EmergencyContactResponse(EmergencyContactBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    user: "UserResponse"
    active_pregnancy: Optional["PregnancyResponse"] = None
    children: List["ChildResponse"] = []
    upcoming_appointments: List["AppointmentResponse"] = []
    overdue_vaccinations: List["VaccinationResponse"] = []
    recent_health_records: List["HealthRecordResponse"] = []
    growth_alerts: List[str] = []

