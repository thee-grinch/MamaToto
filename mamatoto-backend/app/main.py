# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date, timedelta

from .config import settings
from .database import engine, Base, get_db
from .core.deps import get_current_user
from .models.user import User
from .schemas.health import DashboardResponse

# Import API routers
from .api.auth import router as auth_router
from .api.pregnancy import router as pregnancy_router
from .api.child import router as child_router

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(pregnancy_router)
app.include_router(child_router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Mamatoto API",
        "version": settings.api_version,
        "description": "Maternal and Child Health Platform"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": date.today().isoformat()}

@app.get("/dashboard", response_model=DashboardResponse)
def get_dashboard_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard data for the user"""
    from .models.pregnancy import Pregnancy, Appointment
    from .models.child import Child, Vaccination
    from .models.health import HealthRecord
    
    # Get active pregnancy
    active_pregnancy = db.query(Pregnancy).filter(
        Pregnancy.user_id == current_user.id,
        Pregnancy.is_active == True
    ).first()
    
    # Add calculated fields to pregnancy
    if active_pregnancy:
        days_remaining = (active_pregnancy.due_date - date.today()).days
        active_pregnancy.weeks_remaining = max(0, days_remaining // 7)
        active_pregnancy.trimester = min(3, max(1, (active_pregnancy.current_week or 0) // 13 + 1))
    
    # Get children
    children = db.query(Child).filter(
        Child.user_id == current_user.id,
        Child.is_active == True
    ).all()
    
    # Add age to children
    for child in children:
        age_days = (date.today() - child.birth_date).days
        child.age_months = age_days // 30
    
    # Get upcoming appointments
    upcoming_appointments = db.query(Appointment).filter(
        Appointment.user_id == current_user.id,
        Appointment.scheduled_date >= date.today(),
        Appointment.completed == False
    ).order_by(Appointment.scheduled_date).limit(5).all()
    
    # Get overdue vaccinations
    overdue_vaccinations = []
    for child in children:
        overdue_date = date.today() - timedelta(days=30)
        child_overdue = db.query(Vaccination).filter(
            Vaccination.child_id == child.id,
            Vaccination.status.in_(["pending", "overdue"]),
            Vaccination.scheduled_date < overdue_date
        ).all()
        
        # Update status to overdue
        for vaccination in child_overdue:
            vaccination.status = "overdue"
        
        overdue_vaccinations.extend(child_overdue)
    
    if overdue_vaccinations:
        db.commit()
    
    # Get recent health records
    recent_health_records = db.query(HealthRecord).filter(
        HealthRecord.user_id == current_user.id
    ).order_by(HealthRecord.created_at.desc()).limit(5).all()
    
    # Generate growth alerts
    growth_alerts = []
    for child in children:
        from .models.child import GrowthRecord
        latest_growth = db.query(GrowthRecord).filter(
            GrowthRecord.child_id == child.id
        ).order_by(GrowthRecord.recorded_date.desc()).first()
        
        if latest_growth:
            from .utils.growth import get_growth_alerts
            alerts = get_growth_alerts(
                child.age_months,
                latest_growth.weight_percentile,
                latest_growth.height_percentile
            )
            growth_alerts.extend(alerts)
    
    return DashboardResponse(
        user=current_user,
        active_pregnancy=active_pregnancy,
        children=children,
        upcoming_appointments=upcoming_appointments,
        overdue_vaccinations=overdue_vaccinations,
        recent_health_records=recent_health_records,
        growth_alerts=growth_alerts
    )

@app.post("/pregnancy/weekly-info")
def get_pregnancy_weekly_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weekly pregnancy information for active pregnancy"""
    from .models.pregnancy import Pregnancy
    from .utils.pregnancy import get_weekly_info, calculate_pregnancy_week
    
    pregnancy = db.query(Pregnancy).filter(
        Pregnancy.user_id == current_user.id,
        Pregnancy.is_active == True
    ).first()
    
    if not pregnancy:
        raise HTTPException(status_code=404, detail="No active pregnancy found")
    
    current_week = calculate_pregnancy_week(pregnancy.due_date)
    weekly_info = get_weekly_info(current_week)
    
    return weekly_info

@app.get("/pregnancy/danger-signs")
def get_pregnancy_danger_signs():
    """Get list of pregnancy danger signs"""
    from .utils.pregnancy import get_danger_signs
    return {"danger_signs": get_danger_signs()}

@app.post("/chatbot")
async def chatbot_query(
    query: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    AI Chatbot endpoint for health queries
    Note: This is a placeholder - integrate with OpenAI API in production
    """
    
    # Get user context
    from .models.pregnancy import Pregnancy
    from .models.child import Child
    
    active_pregnancy = db.query(Pregnancy).filter(
        Pregnancy.user_id == current_user.id,
        Pregnancy.is_active == True
    ).first()
    
    children = db.query(Child).filter(
        Child.user_id == current_user.id,
        Child.is_active == True
    ).all()
    
    # Build context for AI
    context = {
        "has_active_pregnancy": bool(active_pregnancy),
        "pregnancy_week": active_pregnancy.current_week if active_pregnancy else None,
        "children_ages": [
            (date.today() - child.birth_date).days // 30 
            for child in children
        ]
    }
    
    # Placeholder response - replace with actual AI integration
    if "vaccination" in query.lower():
        response = "Vaccinations are crucial for your child's health. Please ensure all scheduled vaccines are up to date. Check your child's vaccination tracker for due dates."
    elif "pregnancy" in query.lower() and context["has_active_pregnancy"]:
        week = context["pregnancy_week"] or "unknown"
        response = f"You're in week {week} of pregnancy. Make sure to attend regular check-ups, take prenatal vitamins, and contact your healthcare provider if you notice any concerning symptoms."
    elif "growth" in query.lower():
        response = "Monitor your child's growth regularly by recording height and weight. Any concerns about growth patterns should be discussed with your pediatrician."
    else:
        response = "I'm here to help with maternal and child health questions. Please ask about pregnancy care, child development, vaccinations, or nutrition."
    
    return {
        "query": query,
        "response": response,
        "context": context,
        "disclaimer": "This is for informational purposes only. Always consult healthcare providers for medical advice."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

