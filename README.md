# Data Ingestion Service

This service polls brokerage APIs to store balances and trades into PostgreSQL.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set environment variables for tokens and database URL:

```bash
export TOS_TOKEN=token
export SCHWAB_TOKEN=token
export ROBINHOOD_TOKEN=token
export WEBULL_TOKEN=token
export DB_URL=postgresql+asyncpg://user:pass@localhost/db
```

Run the service:

```bash
python -m src.run_service
```

## Docker

```bash
docker build -t ingestion .
docker run -e TOS_TOKEN=token -e SCHWAB_TOKEN=token \
  -e ROBINHOOD_TOKEN=token -e WEBULL_TOKEN=token \
  -e DB_URL=postgresql+asyncpg://user:pass@host/db ingestion
```

### Example HTTP call

```bash
curl -X POST http://localhost:8000/start
```

This is a placeholder for starting the service if an HTTP endpoint is added.
