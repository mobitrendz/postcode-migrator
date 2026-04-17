import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
import pandas as pd

# Configurations
DB_URL = "postgresql+psycopg://postgres:admin@localhost:5432/test_postcode"
CSV_FILE = "postcodes.csv"
CHUNK_SIZE = 10000  # Increased for better throughput with 'multi'


async def migrate_data():
    # 1. Initialize Async Engine
    engine = create_async_engine(DB_URL, pool_size=10, max_overflow=20)

    # 2. Process CSV using a context manager for the reader
    # Using 'with' ensures the file handle is closed properly
    try:
        with pd.read_csv(CSV_FILE, chunksize=CHUNK_SIZE) as reader:
            print(f"Starting migration from {CSV_FILE}...")

            for i, df_chunk in enumerate(reader):
                # Data Cleaning (Chained for readability)
                cleaned_df = (
                    df_chunk[["id", "postcode", "locality", "state", "long", "lat"]]
                    .loc[~df_chunk["locality"].str.endswith((" BC", " DC", " MC"))]
                    .drop_duplicates(subset=["postcode", "locality"])
                )

                # Determine if we drop the table or append
                mode = "replace" if i == 0 else "append"

                # 3. Perform the database write in its own transaction per chunk
                async with engine.begin() as conn:
                    await conn.run_sync(
                        lambda sync_conn: cleaned_df.to_sql(
                            "postcodes",
                            sync_conn,
                            if_exists=mode,
                            index=False,
                            method="multi",  # Significant speed boost for Psycopg 3
                        )
                    )

                print(f"Processed chunk {i + 1} ({len(cleaned_df)} rows)")

    except FileNotFoundError:
        print(f"Error: {CSV_FILE} not found.")
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    # Standard entry point for async scripts
    try:
        asyncio.run(migrate_data())
        print("Migration completed successfully.")
    except KeyboardInterrupt:
        print("\nMigration interrupted by user.")
