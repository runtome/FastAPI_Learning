# test/test_todos.py
from sqlalchemy import create_engine
from fastapi import status
from app.models import Todos

from app.routers.auth import get_current_user
from app.routers.todos import get_db

from app.main import app
from utils import *
   
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated():
    response = client.get("/todos")
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
    response = client.post("/todos/todo/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    todo_in_db = db.query(Todos).filter(Todos.title == "New Todo").first()
    assert todo_in_db is not None
    assert todo_in_db.title == request_data["title"]
    assert todo_in_db.description == request_data["description"]
    assert todo_in_db.priority == request_data["priority"]
    assert todo_in_db.complete == request_data["complete"]
    db.close()


def test_update_todo(test_todo):
    todo_id = test_todo[0].id
    update_data = {
        "title": "Updated Todo",
        "description": "This todo has been updated",
        "priority": 3,
        "complete": True
    }
    response = client.put(f"/todos/todo/{todo_id}/", json=update_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    updated_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    assert updated_todo.title == update_data["title"]
    assert updated_todo.description == update_data["description"]
    assert updated_todo.priority == update_data["priority"]
    assert updated_todo.complete == update_data["complete"]
    db.close()
 
 
def test_update_todo_not_found(test_todo):
    todo_id = 999  # Non-existent todo ID
    update_data = {
        "title": "Updated Todo",
        "description": "This todo has been updated",
        "priority": 3,
        "complete": True
    }
    response = client.put(f"/todos/todo/{todo_id}/", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_todo(test_todo):
    todo_id = test_todo[0].id
    response = client.delete(f"/todos/todo/{todo_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    deleted_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    assert deleted_todo is None
    db.close()
    
def test_delete_todo_not_found():
    todo_id = 999  # Non-existent todo ID
    response = client.delete(f"/todos/todo/{todo_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Todo not found"
