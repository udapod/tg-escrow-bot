import aiosqlite
from config import DB_PATH


async def init_db():
    """Инициализация базы данных — создание таблиц."""
    async with aiosqlite.connect(DB_PATH) as db:
        # WAL mode для лучшей concurrency + timeout при занятой БД
        await db.execute("PRAGMA journal_mode=WAL")
        await db.execute("PRAGMA busy_timeout=5000")

        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                wallet TEXT DEFAULT '',
                lang TEXT DEFAULT 'ru',
                country TEXT DEFAULT '',
                city TEXT DEFAULT '',
                rating REAL DEFAULT 5.0,
                deals_count INTEGER DEFAULT 0,
                registered_at TEXT DEFAULT (datetime('now')),
                is_banned INTEGER DEFAULT 0
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seller_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                photo_id TEXT DEFAULT '',
                country TEXT DEFAULT '',
                city TEXT DEFAULT '',
                currency TEXT DEFAULT 'USDT',
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (seller_id) REFERENCES users(user_id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS deals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id INTEGER NOT NULL,
                seller_id INTEGER NOT NULL,
                buyer_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                commission REAL NOT NULL DEFAULT 0,
                total_escrow REAL NOT NULL DEFAULT 0,
                seller_wallet TEXT NOT NULL,
                buyer_tx_hash TEXT DEFAULT '',
                status TEXT DEFAULT 'created',
                delivered_at TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (listing_id) REFERENCES listings(id),
                FOREIGN KEY (seller_id) REFERENCES users(user_id),
                FOREIGN KEY (buyer_id) REFERENCES users(user_id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deal_id INTEGER NOT NULL,
                reviewer_id INTEGER NOT NULL,
                target_id INTEGER NOT NULL,
                rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
                comment TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (deal_id) REFERENCES deals(id),
                FOREIGN KEY (reviewer_id) REFERENCES users(user_id),
                FOREIGN KEY (target_id) REFERENCES users(user_id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS vip_subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                tx_hash TEXT DEFAULT '',
                amount REAL NOT NULL,
                started_at TEXT DEFAULT (datetime('now')),
                expires_at TEXT NOT NULL,
                is_active INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS deal_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deal_id INTEGER NOT NULL,
                sender_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (deal_id) REFERENCES deals(id),
                FOREIGN KEY (sender_id) REFERENCES users(user_id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS support_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT DEFAULT '',
                full_name TEXT DEFAULT '',
                message TEXT NOT NULL,
                is_read INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                user_id INTEGER NOT NULL,
                seller_id INTEGER NOT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                PRIMARY KEY (user_id, seller_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (seller_id) REFERENCES users(user_id)
            )
        """)

        await db.commit()

    # — Миграции: добавляем новые колонки (безопасно для существующих БД) —
    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute("ALTER TABLE listings ADD COLUMN photo_id TEXT DEFAULT ''")
            await db.commit()
        except Exception:
            pass  # колонка уже существует
        try:
            await db.execute("ALTER TABLE users ADD COLUMN lang TEXT DEFAULT 'ru'")
            await db.commit()
        except Exception:
            pass
        for col in ("country", "city"):
            try:
                await db.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT DEFAULT ''")
                await db.commit()
            except Exception:
                pass
            try:
                await db.execute(f"ALTER TABLE listings ADD COLUMN {col} TEXT DEFAULT ''")
                await db.commit()
            except Exception:
                pass
        # Реферальная программа: кто пригласил пользователя
        try:
            await db.execute("ALTER TABLE users ADD COLUMN referred_by INTEGER DEFAULT 0")
            await db.commit()
        except Exception:
            pass
        # Фото-отзывы
        try:
            await db.execute("ALTER TABLE reviews ADD COLUMN photo_id TEXT DEFAULT ''")
            await db.commit()
        except Exception:
            pass


# ————— Пользователи —————

async def get_user(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def register_user(user_id: int, username: str, full_name: str, referred_by: int = 0):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, full_name, referred_by) VALUES (?, ?, ?, ?)",
            (user_id, username, full_name, referred_by),
        )
        await db.commit()


async def update_wallet(user_id: int, wallet: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET wallet = ? WHERE user_id = ?", (wallet, user_id))
        await db.commit()


async def get_user_lang(user_id: int) -> str:
    """Получить язык пользователя (ru/uz/kk)."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return row[0] if row and row[0] else "ru"


async def set_user_lang(user_id: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
        await db.commit()


async def set_user_location(user_id: int, country: str, city: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET country = ?, city = ? WHERE user_id = ?",
            (country, city, user_id),
        )
        await db.commit()


async def get_user_location(user_id: int) -> tuple[str, str]:
    """Возвращает (country, city) пользователя."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT country, city FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        if row:
            return (row[0] or "", row[1] or "")
        return ("", "")


async def update_user_rating(user_id: int):
    """Пересчитать рейтинг пользователя на основе отзывов."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT AVG(rating) FROM reviews WHERE target_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        avg = row[0] if row[0] is not None else 5.0
        await db.execute("UPDATE users SET rating = ? WHERE user_id = ?", (round(avg, 2), user_id))
        await db.commit()


async def ban_user(user_id: int, ban: bool = True):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET is_banned = ? WHERE user_id = ?", (int(ban), user_id))
        await db.commit()


# ————— Объявления —————

async def create_listing(seller_id: int, category: str, title: str, description: str, price: float, photo_id: str = "", country: str = "", city: str = "") -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO listings (seller_id, category, title, description, price, photo_id, country, city) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (seller_id, category, title, description, price, photo_id, country, city),
        )
        await db.commit()
        return cursor.lastrowid


async def get_listing(listing_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM listings WHERE id = ?", (listing_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def get_active_listings(category: str | None = None, country: str = "", city: str = "", limit: int = 20, offset: int = 0) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        where = ["is_active = 1"]
        params: list = []
        if category:
            where.append("category = ?")
            params.append(category)
        if country:
            where.append("country = ?")
            params.append(country)
        if city:
            where.append("city = ?")
            params.append(city)
        sql = f"SELECT * FROM listings WHERE {' AND '.join(where)} ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        cursor = await db.execute(sql, params)
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def search_listings(query: str, limit: int = 100) -> list[dict]:
    """Поиск объявлений по ключевым словам в названии и описании."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        pattern = f"%{query}%"
        cursor = await db.execute(
            "SELECT * FROM listings WHERE is_active = 1 "
            "AND (title LIKE ? OR description LIKE ?) "
            "ORDER BY created_at DESC LIMIT ?",
            (pattern, pattern, limit),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_user_listings(user_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM listings WHERE seller_id = ? ORDER BY created_at DESC", (user_id,)
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def deactivate_listing(listing_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE listings SET is_active = 0 WHERE id = ?", (listing_id,))
        await db.commit()


async def activate_listing(listing_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE listings SET is_active = 1 WHERE id = ?", (listing_id,))
        await db.commit()


# ————— Сделки —————

async def is_tx_hash_used(tx_hash: str) -> bool:
    """Проверка: использовался ли этот tx hash в другой сделке."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM deals WHERE buyer_tx_hash = ? AND status NOT IN ('cancelled')",
            (tx_hash,),
        )
        row = await cursor.fetchone()
        return row[0] > 0


async def create_deal_atomic(listing_id: int, seller_id: int, buyer_id: int,
                             amount: float, commission: float,
                             total_escrow: float, seller_wallet: str) -> int | None:
    """Атомарно создать сделку + деактивировать объявление (защита от double-buy).
    Возвращает deal_id или None если объявление уже неактивно."""
    if amount <= 0 or commission < 0 or total_escrow <= 0:
        return None
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("BEGIN IMMEDIATE")
        try:
            cursor = await db.execute(
                "SELECT is_active FROM listings WHERE id = ?", (listing_id,)
            )
            row = await cursor.fetchone()
            if not row or not row[0]:
                await db.execute("ROLLBACK")
                return None
            await db.execute(
                "UPDATE listings SET is_active = 0 WHERE id = ?", (listing_id,)
            )
            cursor = await db.execute(
                "INSERT INTO deals (listing_id, seller_id, buyer_id, amount, commission, total_escrow, seller_wallet) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (listing_id, seller_id, buyer_id, amount, commission, total_escrow, seller_wallet),
            )
            deal_id = cursor.lastrowid
            await db.commit()
            return deal_id
        except Exception:
            await db.execute("ROLLBACK")
            raise


async def create_deal(listing_id: int, seller_id: int, buyer_id: int, amount: float, commission: float, total_escrow: float, seller_wallet: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO deals (listing_id, seller_id, buyer_id, amount, commission, total_escrow, seller_wallet) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (listing_id, seller_id, buyer_id, amount, commission, total_escrow, seller_wallet),
        )
        await db.commit()
        return cursor.lastrowid


async def get_deal(deal_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM deals WHERE id = ?", (deal_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def update_deal_status(deal_id: int, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE deals SET status = ?, updated_at = datetime('now') WHERE id = ?",
            (status, deal_id),
        )
        await db.commit()


async def set_buyer_tx_hash(deal_id: int, tx_hash: str):
    """Сохранить хэш транзакции покупателя (отправка на эскроу)."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE deals SET buyer_tx_hash = ?, updated_at = datetime('now') WHERE id = ?",
            (tx_hash, deal_id),
        )
        await db.commit()


async def mark_delivered(deal_id: int):
    """Отметить сделку как доставленную и запустить таймер."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE deals SET status = 'delivered', delivered_at = datetime('now'), updated_at = datetime('now') WHERE id = ?",
            (deal_id,),
        )
        await db.commit()


async def get_active_escrow_deals() -> list[dict]:
    """Получить все сделки с замороженными средствами (эскроу)."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM deals WHERE status IN ('paid', 'delivered', 'disputed') ORDER BY updated_at DESC"
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_expired_delivered_deals(hours: int) -> list[dict]:
    """Сделки со статусом 'delivered', у которых прошло более N часов с delivered_at."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM deals WHERE status = 'delivered' AND delivered_at != '' AND datetime(delivered_at, '+' || ? || ' hours') <= datetime('now')",
            (hours,),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_user_deals(user_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM deals WHERE seller_id = ? OR buyer_id = ? ORDER BY created_at DESC",
            (user_id, user_id),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def increment_deals_count(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET deals_count = deals_count + 1 WHERE user_id = ?", (user_id,))
        await db.commit()


# ————— Отзывы —————

async def create_review(deal_id: int, reviewer_id: int, target_id: int, rating: int, comment: str = "", photo_id: str = ""):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO reviews (deal_id, reviewer_id, target_id, rating, comment, photo_id) VALUES (?, ?, ?, ?, ?, ?)",
            (deal_id, reviewer_id, target_id, rating, comment, photo_id),
        )
        await db.commit()
    await update_user_rating(target_id)


async def get_user_reviews(user_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM reviews WHERE target_id = ? ORDER BY created_at DESC", (user_id,)
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


# ————— VIP-подписка —————

async def create_vip_subscription(user_id: int, amount: float, days: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO vip_subscriptions (user_id, amount, expires_at) "
            "VALUES (?, ?, datetime('now', '+' || ? || ' days'))",
            (user_id, amount, days),
        )
        await db.commit()
        return cursor.lastrowid


async def activate_vip(sub_id: int, tx_hash: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE vip_subscriptions SET is_active = 1, tx_hash = ?, started_at = datetime('now'), "
            "expires_at = datetime('now', '+' || (SELECT ? FROM vip_subscriptions WHERE id = ?) || ' days') "
            "WHERE id = ?",
            (tx_hash, sub_id, sub_id, sub_id),
        )
        await db.commit()


async def activate_vip_simple(sub_id: int, tx_hash: str, days: int):
    """Активировать VIP-подписку — старт с текущего момента."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE vip_subscriptions SET is_active = 1, tx_hash = ?, "
            "started_at = datetime('now'), expires_at = datetime('now', '+' || ? || ' days') "
            "WHERE id = ?",
            (tx_hash, days, sub_id),
        )
        await db.commit()


async def is_vip(user_id: int) -> bool:
    """Проверяет, есть ли у пользователя активная VIP-подписка."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM vip_subscriptions "
            "WHERE user_id = ? AND is_active = 1 AND expires_at > datetime('now')",
            (user_id,),
        )
        count = (await cursor.fetchone())[0]
        return count > 0


async def get_vip_info(user_id: int) -> dict | None:
    """Получить текущую активную VIP-подписку."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM vip_subscriptions "
            "WHERE user_id = ? AND is_active = 1 AND expires_at > datetime('now') "
            "ORDER BY expires_at DESC LIMIT 1",
            (user_id,),
        )
        row = await cursor.fetchone()
        return dict(row) if row else None


async def get_pending_vip(user_id: int) -> dict | None:
    """Получить неоплаченную VIP-заявку."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM vip_subscriptions "
            "WHERE user_id = ? AND is_active = 0 "
            "ORDER BY id DESC LIMIT 1",
            (user_id,),
        )
        row = await cursor.fetchone()
        return dict(row) if row else None


async def get_vip_stats() -> dict:
    """Статистика VIP для админа."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur1 = await db.execute(
            "SELECT COUNT(*) FROM vip_subscriptions WHERE is_active = 1 AND expires_at > datetime('now')"
        )
        active_vips = (await cur1.fetchone())[0]

        cur2 = await db.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM vip_subscriptions WHERE is_active = 1"
        )
        total_vip_revenue = (await cur2.fetchone())[0]

        return {"active_vips": active_vips, "total_vip_revenue": round(total_vip_revenue, 2)}


# ————— Статистика (для админа) —————

async def get_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        cur1 = await db.execute("SELECT COUNT(*) FROM users")
        users_count = (await cur1.fetchone())[0]

        cur2 = await db.execute("SELECT COUNT(*) FROM listings WHERE is_active = 1")
        active_listings = (await cur2.fetchone())[0]

        cur3 = await db.execute("SELECT COUNT(*) FROM deals")
        total_deals = (await cur3.fetchone())[0]

        cur4 = await db.execute("SELECT COUNT(*) FROM deals WHERE status = 'completed'")
        completed_deals = (await cur4.fetchone())[0]

        cur5 = await db.execute("SELECT COALESCE(SUM(commission), 0) FROM deals WHERE status = 'completed'")
        total_commission = (await cur5.fetchone())[0]

        cur6 = await db.execute(
            "SELECT COALESCE(SUM(total_escrow), 0) FROM deals WHERE status IN ('paid', 'delivered', 'disputed')"
        )
        frozen_funds = (await cur6.fetchone())[0]

        cur7 = await db.execute("SELECT COUNT(*) FROM deals WHERE status = 'disputed'")
        active_disputes = (await cur7.fetchone())[0]

        return {
            "users": users_count,
            "active_listings": active_listings,
            "total_deals": total_deals,
            "completed_deals": completed_deals,
            "total_commission": round(total_commission, 2),
            "frozen_funds": round(frozen_funds, 2),
            "active_disputes": active_disputes,
        }


# ————— Чат сделки —————

async def save_deal_message(deal_id: int, sender_id: int, role: str, text: str):
    """Сохранить сообщение чата сделки. role = 'buyer' или 'seller'."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO deal_messages (deal_id, sender_id, role, text) VALUES (?, ?, ?, ?)",
            (deal_id, sender_id, role, text),
        )
        await db.commit()


async def get_deal_messages(deal_id: int) -> list[dict]:
    """Получить всю историю переписки по сделке."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM deal_messages WHERE deal_id = ? ORDER BY created_at ASC",
            (deal_id,),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_active_deal_between(buyer_id: int, seller_id: int) -> dict | None:
    """Найти активную сделку между покупателем и продавцом (для маршрутизации чата)."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM deals WHERE buyer_id = ? AND seller_id = ? "
            "AND status IN ('created', 'paid', 'delivered', 'disputed') "
            "ORDER BY created_at DESC LIMIT 1",
            (buyer_id, seller_id),
        )
        row = await cursor.fetchone()
        return dict(row) if row else None


# ————— Удаление аккаунта —————

async def has_active_deals(user_id: int) -> bool:
    """Проверить, есть ли у пользователя незавершённые сделки."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM deals WHERE (seller_id = ? OR buyer_id = ?) "
            "AND status IN ('created', 'paid', 'delivered', 'disputed')",
            (user_id, user_id),
        )
        count = (await cursor.fetchone())[0]
        return count > 0


async def delete_user_account(user_id: int):
    """Полное удаление аккаунта: профиль, объявления, VIP, обращения."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Деактивируем все объявления
        await db.execute("UPDATE listings SET is_active = 0 WHERE seller_id = ?", (user_id,))
        # Удаляем VIP-подписки
        await db.execute("DELETE FROM vip_subscriptions WHERE user_id = ?", (user_id,))
        # Удаляем обращения в поддержку
        await db.execute("DELETE FROM support_messages WHERE user_id = ?", (user_id,))
        # Удаляем пользователя
        await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        await db.commit()


# ————— Поддержка (support) —————

async def save_support_message(user_id: int, username: str, full_name: str, message_text: str):
    """Сохранить обращение в поддержку."""
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "INSERT INTO support_messages (user_id, username, full_name, message) VALUES (?, ?, ?, ?)",
            (user_id, username, full_name, message_text),
        )
        await conn.commit()


async def get_support_messages(limit: int = 20) -> list[dict]:
    """Получить последние обращения в поддержку."""
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(
            "SELECT * FROM support_messages ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_unread_support_count() -> int:
    """Количество непрочитанных обращений."""
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "SELECT COUNT(*) FROM support_messages WHERE is_read = 0"
        )
        return (await cursor.fetchone())[0]


async def mark_support_read():
    """Пометить все обращения как прочитанные."""
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("UPDATE support_messages SET is_read = 1 WHERE is_read = 0")
        await conn.commit()


async def cleanup_old_data():
    """Удалить старые чат-сообщения (>90 дней) и support-сообщения (>30 дней)."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM deal_messages WHERE created_at < datetime('now', '-90 days')"
        )
        await db.execute(
            "DELETE FROM support_messages WHERE created_at < datetime('now', '-30 days')"
        )
        await db.commit()


# ————— Реферальная программа —————

async def get_referral_count(user_id: int) -> int:
    """Сколько пользователей пригласил user_id."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM users WHERE referred_by = ?", (user_id,)
        )
        return (await cursor.fetchone())[0]


async def get_referral_active_count(user_id: int) -> int:
    """Сколько приглашённых совершили хотя бы 1 сделку."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM users WHERE referred_by = ? AND deals_count > 0",
            (user_id,),
        )
        return (await cursor.fetchone())[0]


async def get_referral_stats_admin() -> list[dict]:
    """Топ-10 рефереров для админа."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT u.user_id, u.full_name, COUNT(r.user_id) as ref_count "
            "FROM users u JOIN users r ON r.referred_by = u.user_id "
            "GROUP BY u.user_id ORDER BY ref_count DESC LIMIT 10"
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


# ————— Избранное / подписка на продавца —————

async def add_favorite(user_id: int, seller_id: int):
    """Подписаться на продавца."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO favorites (user_id, seller_id) VALUES (?, ?)",
            (user_id, seller_id),
        )
        await db.commit()


async def remove_favorite(user_id: int, seller_id: int):
    """Отписаться от продавца."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM favorites WHERE user_id = ? AND seller_id = ?",
            (user_id, seller_id),
        )
        await db.commit()


async def is_favorite(user_id: int, seller_id: int) -> bool:
    """Подписан ли user_id на seller_id."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM favorites WHERE user_id = ? AND seller_id = ?",
            (user_id, seller_id),
        )
        return (await cursor.fetchone())[0] > 0


async def get_favorites(user_id: int) -> list[dict]:
    """Список продавцов в избранном."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT u.* FROM favorites f JOIN users u ON u.user_id = f.seller_id "
            "WHERE f.user_id = ? ORDER BY f.created_at DESC",
            (user_id,),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_seller_followers(seller_id: int) -> list[int]:
    """Список user_id подписчиков продавца."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id FROM favorites WHERE seller_id = ?",
            (seller_id,),
        )
        rows = await cursor.fetchall()
        return [r[0] for r in rows]


async def get_favorites_count(user_id: int) -> int:
    """Сколько подписчиков у продавца."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM favorites WHERE seller_id = ?", (user_id,)
        )
        return (await cursor.fetchone())[0]
