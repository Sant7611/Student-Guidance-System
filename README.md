# Student Guidance System — Backend

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0.6-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.17.1-A30000?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.6.3-37814A?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

The backend API for a career-guidance and educational management platform focused on students exploring programming, computing, and technology careers.

Student Guidance System combines skill-based assessments, deterministic career matching, learning-path recommendations, mentoring, counseling, enrollment management, dashboards, background jobs, caching, and real-time notifications in a Django REST Framework backend.

![Student Guidance System documentation preview](docs_hero.png)

> **Project status:** Actively developed educational MVP. The current recommendation engine is deterministic and assessment-driven. It is intended to support structured career exploration, not replace professional career counseling.

## Table of Contents

- [Overview](#overview)
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
- [Assessment Flow](#assessment-flow)
- [Real-Time Notifications](#real-time-notifications)
- [Celery and Redis](#celery-and-redis)
- [Demo Data](#demo-data)
- [Project Documentation](#project-documentation)
- [Testing and Validation](#testing-and-validation)
- [Current Limitations](#current-limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## Overview

The project is designed around a simple idea:

1. A student completes an assessment.
2. The system calculates overall and per-skill scores.
3. The latest qualifying assessment is compared with career skill requirements.
4. Careers are ranked using weighted requirement matching.
5. The student can see skill gaps and, for stronger matches, an ordered learning path.
6. Human guidance can be added through mentor and counselor workflows.

Alongside career guidance, the platform includes the administrative features needed to manage users, courses, batches, assessments, enrollments, counseling, notifications, and dashboards.

## Problem and Solution

Students interested in technology often struggle to choose a career because they may lack:

- A clear understanding of how their current skills align with different careers
- Structured, evidence-based career guidance
- Visibility into the skills they still need to improve
- A practical learning path after receiving a recommendation
- Access to mentors and counselors who can provide human context

Student Guidance System addresses this by converting assessment performance into skill scores and comparing those scores with weighted career requirements.

Students receive ranked career matches, skill-gap information, and relevant learning paths, while administrators can manage the academic and guidance data behind the platform.

## Core Features

### Assessment and career guidance

- Career aptitude assessments
- Course placement assessments
- Course quizzes
- Course final assessments
- Skill assessments
- Beginner, intermediate, and advanced target levels
- Configurable questions stored in JSON
- Configurable passing scores
- Configurable assessment duration
- Attempt limits
- Start, submit, complete, and abandon workflows
- Overall score calculation
- Per-skill score calculation
- Weak-skill identification
- Weighted career matching
- Match percentage
- Career readiness state
- Skill-gap reporting
- Ordered learning paths for stronger matches

### Academic and career management

- Career profiles
- Career industry and salary information
- Weighted career-to-skill requirements
- Career-to-course learning paths
- Shared skill catalog
- Course categories
- Courses
- Course levels
- Course duration and pricing
- Course batches
- Batch schedules
- Mentor assignment
- Batch capacity tracking
- Enrollment payment status
- Duplicate enrollment protection
- Transaction-safe capacity checks using database row locking

### Mentoring and counseling

- Student profiles
- Mentor profiles
- Counselor profiles
- Mentor skills and expertise
- Student-to-counselor assignments
- Counseling session scheduling
- Counseling session status tracking
- Counselor notes
- Mentor dashboards
- Counselor dashboards

### Platform capabilities

- Custom Django user model
- Email-based login
- JWT access and refresh tokens
- Refresh-token rotation
- Refresh-token blacklisting
- Session authentication for supported Django/DRF workflows
- Role-aware permissions
- Role-specific dashboards
- Redis-backed caching
- Targeted dashboard cache invalidation
- Celery background tasks
- SMTP welcome emails
- Authenticated private WebSockets
- Notification persistence
- Notification read state
- Notification deletion
- Soft deletion
- Audit fields on shared base models
- Limit/offset pagination
- Swagger UI
- ReDoc
- Cloudinary-backed media storage
- ASGI deployment through Daphne
- PostgreSQL persistence
- Docker and Docker Compose support

## User Roles

| Role | Primary capabilities |
| --- | --- |
| **Student** | Manage a profile, take assessments, review results, receive career recommendations, inspect skill gaps and learning paths, view enrollments, receive notifications, and participate in counseling. |
| **Mentor** | Maintain mentor information and skills, view assigned course batches, and monitor students in those batches. |
| **Counselor** | Maintain counselor information, view assigned students, and manage scheduled counseling sessions and notes. |
| **Super Admin** | View platform analytics and manage careers, skills, courses, batches, assessments, enrollments, counselor assignments, counseling sessions, and users. |

## How Career Recommendations Work

The current recommendation engine uses the student's **latest completed assessment with an overall score of at least 60**.

For each career:

1. The system loads the career's active skill requirements.
2. Each requirement contains:
   - A required skill
   - A minimum score
   - A weightage
3. The student's score for the skill is compared with the career's minimum requirement.
4. The contribution for that skill is capped at `1.0`.
5. Each contribution is multiplied by the requirement weightage.
6. Weighted values are combined into a match percentage from `0` to `100`.
7. Requirements below the minimum score are returned as skill gaps.
8. Careers with a match score of at least `30%` are included.
9. Results are sorted by match score.
10. The top five careers are returned.
11. Careers scoring at least `60%` also receive their ordered learning path.

Conceptually:

```text
skill_match = min(student_score / required_score, 1.0)

career_match =
    sum(skill_match × weightage)
    -----------------------------
           sum(weightage)

career_match_percentage = career_match × 100
```

A career is considered fully ready only when the student has no remaining required-skill gaps.

```mermaid
flowchart LR
    A["Student completes assessment"] --> B["Overall + per-skill scores"]
    B --> C["Latest qualifying assessment"]
    C --> D["Career skill requirements"]
    D --> E["Weighted match calculation"]
    E --> F["Ranked recommendations"]
    E --> G["Skill gaps"]
    F --> H["Learning path for matches >= 60%"]
```

## System Architecture

```mermaid
flowchart TB
    Client["Frontend client or API consumer"]
    ASGI["Daphne + Django ASGI"]
    API["Django REST Framework"]
    WS["Django Channels"]
    Worker["Celery worker"]
    DB[("PostgreSQL")]
    Redis[("Redis")]
    Media["Cloudinary"]
    Email["SMTP email service"]

    Client -->|"HTTP(S) + JWT"| ASGI
    Client -->|"WebSocket + JWT"| ASGI

    ASGI --> API
    ASGI --> WS

    API --> DB
    API --> Redis
    API --> Media
    API -->|"enqueue task"| Redis

    Redis --> Worker
    Worker --> DB
    Worker --> Email

    WS --> Redis
```

### Redis database separation

The Django settings use separate Redis databases by responsibility:

| Redis database | Purpose |
| --- | --- |
| `/0` | Django Channels channel layer |
| `/1` | Application and dashboard cache |
| `/2` | Celery message broker |

Celery task results are stored in PostgreSQL through `django-celery-results`.

> `REDIS_URL` should be a base Redis URL such as `redis://localhost:6379`. The Django settings append `/0`, `/1`, and `/2` automatically.

## Technology Stack

| Area | Technology |
| --- | --- |
| Language | Python 3.12 |
| Web framework | Django 6.0.6 |
| REST API | Django REST Framework 3.17.1 |
| Authentication | Simple JWT + Django sessions |
| Database | PostgreSQL 17 |
| Cache | Redis 7 + django-redis 7.0.0 |
| Background jobs | Celery 5.6.3 |
| Task result backend | django-celery-results 2.6.0 |
| Real-time communication | Django Channels 4.2.2 + channels-redis 4.2.1 |
| ASGI server | Daphne 4.2.3 |
| Filtering | django-filter 26.1 |
| Pagination | DRF limit/offset pagination |
| API documentation | drf-yasg, Swagger UI, ReDoc |
| Media storage | Cloudinary + django-cloudinary-storage |
| Image processing | Pillow |
| Database configuration | dj-database-url |
| Environment configuration | python-decouple |
| Containerization | Docker + Docker Compose |

## Project Structure

```text
Student-Guidance-System/
├── assessment/              # Assessments, attempts, scoring, skill results, recommendations
│   ├── serializers/
│   ├── views/
│   ├── models.py
│   ├── recommendation.py
│   └── urls.py
│
├── authentication/          # Custom user, role profiles, login, registration
│   ├── serializers/
│   ├── views/
│   ├── models.py
│   ├── tasks.py
│   └── urls.py
│
├── base/                    # Shared base model, audit/soft-delete behavior, seed command
│   └── management/commands/seed_data.py
│
├── career/                  # Careers, career skills, ordered learning paths
├── counselling/             # Counselor assignments and counseling sessions
├── course/                  # Categories, courses, batches, schedules
├── dashboard/               # Student, mentor, counselor, and admin dashboards
├── enrollment/              # Enrollment and payment management
├── notifications/           # REST notifications, Channels consumer, JWT WebSocket middleware
├── skill/                   # Shared skill catalog
│
├── student_guidance_system/
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── utils/                   # Shared permissions and response helpers
├── docs/                    # Extended technical and project documentation
├── docs_hero.png
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── manage.py
└── requirements.txt
```

## Getting Started

### Prerequisites

Install or have access to:

- Python 3.12+
- PostgreSQL
- Redis
- Cloudinary account
- SMTP credentials if you want welcome-email tasks to succeed

### 1. Clone the repository

```bash
git clone https://github.com/Sant7611/Student-Guidance-System.git
cd Student-Guidance-System
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and replace the placeholders.

Example local configuration:

```env
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=postgresql://postgres:your-password@localhost:5432/student_guidance

# Important: use the base Redis URL without /0, /1, or /2.
REDIS_URL=redis://localhost:6379

CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

LANGUAGE_CODE=en-us
TIME_ZONE=Asia/Kathmandu

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password

CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

### 5. Create the PostgreSQL database

Create an empty database named, for example:

```text
student_guidance
```

Then make sure `DATABASE_URL` points to it.

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Optionally load demonstration data

```bash
python manage.py seed_data
```

The seed command creates development data including skills, careers, career-skill requirements, course categories, courses, learning paths, assessments, users, mentors, counselors, and batches.

The seed command is intended for development/demo use.

### 8. Start the ASGI application

```bash
daphne -b 0.0.0.0 -p 9009 student_guidance_system.asgi:application
```

The API will be available at:

```text
http://127.0.0.1:9009/
```

### 9. Start the Celery worker

Open another terminal with the same virtual environment:

```bash
celery -A student_guidance_system worker --loglevel=info
```

On Windows, use the solo pool if needed:

```powershell
celery -A student_guidance_system worker --loglevel=info --pool=solo
```

## Docker Setup

The repository contains Compose services for:

- PostgreSQL
- Redis
- Django/Daphne web application

A typical Docker `.env` should use Compose service names:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/student_guidance
REDIS_URL=redis://redis:6379
```

Start the stack:

```bash
docker compose up --build
```

The application container is exposed on port `9009`.

The container entrypoint performs:

```text
migrate
   ↓
collectstatic
   ↓
seed_data
   ↓
start Daphne
```

The current Compose file does not define a dedicated Celery service. To run a worker inside the running web container:

```bash
docker compose exec web celery -A student_guidance_system worker --loglevel=info
```

For a production-oriented Compose setup, a dedicated Celery worker service is preferable.

## API Reference

### Interactive documentation

| Documentation | Endpoint |
| --- | --- |
| Swagger UI | `/swagger/` |
| ReDoc | `/redoc/` |
| OpenAPI JSON | `/swagger.json` |
| OpenAPI YAML | `/swagger.yaml` |

### Main API endpoints

All paths are relative to the API host.

| Module | Method / endpoint | Purpose |
| --- | --- | --- |
| Authentication | `POST /api/auth/login/` | Sign in using email and password |
| Authentication | `POST /api/auth/refresh/` | Refresh an access token |
| Authentication | `POST /api/auth/logout/` | Blacklist a refresh token |
| Students | `POST /api/auth/students/register/` | Register a student |
| Mentors | `POST /api/auth/mentors/register/` | Register a mentor |
| Counselors | `POST /api/auth/counselors/register/` | Register a counselor |
| Student profiles | `/api/auth/students/` | Student resource operations |
| Mentor profiles | `/api/auth/mentors/` | Mentor resource operations |
| Counselor profiles | `/api/auth/counselors/` | Counselor resource operations |
| Courses | `/api/courses/` | Course resource |
| Categories | `/api/categories/` | Course-category resource |
| Batches | `/api/batches/` | Course-batch resource |
| Skills | `/api/skills/` | Skill resource |
| Careers | `/api/careers/` | Career resource |
| Career paths | `/api/career-paths/` | Career learning paths |
| Assessments | `/api/assessments/` | Assessment definitions |
| Assessment skills | `/api/assessment-skills/` | Assessment-to-skill mappings |
| Attempts | `POST /api/student-assessments/start/` | Start an assessment attempt |
| Attempts | `POST /api/student-assessments/{id}/submit/` | Submit assessment answers |
| Attempts | `POST /api/student-assessments/{id}/abandon/` | Abandon an attempt |
| Skill results | `GET /api/student-skill-results/` | Authenticated student's skill results |
| Recommendations | `GET /api/recommendations/` | Ranked career recommendations |
| Enrollments | `/api/enrollments/` | Enrollment management |
| Counselor assignments | `/api/student-counselors/` | Student-to-counselor assignments |
| Counseling sessions | `/api/counselling-sessions/` | Counseling session management |
| Student dashboard | `GET /api/dashboard/student/` | Student dashboard |
| Mentor dashboard | `GET /api/dashboard/mentor/` | Mentor dashboard |
| Counselor dashboard | `GET /api/dashboard/counselor/` | Counselor dashboard |
| Admin dashboard | `GET /api/dashboard/admin/` | Administrative analytics |
| Notifications | `GET /api/notifications/` | Notification history |
| Notifications | `POST /api/notifications/{id}/read/` | Mark notification as read |
| Notifications | `DELETE /api/notifications/{id}/delete/` | Delete notification |

DRF router resources also expose standard detail routes such as:

```text
GET    /resource/{id}/
PUT    /resource/{id}/
PATCH  /resource/{id}/
DELETE /resource/{id}/
```

Availability depends on the viewset and permission class configured for that resource.

For more detailed API notes, see:

- [`docs/api-reference.md`](docs/api-reference.md)
- [`docs/system-overview.md`](docs/system-overview.md)
- [`docs/database-schema.md`](docs/database-schema.md)

## Authentication

The API supports JWT authentication through Simple JWT.

### Login

```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "student1@test.com",
  "password": "Student@123"
}
```

A successful login returns user information plus access and refresh tokens.

Use the access token on protected requests:

```http
Authorization: Bearer <access-token>
```

### JWT lifetime

| Token | Lifetime |
| --- | --- |
| Access token | 15 minutes |
| Refresh token | 7 days |

Refresh-token rotation and blacklisting are enabled.

### Refresh

```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "<refresh-token>"
}
```

### Logout

```http
POST /api/auth/logout/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "refresh": "<refresh-token>"
}
```

## Assessment Flow

A student's assessment lifecycle is centered around `StudentAssessment`.

```mermaid
stateDiagram-v2
    [*] --> InProgress: start
    InProgress --> Completed: submit
    InProgress --> Abandoned: abandon
    Completed --> [*]
    Abandoned --> [*]
```

### Start an assessment

```http
POST /api/student-assessments/start/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "assessment": 1
}
```

### Submit an assessment

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

Submission calculates the attempt score and stores skill-level results used by the recommendation engine.

### Abandon an assessment

```http
POST /api/student-assessments/12/abandon/
Authorization: Bearer <access-token>
```

## Real-Time Notifications

Django Channels is used for private notification delivery.

Authenticated clients connect through:

```text
ws://127.0.0.1:9009/ws/notifications/?token=<access-token>
```

Use `wss://` in production.

The ASGI application routes WebSocket traffic through custom JWT middleware before connecting to the notification consumer.

Each authenticated user is assigned to a private Channels group based on the user's ID.

A notification payload follows this general shape:

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

Notifications can be persisted in PostgreSQL while Redis provides the Channels transport layer.

## Celery and Redis

Celery is currently used for background work such as sending welcome emails.

The request path is conceptually:

```text
Registration request
      ↓
Django/DRF creates user
      ↓
send_welcome_email.delay(...)
      ↓
Redis /2
      ↓
Celery worker
      ↓
SMTP email service
```

### Broker vs result backend

The project uses:

```text
Redis /2         → Celery broker
PostgreSQL       → Celery result backend through django-celery-results
```

A Celery result backend is not required merely to execute background tasks, but this project currently configures one so task state/results can be stored.

## Demo Data

Run:

```bash
python manage.py seed_data
```

The development seed command includes demo accounts when they do not already exist.

| Role | Email | Password |
| --- | --- | --- |
| Student | `student1@test.com` | `Student@123` |
| Super Admin | `admin@admin.com` | `admin` |

> **Development only:** Never expose these credentials unchanged in a public or production deployment.

The seed command is designed for convenient local/demo population rather than as a production data-management strategy.

## Project Documentation

The repository contains additional documentation under `docs/`, including:

- [`docs/system-overview.md`](docs/system-overview.md)
- [`docs/api-reference.md`](docs/api-reference.md)
- [`docs/database-schema.md`](docs/database-schema.md)
- [`docs/algorithm_used_details.md`](docs/algorithm_used_details.md)
- [`docs/web_sockets.md`](docs/web_sockets.md)
- [`docs/redis.md`](docs/redis.md)
- [`docs/data_populate.md`](docs/data_populate.md)

These documents provide deeper notes on implementation, architecture, algorithms, data population, Redis, and WebSocket behavior.

## Testing and Validation

Run Django's system checks:

```bash
python manage.py check
```

Run the test suite:

```bash
python manage.py test
```

The repository currently contains test scaffolds, but comprehensive automated coverage is still a work in progress.

High-priority test areas include:

- Authentication and JWT flows
- Role permissions
- Registration workflows
- Assessment attempt rules
- Assessment scoring
- Per-skill scoring
- Career recommendation ranking
- Skill-gap calculation
- Enrollment duplicate protection
- Concurrent batch-capacity enforcement
- Counselor assignment constraints
- Dashboard cache invalidation
- WebSocket JWT authentication
- Notification delivery
- Celery task behavior

## Current Limitations

This is an educational MVP and several areas are intentionally still evolving:

- Automated test coverage is currently limited
- Career recommendations use the latest qualifying completed assessment rather than aggregating long-term performance
- The matching engine is deterministic and rule-based
- The recommendation threshold currently uses an overall score of `60` in the recommendation engine
- Question banks and assessment validation can be expanded further
- Docker Compose currently starts the web, PostgreSQL, and Redis services but not a dedicated Celery service
- The development container entrypoint automatically runs `seed_data`
- API schema metadata still contains generic placeholder project/contact information
- Production hardening, CI/CD, linting, security scanning, and observability can be improved

## Roadmap

- Add comprehensive unit and API tests
- Add permission-focused integration tests
- Add WebSocket tests
- Expand assessment question banks
- Strengthen assessment answer validation
- Track student skill growth over time
- Aggregate multiple assessments for recommendations
- Add explainable recommendation insights
- Add recommendation confidence indicators
- Improve counselor availability and appointment workflows
- Add richer counselor notes
- Improve mentor progress-tracking workflows
- Add institution-level tenancy
- Add institution reporting
- Add audit-log views
- Improve OpenAPI metadata and example payloads
- Add formatting and linting
- Add CI/CD
- Add dependency/security scanning
- Improve production observability

## Contributing

Contributions and constructive feedback are welcome.

1. Create a feature branch.
2. Make a focused change.
3. Add or update tests where appropriate.
4. Run:

```bash
python manage.py check
python manage.py test
```

5. Open a pull request describing the problem and the solution.

Please do not commit:

- `.env` files
- API keys
- Database credentials
- SMTP passwords
- Access or refresh tokens
- Database dumps containing sensitive data
- Other secrets

---

Built as a practical backend engineering project for structured technology-career guidance, assessment-driven recommendations, academic management, and real-time student support.
