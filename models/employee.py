from pydantic import BaseModel, EmailStr, field_validator



class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str
    shift_start_time: str = "09:00"
    shift_end_time: str = "18:00"

    @field_validator("employee_id", "full_name", "department")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace")
        return v.strip()

    @field_validator("full_name", "department")
    @classmethod
    def min_length(cls, v: str) -> str:
        if len(v) < 2:
            raise ValueError("Field must be at least 2 characters")
        return v


class EmployeeResponse(BaseModel):
    id: str
    employee_id: str
    full_name: str
    email: str
    department: str
    shift_start_time: str
    shift_end_time: str

    model_config = {"from_attributes": True}
