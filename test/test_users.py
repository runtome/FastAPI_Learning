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
    
def test_change_password(test_todo):
    response = client.put(
        "/users/password",
        json={
            "password": "testpassword",
            "new_password": "newtestpassword"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    
    # ตรวจสอบว่า รหัสผ่านถูกเปลี่ยนจริง
    response = client.get("/users")
    assert bcrypt_context.verify("newtestpassword",response.json()['hashed_password'])

def test_change_password_incorrect_current(test_todo):
    response = client.put(
        "/users/password",
        json={
            "password": "wrongpassword",
            "new_password": "newtestpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == "Incorrect password"
    
def test_update_phone_number(test_todo):
    new_phone_number = "222222222"
    response = client.put(f"/users/phone/{new_phone_number}")
    assert response.status_code == status.HTTP_200_OK
    
    # ตรวจสอบว่า เบอร์โทรศัพท์ถูกเปลี่ยนจริง
    response = client.get("/users")
    assert response.json()['phone'] == new_phone_number