# Student Guidance System — Backend

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.17-A30000?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

The backend API for a career-guidance and educational management platform focused on students exploring programming, computing, and technology careers.

The system combines skill-based assessments, weighted career matching, learning-path recommendations, mentoring, and personal counseling. It gives students structured guidance while providing educational institutes with centralized tools for managing users, courses, batches, assessments, enrollments, counselors, and student progress.

![Student Guidance System documentation preview](docs_hero.png)

> **Project status:** This is an actively developed educational MVP. The current recommendation engine is deterministic and assessment-driven; it is not presented as a replacement for professional career counseling.

## Table of Contents

- [Problem and Solution](#problem-and-solution)
- [Core Features](#core-features)
- [User Roles](#user-roles)
- [How Career Recommendations Work](#how-career-recommendations-work)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Docker Setup](#docker-setup)
- [API Reference](#api-reference)
- [Authentication](#authentication)
- [Real-Time Notifications](#real-time-notifications)
- [Demo Data](#demo-data)
- [Testing and Validation](#testing-and-validation)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## Problem and Solution

Students interested in technology frequently struggle to choose a career because they lack:

- A clear understanding of how their current skills align with different careers
- Structured, evidence-based career guidance
- Visibility into the skills they still need to develop
- A practical learning path after receiving a recommendation
- Access to mentors and counselors who can add human context to automated results

The Student Guidance System addresses this by turning assessment performance into skill scores and comparing those scores with weighted career requirements. Students receive ranked career matches, skill-gap information, and relevant learning paths. Educational institutions can supplement these automated results with counselor assignments and scheduled counseling sessions.

## Core Features

### Assessment and career guidance

- Career aptitude, course placement, course quiz, course final, and skill assessments
- Beginner, intermediate, and advanced target levels
- Configurable questions stored as structured JSON
- Timed assessments with configurable passing scores and attempt limits
- Start, submit, complete, and abandon attempt workflows
- Automatic overall scoring and per-skill score calculation
- Weak-skill identification for completed attempts
- Ranked career recommendations based on weighted skill requirements
- Career readiness, match percentage, skill gaps, and recommended learning paths

### Academic and career management

- Career profiles with industry, description, salary, and required skills
- Ordered career-to-course learning paths
- Skills catalog shared by assessments, careers, and mentors
- Courses with categories, levels, pricing, and duration
- Course batches with schedules, mentors, dates, capacity, and status
- Transaction-safe enrollment with duplicate and capacity protection
- Enrollment payment tracking

### Mentoring and counseling

- Student, mentor, counselor, and administrator profiles
- Mentor expertise, experience, and skill management
- Student-to-counselor assignments
- One active counselor assignment per student
- Counseling session scheduling, status tracking, and notes
- Counselor dashboards with assigned students and upcoming sessions
- Mentor dashboards with assigned batches and enrolled students

### Platform capabilities

- Email-based authentication with JWT access and refresh tokens
- Refresh-token rotation and blacklisting on logout
- Role-aware dashboards for students, mentors, counselors, and administrators
- Private real-time notifications over authenticated WebSockets
- Notification history, read state, and deletion
- Welcome emails through Celery background tasks
- Redis-backed caching with targeted dashboard invalidation
- Soft deletion and audit fields on core domain models
- Limit/offset pagination
- Swagger and ReDoc API documentation
- Cloudinary-backed media storage
- ASGI deployment with Daphne

## User Roles

| Role | Primary capabilities |
| --- | --- |
| **Student** | Manage a profile, take assessments, review scores and skill results, receive career recommendations, view learning paths, see enrolled batches, receive notifications, and participate in counseling. |
| **Mentor** | Maintain expertise and skills, view assigned course batches, and monitor students enrolled in those batches. |
| **Counselor** | Maintain a professional profile, view assigned students, and work with scheduled counseling sessions and notes. |
| **Super Admin** | View platform analytics and manage careers, skills, courses, batches, assessments, users, enrollments, counselor assignments, and counseling sessions. |

## How Career Recommendations Work

The recommendation engine uses the latest completed assessment with a passing score of at least 60.

1. Submitted answers are checked against the assessment's correct answers.
2. The system calculates a percentage score for each assessed skill.
3. Each career defines required skills, minimum scores, and importance weightages.
4. A student's skill score is compared with each career requirement.
5. Weighted matches are combined into a career match score from 0–100.
6. Careers scoring at least 30% are ranked, with the top five returned.
7. Missing requirements become skill gaps.
8. Careers scoring at least 60% also include an ordered learning path.

```mermaid
flowchart LR
    A["Student completes assessment"] --> B["Per-skill scores"]
    B --> C["Weighted career requirements"]
    C --> D["Career match score"]
    D --> E["Ranked recommendations"]
    D --> F["Skill gaps"]
    D --> G["Learning path"]
```

## System Architecture

```mermaid
flowchart TB
    Client["React client or API consumer"]
    ASGI["Daphne and Django ASGI"]
    API["Django REST Framework API"]
    WS["Django Channels WebSockets"]
    Worker["Celery worker"]
    DB[("PostgreSQL")]
    Redis[("Redis")]
    Media["Cloudinary media storage"]
    Email["SMTP email service"]

    Client -->|"HTTPS and JWT"| ASGI
    Client -->|"WebSocket and JWT"| ASGI
    ASGI --> API
    ASGI --> WS
    API --> DB
    API --> Redis
    API --> Media
    API --> Worker
    WS --> Redis
    Worker --> Redis
    Worker --> Email
```

Redis databases are separated by responsibility:

| Redis database | Purpose |
| --- | --- |
| `/0` | Django Channels layer |
| `/1` | Application and dashboard cache |
| `/2` | Celery broker |

Celery task results are stored in PostgreSQL through `django-celery-results`.

## Technology Stack

| Area | Technology |
| --- | --- |
| Language | Python 3.12 |
| Web framework | Django 6.0 |
| API | Django REST Framework 3.17 |
| Authentication | Simple JWT and Django sessions |
| Database | PostgreSQL 17 |
| Cache and messaging | Redis 7 and django-redis |
| Background jobs | Celery and django-celery-results |
| Real-time communication | Django Channels, channels-redis, and WebSockets |
| ASGI server | Daphne |
| Filtering and pagination | django-filter and DRF limit/offset pagination |
| API documentation | drf-yasg, Swagger UI, and ReDoc |
| Media storage | Cloudinary and django-cloudinary-storage |
| Image processing | Pillow |
| Configuration | python-decouple and dj-database-url |
| Containerization | Docker and Docker Compose |

## Project Structure

```text
Student-Guidance-System/
├── assessment/             # Assessments, attempts, skill results, recommendations
├── authentication/         # Custom users, role profiles, login, registration
├── base/                   # Auditing, soft deletion, and seed command
├── career/                 # Careers, career skills, and learning paths
├── counselling/            # Counselor assignments and sessions
├── course/                 # Categories, courses, batches, and schedules
├── dashboard/              # Role-specific dashboard aggregation and caching
├── enrollment/             # Admin-managed batch enrollment and payments
├── notifications/          # REST and WebSocket notification delivery
├── skill/                  # Shared skills catalog
├── student_guidance_system/# Settings, root URLs, ASGI, WSGI, and Celery
├── utils/                  # Shared permissions and response helpers
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── manage.py
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- Redis
- A Cloudinary account
- SMTP credentials, such as a Gmail account with an app password

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and replace every placeholder.

```env
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=postgresql://postgres:your-password@localhost:5432/student_guidance

# Use the Redis base URL without a database suffix.
REDIS_URL=redis://localhost:6379

CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

LANGUAGE_CODE=en-us
TIME_ZONE=Asia/Kathmandu

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password

CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

> `REDIS_URL` must be a base connection URL because the settings append `/0`, `/1`, and `/2` for Channels, caching, and Celery.

### 4. Create the database and run migrations

Create an empty PostgreSQL database named `student_guidance`, then run:

```bash
python manage.py migrate
```

### 5. Optionally load demonstration data

```bash
python manage.py seed_data
```

The seed command creates sample skills, categories, courses, careers, career-skill mappings, learning paths, assessments, mentors, counselors, batches, and demo users. It is designed to be rerunnable for development, but should not be part of a production data strategy.

### 6. Start the services

Start the ASGI application:

```bash
daphne -b 0.0.0.0 -p 9009 student_guidance_system.asgi:application
```

Start a Celery worker in another terminal:

```bash
celery -A student_guidance_system worker --loglevel=info
```

On Windows, use the solo worker pool if the default pool is unavailable:

```powershell
celery -A student_guidance_system worker --loglevel=info --pool=solo
```

The API will be available at `http://127.0.0.1:9009/`.

## Docker Setup

The repository includes PostgreSQL, Redis, and web services in `docker-compose.yml`.

For Docker, use container service names in `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/student_guidance
REDIS_URL=redis://redis:6379
```

Then start the stack:

```bash
docker compose up --build
```

The container entrypoint automatically runs migrations, collects static files, loads seed data, and starts Daphne on port `9009`.

To run the Celery worker with Compose as currently configured, start it separately:

```bash
docker compose exec web celery -A student_guidance_system worker --loglevel=info
```

## API Reference

### Interactive documentation

| Documentation | URL |
| --- | --- |
| Swagger UI | `/swagger/` |
| ReDoc | `/redoc/` |
| OpenAPI JSON | `/swagger.json` |
| OpenAPI YAML | `/swagger.yaml` |

### Main endpoints

All paths below are relative to the API host.

| Module | Method and endpoint | Purpose |
| --- | --- | --- |
| Authentication | `POST /api/auth/login/` | Sign in with email and password |
| Authentication | `POST /api/auth/refresh/` | Refresh an access token |
| Authentication | `POST /api/auth/logout/` | Blacklist a refresh token |
| Students | `POST /api/auth/students/register/` | Register a student account |
| Mentors | `POST /api/auth/mentors/register/` | Register a mentor account |
| Counselors | `POST /api/auth/counselors/register/` | Register a counselor account |
| Profiles | `/api/auth/students/`, `/mentors/`, `/counselors/` | List, retrieve, update, or soft-delete role profiles |
| Courses | `/api/courses/` | Course CRUD |
| Categories | `/api/categories/` | Course-category CRUD with search and filters |
| Batches | `/api/batches/` | Course-batch, mentor, schedule, and capacity management |
| Skills | `/api/skills/` | Skills catalog CRUD |
| Careers | `/api/careers/` | Career and required-skill management |
| Career paths | `/api/career-paths/` | Ordered career learning paths |
| Assessments | `/api/assessments/` | Assessment definitions and questions |
| Assessment skills | `/api/assessment-skills/` | Assessment-to-skill weight mappings |
| Attempts | `POST /api/student-assessments/start/` | Start an assessment attempt |
| Attempts | `POST /api/student-assessments/{id}/submit/` | Submit answers and calculate results |
| Attempts | `POST /api/student-assessments/{id}/abandon/` | Abandon an in-progress attempt |
| Skill results | `GET /api/student-skill-results/` | Get the authenticated student's skill results |
| Recommendations | `GET /api/recommendations/` | Get ranked career recommendations |
| Enrollments | `/api/enrollments/` | Admin-only enrollment management |
| Counselor assignments | `/api/student-counselors/` | Assign students to counselors |
| Counseling sessions | `/api/counselling-sessions/` | Schedule and manage counseling sessions |
| Student dashboard | `GET /api/dashboard/student/` | Student enrollments, counseling, and assessments |
| Mentor dashboard | `GET /api/dashboard/mentor/` | Assigned batches and enrolled students |
| Counselor dashboard | `GET /api/dashboard/counselor/` | Active students and session summary |
| Admin dashboard | `GET /api/dashboard/admin/` | Platform-wide analytics and recent activity |
| Notifications | `GET /api/notifications/` | List the authenticated user's notifications |
| Notifications | `POST /api/notifications/{id}/read/` | Mark a notification as read |
| Notifications | `DELETE /api/notifications/{id}/delete/` | Delete a notification |

DRF router resources also expose their standard detail endpoints, such as `GET`, `PUT`, `PATCH`, and `DELETE` on `/{id}/`, subject to the permission class configured for that resource.

## Authentication

### Login request

```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "student1@test.com",
  "password": "Student@123"
}
```

Successful login returns user information plus an access and refresh token. Send the access token with protected requests:

```http
Authorization: Bearer <access-token>
```

Access tokens expire after 15 minutes. Refresh tokens expire after seven days and rotate when refreshed.

### Start and submit an assessment

Start:

```http
POST /api/student-assessments/start/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "assessment": 1
}
```

Submit:

```http
POST /api/student-assessments/12/submit/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "answers": {
    "answers": [
      {"question_id": 1, "answer": "A"},
      {"question_id": 2, "answer": "C"}
    ]
  },
  "time_taken_seconds": 420
}
```

## Real-Time Notifications

Authenticated clients can connect to the private notification WebSocket with a JWT access token:

```text
ws://127.0.0.1:9009/ws/notifications/?token=<access-token>
```

Use `wss://` in production. Every authenticated user joins a private channel group named from their user ID. Notification events use this shape:

```json
{
  "event": "notification",
  "data": {
    "id": 42,
    "title": "Assessment Completed",
    "body": "You completed Career Aptitude Assessment with a score of 82%.",
    "notification_type": "assessment_completed",
    "created_at": "2026-08-09 10:00:00+00:00",
    "is_read": false
  }
}
```

Notifications are generated for events such as assessment activity, enrollment, counselor assignment, career creation, and batch assignment.

## Demo Data

Running `python manage.py seed_data` creates these development accounts when they do not already exist:

| Role | Email | Password |
| --- | --- | --- |
| Student | `student1@test.com` | `Student@123` |
| Super Admin | `admin@admin.com` | `admin` |

> These credentials are for local development only. Change or remove them before exposing any deployment publicly. If an account already exists, the student password is not reset by the current seed command.

## Testing and Validation

Run Django's system checks:

```bash
python manage.py check
```

Run the test suite:

```bash
python manage.py test
```

The repository currently contains test scaffolds but still needs comprehensive automated coverage. High-priority areas include assessment scoring, recommendation ranking, permissions, concurrent enrollment capacity, WebSocket authentication, and cache invalidation.

## Roadmap

- Expand the assessment question bank and validation rules
- Add comprehensive unit, API, permission, and WebSocket tests
- Strengthen API-level role permissions across all management resources
- Add richer counselor notes, availability, and appointment workflows
- Track longitudinal student skill growth across multiple assessments
- Improve career matching with multiple-assessment aggregation
- Add explainable recommendation insights and confidence indicators
- Introduce institution-level tenancy and reporting
- Add audit-log views and administrative activity history
- Add CI/CD, formatting, linting, and security scanning
- Improve OpenAPI metadata and example payload coverage

## Contributing

Contributions and constructive feedback are welcome.

1. Create a feature branch.
2. Make a focused change.
3. Add or update tests.
4. Run `python manage.py check` and `python manage.py test`.
5. Open a pull request describing the problem and solution.

Please avoid committing `.env` files, credentials, database dumps, access tokens, or other secrets.

---

Built as a practical learning project to make technology career guidance more structured, accessible, and student-centered.
