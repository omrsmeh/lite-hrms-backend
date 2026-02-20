from fastapi import APIRouter, HTTPException, status
from database import employees_collection, attendance_collection
from models.employee import EmployeeCreate, EmployeeResponse

router = APIRouter(prefix="/employees", tags=["Employees"])


def serialize_employee(emp: dict) -> dict:
    return {
        "id": str(emp["_id"]),
        "employee_id": emp["employee_id"],
        "full_name": emp["full_name"],
        "email": emp["email"],
        "department": emp["department"],
        "shift_start_time": emp.get("shift_start_time", "09:00"),
        "shift_end_time": emp.get("shift_end_time", "18:00"),
    }


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def add_employee(employee: EmployeeCreate):
    # Check duplicate employee_id
    existing = await employees_collection.find_one({"employee_id": employee.employee_id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Employee with ID '{employee.employee_id}' already exists.",
        )

    # Check duplicate email
    email_existing = await employees_collection.find_one({"email": employee.email})
    if email_existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Employee with email '{employee.email}' already exists.",
        )

    result = await employees_collection.insert_one(employee.model_dump())
    created = await employees_collection.find_one({"_id": result.inserted_id})
    return EmployeeResponse(**serialize_employee(created))


@router.get("", response_model=list[EmployeeResponse])
async def list_employees():
    employees = []
    async for emp in employees_collection.find():
        employees.append(EmployeeResponse(**serialize_employee(emp)))
    return employees


@router.delete("/{employee_id}", status_code=status.HTTP_200_OK)
async def delete_employee(employee_id: str):
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{employee_id}' not found.",
        )

    # Also delete all attendance records for this employee
    await attendance_collection.delete_many({"employee_id": employee_id})
    await employees_collection.delete_one({"employee_id": employee_id})

    return {"message": f"Employee '{employee_id}' and their attendance records deleted successfully."}
