from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db

from sqlalchemy import select
from app.models import User

from app.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email
    )

    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    statement = select(User)
    results = db.execute(statement)
    users = results.scalars().all()

    return users