# Postcode Migrator

Efficiently migrates postcode data from CSV to PostgreSQL using asynchronous processing and batch inserts.

## Tech Stack
- **Language:** Python 3.14+
- **Data Processing:** `pandas`
- **Database:** `PostgreSQL` via `SQLAlchemy` (Async) and `psycopg` (v3)
- **Environment Management:** `uv`

## Core Migration Logic (`migration_script.py`)
- **Async Processing:** Utilizes `asyncio` and `create_async_engine` for non-blocking database operations.
- **Chunked Reading:** Reads `postcodes.csv` in chunks (default: 10,000) to manage memory efficiency.
- **Data Cleaning:**
  - Selects specific columns: `id`, `postcode`, `locality`, `state`, `long`, `lat`.
  - Filters out localities ending with ` BC`, ` DC`, or ` MC`.
  - Removes duplicates based on `postcode` and `locality`.
- **Database Write:**
  - Uses `replace` mode for the first chunk to initialize the table.
  - Uses `append` mode for subsequent chunks.
  - Employs `method='multi'` for optimized `psycopg 3` performance.

## Configuration
- **DB_URL:** `postgresql+psycopg://postgres:admin@localhost:5432/test_postcode`
- **Source:** `postcodes.csv`
- **Chunk Size:** 10,000

## How to Run
```bash
uv run migration_script.py
```

## Architectural Guidelines
- **Maintain Async Integrity:** Ensure all database interactions remain asynchronous.
- **Memory Efficiency:** Always process CSV data in chunks to handle large datasets.
- **Idempotency:** The script replaces the table on the first chunk, ensuring a clean state per run.
