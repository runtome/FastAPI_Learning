from fastapi import APIRouter
from starlette import status


router = APIRouter()

@router.get("/auth/", status_code=status.HTTP_200_OK)
async def get_user():
    return {"user": "authenticated_user"}