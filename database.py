from db.core import init_db, fetch, fetchrow, fetchval, execute, get_pool

# Expose init_db so api/index.py can call it
init_db = init_db

# ————— Пользователи —————

async def get_user(user_id: int) -> dict | None:
    return await fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)

async def register_user(user_id: int, username: str, full_name: str, referred_by: int = 0):
    await execute(
        "INSERT INTO users (user_id, username, full_name, referred_by) VALUES ($1, $2, $3, $4) ON CONFLICT (user_id) DO NOTHING",
        user_id, username, full_name, referred_by,
    )

async def update_wallet(user_id: int, wallet: str):
    await execute("UPDATE users SET wallet = $1 WHERE user_id = $2", wallet, user_id)

async def get_user_lang(user_id: int) -> str:
    row = await fetchval("SELECT lang FROM users WHERE user_id = $1", user_id)
    return row if row else "ru"

async def set_user_lang(user_id: int, lang: str):
    await execute("UPDATE users SET lang = $1 WHERE user_id = $2", lang, user_id)

async def set_user_location(user_id: int, country: str, city: str):
    await execute("UPDATE users SET country = $1, city = $2 WHERE user_id = $3", country, city, user_id)

async def get_user_location(user_id: int) -> tuple[str, str]:
    row = await fetchrow("SELECT country, city FROM users WHERE user_id = $1", user_id)
    if row:
        return (row.get("country") or "", row.get("city") or "")
    return ("", "")

async def update_user_rating(user_id: int):
    avg = await fetchval("SELECT AVG(rating) FROM reviews WHERE target_id = $1", user_id)
    if avg is None:
        avg = 5.0
    await execute("UPDATE users SET rating = $1 WHERE user_id = $2", round(avg, 2), user_id)

async def ban_user(user_id: int, ban: bool = True):
    await execute("UPDATE users SET is_banned = $1 WHERE user_id = $2", int(ban), user_id)


# ————— Объявления —————

async def create_listing(seller_id: int, category: str, title: str, description: str, price: float, photo_id: str = "", country: str = "", city: str = "", currency: str = "USDT") -> int:
    return await fetchval(
        "INSERT INTO listings (seller_id, category, title, description, price, photo_id, country, city, currency) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING id",
        seller_id, category, title, description, price, photo_id, country, city, currency,
    )

async def get_listing(listing_id: int) -> dict | None:
    return await fetchrow("SELECT * FROM listings WHERE id = $1", listing_id)

async def get_active_listings(category: str | None = None, country: str = "", city: str = "", limit: int = 20, offset: int = 0) -> list[dict]:
    where = ["is_active = 1"]
    params = []
    
    if category:
        params.append(category)
        where.append(f"category = ${len(params)}")
    if country:
        params.append(country)
        where.append(f"country = ${len(params)}")
    if city:
        params.append(city)
        where.append(f"city = ${len(params)}")
        
    params.append(limit)
    limit_idx = len(params)
    params.append(offset)
    offset_idx = len(params)
    
    sql = f"SELECT * FROM listings WHERE {' AND '.join(where)} ORDER BY created_at DESC LIMIT ${limit_idx} OFFSET ${offset_idx}"
    return await fetch(sql, *params)

async def search_listings(query: str, limit: int = 100) -> list[dict]:
    pattern = f"%{query}%"
    return await fetch(
        "SELECT * FROM listings WHERE is_active = 1 AND (title LIKE $1 OR description LIKE $2) ORDER BY created_at DESC LIMIT $3",
        pattern, pattern, limit,
    )

async def get_user_listings(user_id: int) -> list[dict]:
    return await fetch("SELECT * FROM listings WHERE seller_id = $1 ORDER BY created_at DESC", user_id)

async def deactivate_listing(listing_id: int):
    await execute("UPDATE listings SET is_active = 0 WHERE id = $1", listing_id)

async def activate_listing(listing_id: int):
    await execute("UPDATE listings SET is_active = 1 WHERE id = $1", listing_id)


# ————— Сделки —————

async def is_tx_hash_used(tx_hash: str) -> bool:
    count = await fetchval("SELECT COUNT(*) FROM deals WHERE buyer_tx_hash = $1 AND status NOT IN ('cancelled')", tx_hash)
    return count > 0

async def create_deal_atomic(listing_id: int, seller_id: int, buyer_id: int,
                             amount: float, commission: float,
                             total_escrow: float, seller_wallet: str, currency: str = None) -> int | None:
    if amount <= 0 or commission < 0 or total_escrow <= 0:
        return None
        
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            row = await conn.fetchrow("SELECT is_active, currency FROM listings WHERE id = $1 FOR UPDATE", listing_id)
            if not row or not row['is_active']:
                return None
                
            if currency is None:
                currency = row['currency'] or 'USDT'
                
            await conn.execute("UPDATE listings SET is_active = 0 WHERE id = $1", listing_id)
            
            deal_id = await conn.fetchval(
                """INSERT INTO deals 
                   (listing_id, seller_id, buyer_id, amount, commission, total_escrow, seller_wallet, currency) 
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id""",
                listing_id, seller_id, buyer_id, amount, commission, total_escrow, seller_wallet, currency
            )
            return deal_id

async def create_deal(listing_id: int, seller_id: int, buyer_id: int, amount: float, commission: float, total_escrow: float, seller_wallet: str, currency: str = "USDT") -> int:
    return await fetchval(
        "INSERT INTO deals (listing_id, seller_id, buyer_id, amount, commission, total_escrow, seller_wallet, currency) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id",
        listing_id, seller_id, buyer_id, amount, commission, total_escrow, seller_wallet, currency,
    )

async def get_deal(deal_id: int) -> dict | None:
    return await fetchrow("SELECT * FROM deals WHERE id = $1", deal_id)

async def update_deal_status(deal_id: int, status: str):
    await execute("UPDATE deals SET status = $1, updated_at = NOW() WHERE id = $2", status, deal_id)

async def set_buyer_tx_hash(deal_id: int, tx_hash: str):
    await execute("UPDATE deals SET buyer_tx_hash = $1, updated_at = NOW() WHERE id = $2", tx_hash, deal_id)

async def mark_delivered(deal_id: int):
    await execute("UPDATE deals SET status = 'delivered', delivered_at = NOW(), updated_at = NOW() WHERE id = $1", deal_id)

async def get_active_escrow_deals() -> list[dict]:
    return await fetch("SELECT * FROM deals WHERE status IN ('paid', 'delivered', 'disputed') ORDER BY updated_at DESC")

async def get_expired_delivered_deals(hours: int) -> list[dict]:
    return await fetch(
        "SELECT * FROM deals WHERE status = 'delivered' AND delivered_at IS NOT NULL AND delivered_at + (interval '1 hour' * $1) <= NOW()",
        hours,
    )

async def get_user_deals(user_id: int) -> list[dict]:
    return await fetch("SELECT * FROM deals WHERE seller_id = $1 OR buyer_id = $1 ORDER BY created_at DESC", user_id)

async def increment_deals_count(user_id: int):
    await execute("UPDATE users SET deals_count = deals_count + 1 WHERE user_id = $1", user_id)


# ————— Отзывы —————

async def create_review(deal_id: int, reviewer_id: int, target_id: int, rating: int, comment: str = "", photo_id: str = ""):
    await execute(
        "INSERT INTO reviews (deal_id, reviewer_id, target_id, rating, comment, photo_id) VALUES ($1, $2, $3, $4, $5, $6)",
        deal_id, reviewer_id, target_id, rating, comment, photo_id,
    )
    await update_user_rating(target_id)

async def get_user_reviews(user_id: int) -> list[dict]:
    return await fetch("SELECT * FROM reviews WHERE target_id = $1 ORDER BY created_at DESC", user_id)


# ————— VIP-подписка —————

async def create_vip_subscription(user_id: int, amount: float, days: int) -> int:
    return await fetchval(
        "INSERT INTO vip_subscriptions (user_id, amount, expires_at) VALUES ($1, $2, NOW() + (interval '1 day' * $3)) RETURNING id",
        user_id, amount, days,
    )

async def activate_vip(sub_id: int, tx_hash: str):
    # Defaulting to 30 days if days aren't strictly stored in the schema
    await execute(
        "UPDATE vip_subscriptions SET is_active = 1, tx_hash = $1, started_at = NOW(), expires_at = NOW() + interval '30 days' WHERE id = $2",
        tx_hash, sub_id,
    )

async def activate_vip_simple(sub_id: int, tx_hash: str, days: int):
    await execute(
        "UPDATE vip_subscriptions SET is_active = 1, tx_hash = $1, started_at = NOW(), expires_at = NOW() + (interval '1 day' * $2) WHERE id = $3",
        tx_hash, days, sub_id,
    )

async def is_vip(user_id: int) -> bool:
    count = await fetchval("SELECT COUNT(*) FROM vip_subscriptions WHERE user_id = $1 AND is_active = 1 AND expires_at > NOW()", user_id)
    return count > 0

async def get_vip_info(user_id: int) -> dict | None:
    return await fetchrow(
        "SELECT * FROM vip_subscriptions WHERE user_id = $1 AND is_active = 1 AND expires_at > NOW() ORDER BY expires_at DESC LIMIT 1",
        user_id,
    )

async def get_pending_vip(user_id: int) -> dict | None:
    return await fetchrow("SELECT * FROM vip_subscriptions WHERE user_id = $1 AND is_active = 0 ORDER BY id DESC LIMIT 1", user_id)

async def get_vip_stats() -> dict:
    active_vips = await fetchval("SELECT COUNT(*) FROM vip_subscriptions WHERE is_active = 1 AND expires_at > NOW()")
    total_vip_revenue = await fetchval("SELECT COALESCE(SUM(amount), 0) FROM vip_subscriptions WHERE is_active = 1")
    return {"active_vips": active_vips or 0, "total_vip_revenue": round(total_vip_revenue or 0, 2)}


# ————— Статистика (для админа) —————

async def get_stats() -> dict:
    users_count = await fetchval("SELECT COUNT(*) FROM users") or 0
    active_listings = await fetchval("SELECT COUNT(*) FROM listings WHERE is_active = 1") or 0
    total_deals = await fetchval("SELECT COUNT(*) FROM deals") or 0
    completed_deals = await fetchval("SELECT COUNT(*) FROM deals WHERE status = 'completed'") or 0
    total_commission = await fetchval("SELECT COALESCE(SUM(commission), 0) FROM deals WHERE status = 'completed'") or 0
    frozen_funds = await fetchval("SELECT COALESCE(SUM(total_escrow), 0) FROM deals WHERE status IN ('paid', 'delivered', 'disputed')") or 0
    active_disputes = await fetchval("SELECT COUNT(*) FROM deals WHERE status = 'disputed'") or 0

    return {
        "users": users_count, "active_listings": active_listings, "total_deals": total_deals,
        "completed_deals": completed_deals, "total_commission": round(total_commission, 2),
        "frozen_funds": round(frozen_funds, 2), "active_disputes": active_disputes,
    }


# ————— Чат сделки —————

async def save_deal_message(deal_id: int, sender_id: int, role: str, text: str):
    await execute("INSERT INTO deal_messages (deal_id, sender_id, role, text) VALUES ($1, $2, $3, $4)", deal_id, sender_id, role, text)

async def get_deal_messages(deal_id: int) -> list[dict]:
    return await fetch("SELECT * FROM deal_messages WHERE deal_id = $1 ORDER BY created_at ASC", deal_id)

async def get_active_deal_between(buyer_id: int, seller_id: int) -> dict | None:
    return await fetchrow(
        "SELECT * FROM deals WHERE buyer_id = $1 AND seller_id = $2 AND status IN ('created', 'paid', 'delivered', 'disputed') ORDER BY created_at DESC LIMIT 1",
        buyer_id, seller_id,
    )


# ————— Удаление аккаунта —————

async def has_active_deals(user_id: int) -> bool:
    count = await fetchval(
        "SELECT COUNT(*) FROM deals WHERE (seller_id = $1 OR buyer_id = $1) AND status IN ('created', 'paid', 'delivered', 'disputed')",
        user_id,
    )
    return count > 0

async def delete_user_account(user_id: int):
    await execute("UPDATE listings SET is_active = 0 WHERE seller_id = $1", user_id)
    await execute("DELETE FROM vip_subscriptions WHERE user_id = $1", user_id)
    await execute("DELETE FROM support_messages WHERE user_id = $1", user_id)
    await execute("DELETE FROM users WHERE user_id = $1", user_id)


# ————— Поддержка (support) —————

async def save_support_message(user_id: int, username: str, full_name: str, message_text: str):
    await execute("INSERT INTO support_messages (user_id, username, full_name, message) VALUES ($1, $2, $3, $4)", user_id, username, full_name, message_text)

async def get_support_messages(limit: int = 20) -> list[dict]:
    return await fetch("SELECT * FROM support_messages ORDER BY created_at DESC LIMIT $1", limit)

async def get_unread_support_count() -> int:
    return await fetchval("SELECT COUNT(*) FROM support_messages WHERE is_read = 0") or 0

async def mark_support_read():
    await execute("UPDATE support_messages SET is_read = 1 WHERE is_read = 0")

async def cleanup_old_data():
    await execute("DELETE FROM deal_messages WHERE created_at < NOW() - interval '90 days'")
    await execute("DELETE FROM support_messages WHERE created_at < NOW() - interval '30 days'")


# ————— Реферальная программа —————

async def get_referral_count(user_id: int) -> int:
    return await fetchval("SELECT COUNT(*) FROM users WHERE referred_by = $1", user_id) or 0

async def get_referral_active_count(user_id: int) -> int:
    return await fetchval("SELECT COUNT(*) FROM users WHERE referred_by = $1 AND deals_count > 0", user_id) or 0

async def get_referral_stats_admin() -> list[dict]:
    return await fetch(
        "SELECT u.user_id, u.full_name, COUNT(r.user_id) as ref_count FROM users u JOIN users r ON r.referred_by = u.user_id GROUP BY u.user_id, u.full_name ORDER BY ref_count DESC LIMIT 10"
    )


# ————— Избранное / подписка на продавца —————

async def add_favorite(user_id: int, seller_id: int):
    await execute("INSERT INTO favorites (user_id, seller_id) VALUES ($1, $2) ON CONFLICT DO NOTHING", user_id, seller_id)

async def remove_favorite(user_id: int, seller_id: int):
    await execute("DELETE FROM favorites WHERE user_id = $1 AND seller_id = $2", user_id, seller_id)

async def is_favorite(user_id: int, seller_id: int) -> bool:
    count = await fetchval("SELECT COUNT(*) FROM favorites WHERE user_id = $1 AND seller_id = $2", user_id, seller_id)
    return count > 0

async def get_favorites(user_id: int) -> list[dict]:
    return await fetch("SELECT u.* FROM favorites f JOIN users u ON u.user_id = f.seller_id WHERE f.user_id = $1 ORDER BY f.created_at DESC", user_id)

async def get_seller_followers(seller_id: int) -> list[int]:
    rows = await fetch("SELECT user_id FROM favorites WHERE seller_id = $1", seller_id)
    return [r["user_id"] for r in rows]

async def get_favorites_count(user_id: int) -> int:
    return await fetchval("SELECT COUNT(*) FROM favorites WHERE seller_id = $1", user_id) or 0