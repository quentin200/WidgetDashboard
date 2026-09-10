from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import User
from app.schemas import UserLogin
from app.auth import password_hash, create_access_token, get_current_user


router = APIRouter(prefix="/auth")

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    statement = select(User).where(User.email == credentials.email)
    result = db.execute(statement)
    user = result.scalar_one_or_none()

    if user is None or not password_hash.verify(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }