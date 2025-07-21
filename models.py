# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    location = Column(String)
    preferred_language = Column(String, default="en")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pregnancies = relationship("Pregnancy", back_populates="user", cascade="all, delete-orphan")
    children = relationship("Child", back_populates="user", cascade="all, delete-orphan")
    health_records = relationship("HealthRecord", back_populates="user", cascade="all, delete-orphan")

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