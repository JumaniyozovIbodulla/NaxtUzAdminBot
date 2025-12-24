import asyncpg
from data.config import DB_URL

pool: asyncpg.Pool = None

async def create_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            dsn=DB_URL, 
            min_size=1,
            max_size=100
        )

        print("Database pool created successfully")

# create tables 
async def create_tables_if_not_exist():
    async with pool.acquire() as conn:
        await conn.execute("""      
   
        CREATE TABLE IF NOT EXISTS leads (
            id BIGINT PRIMARY KEY,
            tg_name VARCHAR(200) NOT NULL,
            username VARCHAR(40) DEFAULT '',
            lang VARCHAR(10) NOT NULL,
            tarif VARCHAR(100) NOT NULL,
            real_name VARCHAR(100) DEFAULT '',
            phone_numbber VARCHAR(100) DEFAULT '',       
            business_type VARCHAR(100) DEFAULT '',
            business_lat NUMERIC(5,2) DEFAULT 0,
            business_long NUMERIC(5,2) DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            deleted_at TIMESTAMPTZ);
        """)

        print("Tables are created or already exist")

