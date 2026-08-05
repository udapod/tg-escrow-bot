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