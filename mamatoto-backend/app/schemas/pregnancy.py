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
