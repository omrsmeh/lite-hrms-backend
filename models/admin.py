from pydantic import BaseModel, field_validator
from typing import Optional


class AdminCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = "Admin"

    @field_validator("username", "password")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

    @field_validator("password")
    @classmethod
    def min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class AdminResponse(BaseModel):
    username: str
    full_name: str
    role: str = "admin"

    model_config = {"from_attributes": True}


class AdminLogin(BaseModel):
    username: str
    password: str
