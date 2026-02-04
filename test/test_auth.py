from utils import *
from app.routers.auth import create_access_token, get_current_user,get_db,authenticate_user, SECRET_KEY,ALGORITHM
from jose import jwt
from datetime import datetime, timedelta

app.dependency_overrides[get_db] = override_get_db


def test_authentication_user(test_todo):
    db = TestingSessionLocal()

    user = authenticate_user(
        db,
        test_todo[1].username,
        "testpassword"
    )

    assert user is not None
    assert user.username == test_todo[1].username

    non_user = authenticate_user(
        db, "nonexistentuser", "wrongpassword"
    )
    assert non_user is False
    
    wrong_password_user = authenticate_user(
        db, test_todo[1].username, "wrongpassword"
    )
    assert wrong_password_user is False
    
def test_create_access_token():
    username = "testuser"
    user_id = 1
    role = "user"
    expire_delta = timedelta(minutes=15)

    token = create_access_token(username, user_id, role, expire_delta)
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_payload["sub"] == username
    assert decoded_payload["id"] == user_id
    assert decoded_payload["role"] == role

@pytest.mark.asyncio #using pytest-asyncio to test async function
async def test_get_current_user(test_todo):
    username = test_todo[1].username
    user_id = test_todo[1].id
    role = test_todo[1].role
    expire_delta = timedelta(minutes=15)

    token = create_access_token(username, user_id, role, expire_delta)

    current_user = await get_current_user(token)

    assert current_user["username"] == username
    assert current_user["id"] == user_id
    assert current_user["user_role"] == role