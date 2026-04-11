"""
CSV to PostgreSQL Migration Script using pandas and SQLModel

This module reads postcode data from a CSV file, performs data cleaning
and deduplication, and migrates the cleaned data to a PostgreSQL database.

Dependencies:
    - pandas: Data manipulation and CSV reading
    - sqlmodel: SQL database connection and ORM
    - psycopg2-binary: PostgreSQL database adapter

Data Processing Steps:
    1. Load postcode data from CSV
    2. Select relevant columns (id, postcode, locality, state, longitude, latitude)
    3. Filter out invalid entries (BC, DC, MC suffixes)
    4. Remove duplicate postcode-locality combinations
    5. Load cleaned data into PostgreSQL 'postcodes' table
"""
import pandas as pd
from sqlmodel import create_engine
from sqlalchemy.exc import SQLAlchemyError

def main():
    """
    Load, clean, and migrate postcode data to PostgreSQL.
    
    Process:
    - Reads postcodes.csv into a pandas DataFrame
    - Selects relevant columns for the database
    - Removes entries with locality names ending in ' BC', ' DC', or ' MC'
      (likely internal/administrative designations)
    - Deduplicates based on postcode and locality combinations
    - Loads cleaned data into 'postcodes' table (replacing if exists)
    - Prints row count of processed data
    
    Database Connection:
        PostgreSQL at localhost:5432
        Database: test_postcode
        User: postgres
        
    Raises:
        ConnectionError: If unable to connect to PostgreSQL database
        FileNotFoundError: If postcodes.csv not found
    """
    # Load data from CSV file
    df = pd.read_csv("postcodes.csv")

    # Select only relevant columns for the database
    df = df[['id', 'postcode', 'locality', 'state', 'long', 'lat']]

    # Filter out invalid locality designations
    # BC: Business Center, DC: Data Center, MC: Mail Center (internal designations)
    df = df[~df['locality'].str.endswith(' BC')]
    df = df[~df['locality'].str.endswith(' DC')]
    df = df[~df['locality'].str.endswith(' MC')]

    # Remove duplicate postcode-locality pairs, keeping the first occurrence
    df = df[~df.duplicated(subset=['postcode', 'locality'], keep='first')]

    # Display record count after processing
    print(f"Number of records after processing: {df.shape[0]}")

    # Create PostgreSQL database connection and load cleaned data
    engine = create_engine('postgresql://postgres:admin@localhost:5432/test_postcode')

    # Write DataFrame to database, replacing table if it already exists
    df.to_sql('postcodes', engine, if_exists='replace', index=False)

# This ensures that main() runs only when this script is executed directly, not when imported as a module
if __name__ == "__main__":
    try:
        print("Starting postcode data migration...")
        main()
        print("Postcode data migration completed successfully.")
    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure 'postcodes.csv' exists in the current directory.")
    except SQLAlchemyError as e:
        print(f"Database connection or processing error: {e}")    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

