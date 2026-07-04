# System Architecture

The following diagram illustrates the high-level architecture of the **Distributed Job Scheduler**. It showcases how the API, database, message broker, and various background workers interact to process jobs asynchronously.

```mermaid
flowchart TD
    %% Define Styles
    classDef client fill:#3b82f6,stroke:#1e40af,stroke-width:2px,color:#fff
    classDef api fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff
    classDef db fill:#f59e0b,stroke:#b45309,stroke-width:2px,color:#fff
    classDef broker fill:#ef4444,stroke:#b91c1c,stroke-width:2px,color:#fff
    classDef worker fill:#8b5cf6,stroke:#6d28d9,stroke-width:2px,color:#fff

    %% Nodes
    Client["Client App / Swagger UI"]:::client
    API["Django REST API<br/>(Gunicorn / WSGI)"]:::api
    
    DB[("PostgreSQL 16<br/>(Jobs, Queues, Logs)")]:::db
    Redis[("Redis<br/>(Celery Broker)")]:::broker
    
    CustomWorker["Custom DB Worker<br/>(manage.py runworker)"]:::worker
    CeleryWorker["Celery Worker<br/>(Executes Tasks)"]:::worker
    CeleryBeat["Celery Beat<br/>(Cron Scheduler)"]:::worker

    %% Connections
    Client -- "HTTP Requests (JWT Auth)" --> API
    
    API -- "Read/Write Jobs & Queues" --> DB
    
    CustomWorker -- "1. Polls highest priority queues<br/>(SELECT FOR UPDATE SKIP LOCKED)" --> DB
    CustomWorker -- "2. Dispatches task ID" --> Redis
    
    CeleryBeat -- "Schedules recurring jobs" --> DB
    CeleryBeat -- "Wakes up workers" --> Redis
    
    Redis -- "3. Consumes task ID" --> CeleryWorker
    CeleryWorker -- "4. Updates status & result" --> DB
    
    %% Subgraphs for organization
    subgraph "Web Layer"
        Client
        API
    end
    
    subgraph "Data Layer"
        DB
        Redis
    end
    
    subgraph "Execution Layer"
        CustomWorker
        CeleryWorker
        CeleryBeat
    end
```

### Component Breakdown
1. **Client / Web Layer**: Users interact with the system via JWT-authenticated API requests to create Projects, Queues, and Jobs.
2. **PostgreSQL**: Acts as the central source of truth. It stores all hierarchical data, job metadata, schedules, and logs. `SELECT FOR UPDATE SKIP LOCKED` ensures job claiming is highly concurrent and atomic.
3. **Custom DB Worker**: A persistent background process that polls PostgreSQL based on queue priority, atomically claims jobs, and pushes their IDs to the Celery broker.
4. **Redis**: The fast, in-memory message broker that queues the actual execution commands for Celery.
5. **Celery Worker**: Consumes the dispatched tasks from Redis, executes the actual job payloads, and writes the `result` and `status` (`completed`, `failed`) back to PostgreSQL.
6. **Celery Beat**: A periodic scheduler that reads from the database schedules and triggers recurring cron jobs automatically.
