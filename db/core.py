import asyncio
import asyncpg
import os

_pool = None
_lock = asyncio.Lock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    full_name TEXT,
    wallet TEXT DEFAULT '',
    lang TEXT DEFAULT 'en',
    country TEXT DEFAULT '',
    city TEXT DEFAULT '',
    rating REAL DEFAULT 5.0,
    deals_count INTEGER DEFAULT 0,
    registered_at TIMESTAMPTZ DEFAULT NOW(),
    is_banned INTEGER DEFAULT 0,
    referred_by BIGINT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS listings (
    id SERIAL PRIMARY KEY,
    seller_id BIGINT NOT NULL,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    photo_id TEXT DEFAULT '',
    country TEXT DEFAULT '',
    city TEXT DEFAULT '',
    currency TEXT DEFAULT 'USDT',
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS deals (
    id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL,
    seller_id BIGINT NOT NULL,
    buyer_id BIGINT NOT NULL,
    amount REAL NOT NULL,
    commission REAL NOT NULL DEFAULT 0,
    total_escrow REAL NOT NULL DEFAULT 0,
    seller_wallet TEXT NOT NULL,
    buyer_tx_hash TEXT DEFAULT '',
    status TEXT DEFAULT 'created',
    currency TEXT DEFAULT 'USDT',
    delivered_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    deal_id INTEGER NOT NULL,
    reviewer_id BIGINT NOT NULL,
    target_id BIGINT NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    comment TEXT DEFAULT '',
    photo_id TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vip_subscriptions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    tx_hash TEXT DEFAULT '',
    amount REAL NOT NULL,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    is_active INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS deal_messages (
    id SERIAL PRIMARY KEY,
    deal_id INTEGER NOT NULL,
    sender_id BIGINT NOT NULL,
    role TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS support_messages (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    username TEXT DEFAULT '',
    full_name TEXT DEFAULT '',
    message TEXT NOT NULL,
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS favorites (
    user_id BIGINT NOT NULL,
    seller_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, seller_id)
);



CREATE TABLE IF NOT EXISTS group_deals (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL UNIQUE,
    seller_id BIGINT,
    seller_wallet TEXT,
    buyer_id BIGINT,
    buyer_wallet TEXT,
    currency TEXT,
    status TEXT DEFAULT 'setup',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bot_admins (
    user_id BIGINT PRIMARY KEY,
    added_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS review_prompts (
    chat_id BIGINT PRIMARY KEY,
    message_id BIGINT NOT NULL,
    buyer_id BIGINT,
    seller_id BIGINT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

def _database_url():
    url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is missing")
    return url

async def get_pool():
    global _pool
    async with _lock:
        if _pool is None:
            _pool = await asyncpg.create_pool(
                _database_url(),
                ssl="require",
                min_size=1,
                max_size=5,
                command_timeout=60,
            )
    return _pool

async def init_db():
    pool = await get_pool()
    async with pool.acquire() as conn:
        for statement in SCHEMA.split(";"):
            statement = statement.strip()
            if statement:
                await conn.execute(statement)

async def fetch(query: str, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *args)
        return [dict(r) for r in rows]

async def fetchrow(query: str, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, *args)
        return dict(row) if row else None

async def fetchval(query: str, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchval(query, *args)

async def execute(query: str, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.execute(query, *args)