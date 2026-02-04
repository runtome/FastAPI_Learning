from utils import *
from app.routers.auth import get_current_user,get_db,authenticate_user

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