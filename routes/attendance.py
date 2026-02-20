from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from database import employees_collection, attendance_collection
from models.attendance import AttendanceResponse
from datetime import datetime, date, timedelta

router = APIRouter(prefix="/attendance", tags=["Attendance"])


def serialize_attendance(record: dict) -> dict:
    return {
        "id": str(record["_id"]),
        "employee_id": record["employee_id"],
        "date": str(record["date"]),
        "in_time": record.get("in_time"),
        "out_time": record.get("out_time"),
        "status": record["status"],
    }


def parse_time(time_str: str) -> datetime.time:
    """Helper to parse HH:MM string to time object for comparison"""
    return datetime.strptime(time_str, "%H:%M").time()


def add_minutes(time_obj: datetime.time, minutes: int) -> datetime.time:
    """Add minutes to a time object"""
    dt = datetime.combine(date.today(), time_obj)
    new_dt = dt + timedelta(minutes=minutes)
    return new_dt.time()


@router.post("/mark-in", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def mark_in(data: dict):
    # data expects: {"employee_id": "EMP01", "date": "2026-02-20", "in_time": "09:10"}
    employee_id = data.get("employee_id")
    att_date = data.get("date")
    in_time = data.get("in_time")

    if not all([employee_id, att_date, in_time]):
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Validate employee
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")

    # Check if already marked
    existing = await attendance_collection.find_one({
        "employee_id": employee_id,
        "date": att_date,
    })
    if existing:
        raise HTTPException(status_code=409, detail="Attendance already has a record for this date.")

    shift_start_str = employee.get("shift_start_time", "09:00")
    
    # Calculate status based on 15 min delay rule
    in_time_obj = parse_time(in_time)
    shift_start_obj = parse_time(shift_start_str)
    
    # 15 min grace period
    grace_period_end = add_minutes(shift_start_obj, 15)
    
    # Initial status is incomplete because they haven't exited yet
    # Or Late if they came in late
    att_status = "Incomplete"
    if in_time_obj > grace_period_end:
        att_status = "Late"

    new_record = {
        "employee_id": employee_id,
        "date": att_date,
        "in_time": in_time,
        "out_time": None,
        "status": att_status
    }

    result = await attendance_collection.insert_one(new_record)
    created = await attendance_collection.find_one({"_id": result.inserted_id})
    return AttendanceResponse(**serialize_attendance(created))


@router.post("/mark-out", response_model=AttendanceResponse)
async def mark_out(data: dict):
    # data expects: {"employee_id": "EMP01", "date": "2026-02-20", "out_time": "17:05"}
    employee_id = data.get("employee_id")
    att_date = data.get("date")
    out_time = data.get("out_time")

    if not all([employee_id, att_date, out_time]):
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Find existing attendance to update
    record = await attendance_collection.find_one({
        "employee_id": employee_id,
        "date": att_date,
    })
    
    if not record:
        raise HTTPException(status_code=404, detail="No IN record found for this date. Cannot mark OUT.")
        
    if record.get("out_time"):
        raise HTTPException(status_code=409, detail="Already marked OUT for this date.")

    # Validate employee to get shift end time
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")

    shift_end_str = employee.get("shift_end_time", "18:00")
    
    # Calculate final status
    out_time_obj = parse_time(out_time)
    shift_end_obj = parse_time(shift_end_str)
    
    current_status = record.get("status")
    final_status = current_status
    
    # If early exit
    if out_time_obj < shift_end_obj:
        if current_status == "Late":
            final_status = "Late & Early Exit" # Or just Early Exit depending on preference
        else:
            final_status = "Early Exit"
    else:
        # If they left on time or after shift
        if current_status == "Incomplete":
            final_status = "Present"
        # If they were late but left on time, they stay "Late"
        
    await attendance_collection.update_one(
        {"_id": record["_id"]},
        {"$set": {"out_time": out_time, "status": final_status}}
    )

    updated = await attendance_collection.find_one({"_id": record["_id"]})
    return AttendanceResponse(**serialize_attendance(updated))


@router.post("/mark-absent", response_model=AttendanceResponse)
async def mark_absent(data: dict):
    employee_id = data.get("employee_id")
    att_date = data.get("date")

    if not all([employee_id, att_date]):
        raise HTTPException(status_code=400, detail="Missing required fields")

    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")

    existing = await attendance_collection.find_one({"employee_id": employee_id, "date": att_date})
    if existing:
         raise HTTPException(status_code=409, detail="Attendance already has a record for this date.")
         
    new_record = {
        "employee_id": employee_id,
        "date": att_date,
        "in_time": None,
        "out_time": None,
        "status": "Absent"
    }

    result = await attendance_collection.insert_one(new_record)
    created = await attendance_collection.find_one({"_id": result.inserted_id})
    return AttendanceResponse(**serialize_attendance(created))


@router.get("", response_model=list[AttendanceResponse])
async def get_all_attendance(date: Optional[str] = Query(None, description="Filter by date (YYYY-MM-DD)")):
    query = {}
    if date:
        query["date"] = date
    records = []
    async for record in attendance_collection.find(query).sort("date", -1):
        records.append(AttendanceResponse(**serialize_attendance(record)))
    return records


@router.get("/{employee_id}", response_model=list[AttendanceResponse])
async def get_attendance_by_employee(
    employee_id: str,
    date: Optional[str] = Query(None, description="Filter by date (YYYY-MM-DD)")
):
    query = {"employee_id": employee_id}
    if date:
        query["date"] = date
    records = []
    async for record in attendance_collection.find(query).sort("date", -1):
        records.append(AttendanceResponse(**serialize_attendance(record)))
    return records
