Distributed Job Scheduler

Project Overview

A production-ready backend for scheduling and executing distributed background jobs. This system allows users to create hierarchical projects and queues, submit asynchronous jobs with complex scheduling requirements, and execute them reliably using a custom worker implementation alongside Celery. It includes built-in retry mechanisms, dead-letter queues, worker node management, and a comprehensive REST API.

Features

- JWT Authentication — Register, Login, Refresh, Logout (token blacklist), and Password Change.
- Role-Based Permissions — Admin and User roles ensuring tenant data isolation.
- Project Management — Organizations → Projects → Queues hierarchy.
- Queue Management — Create queues with concurrency limits, dynamic priority draining, pause/resume states, and live statistics.
- Job Lifecycle — State transitions: `Queued → Scheduled → Claimed → Running → Completed → Failed → Dead Letter`.
- Job Types — Supports Immediate, Delayed, Scheduled, Recurring (Cron), and Batch jobs.
- Worker Service — Dynamic custom worker pooling that atomically claims jobs from PostgreSQL, registers dynamically, sends heartbeats, detects stale nodes, and dispatches to Celery.
- Retry Mechanism — Configurable policies (Fixed delay, Linear backoff, Exponential backoff).
- Centralized Logging — Auditing for job events, worker heartbeats, retry attempts, and schedule dispatches.
- Swagger UI — Full OpenAPI documentation seamlessly integrated.

Tech Stack

| Component        | Technology                        |
|-----------------|-----------------------------------|
| Language    | Python 3.9+                       |
| Framework   | Django 4.2 + Django REST Framework|
| Database    | PostgreSQL 16                     |
| Task Queue  | Celery 5 + Redis                  |
| Auth        | SimpleJWT (Access + Refresh)      |
| API Docs    | drf-yasg (Swagger/OpenAPI)        |

Project Structure

```text
backend/
├── scheduler/
├── authentication/
├── common/
├── projects/
├── queues/
├── jobs/
├── workers/
├── scheduling/
├── retry/
├── logs/
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env
└── pytest.ini
```

Installation

1. Prerequisites
- Python 3.9+
- PostgreSQL 16
- Redis (Running locally or via Docker)

. Setup Virtual Environment
Unzip the project folder and open your terminal inside it.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Environment Variables

Copy the provided example environment configuration:
```bash
cp .env.example .env
```
Ensure your `.env` contains secure defaults for production:
```env
DEBUG=False
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=scheduler
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
REDIS_URL=redis://localhost:6379/0
```

Database Setup

Run the following commands in your terminal to set up PostgreSQL:
```bash
# Create postgres superuser (if not exists)
createuser -h localhost -U <your-pg-admin-user> --superuser postgres

# Set password for postgres user
psql -h localhost -U <your-pg-admin-user> -c "ALTER USER postgres PASSWORD 'postgres';"

# Create the database
createdb -h localhost -U postgres scheduler
```

Apply all database migrations and create an admin user:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Running the Project

Start the Django Development Server:
```bash
python manage.py runserver
```
- API Base URL: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/

 Running Celery Worker

The system utilizes both Celery and a custom database-polling worker. Run these in separate terminal windows (ensure `.venv` is activated in each).

1. Start the Custom DB Worker (Polls PostgreSQL securely):
```bash
python manage.py runworker --name worker1 --concurrency 4 --poll-interval 5
```

2. Start Celery (Executes tasks):
```bash
celery -A scheduler worker --loglevel=info
```

3. Start Celery Beat (For scheduled cron jobs):
```bash
celery -A scheduler beat --loglevel=info
```

 Running Tests

The project includes a comprehensive suite of 51 automated unit tests.
To run the test suite:
```bash
pytest -v
```

 API Documentation

Full OpenAPI documentation is automatically generated. While the server is running, visit:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

 Future Improvements

1. Message Broker Migration: Currently, the custom worker polls PostgreSQL. While this perfectly fulfills the mock requirements, transitioning the custom polling mechanism entirely to Redis or RabbitMQ would eliminate database CPU overhead for millions of jobs.
2. WebSocket Real-time Updates: Implement Django Channels to push real-time job status updates (`queued` -> `running` -> `completed`) to the frontend instead of requiring the client to poll `/api/queues/{id}/stats/`.
3. Advanced Rate Limiting: Implement token-bucket rate limiting per Organization to prevent noisy-neighbor problems in a multi-tenant environment.
