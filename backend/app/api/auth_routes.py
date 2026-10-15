from fastapi import APIRouter, Query
from app.core.security import DEMO_USERS, get_current_user, User
from app.schemas.schemas import UserResponse, SwitchRoleRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/me", response_model=UserResponse)
def get_user_profile(role: str = Query(default="ADMIN")):
    user = get_current_user(role)
    return user

@router.get("/roles")
def list_available_roles():
    return [
        {"role": u.role.value, "username": u.username, "full_name": u.full_name, "department": u.department}
        for u in DEMO_USERS
    ]
