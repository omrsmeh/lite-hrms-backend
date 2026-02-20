"""
Admin routes — verify admin credentials (no JWT, session-free)
"""
import hashlib
from fastapi import APIRouter, HTTPException, status
from database import admins_collection
from models.admin import AdminLogin, AdminResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, hashed = stored.split(":")
        return hashlib.sha256(f"{salt}{password}".encode()).hexdigest() == hashed
    except Exception:
        return False


@router.post("/login", response_model=AdminResponse)
async def admin_login(credentials: AdminLogin):
    """
    Verify admin credentials.
    Returns admin info on success, 401 on failure.
    """
    admin = await admins_collection.find_one({"username": credentials.username})
    if not admin or not verify_password(credentials.password, admin["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )
    return AdminResponse(
        username=admin["username"],
        full_name=admin["full_name"],
        role=admin.get("role", "admin"),
    )


@router.get("/info", response_model=AdminResponse)
async def get_admin_info(username: str):
    """
    Get admin info by username (for display purposes).
    """
    admin = await admins_collection.find_one({"username": username})
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin '{username}' not found.",
        )
    return AdminResponse(
        username=admin["username"],
        full_name=admin["full_name"],
        role=admin.get("role", "admin"),
    )
