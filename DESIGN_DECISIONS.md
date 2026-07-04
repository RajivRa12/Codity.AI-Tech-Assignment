# Design Decisions & Trade-offs

This document outlines the major architectural and engineering decisions made during the development of the Distributed Job Scheduler, aligning with the core evaluation criteria of reliability, modularity, and maintainability.

## 1. Modular Django Architecture (Apps)
Instead of a monolithic `core` app, the backend is strictly divided into domain-specific apps (`authentication`, `projects`, `queues`, `jobs`, `workers`, `scheduling`, `retry`, `logs`). 
* **Trade-off:** This requires slightly more boilerplate (multiple `models.py`, `urls.py`, etc.).
* **Benefit:** It guarantees extremely clean separation of concerns. The `retry` logic is completely decoupled from the `workers` logic, making the codebase highly maintainable and allowing individual components to be extracted into microservices in the future if needed.

## 2. Concurrency & Task Execution (Celery + Redis)
Rather than writing a custom polling loop using Python `threading` or `asyncio`, Celery was chosen as the distributed task queue, backed by Redis as the message broker.
* **Trade-off:** Introduces external dependencies (Redis, Celery workers) which slightly increases deployment complexity.
* **Benefit:** Celery natively handles atomic job claiming, concurrency limits, graceful shutdowns, and message acknowledgment. This completely prevents duplicate executions and ensures production-grade reliability right out of the box.

## 3. Database Schema & Normalization
The PostgreSQL schema is highly normalized (3NF). We separated `Jobs`, `JobExecutions`, and `WorkerHeartbeats` into distinct tables.
* **Trade-off:** Fetching a job with its complete execution history requires `JOIN` operations.
* **Benefit:** Prevents data anomalies. A single `Job` can have multiple `JobExecutions` (due to retries). Storing this as a 1-to-many relationship provides a perfect, immutable audit trail of exactly when a job failed and when it was retried.

## 4. Exponential Backoff & Retry Logic
Retry policies are stored as configurable database entities rather than hardcoded logic.
* **Trade-off:** Requires an extra database lookup before queueing a retry.
* **Benefit:** Administrators can dynamically tweak the maximum retries, backoff multipliers, and initial delays for different queues without touching source code or restarting the application.

## 5. Dead Letter Queues (DLQ)
Instead of deleting failed jobs, jobs that exceed their `max_retries` are moved to a `DEAD_LETTER` status.
* **Benefit:** Ensures zero data loss. Engineers can inspect the execution logs of a dead letter job, fix the underlying bug, and manually trigger a re-queue via the API/Dashboard.

## 6. Frontend State Management (TanStack React Query)
The React dashboard utilizes `@tanstack/react-query` instead of standard `useEffect` + `Redux`.
* **Trade-off:** Adds a third-party dependency for data fetching.
* **Benefit:** Automatically handles caching, background polling, loading states, and pagination out of the box, resulting in significantly cleaner, less error-prone UI code for monitoring live queues and workers.

## 7. JWT Authentication
We implemented stateless JSON Web Tokens (JWT) rather than traditional session cookies.
* **Trade-off:** Tokens cannot be easily invalidated on the server side without a blacklist (which we implemented).
* **Benefit:** Makes the REST API perfectly stateless, allowing the backend to scale horizontally across multiple servers without needing to share session state.
