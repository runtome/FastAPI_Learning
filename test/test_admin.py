from utils import *
from app.routers.admin import get_db, get_current_user
from fastapi import status

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