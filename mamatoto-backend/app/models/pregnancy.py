# app/models/pregnancy.py
from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Pregnancy(Base):
    __tablename__ = "pregnancies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    due_date = Column(Date, nullable=False)
    current_week = Column(Integer)
    is_active = Column(Boolean, default=True)
    last_weight = Column(Float)
    last_checkup = Column(Date)
    complications = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="pregnancies")
    appointments = relationship("Appointment", back_populates="pregnancy", cascade="all, delete-orphan")

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    pregnancy_id = Column(Integer, ForeignKey("pregnancies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    appointment_type = Column(String, nullable=False)  # anc, ultrasound, specialist
    scheduled_date = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    notes = Column(Text)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    pregnancy = relationship("Pregnancy", back_populates="appointments")
    user = relationship("User")
