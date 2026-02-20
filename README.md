# HRMS Lite — Human Resource Management System

> A lightweight, production-ready HR tool for managing employees and tracking daily attendance.  
> Built with **React + Vite** (Frontend) and **FastAPI + MongoDB** (Backend).

---

## 📁 Project Structure

```
lite-hrms-backend/        # FastAPI backend
├── main.py
├── database.py
├── models/
│   ├── employee.py
│   └── attendance.py
├── routes/
│   ├── employees.py
│   └── attendance.py
├── requirements.txt
├── setup.py
├── README.md
└── .env
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Pydantic v2, Motor (async MongoDB driver) |
| Database | MongoDB |

---

## ✅ Prerequisites

Before you begin, make sure you have the following installed:

| Tool | Required Version | Download |
|---|---|---|
| **Node.js** | >= 18.x | [nodejs.org](https://nodejs.org) |
| **Python** | >= 3.10 | [python.org](https://python.org) |
| **MongoDB** | Latest | [mongodb.com](https://www.mongodb.com/try/download/community) |

> **Note:** MongoDB must be running locally on port `27017`, OR you can use a free [MongoDB Atlas](https://www.mongodb.com/atlas) cloud cluster.

---

## 🚀 Getting Started

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/hrms-lite.git
cd hrms-lite
```

---

### Step 2 — Backend Setup

```bash
# Navigate to the backend folder
cd backend
```

#### 2a. Create and activate a Python virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2b. Install Python dependencies

```bash
pip install -r requirements.txt
```

#### 2c. Configure environment variables

Open `backend/.env` and update if needed:

```env
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=hrms_lite

# Admin credentials (used by setup.py)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=Admin@123
ADMIN_NAME=System Administrator
```

> If using **MongoDB Atlas**, replace `MONGO_URI` with your Atlas connection string:
> ```env
> MONGO_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/
> ```

#### 2d. Run the setup script (IMPORTANT — run this once)

```bash
python setup.py
```

This will:
- 📌 Create MongoDB **unique indexes** (employee_id, email, attendance date)
- 👤 Create the **default admin user** in the database
- Print a confirmation with the credentials

Expected output:
```
🚀  HRMS Lite — Setup Script
========================================

📌  Creating database indexes...
  ✅  employees.employee_id  (unique)
  ✅  employees.email        (unique)
  ✅  attendance.(employee_id + date)  (unique compound)
  ✅  admins.username  (unique)

👤  Setting up admin user...
  ✅  Admin user created successfully!

  ┌─────────────────────────────────┐
  │  Username : admin                │
  │  Password : Admin@123            │
  │  Role     : admin                │
  └─────────────────────────────────┘

  ⚠️   Change your password after first login!

✅  Setup complete! You can now start the server:
    uvicorn main:app --reload --port 8000
```

> ⚠️ **Only run `setup.py` once.** Re-running it is safe — it skips if admin already exists.

#### 2e. Start the backend server

```bash
uvicorn main:app --reload --port 8000
```

✅ Backend will be live at: **`http://localhost:8000`**  
📄 Swagger API docs: **`http://localhost:8000/docs`**

---

The admin user exists **for API-level access only** (e.g. testing via Swagger or future auth integrations).

### Default Admin Credentials

| Field | Value |
|---|---|
| **Username** | `admin` |
| **Password** | `Admin@123` |
| **Role** | `admin` |

> To use **custom credentials**, edit `backend/.env` **before** running `setup.py`.

### How to Verify Admin via Swagger UI
1. Open **`http://localhost:8000/docs`**
2. Find `POST /admin/login` → click **Try it out**
3. Enter the body below and click **Execute**:
```json
{
  "username": "admin",
  "password": "Admin@123"
}
```

### How to Verify via PowerShell
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/admin/login" `
  -Method POST `
  -Body '{"username":"admin","password":"Admin@123"}' `
  -ContentType "application/json"
```

Expected response:
```json
{
  "username": "admin",
  "full_name": "System Administrator",
  "role": "admin"
}
```

### Admin API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/admin/login` | Verify admin credentials |
| `GET` | `/admin/info?username=admin` | Get admin info |



---


## 🌐 API Reference

### Health Check
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check if API is running |

### Employees
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/employees` | List all employees |
| `POST` | `/employees` | Add a new employee |
| `DELETE` | `/employees/{employee_id}` | Delete an employee |

**Add Employee — Request Body:**
```json
{
  "employee_id": "EMP001",
  "full_name": "Jane Smith",
  "email": "jane@company.com",
  "department": "Engineering"
}
```

### Attendance
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/attendance` | Mark attendance |
| `GET` | `/attendance/{employee_id}` | Get attendance for an employee |
| `GET` | `/attendance?date=YYYY-MM-DD` | Get all attendance (optional date filter) |

**Mark Attendance — Request Body:**
```json
{
  "employee_id": "EMP001",
  "date": "2026-02-20",
  "status": "Present"
}
```

---

## ✨ Features

- 👥 **Employee Management** — Add, view, and delete employees with full validation
- 📋 **Attendance Tracking** — Mark daily attendance (Present / Absent) per employee
- 📊 **Dashboard** — Live summary: total employees, present/absent today, department breakdown
- 🔍 **Date Filter** — Filter attendance history by any date
- ✅ **Present Days Count** — View total present days per employee
- ⚠️ **Validations** — Required fields, valid email format, duplicate employee ID prevention
- 🔄 **UI States** — Loading spinners, empty states, and error messages throughout

---

## ⚙️ Build for Production

### Frontend (Vite build)
```bash
cd frontend
npm run build
# Output: frontend/dist/
```

### Backend (Production server)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🚢 Deployment

| Service | Purpose | Free Tier |
|---|---|---|
| [Vercel](https://vercel.com) | Host the React frontend | ✅ Yes |
| [Render](https://render.com) | Host the FastAPI backend | ✅ Yes |
| [MongoDB Atlas](https://www.mongodb.com/atlas) | Cloud MongoDB database | ✅ Yes (512MB) |

### Deploying Frontend to Vercel
1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) → New Project → Import your repo
3. Set **Root Directory** to `frontend`
4. Add environment variable: `VITE_API_URL=https://your-backend.onrender.com`
5. Deploy ✅

### Deploying Backend to Render
1. Go to [render.com](https://render.com) → New Web Service → Connect your repo
2. Set **Root Directory** to `backend`
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Add environment variables:
   - `MONGO_URI` = your MongoDB Atlas connection string
   - `DATABASE_NAME` = `hrms_lite`
6. Deploy ✅

---

## ⚠️ Assumptions & Limitations

- Single admin user — **no authentication** required
- One attendance record per employee per date (duplicates are rejected)
- Deleting an employee **also deletes** all their attendance records
- Leave management, payroll, and advanced HR features are **out of scope**

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is built as part of an HRMS Lite assignment. Feel free to use and modify it.
