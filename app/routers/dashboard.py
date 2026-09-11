from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import User, WidgetPreference
from app.schemas import WidgetPreferenceCreate, WidgetPreferenceUpdate

from app.routers.widgets.weather import fetch_weather
from app.routers.widgets.github import fetch_github
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
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Widget preference already exists")
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

@router.get("/weather")
def get_dashboard_weather(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    statement = select(WidgetPreference).where(WidgetPreference.user_id == current_user.id, WidgetPreference.widget_name == "weather")
    result = db.execute(statement)
    preference = result.scalar_one_or_none()
    
    if preference is None:
        raise HTTPException(status_code=404, detail="Weather widget preference not found")
    
    city = preference.config.get("city")
    
    if not city:
        raise HTTPException(status_code=400, detail="City not set in weather widget preference")
    
    return fetch_weather(city)

@router.get("/github")
def get_dashboard_github(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    statement = select(WidgetPreference).where(
        WidgetPreference.user_id == current_user.id,
        WidgetPreference.widget_name == "github"
    )

    result = db.execute(statement)
    preference = result.scalar_one_or_none()

    if preference is None:
        raise HTTPException(
            status_code=404,
            detail="GitHub widget preference not found"
        )
    username = preference.config.get("username")
    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username not set in GitHub widget preference"
        )
    return fetch_github(username)

@router.put("/preferences/{widget_name}")
def update_widget(
    widget_name: str,
    widget: WidgetPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    statement = select(WidgetPreference).where(WidgetPreference.user_id == current_user.id, WidgetPreference.widget_name == widget_name)
    result = db.execute(statement)
    preference = result.scalar_one_or_none()

    if preference is None:
        raise HTTPException(status_code=404, detail="Widget preference not found")
    
    preference.config = widget.config

    db.commit()
    db.refresh(preference)

    return preference
