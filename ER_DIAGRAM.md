# Database Entity-Relationship Diagram

This document illustrates the data model and the relationships between the core entities in the Distributed Job Scheduler.

```mermaid
erDiagram
    %% Core Organization
    USER ||--o{ ORGANIZATION : "owns (1:N)"
    USER ||--o{ PROJECT : "creates (1:N)"
    ORGANIZATION ||--o{ PROJECT : "contains (1:N)"
    
    %% Job Management
    PROJECT ||--o{ QUEUE : "has (1:N)"
    QUEUE ||--o{ JOB : "holds (1:N)"
    
    %% Retry System
    RETRY_POLICY ||--o{ JOB : "assigned to (1:N)"
    JOB ||--o{ RETRY_ATTEMPT : "tracks (1:N)"
    
    %% Execution & Workers
    JOB ||--o{ JOB_EXECUTION : "records (1:N)"
    WORKER ||--o{ JOB_EXECUTION : "executes (1:N)"
    WORKER ||--o{ WORKER_HEARTBEAT : "emits (1:N)"
    
    %% Scheduling
    QUEUE ||--o{ SCHEDULE : "dispatches to (1:N)"
    SCHEDULE ||--o{ SCHEDULE_EXECUTION : "logs (1:N)"
    SCHEDULE ||--o{ JOB : "generates (1:N)"
    
    %% Logging (Polymorphic relations)
    LOG_ENTRY }o--o| JOB : "logs (N:1)"
    LOG_ENTRY }o--o| WORKER : "logs (N:1)"
    LOG_ENTRY }o--o| SCHEDULE : "logs (N:1)"
    LOG_ENTRY }o--o| RETRY_ATTEMPT : "logs (N:1)"

    %% Entity Details
    USER {
        uuid id PK
        string username
        string email
        string password
        string role "admin/user"
    }

    ORGANIZATION {
        uuid id PK
        string name
        uuid owner_id FK
    }

    PROJECT {
        uuid id PK
        string name
        uuid organization_id FK
        uuid created_by_id FK
    }

    QUEUE {
        uuid id PK
        string name
        uuid project_id FK
        int concurrency_limit
        int priority
        boolean is_paused
    }

    RETRY_POLICY {
        uuid id PK
        string name
        string policy_type "fixed/linear/exponential"
        int max_retries
        int initial_delay
    }

    JOB {
        uuid id PK
        uuid queue_id FK
        uuid retry_policy_id FK
        string type "immediate/delayed/scheduled"
        string status "queued/running/completed/failed"
        jsonb payload
        jsonb result
        datetime scheduled_at
    }

    JOB_EXECUTION {
        uuid id PK
        uuid job_id FK
        uuid worker_id FK
        string status
        int attempt_number
    }

    WORKER {
        uuid id PK
        string name
        string hostname
        int concurrency
        string status
        datetime last_heartbeat
    }

    WORKER_HEARTBEAT {
        uuid id PK
        uuid worker_id FK
        jsonb meta
        datetime timestamp
    }

    SCHEDULE {
        uuid id PK
        uuid queue_id FK
        string name
        string cron
        jsonb payload_template
        datetime next_run_at
    }

    SCHEDULE_EXECUTION {
        uuid id PK
        uuid schedule_id FK
        string status
    }

    RETRY_ATTEMPT {
        uuid id PK
        uuid job_id FK
        int attempt_number
        datetime delayed_until
    }

    LOG_ENTRY {
        uuid id PK
        string level
        string event_type
        string message
        uuid job_id FK "nullable"
        uuid worker_id FK "nullable"
        uuid schedule_id FK "nullable"
    }
```

### Key Relationships
- Multi-Tenancy: Users own `Organizations`, which contain `Projects`. All `Queues` and `Jobs` sit under a specific project, strictly scoping access based on JWT permissions.
- Job Execution: A `Job` represents the overarching task state, while `JobExecution` instances track every individual attempt a `Worker` makes at executing it.
- Scheduling Engine: A `Schedule` runs periodically (driven by Celery Beat) and dynamically inserts new `Job` instances into its assigned `Queue`.
- Fault Tolerance: If a job fails, the `RetryPolicy` dictates the backoff. A `RetryAttempt` is generated and tracked until the job either succeeds or moves to a Dead Letter state.
- Centralized Auditing: The `LogEntry` table maintains optional foreign keys to `Job`, `Worker`, `Schedule`, and `RetryAttempt` for incredibly deep, interconnected audit trails across the system.
