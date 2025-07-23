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
