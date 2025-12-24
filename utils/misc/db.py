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


async def get_lang(user_id: int):
    async with pool.acquire() as conn:
        lang = await conn.fetchval("SELECT lang FROM leads WHERE id = $1;", user_id)
        return lang or "uz"



async def create_lead_1(user_id: int, tg_name: str, username: str, lang: str, tarif: str):
    async with pool.acquire() as conn:
        result = await conn.fetchval("""
            INSERT INTO leads (id, tg_name, username, lang, tarif)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (id) DO UPDATE
            SET name = EXCLUDED.name,
                username = EXCLUDED.username,
                lang = EXCLUDED.lang,
                tarif = EXCLUDED.tarif
            RETURNING id;
        """, user_id, tg_name, username, lang, tarif)
        print(f"User added or updated: {result}")
        return result


async def create_lead_2(user_id: int, real_name: str, number: str, business_type: str, lat: float, long: float):
    async with pool.acquire() as conn:
        result = await conn.fetchval("""
            UPDATE
                leads
            SET
                real_name = $2,
                phone_numbber = $3,
                business_type = $4,
                business_lat = $5,
                business_long = $6
            WHERE
                id = $1
            RETURNING real_name;
        """, user_id, real_name, number, business_type, lat, long)
        print(f"User updated fully: {result}")
        return result


async def get_lean_ids(batch_size: int = 30):
    offset = 0
    while True:
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT 
                    id
                FROM 
                    leads
                WHERE 
                    deleted_at IS NULL
                ORDER BY 
                    created_at
                LIMIT 
                    $1 
                OFFSET 
                    $2;
                """,
                batch_size,
                offset
            )

        if not rows:
            break

        # Faqat id larni ro'yxat qilib beradi
        yield [r['id'] for r in rows]

        offset += batch_size



async def delete_lead(user_id: int):
    try:
        async with pool.acquire() as conn:
            result = await conn.execute(
                "UPDATE leads SET deleted_at = NOW() WHERE id = $1;",
                user_id
            )
            print(f"lead o'chirildi: {result}")
    except Exception as e:
        print(f"Xatolik (delete_lead): {e}")


