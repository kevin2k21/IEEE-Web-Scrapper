import asyncio
import os
import sys
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

async def main():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not set in .env")
        return
        
    print(f"Connecting to: {db_url.split('@')[-1]}")
    engine = create_async_engine(db_url)
    
    try:
        async with engine.connect() as conn:
            print("Wiping the public schema (dropping all tables)...")
            # Drop the public schema cascade and recreate it to completely reset the DB
            await conn.execute(text("DROP SCHEMA public CASCADE;"))
            await conn.execute(text("CREATE SCHEMA public;"))
            await conn.execute(text("GRANT ALL ON SCHEMA public TO postgres;"))
            await conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
            await conn.commit()
            print("Database public schema wiped clean successfully!")
    except Exception as e:
        print(f"Error wiping database: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
