from fastapi import APIRouter
from database import employees_collection, attendance_collection
from datetime import date as dt_date

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
async def get_dashboard_summary(date: str = None):
    # Default to today if no date provided
    if not date:
        date = str(dt_date.today())

    # Total employees
    total_employees = await employees_collection.count_documents({})
    
    # Get all attendance records for the date
    attendance_records = []
    async for record in attendance_collection.find({"date": date}):
        attendance_records.append(record)
        
    total_present = 0
    total_absent = 0
    total_late = 0
    total_early_exit = 0
    total_incomplete = 0
    
    for rec in attendance_records:
        status = rec.get("status", "")
        if "Present" in status:
            total_present += 1
        elif "Absent" in status:
            total_absent += 1
        elif "Late" in status:
            total_late += 1
        elif "Early Exit" in status:
            total_early_exit += 1
        elif "Incomplete" in status:
            total_incomplete += 1
            
    # Calculate un-marked employees (assumed absent implicitly for the dashboard, or just 'unmarked')
    marked_employees_count = len(attendance_records)
    unmarked_employees = max(0, total_employees - marked_employees_count)

    return {
        "date": date,
        "total_employees": total_employees,
        "attendance": {
            "present": total_present,
            "late": total_late,
            "early_exit": total_early_exit,
            "incomplete": total_incomplete,
            "absent": total_absent,
            "unmarked": unmarked_employees
        }
    }
