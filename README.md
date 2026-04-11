## CSV to PostgreSQL Migration using pandas and SQLModel

This is a Python script that processes postcode data and migrates it to PostgreSQL.

- CSV source - https://github.com/matthewproctor/australianpostcodes

**Purpose:** Load, clean, and deduplicate postcode data from a CSV file, then store it in a PostgreSQL database.

**Key Processing Steps:**
1. Loads postcode data from australian_postcodes.csv
2. Selects relevant columns: id, postcode, locality, state, longitude, latitude
3. Filters out invalid entries (those ending with ' BC', ' DC', or ' MC')
4. Removes duplicate postcode-locality combinations
5. Loads cleaned data into PostgreSQL `postcodes` table

**Dependencies:**
- `pandas` — Data manipulation and CSV reading
- `sqlmodel` — SQL database ORM
- `psycopg2-binary` — PostgreSQL adapter

**Database Config:**
- Host: localhost:5432
- Database: test_postcode
- User: postgres
