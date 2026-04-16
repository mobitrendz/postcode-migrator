import asyncio
import pandas as pd
from sqlalchemy.ext.asyncio import create_async_engine

# Use the +psycopg dialect for Psycopg 3
DB_URL = "postgresql+psycopg://postgres:admin@localhost:5432/test_postcode"
CSV_FILE = "postcodes.csv"
CHUNK_SIZE = 5000  # Number of rows per chunk

async def migrate_data():
    # 1. Setup Async Engine
    engine = create_async_engine(DB_URL)
    
    first_chunk = True

    # 2. Read the CSV in chunks to save RAM
    # chunksize here returns an iterator
    reader = pd.read_csv(CSV_FILE, chunksize=CHUNK_SIZE)

    print(f"Starting chunked migration (Size: {CHUNK_SIZE})...")

    async with engine.begin() as conn:
        for i, df_chunk in enumerate(reader):
            # --- Processing Logic (Internal to each chunk) ---
            df_chunk = df_chunk[['id', 'postcode', 'locality', 'state', 'long', 'lat']]
            df_chunk = df_chunk[~df_chunk['locality'].str.endswith((' BC', ' DC', ' MC'))]
            df_chunk = df_chunk.drop_duplicates(subset=['postcode', 'locality'], keep='first')

            # --- Database Write ---
            # 'replace' for the first chunk to clear the table, 
            # 'append' for all subsequent chunks.
            mode = 'replace' if first_chunk else 'append'
            
            await conn.run_sync(
                lambda sync_conn: df_chunk.to_sql(
                    'postcodes', 
                    sync_conn, 
                    if_exists=mode, 
                    index=False,
                    method='multi' # Optional: speeds up inserts
                )
            )
            
            print(f"Processed chunk {i+1}...")
            first_chunk = False

    await engine.dispose()

if __name__ == "__main__":
    try:
        asyncio.run(migrate_data())
        print("Migration completed successfully.")
    except FileNotFoundError:
        print(f"Error: {CSV_FILE} not found.")
    except Exception as e:
        print(f"Error: {e}")