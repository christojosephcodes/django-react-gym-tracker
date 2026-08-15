# ??? Full-Stack Gym / Workout Logger

A full-stack fitness tracker application built with **Django REST Framework** and **React**.

## ?? Features
- **User Authentication**: Token-based authentication with Login, Sign-up, and Logout.
- **Nested Writable Serializers**: Log complete workout sessions with dynamic exercise sets, reps, and weights in a single database transaction.
- **Full CRUD Operations**: Create, view, update/edit, and delete past workout sessions.
- **SQL Aggregations**: Real-time Personal Records (PR) calculations and total workout metrics.
- **Isolated User Scope**: Each user only views and modifies their own fitness data.

## ??? Tech Stack
- **Backend**: Python, Django 5.x, Django REST Framework, SQLite
- **Frontend**: React, Axios, JavaScript (ES6+)

## ?? Installation & Setup

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
call venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```
