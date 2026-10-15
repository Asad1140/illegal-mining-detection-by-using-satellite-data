from enum import Enum
from typing import Optional, List
from pydantic import BaseModel

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    FIELD_OFFICER = "FIELD_OFFICER"
    VIEWER = "VIEWER"

class User(BaseModel):
    id: str
    username: str
    full_name: str
    email: str
    role: UserRole
    department: str
    is_active: bool = True

# In-memory mock demo users
DEMO_USERS: List[User] = [
    User(
        id="usr-admin-01",
        username="admin",
        full_name="Rajesh Verma (Dir. Mining Surveillance)",
        email="rajesh.verma@mines.gov.in",
        role=UserRole.ADMIN,
        department="Directorate of Mines & Geology"
    ),
    User(
        id="usr-analyst-01",
        username="analyst",
        full_name="Priya Sharma (Senior GIS Analyst)",
        email="priya.sharma@mines.gov.in",
        role=UserRole.ANALYST,
        department="Satellite Remote Sensing Cell"
    ),
    User(
        id="usr-officer-01",
        username="officer",
        full_name="Anil Kumar Patnaik (District Mining Officer)",
        email="anil.patnaik@mines.gov.in",
        role=UserRole.FIELD_OFFICER,
        department="Keonjhar District Mining Enforcement"
    ),
    User(
        id="usr-viewer-01",
        username="viewer",
        full_name="Dr. Sunita Das (Environmental Auditor)",
        email="sunita.das@env.gov.in",
        role=UserRole.VIEWER,
        department="State Pollution Control Board"
    )
]

def get_current_user(role: Optional[str] = None) -> User:
    """Returns the matching active user context or defaults to ADMIN."""
    if role:
        for u in DEMO_USERS:
            if u.role.value == role or u.username == role:
                return u
    return DEMO_USERS[0]
