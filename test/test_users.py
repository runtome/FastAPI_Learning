from utils import*
from app.routers.users import get_current_user, get_db
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_users(test_todo):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'test'
    assert response.json()['email'] == 'test@test.com'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone'] == '111111111'
    assert bcrypt_context.verify("testpassword",response.json()['hashed_password'])