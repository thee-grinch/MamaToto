# app/models/child.py
from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class Child(Base):
    __tablename__ = "children"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(Enum(GenderEnum))
    birth_weight = Column(Float)  # in kg
    birth_length = Column(Float)  # in cm
    birth_complications = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="children")
    vaccinations = relationship("Vaccination", back_populates="child", cascade="all, delete-orphan")
    growth_records = relationship("GrowthRecord", back_populates="child", cascade="all, delete-orphan")
    milestones = relationship("Milestone", back_populates="child", cascade="all, delete-orphan")

class Vaccination(Base):
    __tablename__ = "vaccinations"
    
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    vaccine_name = Column(String, nullable=False)
    vaccine_code = Column(String)  # WHO vaccine codes
    scheduled_date = Column(Date, nullable=False)
    administered_date = Column(Date)
    status = Column(String, default="pending")  # pending, completed, overdue, skipped
    batch_number = Column(String)
    healthcare_provider = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    child = relationship("Child", back_populates="vaccinations")

class GrowthRecord(Base):
    __tablename__ = "growth_records"
    
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    recorded_date = Column(Date, nullable=False)
    age_months = Column(Integer)  # Age in months at recording
    weight = Column(Float)  # in kg
    height = Column(Float)  # in cm
    head_circumference = Column(Float)  # in cm
    weight_percentile = Column(Float)
    height_percentile = Column(Float)
    bmi = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    child = relationship("Child", back_populates="growth_records")

class Milestone(Base):
    __tablename__ = "milestones"
    
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    milestone_type = Column(String, nullable=False)  # motor, language, social, cognitive
    milestone_name = Column(String, nullable=False)
    typical_age_months = Column(Integer)  # Typical age for milestone
    achieved_date = Column(Date)
    is_achieved = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    child = relationship("Child", back_populates="milestones")