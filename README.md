# 📮 CSV to PostgreSQL Postcode Migrator

A robust Python utility designed to clean, deduplicate, and migrate Australian postcode data from a CSV source into a PostgreSQL database. This script leverages **Pandas** for high-performance data manipulation and **SQLModel** for seamless database integration.

## 🚀 Features

- **Data Cleaning**: Automatically filters out administrative designations (BC, DC, MC) from localities.
- **Smart Deduplication**: Ensures data integrity by removing duplicate postcode-locality combinations.
- **Optimized Migration**: Uses SQLAlchemy-based engines to handle bulk data transfers to PostgreSQL.
- **Error Handling**: Provides clear feedback for missing files or database connection failures.

## 🛠️ Prerequisites

- **Python 3.x**
- **PostgreSQL** instance running locally or remotely.
- **uv** (recommended) or `pip` for dependency management.

## 📦 Dependencies

The script requires the following Python libraries:
- `pandas`: For data cleaning and filtering.
- `sqlmodel`: For database connection and ORM logic.
- `psycopg2-binary`: The PostgreSQL adapter for Python.

## 🖥️ Usage

1. **Clone the repository and navigate to the folder:**

```bash
git clone https://github.com/mobitrendz/postcode-migrator.git
cd postcode-migrator
```

2. **CPlace your data source:**
Ensure the australian_postcodes.csv file is located in the root directory.

3. **CInitialize the environment & install dependencies:**C


```bash
uv sync
```

4. **CConfigure the Database Connection:**

Update the connection string in main() if your credentials differ:
postgresql://<user>:<password>@localhost:5432/<database>

5. **CRun the migration:**

```bash
uv run python migration_script.py
```

## 📖 Data Processing Logic

The script performs the following transformations:
1. **Column Selection:** Retains only `id`, `postcode`, locality, state, long, and lat.
2. **Administrative Filtering:** Removes localities ending in **BC** (Business Centre), **DC** (Distribution Centre), or **MC** (Mail Centre).
3. **Deduplication:** Removes redundant rows where the postcode and locality pair are identical.
4. **Database Load:** Transfers the final DataFrame to the postcodes table using the replace method to ensure a fresh dataset.

## 🛠️ Troubleshooting

| Issue | Potential Cause | Solution |
| :--- | :--- | :--- |
| **FileNotFoundError** | `australian_postcodes.csv` is missing. | Place the CSV in the script's root folder. |
| **Connection Error** | PostgreSQL service is not running. | Start your local PostgreSQL server. |
| **Authentication Error** | Wrong username or password. | Update the connection string in the script. |
| **ModuleNotFoundError** | Dependencies not synced. | Run `uv sync` or `pip install pandas sqlmodel psycopg2-binary`. |

## ✍️ Metadata

Created by **Sreeraj Sreenivasan** on April 12, 2026

## 🛡️ Disclaimer

This script is intended for **educational and administrative purposes**. Ensure you have the necessary permissions to write to the target database and that your CSV source complies with data privacy standards.
