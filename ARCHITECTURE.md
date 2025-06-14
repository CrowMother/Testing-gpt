# Architecture Overview

```
Scheduler
  -> ThinkOrSwimClient
  -> CharlesSchwabClient
  -> RobinhoodClient
  -> WebullClient
Database (PostgreSQL via async SQLAlchemy)
```

The scheduler polls each brokerage API every 5 seconds using asynchronous
clients. Responses are stored into `account_balances` and `trades` tables.
Each client returns only new trades based on the last seen trade identifier.
