# 📮 CSV to PostgreSQL - Postcode Migrator

An efficient, asynchronous Python utility designed to clean, deduplicate, and migrate large postcode datasets from CSV to PostgreSQL. Optimized for performance with chunked processing and batch inserts.

## 🚀 Features

- **Asynchronous Execution**: Leverages `asyncio` and `SQLAlchemy` (Async) for non-blocking database I/O.
- **High Performance**: Uses `psycopg 3` with `method='multi'` for rapid batch inserts.
- **Memory Efficient**: Processes data in configurable chunks (default: 10,000 rows) to handle massive CSV files.
- **Smart Data Cleaning**:
  - Filters out administrative designations (BC, DC, MC) from localities.
  - Ensures data integrity via postcode-locality deduplication.
- **Idempotent Start**: Automatically replaces the table on the first chunk and appends subsequent data.

## 🛠️ Prerequisites

- **Python 3.14+**
- **PostgreSQL** instance.
- **uv** (recommended) for modern dependency management.

## 📦 Dependencies

Managed via `pyproject.toml`:
- `pandas`: High-performance data manipulation.
- `sqlalchemy`: Async SQL toolkit and ORM.
- `psycopg[binary]`: Next-generation PostgreSQL adapter (v3).
- `sqlmodel`: Type-safe SQL interaction.

## 🖥️ Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mobitrendz/postcode-migrator.git
   cd postcode-migrator
   ```

2. **Prepare the Data:**
   Place your `postcodes.csv` file in the root directory.

3. **Install Dependencies:**
   ```bash
   uv sync
   ```

4. **Configure Database:**
   Update `DB_URL` in `migration_script.py` if needed:
   `postgresql+psycopg://<user>:<password>@localhost:5432/<database>`

5. **Run the Migration:**
   ```bash
   uv run migration_script.py
   ```

## 📖 Data Processing Logic

1. **Chunked Reader:** Reads the CSV using a context manager to ensure safe file handling.
2. **Cleaning Pipeline:**
   - Retains columns: `id`, `postcode`, `locality`, `state`, `long`, `lat`.
   - Filters localities ending with ` BC`, ` DC`, or ` MC`.
   - Drops duplicates on `['postcode', 'locality']`.
3. **Optimized Write:**
   - **Chunk 1:** `if_exists='replace'` to initialize schema.
   - **Chunk N:** `if_exists='append'`.
   - **Batching:** `method='multi'` significantly boosts throughput in Psycopg 3.

## 🛠️ Troubleshooting

| Issue | Potential Cause | Solution |
| :--- | :--- | :--- |
| **FileNotFoundError** | `postcodes.csv` missing. | Ensure the file is in the root directory. |
| **Connection Error** | Postgres not running. | Check your database service status. |
| **Auth Error** | Wrong credentials. | Update `DB_URL` in the script. |
| **Version Error** | Python < 3.14. | Upgrade to Python 3.14+ as required by `pyproject.toml`. |

## ✍️ Metadata

Updated by **Gemini CLI** on April 17, 2026.
Original by **Sreeraj Sreenivasan**.

## 🛡️ Disclaimer

This script is intended for educational and administrative purposes. Ensure your CSV source complies with data privacy standards before migration.
