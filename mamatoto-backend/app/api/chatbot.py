
# app/api/chatbot.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ..core.deps import get_db, get_current_user
from ..models.user import User
from ..models.pregnancy import Pregnancy
from ..models.child import Child
from ..config import settings
import openai
import json

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

# Configure OpenAI (if API key is provided)
if settings.openai_api_key:
    openai.api_key = settings.openai_api_key

@router.post("/query")
async def chatbot_query(
    query: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    AI Chatbot endpoint for health queries
    """
    
    # Get user context
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
        "user_name": current_user.first_name or "there",
        "has_active_pregnancy": bool(active_pregnancy),
        "pregnancy_week": active_pregnancy.current_week if active_pregnancy else None,
        "children_count": len(children),
        "children_ages": [
            f"{child.name} ({calculate_age_months(child.birth_date)} months)"
            for child in children
        ]
    }
    
    # Generate response
    if settings.openai_api_key:
        response = await generate_ai_response(query, context)
    else:
        response = generate_fallback_response(query, context)
    
    return {
        "query": query,
        "response": response,
        "context": context,
        "disclaimer": "This information is for educational purposes only. Always consult healthcare providers for medical advice."
    }

async def generate_ai_response(query: str, context: dict) -> str:
    """Generate AI response using OpenAI API"""
    try:
        # Build system message with context
        system_message = f"""You are a helpful maternal and child health assistant. 
        
        User context:
        - User has {'an active pregnancy' if context['has_active_pregnancy'] else 'no active pregnancy'}
        {f"- Currently at week {context['pregnancy_week']} of pregnancy" if context['pregnancy_week'] else ""}
        - Has {context['children_count']} children: {', '.join(context['children_ages']) if context['children_ages'] else 'none'}
        
        Provide helpful, accurate health information while always recommending professional medical consultation for serious concerns.
        Be supportive and culturally sensitive. Keep responses concise but informative.
        """
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": query}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return generate_fallback_response(query, context)

def generate_fallback_response(query: str, context: dict) -> str:
    """Generate fallback response when AI is not available"""
    query_lower = query.lower()
    user_name = context.get("user_name", "")
    
    # Pregnancy-related queries
    if any(word in query_lower for word in ["pregnancy", "pregnant", "baby", "trimester"]):
        if context["has_active_pregnancy"]:
            week = context.get("pregnancy_week", "unknown")
            return f"Hi {user_name}! You're currently at week {week} of pregnancy. For pregnancy-related questions, I recommend discussing with your healthcare provider during your regular check-ups. Make sure to take your prenatal vitamins, stay hydrated, and attend all scheduled appointments."
        else:
            return f"Hi {user_name}! For pregnancy-related questions, it's always best to consult with a qualified healthcare provider who can give you personalized advice based on your specific situation."
    
    # Vaccination queries
    elif any(word in query_lower for word in ["vaccination", "vaccine", "immunization"]):
        return f"Hi {user_name}! Vaccinations are crucial for protecting your children's health. Please ensure all scheduled vaccines are up to date according to the Kenya immunization schedule. Check your vaccination tracker for due dates and consult your pediatrician if you have concerns."
    
    # Growth and development
    elif any(word in query_lower for word in ["growth", "development", "milestone", "weight", "height"]):
        return f"Hi {user_name}! Monitoring your child's growth and development is important. Regular check-ups with your pediatrician, tracking milestones, and maintaining a healthy diet all contribute to proper development. If you have specific concerns about your child's growth, please consult your healthcare provider."
    
    # Nutrition queries
    elif any(word in query_lower for word in ["nutrition", "food", "eating", "diet", "breastfeeding"]):
        return f"Hi {user_name}! Good nutrition is essential for both mothers and children. For pregnant mothers, focus on a balanced diet with prenatal vitamins. For children, age-appropriate nutrition supports healthy growth. Consult your healthcare provider for personalized dietary advice."
    
    # General health
    elif any(word in query_lower for word in ["fever", "cough", "sick", "illness", "symptoms"]):
        return f"Hi {user_name}! For any health concerns or symptoms, especially in children, it's important to consult with a healthcare provider promptly. They can properly assess symptoms and provide appropriate treatment. Keep track of symptoms and don't hesitate to seek medical attention when needed."
    
    # Mental health
    elif any(word in query_lower for word in ["stress", "anxiety", "depression", "mood", "mental"]):
        return f"Hi {user_name}! Mental health is just as important as physical health, especially during pregnancy and early parenthood. If you're experiencing persistent stress, anxiety, or mood changes, please reach out to a healthcare provider or mental health professional. Support is available and seeking help is a sign of strength."
    
    # Default response
    else:
        return f"Hi {user_name}! I'm here to help with maternal and child health questions. You can ask me about pregnancy care, child development, vaccinations, nutrition, or general health concerns. For specific medical advice, always consult with qualified healthcare providers."

def calculate_age_months(birth_date) -> int:
    """Calculate age in months from birth date"""
    from datetime import date
    today = date.today()
    age_days = (today - birth_date).days
    return age_days // 30