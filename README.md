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
export SCHWAB_CLIENT_ID=your_client_id
export SCHWAB_CLIENT_SECRET=your_client_secret
export ROBINHOOD_TOKEN=token
export WEBULL_TOKEN=token
export DB_URL=postgresql+asyncpg://user:password@localhost/db
```

### Schwab login

Generate a browser authorization URL and exchange the returned code for a token:

```python
from src.clients.schwab_api import CharlesSchwabClient

client = CharlesSchwabClient()
print(client.get_authorization_url("https://example.com/callback", "state123"))
# After redirect, call:
# await client.exchange_code(received_code, "https://example.com/callback")
```

Run the service:

```bash
python -m src.run_service
```

## Docker

```bash
docker build -t ingestion .
docker run -e TOS_TOKEN=token -e SCHWAB_TOKEN=token \
  -e SCHWAB_CLIENT_ID=your_client_id \
  -e SCHWAB_CLIENT_SECRET=your_client_secret \
  -e ROBINHOOD_TOKEN=token -e WEBULL_TOKEN=token \
  -e DB_URL=postgresql+asyncpg://user:password@host/db ingestion
```

### Example HTTP call

```bash
curl -X POST http://localhost:8000/start
```

This is a placeholder for starting the service if an HTTP endpoint is added.
