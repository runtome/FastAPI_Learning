from pathlib import Path
from fastapi import APIRouter, Depends, Path
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos, Users
from fastapi.exceptions import HTTPException as HttpException
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["users"],
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerifyRequest(BaseModel):
    password: str
    new_password: str
    

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_details(
    user: user_dependency,
    db: db_dependency
):
  if user is None:
      raise HttpException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
  
  user = db.query(Users).filter(Users.id == user["id"]).first()
  if not user:
      raise HttpException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  return user
  
@router.put("/password", status_code=status.HTTP_200_OK)
async def update_user_password(
    user: user_dependency,
    user_verify: UserVerifyRequest,
    db: db_dependency
):
  if user is None:
      raise HttpException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
  
  user = db.query(Users).filter(Users.id == user["id"]).first()
  if not user:
      raise HttpException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  
  if not bcrypt_context.verify(user_verify.password, user.hashed_password):
      raise HttpException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
  
  new_hashed_password = bcrypt_context.hash(user_verify.new_password)
  user.hashed_password = new_hashed_password
  db.commit()

@router.put("/phone/{phone_number}", status_code=status.HTTP_200_OK)
async def update_user_phone(
    db: db_dependency,
    user: user_dependency,
    phone_number: str,
):
    if user is None:
        raise HttpException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    user = db.query(Users).filter(Users.id == user["id"]).first()
    if not user:
        raise HttpException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.phone = phone_number
    db.add(user)
    db.commit()

    return {"message": "Phone number updated successfully"}