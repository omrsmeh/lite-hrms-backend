from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.employees import router as employees_router
from routes.attendance import router as attendance_router
from routes.admin import router as admin_router
from routes.dashboard import router as dashboard_router

app = FastAPI(
    title="HRMS Lite API",
    description="Human Resource Management System - Lite Edition",
    version="1.0.0",
)

# CORS — allow all origins for development; restrict to frontend URL in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)
app.include_router(employees_router)
app.include_router(attendance_router)
app.include_router(dashboard_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "HRMS Lite API is running"}


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to HRMS Lite API. Visit /docs for Swagger UI."}
