# Component Overview

This document explains the major modules of the ingestion service.

## scheduler.py
Coordinates polling brokerage APIs for balances and trades and writes
results to the database.

## db.py
Defines the SQLAlchemy models and helper functions for inserting account
balances and trades.

## clients package
Contains one client per brokerage. Each client exposes asynchronous
methods `fetch_balance`, `fetch_trades`, and `close`.

## run_service.py
Bootstrap file that initializes the database engine, creates tables and
starts the scheduler.
