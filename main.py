from pathlib import Path
from fastapi import FastAPI, Depends, Path
from starlette import status
from database import SessionLocal, engine
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
import models
from fastapi.exceptions import HTTPException as HttpException
from pydantic import BaseModel, Field


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str
    priority: int =Field(gt=0, lt=6)
    complete: bool


@app.get("/",status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int=Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HttpException(status_code=404, detail="Todo not found")


@app.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest, db: db_dependency):
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()
    return {
        "status": "success",
        "message": "Todo created successfully"
    }