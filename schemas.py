# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    preferred_language: str = "en"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    preferred_language: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

# app/schemas/pregnancy.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class PregnancyBase(BaseModel):
    due_date: date
    current_week: Optional[int] = None
    last_weight: Optional[float] = None
    last_checkup: Optional[date] = None
    complications: Optional[str] = None
    notes: Optional[str] = None

class PregnancyCreate(PregnancyBase):
    pass

class PregnancyUpdate(BaseModel):
    current_week: Optional[int] = None
    last_weight: Optional[float] = None
    last_checkup: Optional[date] = None
    complications: Optional[str] = None
    notes: Optional[str] = None

class PregnancyResponse(PregnancyBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    weeks_remaining: Optional[int] = None
    trimester: Optional[int] = None

    class Config:
        from_attributes = True

class AppointmentBase(BaseModel):
    appointment_type: str
    scheduled_date: date
    notes: Optional[str] = None
    location: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pregnancy_id: Optional[int] = None

class AppointmentUpdate(BaseModel):
    scheduled_date: Optional[date] = None
    completed: Optional[bool] = None
    notes: Optional[str] = None
    location: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: int
    pregnancy_id: Optional[int]
    user_id: int
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True

# app/schemas/child.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class ChildBase(BaseModel):
    name: str
    birth_date: date
    gender: Optional[GenderEnum] = None
    birth_weight: Optional[float] = None
    birth_length: Optional[float] = None
    birth_complications: Optional[str] = None

class ChildCreate(ChildBase):
    pass

class ChildUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[GenderEnum] = None
    birth_complications: Optional[str] = None

class ChildResponse(ChildBase):
    id: int
    user_id: int
    age_months: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VaccinationBase(BaseModel):
    vaccine_name: str
    vaccine_code: Optional[str] = None
    scheduled_date: date
    administered_date: Optional[date] = None
    batch_number: Optional[str] = None
    healthcare_provider: Optional[str] = None
    notes: Optional[str] = None

class VaccinationCreate(VaccinationBase):
    child_id: int

class VaccinationUpdate(BaseModel):
    administered_date: Optional[date] = None
    status: Optional[str] = None
    batch_number: Optional[str] = None
    healthcare_provider: Optional[str] = None
    notes: Optional[str] = None

class VaccinationResponse(VaccinationBase):
    id: int
    child_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class GrowthRecordBase(BaseModel):
    recorded_date: date
    weight: Optional[float] = None
    height: Optional[float] = None
    head_circumference: Optional[float] = None
    notes: Optional[str] = None

class GrowthRecordCreate(GrowthRecordBase):
    child_id: int

class GrowthRecordResponse(GrowthRecordBase):
    id: int
    child_id: int
    age_months: Optional[int]
    weight_percentile: Optional[float]
    height_percentile: Optional[float]
    bmi: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True

class MilestoneBase(BaseModel):
    milestone_type: str
    milestone_name: str
    typical_age_months: int
    achieved_date: Optional[date] = None
    is_achieved: bool = False
    notes: Optional[str] = None

class MilestoneCreate(MilestoneBase):
    child_id: int

class MilestoneUpdate(BaseModel):
    achieved_date: Optional[date] = None
    is_achieved: Optional[bool] = None
    notes: Optional[str] = None

class MilestoneResponse(MilestoneBase):
    id: int
    child_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# app/schemas/health.py
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date

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