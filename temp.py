
import pandas as pd
from sqlmodel import create_engine
from sqlalchemy.exc import SQLAlchemyError

def main():
   
    # Load data from CSV file
    df = pd.read_csv("postcodes.csv")

    # Select only relevant columns for the database
    df = df[['id', 'postcode', 'locality', 'state', 'long', 'lat']]

    # Filter out invalid locality designations
    # BC: Business Center, DC: Delivery Center, MC: Mail Center (internal designations)
    df = df[~df['locality'].str.endswith((' BC', ' DC', ' MC'))]

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
        print("✅Postcode data migration completed successfully.")
    except FileNotFoundError as e:
        print(f"❌Error: {e}. Please ensure 'postcodes.csv' exists in the current directory.")
    except SQLAlchemyError as e:
        print(f"Database connection or processing error: {e}")    
    except Exception as e:
        print(f"❌An unexpected error occurred: {e}")
