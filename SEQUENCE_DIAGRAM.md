# Sequence Diagram

The following diagram illustrates the flow of a job from creation to execution and logging:

```text
User
  |
POST /jobs/
  |
Django API
  |
Save Job
  |
PostgreSQL
  |
Worker polls
  |
Execute Job
  |
Update Status
  |
Create Log
```
