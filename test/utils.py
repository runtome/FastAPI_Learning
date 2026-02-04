#test/utils.py
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.models import Todos, Users
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from app.models import Users, Todos
from app.routers.auth import bcrypt_context



SQLALCHEMY_DATABASE_URL = "postgresql://test:test@localhost/test_db"

engine = create_engine(
  SQLALCHEMY_DATABASE_URL,
  poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()
    
def override_get_current_user():
    return {"username": 'test', "id": 1, "user_role": "admin"}


client = TestClient(app)


@pytest.fixture(autouse=True)
def test_todo():
    db = TestingSessionLocal()

    # 1. สร้าง user ก่อน
    user = Users(
        id=1,
        username="test",
        email="test@test.com",
        hashed_password=bcrypt_context.hash("testpassword"),
        is_active=True,
        role="admin",
        phone='111111111'
    )
    db.add(user)
    db.commit()

    # 2. สร้าง todo ที่อ้างถึง user
    todo = Todos(
        title="Test Todo",
        description="This is a test todo",
        priority=1,
        complete=False,
        owner_id=1
    )
    db.add(todo)
    db.commit()

    yield todo , user

    # cleanup
    db.query(Todos).delete()
    db.query(Users).delete()
    db.commit()
    db.close()
