from fastapi import FastAPI, Depends
from database import SessionLocal, engine
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todo
import models


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todo).all()

