# 🏋️ Full-Stack Gym / Workout Logger

A modern, full-stack fitness tracker application built with **Django REST Framework** and **React**. It allows users to manage workouts, track nested exercises (sets, reps, and weights), and automatically calculates personal records (PRs) using optimized database queries.

---

## 🚀 Features

* **User Authentication**: Token-based authentication with Login, Sign-up, and Logout capabilities.
* **Nested Writable Serializers**: Create and edit workout sessions along with nested exercise rows in a single atomic database transaction.
* **Full CRUD Functionality**: Create, view, update/edit, and delete past workout sessions seamlessly.
* **SQL-Level Aggregations**: Real-time Personal Record (PR) tracking calculated directly in SQL via Django ORM (`Max` annotations).
* **User Isolation**: Secure querysets ensuring users can only view and manipulate their own workout logs.

---

## 🛠️ Tech Stack

* **Backend**: Python 3, Django 5.x, Django REST Framework (DRF), SQLite
* **Frontend**: React, Axios, JavaScript (ES6+), CSS

---

## 📂 Project Structure

```text
django-react-gym-tracker/
├── backend/
│   ├── core/              # Django settings, root URLs, and WSGI/ASGI
│   ├── workouts/          # Models, Serializers, Views, and URL routing
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api.js         # Axios instance with DRF Token interceptor
│   │   ├── App.js         # Main UI, Auth screens, Form, and History list
│   │   └── index.js
│   └── package.json
└── .gitignore
```
