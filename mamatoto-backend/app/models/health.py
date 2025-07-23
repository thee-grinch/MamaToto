# app/models/health.py
from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class HealthRecord(Base):
    __tablename__ = "health_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    child_id = Column(Integer, ForeignKey("children.id"))  # Optional - for child health records
    pregnancy_id = Column(Integer, ForeignKey("pregnancies.id"))  # Optional - for pregnancy records
    record_type = Column(String, nullable=False)  # symptom, medication, test_result, general
    title = Column(String, nullable=False)
    description = Column(Text)
    severity = Column(String)  # low, medium, high, critical
    symptoms = Column(JSON)  # Store list of symptoms
    medications = Column(JSON)  # Store medication info
    test_results = Column(JSON)  # Store test results
    action_taken = Column(Text)
    outcome = Column(Text)
    recorded_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="health_records")
    child = relationship("Child")
    pregnancy = relationship("Pregnancy")

class MentalHealthAssessment(Base):
    __tablename__ = "mental_health_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_type = Column(String, nullable=False)  # epds, gad7, phq9
    score = Column(Integer)
    risk_level = Column(String)  # low, moderate, high
    responses = Column(JSON)  # Store all responses
    recommendations = Column(Text)
    assessment_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    relationship = Column(String)  # spouse, mother, friend, doctor
    phone = Column(String, nullable=False)
    email = Column(String)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")