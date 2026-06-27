# ResuMate AI v3 — Enhanced Resume Builder

A full-stack AI resume builder with admin panel, real-time auto-save, ATS scoring, and job description matching.

## ✨ What's New in v3

| Feature | Description |
|---|---|
| **Admin Panel** | Full `/admin` dashboard — user management, ban/unban, promote admins, resume overview, activity log, growth chart |
| **Real-time Auto-save** | Changes save automatically 1.5s after you stop typing, with a live save indicator |
| **Profile Management** | Change your name, avatar colour, and password from the Profile tab |
| **Activity Logging** | Every login, register, and resume action is tracked |
| **ATS Score Persistence** | ATS scores are stored per-resume and shown in the dashboard |
| **View Counter** | Public shared resumes track view counts |
| **Projects & Certifications** | New editor sections for projects and certifications |
| **Admin Auto-promotion** | First registered user is automatically given admin access |

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy env file
cp .env.example .env
# Edit .env — at minimum change JWT_SECRET

# 3. Start the server
uvicorn server:app --reload --port 8000
# Or: python server.py

# 4. Open in browser
# Landing:   http://localhost:8000/
# App:       http://localhost:8000/app
# Admin:     http://localhost:8000/admin
# API docs:  http://localhost:8000/docs
```

## 🗂 Project Structure

```
resumate-pro/
├── server.py              # FastAPI entry point
├── backend/
│   ├── models.py          # SQLAlchemy ORM (User, Resume, ActivityLog)
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── auth.py            # JWT + bcrypt helpers
│   ├── database.py        # SQLAlchemy engine (SQLite default)
│   ├── deps.py            # FastAPI dependencies (auth guards)
│   └── routes/
│       ├── auth.py        # Register, login, profile, password change
│       ├── resumes.py     # Resume CRUD + share link
│       ├── ai.py          # AI enhance, summary, cover letter, chat
│       ├── analyze.py     # ATS scoring + JD match
│       ├── export.py      # PDF export
│       ├── parse.py       # Resume upload parser
│       └── admin.py       # 🆕 Full admin panel API
├── core/                  # AI engine, ATS analyser, PDF generator
├── data/                  # Skills DB, action verbs, industry keywords
├── frontend/
│   ├── index.html         # Landing page
│   ├── auth.html          # Login / Register
│   ├── app.html           # 🆕 Enhanced main workspace
│   ├── admin.html         # 🆕 Admin panel
│   ├── share.html         # Public resume viewer
│   ├── css/styles.css     # 🆕 Enhanced design system
│   └── js/
│       ├── api.js         # 🆕 Extended API client (admin methods)
│       └── auth.js        # Login/register controller
└── .env.example           # 🆕 Environment variable template
```

## 🛡️ Admin Panel

The first user to register automatically receives admin access.

**Admin features:**
- **Overview** — Live stats: total users, resumes, logins, signups today; user growth chart
- **Users** — Search, paginate, ban/unban, promote/demote admin, delete users
- **Resumes** — View all resumes across all users, delete any resume
- **Activity Log** — Full audit trail of logins, registrations, and resume actions

Access at `/admin` — redirects to `/app` for non-admins.

## 🔌 API Endpoints

All endpoints documented at `/docs`.

| Group | Prefix | Highlights |
|---|---|---|
| Auth | `/api/auth` | register, login, me, profile, change-password |
| Resumes | `/api/resumes` | CRUD, duplicate, public share |
| AI | `/api/ai` | enhance-bullet, summary, cover-letter, chat, skill-suggestions |
| Analysis | `/api/analyze` | ATS score, JD match |
| Export | `/api/export` | PDF resume, cover letter PDF |
| Parse | `/api/parse` | Upload PDF/DOCX and extract data |
| Admin | `/api/admin` | stats, growth, users, resumes, activity |

## ⚙️ Environment Variables

| Variable | Default | Description |
|---|---|---|
| `JWT_SECRET` | `change-me-…` | **Change in production!** JWT signing secret |
| `JWT_EXPIRE_HOURS` | `24` | Token expiry in hours |
| `OPENAI_API_KEY` | — | Enables GPT-powered features |
| `DATABASE_URL` | SQLite in-file | Override with PostgreSQL for production |
| `ALLOWED_ORIGINS` | `*` | Restrict CORS origins in production |
| `PORT` | `8000` | Server port |

## 🧪 Tech Stack

- **Backend:** FastAPI, SQLAlchemy 2.0, SQLite (dev) / PostgreSQL (prod)
- **Auth:** JWT (python-jose) + bcrypt
- **AI:** OpenAI API with local fallback engine (scikit-learn TF-IDF)
- **PDF:** ReportLab
- **Frontend:** Vanilla HTML + Alpine.js + Tailwind CSS
- **Styling:** CSS custom properties (dark mode native)
