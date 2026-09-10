from fastapi import APIRouter, Depends

from app.auth import get_current_user

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import User, WidgetPreference
from app.schemas import WidgetPreferenceCreate

router = APIRouter(prefix="/dashboard")


@router.get("/")
def get_dashboard(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome to the dashboard, {current_user.username}!"}

@router.post("/preferences")
def create_widget(widget: WidgetPreferenceCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_widget = WidgetPreference(
        user_id=current_user.id,
        widget_name=widget.widget_name,
        config=widget.config
    )
    db.add(new_widget)
    db.commit()
    db.refresh(new_widget)
    return {
        "id": new_widget.id,
        "widget_name": new_widget.widget_name,
        "config": new_widget.config
    }

@router.get("/preferences")
def get_widget_preferences(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    statement = select(WidgetPreference).where(WidgetPreference.user_id == current_user.id)
    results = db.execute(statement)
    preferences = results.scalars().all()
    return preferences
