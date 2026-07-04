Distributed Job Scheduler - Getting Started Guide

Local Development Setup (PostgreSQL)

Your Django development server is running with PostgreSQL at http://localhost:8000

What's Ready

- Database: PostgreSQL (automatically created at `PostgreSQL Database`)
- Admin Panel: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/api/docs/ (Swagger UI)
- Admin User: Username `admin`, Password `admin123`

API Documentation

The interactive API documentation is available at:
```
http://localhost:8000/api/docs/
```

All endpoints are documented there with request/response examples.

---

Authentication

Admin Panel Access

1. Go to http://localhost:8000/admin/
2. Login with:
   - Username: `admin`
   - Password: `admin123`

API Authentication

The API uses JWT (JSON Web Tokens) for authentication.

1. Get JWT Tokens

Endpoint: `POST /api/auth/login/`

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

2. Use Access Token in Requests

Include the access token in the Authorization header:

```bash
curl -H "Authorization: Bearer <access_token>" \
  http://localhost:8000/api/projects/
```

3. Refresh Token

When access token expires (15 minutes), refresh it:

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

---

Example Workflows

1. Create a Project

```bash
Get access token first
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.access')

Create project
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project",
    "description": "Test project"
  }'
```

2. Create a Queue

```bash
curl -X POST http://localhost:8000/api/queues/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "default-queue",
    "description": "Default job queue",
    "priority": 5,
    "concurrency_limit": 10,
    "project": 1
  }'
```

3. Create an Immediate Job

```bash
curl -X POST http://localhost:8000/api/jobs/create-immediate/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "queue": 1,
    "job_type": "email_notification",
    "payload": {"email": "user@example.com", "subject": "Hello"}
  }'
```

4. Create a Delayed Job (run after 10 seconds)

```bash
curl -X POST http://localhost:8000/api/jobs/create-delayed/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "queue": 1,
    "job_type": "data_processing",
    "payload": {"data": "example"},
    "delay_seconds": 10
  }'
```

5. Create a Recurring Job (Cron)

```bash
curl -X POST http://localhost:8000/api/jobs/create-recurring/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "queue": 1,
    "job_type": "cleanup_task",
    "payload": {},
    "cron_expression": "0 * * * *"
  }'
```

6. List Jobs

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/jobs/?queue=1&status=pending
```

7. Cancel a Job

```bash
curl -X POST http://localhost:8000/api/jobs/{job_id}/cancel/ \
  -H "Authorization: Bearer $TOKEN"
```

8. View Queue Statistics

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/queues/{queue_id}/statistics/
```

---

User Management

Create a New User

Via Django Shell:

```bash
source .venv/bin/activate
python manage.py shell
```

```python
from authentication.models import User

Create regular user
user = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='secure_password_123'
)
print(f"Created user: {user.username}")

Create admin user
admin = User.objects.create_superuser(
    username='alice',
    email='alice@example.com',
    password='admin_password_123'
)
admin.role = 'admin'
admin.save()
print(f"Created admin: {admin.username}")
```

Via Django Admin:
1. Go to http://localhost:8000/admin/
2. Login as `admin`
3. Click "Users" → "Add User"
4. Fill in username, email, password, and role

---

API Endpoints Summary

Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Get JWT tokens
- `POST /api/auth/refresh/` - Refresh access token
- `GET /api/auth/me/` - Get current user profile
- `PUT /api/auth/me/` - Update profile
- `POST /api/auth/password-change/` - Change password
- `POST /api/auth/logout/` - Logout (invalidate token)

Projects
- `GET /api/projects/` - List projects
- `POST /api/projects/` - Create project
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project

Queues
- `GET /api/queues/` - List queues
- `POST /api/queues/` - Create queue
- `GET /api/queues/{id}/` - Get queue details
- `PUT /api/queues/{id}/` - Update queue
- `DELETE /api/queues/{id}/` - Delete queue
- `POST /api/queues/{id}/pause/` - Pause queue
- `POST /api/queues/{id}/resume/` - Resume queue
- `GET /api/queues/{id}/statistics/` - Queue statistics

Jobs
- `GET /api/jobs/` - List jobs
- `POST /api/jobs/create-immediate/` - Create immediate job
- `POST /api/jobs/create-delayed/` - Create delayed job (runs after N seconds)
- `POST /api/jobs/create-scheduled/` - Create scheduled job (runs at specific time)
- `POST /api/jobs/create-recurring/` - Create recurring job (Cron)
- `POST /api/jobs/create-batch/` - Create batch jobs
- `GET /api/jobs/{id}/` - Get job details
- `PUT /api/jobs/{id}/` - Update job
- `DELETE /api/jobs/{id}/` - Delete job
- `POST /api/jobs/{id}/cancel/` - Cancel job
- `POST /api/jobs/{id}/retry/` - Retry failed job

Workers
- `GET /api/workers/` - List workers
- `GET /api/workers/{id}/` - Get worker details
- `GET /api/workers/{id}/statistics/` - Worker statistics
- `POST /api/workers/{id}/heartbeat/` - Register heartbeat

Logs
- `GET /api/logs/` - List execution logs
- `GET /api/logs/{id}/` - Get log details

Scheduling
- `GET /api/scheduling/` - List schedules
- `POST /api/scheduling/` - Create schedule
- `GET /api/scheduling/{id}/` - Get schedule details
- `PUT /api/scheduling/{id}/` - Update schedule
- `DELETE /api/scheduling/{id}/` - Delete schedule

---

Database Schema

Main Tables:
- `authentication_user` - Users with roles (admin/user)
- `projects_organization` - Organizations
- `projects_project` - Projects
- `queues_queue` - Job queues
- `jobs_job` - Job records
- `jobs_jobexecution` - Job execution history
- `jobs_deadletter` - Failed jobs
- `workers_worker` - Background workers
- `workers_workerheartbeat` - Worker health monitoring
- `logs_logentry` - Execution logs
- `retry_retrypolicy` - Retry configurations
- `scheduling_schedule` - Cron schedules
- `scheduling_scheduleexecution` - Schedule execution records

---

Development Server Management

Start Server
```bash
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

Run Migrations
```bash
source .venv/bin/activate
python manage.py migrate
```

Create Superuser
```bash
source .venv/bin/activate
python manage.py createsuperuser
```

Access Django Shell
```bash
source .venv/bin/activate
python manage.py shell
```

Run Tests
```bash
source .venv/bin/activate
pytest
```

---

Job States

A job goes through these states:

- Queued: Waiting in queue
- Scheduled: Waiting for scheduled time
- Claimed: Worker has claimed the job
- Running: Currently executing
- Completed: Successfully finished
- Failed: Execution failed
- Dead Letter: Moved after max retries

---

Retry Mechanism

Jobs support automatic retries with three backoff strategies:

1. Fixed Delay: Wait same duration before each retry
2. Linear Backoff: Delay increases linearly (1s, 2s, 3s...)
3. Exponential Backoff: Delay doubles each time (1s, 2s, 4s, 8s...)

After max retries, job moves to Dead Letter Queue.

---

Troubleshooting

Server won't start
```bash
Ensure venv is activated
source .venv/bin/activate

Ensure PostgreSQL is enabled

Check Django system
python manage.py check
```

Database errors
```bash
Fresh database
rm PostgreSQL Database
python manage.py migrate
```

Permission denied errors
```bash
Create admin user
python manage.py createsuperuser

Then access admin panel
```

Port already in use
```bash
Use different port
python manage.py runserver 0.0.0.0:8001
```

---

Additional Resources

- API Docs: http://localhost:8000/api/docs/
- Admin Panel: http://localhost:8000/admin/
- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- JWT Docs: https://django-rest-framework-simplejwt.readthedocs.io/

---

Next Steps

1.  Create your first project
2.  Create a queue
3.  Create and submit jobs
4.  Monitor job execution via admin panel or logs API
5.  Test different job types (immediate, delayed, scheduled, recurring)
6.  Experiment with retry policies

Happy job scheduling! 
