# app/api/pregnancy.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
from ..core.deps import get_db, get_current_user
from ..models.user import User
from ..models.pregnancy import Pregnancy, Appointment
from ..schemas.pregnancy import (
    PregnancyCreate, PregnancyResponse, PregnancyUpdate,
    AppointmentCreate, AppointmentResponse, AppointmentUpdate
)

router = APIRouter(prefix="/pregnancy", tags=["pregnancy"])

@router.post("/", response_model=PregnancyResponse)
def create_pregnancy(
    pregnancy: PregnancyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Deactivate existing pregnancies
    db.query(Pregnancy).filter(
        Pregnancy.user_id == current_user.id,
        Pregnancy.is_active == True
    ).update({"is_active": False})
    
    # Calculate current week
    current_week = None
    if pregnancy.due_date:
        weeks_pregnant = (280 - (pregnancy.due_date - date.today()).days) // 7
        current_week = max(1, min(42, weeks_pregnant))
    
    db_pregnancy = Pregnancy(
        user_id=current_user.id,
        due_date=pregnancy.due_date,
        current_week=current_week,
        last_weight=pregnancy.last_weight,
        last_checkup=pregnancy.last_checkup,
        complications=pregnancy.complications,
        notes=pregnancy.notes
    )
    
    db.add(db_pregnancy)
    db.commit()
    db.refresh(db_pregnancy)
    
    # Calculate additional fields
    days_remaining = (db_pregnancy.due_date - date.today()).days
    db_pregnancy.weeks_remaining = max(0, days_remaining // 7)
    db_pregnancy.trimester = min(3, max(1, (current_week or 0) // 13 + 1))
    
    return db_pregnancy

@router.get("/", response_model=List[PregnancyResponse])
def get_pregnancies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pregnancies = db.query(Pregnancy).filter(
        Pregnancy.user_id == current_user.id
    ).order_by(Pregnancy.created_at.desc()).all()
    
    # Add calculated fields
    for pregnancy in pregnancies:
        if pregnancy.due_date:
            days_remaining = (pregnancy.due_date - date.today()).days
            pregnancy.weeks_remaining = max(0, days_remaining // 7)
            pregnancy.trimester = min(3, max(1, (pregnancy.current_week or 0) // 13 + 1))
    
    return pregnancies

@router.get("/active", response_model=PregnancyResponse)
def get_active_pregnancy(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pregnancy = db.query(Pregnancy).filter(
        Pregnancy.user_id == current_user.id,
        Pregnancy.is_active == True
    ).first()
    
    if not pregnancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active pregnancy found"
        )
    
    # Add calculated fields
    days_remaining = (pregnancy.due_date - date.today()).days
    pregnancy.weeks_remaining = max(0, days_remaining // 7)
    pregnancy.trimester = min(3, max(1, (pregnancy.current_week or 0) // 13 + 1))
    
    return pregnancy

@router.put("/{pregnancy_id}", response_model=PregnancyResponse)
def update_pregnancy(
    pregnancy_id: int,
    pregnancy_update: PregnancyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pregnancy = db.query(Pregnancy).filter(
        Pregnancy.id == pregnancy_id,
        Pregnancy.user_id == current_user.id
    ).first()
    
    if not pregnancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pregnancy not found"
        )
    
    for field, value in pregnancy_update.dict(exclude_unset=True).items():
        setattr(pregnancy, field, value)
    
    db.commit()
    db.refresh(pregnancy)
    return pregnancy

@router.post("/appointments", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_appointment = Appointment(
        user_id=current_user.id,
        pregnancy_id=appointment.pregnancy_id,
        appointment_type=appointment.appointment_type,
        scheduled_date=appointment.scheduled_date,
        notes=appointment.notes,
        location=appointment.location
    )
    
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.get("/appointments", response_model=List[AppointmentResponse])
def get_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appointments = db.query(Appointment).filter(
        Appointment.user_id == current_user.id
    ).order_by(Appointment.scheduled_date).all()
    
    return appointments