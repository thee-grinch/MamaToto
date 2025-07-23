# app/api/child.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
from ..core.deps import get_db, get_current_user
from ..models.user import User
from ..models.child import Child, Vaccination, GrowthRecord, Milestone
from ..schemas.child import (
    ChildCreate, ChildResponse, ChildUpdate,
    VaccinationCreate, VaccinationResponse, VaccinationUpdate,
    GrowthRecordCreate, GrowthRecordResponse,
    MilestoneCreate, MilestoneResponse, MilestoneUpdate
)
from ..utils.vaccination import get_vaccination_schedule
from ..utils.growth import calculate_percentiles

router = APIRouter(prefix="/children", tags=["children"])

@router.post("/", response_model=ChildResponse)
def create_child(
    child: ChildCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_child = Child(
        user_id=current_user.id,
        name=child.name,
        birth_date=child.birth_date,
        gender=child.gender,
        birth_weight=child.birth_weight,
        birth_length=child.birth_length,
        birth_complications=child.birth_complications
    )
    
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    
    # Calculate age and add to response
    age_days = (date.today() - db_child.birth_date).days
    db_child.age_months = age_days // 30
    
    # Create vaccination schedule
    vaccination_schedule = get_vaccination_schedule()
    for vaccine_info in vaccination_schedule:
        scheduled_date = db_child.birth_date + timedelta(days=vaccine_info["days_from_birth"])
        vaccination = Vaccination(
            child_id=db_child.id,
            vaccine_name=vaccine_info["name"],
            vaccine_code=vaccine_info["code"],
            scheduled_date=scheduled_date,
            status="pending"
        )
        db.add(vaccination)
    
    db.commit()
    return db_child

@router.get("/", response_model=List[ChildResponse])
def get_children(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    children = db.query(Child).filter(
        Child.user_id == current_user.id,
        Child.is_active == True
    ).order_by(Child.birth_date.desc()).all()
    
    # Add calculated age
    for child in children:
        age_days = (date.today() - child.birth_date).days
        child.age_months = age_days // 30
    
    return children

@router.get("/{child_id}", response_model=ChildResponse)
def get_child(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    child = db.query(Child).filter(
        Child.id == child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    age_days = (date.today() - child.birth_date).days
    child.age_months = age_days // 30
    
    return child

@router.put("/{child_id}", response_model=ChildResponse)
def update_child(
    child_id: int,
    child_update: ChildUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    child = db.query(Child).filter(
        Child.id == child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    for field, value in child_update.dict(exclude_unset=True).items():
        setattr(child, field, value)
    
    db.commit()
    db.refresh(child)
    return child

@router.post("/{child_id}/vaccinations", response_model=VaccinationResponse)
def create_vaccination(
    child_id: int,
    vaccination: VaccinationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify child belongs to current user
    child = db.query(Child).filter(
        Child.id == child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    db_vaccination = Vaccination(
        child_id=child_id,
        vaccine_name=vaccination.vaccine_name,
        vaccine_code=vaccination.vaccine_code,
        scheduled_date=vaccination.scheduled_date,
        administered_date=vaccination.administered_date,
        batch_number=vaccination.batch_number,
        healthcare_provider=vaccination.healthcare_provider,
        notes=vaccination.notes,
        status="completed" if vaccination.administered_date else "pending"
    )
    
    db.add(db_vaccination)
    db.commit()
    db.refresh(db_vaccination)
    return db_vaccination

@router.get("/{child_id}/vaccinations", response_model=List[VaccinationResponse])
def get_child_vaccinations(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify child belongs to current user
    child = db.query(Child).filter(
        Child.id == child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    vaccinations = db.query(Vaccination).filter(
        Vaccination.child_id == child_id
    ).order_by(Vaccination.scheduled_date).all()
    
    # Update overdue status
    for vaccination in vaccinations:
        if (vaccination.status == "pending" and 
            vaccination.scheduled_date < date.today() - timedelta(days=30)):
            vaccination.status = "overdue"
    
    db.commit()
    return vaccinations

@router.post("/{child_id}/growth", response_model=GrowthRecordResponse)
def create_growth_record(
    child_id: int,
    growth_record: GrowthRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify child belongs to current user
    child = db.query(Child).filter(
        Child.id == child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    # Calculate age at recording
    age_days = (growth_record.recorded_date - child.birth_date).days
    age_months = age_days // 30
    
    # Calculate percentiles using WHO standards
    percentiles = calculate_percentiles(
        age_months=age_months,
        weight=growth_record.weight,
        height=growth_record.height,
        gender=child.gender.value if child.gender else "unknown"
    )
    
    db_growth_record = GrowthRecord(
        child_id=child_id,
        recorded_date=growth_record.recorded_date,
        age_months=age_months,
        weight=growth_record.weight,
        height=growth_record.height,
        head_circumference=growth_record.head_circumference,
        weight_percentile=percentiles.get("weight_percentile"),
        height_percentile=percentiles.get("height_percentile"),
        bmi=percentiles.get("bmi"),
        notes=growth_record.notes
    )
    
    db.add(db_growth_record)
    db.commit()
    db.refresh(db_growth_record)
    return db_growth_record

@router.get("/{child_id}/growth", response_model=List[GrowthRecordResponse])
def get_child_growth_records(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify child belongs to current user
    child = db.query(Child).filter(
        Child.id == child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    growth_records = db.query(GrowthRecord).filter(
        GrowthRecord.child_id == child_id
    ).order_by(GrowthRecord.recorded_date).all()
    
    return growth_records