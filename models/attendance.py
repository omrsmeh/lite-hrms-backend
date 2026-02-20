from pydantic import BaseModel, field_validator
from typing import Literal, Optional
from datetime import date


class AttendanceCreate(BaseModel):
    employee_id: str
    date: date
    in_time: Optional[str] = None
    out_time: Optional[str] = None
    status: Literal["Present", "Absent", "Late", "Early Exit", "Incomplete"]

    @field_validator("employee_id")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("employee_id cannot be empty")
        return v.strip()

class AttendanceUpdate(BaseModel):
    out_time: str

class AttendanceResponse(BaseModel):
    id: str
    employee_id: str
    date: str
    in_time: Optional[str] = None
    out_time: Optional[str] = None
    status: str

    model_config = {"from_attributes": True}



