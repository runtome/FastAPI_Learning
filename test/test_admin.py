from utils import *
from app.routers.admin import get_db, get_current_user
from fastapi import status
from app.models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_admin_authenticated():
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) >= 1  # At least one todo from the fixture
    assert data[0]["title"] == "Test Todo"
    assert data[0]["description"] == "This is a test todo"
    assert data[0]["priority"] == 1
    assert data[0]["complete"] is False
    assert data[0]["owner_id"] == 1
    
def test_read_all_admin_unauthenticated():
    # Override to simulate non-admin user
    def override_get_current_user_non_admin():
        return {"username": 'test', "id": 1, "user_role": "user"} # non-admin role
      
    app.dependency_overrides[get_current_user] = override_get_current_user_non_admin
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    app.dependency_overrides[get_current_user] = override_get_current_user
    

def test_admin_delete_todo():
    # First, create a todo to delete
    db = TestingSessionLocal()
    todo = Todos(
        title="Todo to Delete",
        description="This todo will be deleted by admin",
        priority=2,
        complete=False,
        owner_id=1
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    todo_id = todo.id
    db.close()

    # Now, delete the todo as admin
    response = client.delete(f"/admin/todo/{todo_id}")
    assert response.status_code == status.HTTP_200_OK

    # Verify the todo is deleted
    db = TestingSessionLocal()
    deleted_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    assert deleted_todo is None
    db.close()
    
def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/9999")  # Assuming 9999 does not exist
    assert response.status_code == status.HTTP_404_NOT_FOUND