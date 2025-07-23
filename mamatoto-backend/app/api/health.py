# app/api/health.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ..core.deps import get_db, get_current_user
from ..models.user import User
from ..models.health import HealthRecord, MentalHealthAssessment, EmergencyContact
from ..schemas.health import (
    HealthRecordCreate, HealthRecordResponse,
    MentalHealthAssessmentCreate, MentalHealthAssessmentResponse,
    EmergencyContactCreate, EmergencyContactResponse
)

router = APIRouter(prefix="/health", tags=["health"])

# Health Records
@router.post("/records", response_model=HealthRecordResponse)
def create_health_record(
    record: HealthRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_record = HealthRecord(
        user_id=current_user.id,
        child_id=record.child_id,
        pregnancy_id=record.pregnancy_id,
        record_type=record.record_type,
        title=record.title,
        description=record.description,
        severity=record.severity,
        symptoms=record.symptoms,
        medications=record.medications,
        test_results=record.test_results,
        action_taken=record.action_taken,
        outcome=record.outcome,
        recorded_date=record.recorded_date
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/records", response_model=List[HealthRecordResponse])
def get_health_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = db.query(HealthRecord).filter(
        HealthRecord.user_id == current_user.id
    ).order_by(HealthRecord.created_at.desc()).all()
    
    return records

@router.get("/records/{record_id}", response_model=HealthRecordResponse)
def get_health_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = db.query(HealthRecord).filter(
        HealthRecord.id == record_id,
        HealthRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health record not found"
        )
    
    return record

# Mental Health Assessments
@router.post("/mental-health", response_model=MentalHealthAssessmentResponse)
def create_mental_health_assessment(
    assessment: MentalHealthAssessmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Calculate score based on assessment type
    score = calculate_assessment_score(assessment.assessment_type, assessment.responses)
    risk_level = determine_risk_level(assessment.assessment_type, score)
    recommendations = generate_recommendations(assessment.assessment_type, risk_level)
    
    db_assessment = MentalHealthAssessment(
        user_id=current_user.id,
        assessment_type=assessment.assessment_type,
        score=score,
        risk_level=risk_level,
        responses=assessment.responses,
        recommendations=recommendations,
        assessment_date=assessment.assessment_date
    )
    
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

@router.get("/mental-health", response_model=List[MentalHealthAssessmentResponse])
def get_mental_health_assessments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assessments = db.query(MentalHealthAssessment).filter(
        MentalHealthAssessment.user_id == current_user.id
    ).order_by(MentalHealthAssessment.created_at.desc()).all()
    
    return assessments

# Emergency Contacts
@router.post("/emergency-contacts", response_model=EmergencyContactResponse)
def create_emergency_contact(
    contact: EmergencyContactCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # If this is set as primary, unset other primary contacts
    if contact.is_primary:
        db.query(EmergencyContact).filter(
            EmergencyContact.user_id == current_user.id,
            EmergencyContact.is_primary == True
        ).update({"is_primary": False})
    
    db_contact = EmergencyContact(
        user_id=current_user.id,
        name=contact.name,
        relationship=contact.relationship,
        phone=contact.phone,
        email=contact.email,
        is_primary=contact.is_primary
    )
    
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/emergency-contacts", response_model=List[EmergencyContactResponse])
def get_emergency_contacts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contacts = db.query(EmergencyContact).filter(
        EmergencyContact.user_id == current_user.id
    ).order_by(EmergencyContact.is_primary.desc(), EmergencyContact.name).all()
    
    return contacts

# Helper functions
def calculate_assessment_score(assessment_type: str, responses: dict) -> int:
    """Calculate score based on assessment type and responses"""
    if assessment_type == "epds":  # Edinburgh Postnatal Depression Scale
        score = sum(responses.values())
        return min(30, max(0, score))
    elif assessment_type == "gad7":  # Generalized Anxiety Disorder 7
        score = sum(responses.values())
        return min(21, max(0, score))
    elif assessment_type == "phq9":  # Patient Health Questionnaire 9
        score = sum(responses.values())
        return min(27, max(0, score))
    
    return 0

def determine_risk_level(assessment_type: str, score: int) -> str:
    """Determine risk level based on assessment type and score"""
    if assessment_type == "epds":
        if score >= 13:
            return "high"
        elif score >= 10:
            return "moderate"
        else:
            return "low"
    elif assessment_type == "gad7":
        if score >= 15:
            return "high"
        elif score >= 10:
            return "moderate"
        elif score >= 5:
            return "low"
        else:
            return "minimal"
    elif assessment_type == "phq9":
        if score >= 20:
            return "high"
        elif score >= 15:
            return "moderate"
        elif score >= 10:
            return "low"
        else:
            return "minimal"
    
    return "low"

def generate_recommendations(assessment_type: str, risk_level: str) -> str:
    """Generate recommendations based on assessment results"""
    if risk_level == "high":
        return "Please consider speaking with a healthcare professional immediately. Your responses indicate you may benefit from professional support."
    elif risk_level == "moderate":
        return "Your responses suggest you may be experiencing some challenges. Consider discussing these feelings with a healthcare provider."
    else:
        return "Your responses indicate you're doing well. Continue with healthy habits and don't hesitate to seek support if needed."
