from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from app.models import Todos

from app.routers.auth import get_current_user
from app.routers.todos import get_db

from app.main import app
from app.database import Base, SessionLocal
from sqlalchemy.orm import sessionmaker

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
        
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

from app.models import Todos, Users

@pytest.fixture(autouse=True)
def test_todo():
    db = TestingSessionLocal()

    # 1. สร้าง user ก่อน
    user = Users(
        id=1,
        username="test",
        email="test@test.com",
        hashed_password="fakehashedpassword",
        is_active=True,
        role="admin"
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

    yield todo

    # cleanup
    db.query(Todos).delete()
    db.query(Users).delete()
    db.commit()
    db.close()

def test_read_all_authenticated():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 1

    todo = data[0]
    assert todo["title"] == "Test Todo"
    assert todo["description"] == "This is a test todo"
    assert todo["priority"] == 1
    assert todo["complete"] is False
    assert todo["owner_id"] == 1


def test_create_todo():
    
    request_data = {
        "title": "New Todo",
        "description": "This is a new todo",
        "priority": 2,
        "complete": False
    }
    response = client.post("/todo/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    todo_in_db = db.query(Todos).filter(Todos.title == "New Todo").first()
    assert todo_in_db is not None
    assert todo_in_db.title == request_data["title"]
    assert todo_in_db.description == request_data["description"]
    assert todo_in_db.priority == request_data["priority"]
    assert todo_in_db.complete == request_data["complete"]
    db.close()

 