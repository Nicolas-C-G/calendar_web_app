# 📅 Calendar Web App

A full-stack web application that allows users to log in (via username/password or Google OAuth), sync their Google Calendar events, and interact with them via a responsive dashboard.

---

## 🔧 Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Frontend:** React.js, Bootstrap, FullCalendar
- **Auth:** Google OAuth 2.0, JWT-based tokens via `itsdangerous`
- **Testing:** `pytest`, SQLite (in-memory)
- **Rate limiting:** `slowapi`

---

## 📁 Project Structure

```
calendar_web_app/
│
├── backend/               # FastAPI backend
│   ├── config.py          # App settings and constants
│   ├── database.py        # SQLAlchemy session & DB access
│   ├── limiter_config.py  # SlowAPI limiter setup
│   ├── main.py            # FastAPI entry point
│   ├── functions/         # Shared utility functions
│   ├── models/            # SQLAlchemy models
│   ├── routers/           # API route logic
│   └── schemas/           # Pydantic models
│
├── frontend/              # React frontend
│   ├── public/            # Static files
│   ├── src/               # React components
│   ├── package.json       # React dependencies
│   └── .env               # React environment variables
│
├── testing/               # Pytest-based API testing
│   ├── test_auth.py       # Authentication endpoint tests
│   └── README.txt
│
└── requirements.txt       # Python backend dependencies
```

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.10+
- Node.js + npm
- A Google Cloud project with OAuth2.0 credentials

---

### 🐍 Backend Setup (FastAPI)

```bash
cd backend
python -m venv env
source env/bin/activate      # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

**.env (optional variables for config.py):**
```env
SESSION_SECRET_KEY=your_secret
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
```

**Run server:**
```bash
uvicorn main:app --reload
```

---

### 🌐 Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

Set `.env` for React:
```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 🔐 Authentication

- **Standard login/register:** `/login`, `/register`
- **Google OAuth:** `/auth/google`
  - Redirects and posts the token back via `window.opener.postMessage`

---

## 🧪 Running Tests

```bash
cd testing
pytest test_auth.py
```

Make sure you run the test with proper `PYTHONPATH`:

```bash
PYTHONPATH=../backend pytest test_auth.py
```

Or on Windows:
```cmd
set PYTHONPATH=../backend && pytest test_auth.py
```

---

## ✅ Features

- Google Calendar event fetch
- Token-based session auth
- Daily event modal pop-ups
- Clickable calendar UI
- Full test coverage of core endpoints

---

## 🧼 TODO

- [ ] Add token expiration refresh flow
- [ ] Add frontend tests
- [ ] Deploy with Docker or Heroku
