import asyncio
import asyncpg
import os

_pool = None
_lock = asyncio.Lock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    language TEXT DEFAULT 'en',
    country TEXT,
    city TEXT,
    wallet_trc20 TEXT,
    wallet_ltc TEXT,
    is_banned BOOLEAN DEFAULT FALSE,
    is_vip BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS listings (
    id BIGSERIAL PRIMARY KEY,
    seller_id BIGINT,
    title TEXT,
    description TEXT,
    category TEXT,
    currency TEXT,
    price NUMERIC(30,8),
    location TEXT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS deals (
    id BIGSERIAL PRIMARY KEY,
    external_id TEXT UNIQUE,
    listing_id BIGINT,
    buyer_id BIGINT,
    seller_id BIGINT,
    currency TEXT,
    amount NUMERIC(30,8),
    tx_hash TEXT,
    status TEXT DEFAULT 'pending_payment',
    dispute BOOLEAN DEFAULT FALSE,
    payload JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reviews (
    id BIGSERIAL PRIMARY KEY,
    deal_id BIGINT,
    from_id BIGINT,
    to_id BIGINT,
    stars INT CHECK (stars >= 1 AND stars <= 5),
    review TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS disputes (
    id BIGSERIAL PRIMARY KEY,
    deal_id BIGINT,
    opened_by BIGINT,
    reason TEXT,
    status TEXT DEFAULT 'open',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_listings_seller ON listings(seller_id);
CREATE INDEX IF NOT EXISTS idx_listings_active ON listings(active);
CREATE INDEX IF NOT EXISTS idx_deals_buyer ON deals(buyer_id);
CREATE INDEX IF NOT EXISTS idx_deals_seller ON deals(seller_id);
CREATE INDEX IF NOT EXISTS idx_deals_status ON deals(status);
CREATE INDEX IF NOT EXISTS idx_deals_currency ON deals(currency);
CREATE UNIQUE INDEX IF NOT EXISTS idx_deals_currency_tx ON deals(currency, tx_hash) WHERE tx_hash IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_reviews_to ON reviews(to_id);
CREATE INDEX IF NOT EXISTS idx_disputes_deal ON disputes(deal_id);
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
        return await conn.fetch(query, *args)


async def fetchrow(query: str, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, *args)


async def fetchval(query: str, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchval(query, *args)


async def execute(query: str, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.execute(query, *args)