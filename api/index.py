import asyncio
import logging
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher
from aiogram.types import Update, BotCommand, BotCommandScopeChat
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("escrow-webhook")

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0") or 0)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "telegram-webhook").strip("/")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
SETUP_SECRET = os.getenv("SETUP_SECRET")
REDIS_URL = os.getenv("REDIS_URL")
PROXY = os.getenv("PROXY")

app = FastAPI(title="HandshakeDealBot Webhook")

bot = None
dp = None
initialized = False
init_lock = asyncio.Lock()

if BOT_TOKEN and REDIS_URL:
    try:
        redis_client = Redis.from_url(
            REDIS_URL,
            encoding="utf-8",
            socket_timeout=5,
            socket_connect_timeout=5,
        )
        storage = RedisStorage(redis=redis_client)

        session = AiohttpSession(proxy=PROXY) if PROXY else None
        bot = Bot(
            token=BOT_TOKEN,
            session=session,
            default=DefaultBotProperties(parse_mode="HTML"),
        )

        dp = Dispatcher(storage=storage)

        from handlers.common import router as common_router
        from handlers.listings import router as listings_router
        from handlers.deals import router as deals_router
        from handlers.vip import router as vip_router

        dp.include_router(common_router)
        dp.include_router(listings_router)
        dp.include_router(deals_router)
        dp.include_router(vip_router)

        logger.info("ROUTERS_LOADED")
    except Exception:
        logger.exception("BOT_INIT_FAILED")
else:
    logger.warning("BOT_TOKEN or REDIS_URL missing")


async def ensure_db():
    global initialized

    async with init_lock:
        if initialized:
            return

        try:
            from db.core import init_db
            await init_db()
            logger.info("DB_INITIALIZED")
        except Exception:
            logger.exception("DB_INIT_FAILED")

        initialized = True


async def register_commands():
    if not bot:
        return

    user_commands = [
        BotCommand(command="start", description="Start / Restart bot"),
        BotCommand(command="help", description="Help"),
        BotCommand(command="wallet", description="Set payout wallet"),
        BotCommand(command="lang", description="Change language"),
        BotCommand(command="location", description="Change location"),
        BotCommand(command="support", description="Support"),
        BotCommand(command="cancel", description="Cancel current action"),
        BotCommand(command="qr", description="QR code"),
    ]

    await bot.set_my_commands(user_commands)

    if ADMIN_ID:
        admin_commands = user_commands + [
            BotCommand(command="admin", description="Admin panel"),
            BotCommand(command="chatlog", description="Deal chat log"),
        ]

        await bot.set_my_commands(
            admin_commands,
            scope=BotCommandScopeChat(chat_id=ADMIN_ID),
        )


@app.get("/")
async def health():
    return {
        "ok": True,
        "bot": bool(bot),
        "dispatcher": bool(dp),
        "webhook_path": f"/{WEBHOOK_PATH}",
    }


@app.get("/setup-webhook")
async def setup_webhook(key: str = ""):
    if not SETUP_SECRET or key != SETUP_SECRET:
        raise HTTPException(status_code=403, detail="Invalid setup key")

    if not bot:
        raise HTTPException(status_code=500, detail="Bot not initialized")

    if not WEBHOOK_URL or not WEBHOOK_SECRET:
        raise HTTPException(
            status_code=500,
            detail="WEBHOOK_URL and WEBHOOK_SECRET are required",
        )

    webhook_url = f"{WEBHOOK_URL.rstrip('/')}/{WEBHOOK_PATH}"

    await bot.set_webhook(
        url=webhook_url,
        secret_token=WEBHOOK_SECRET,
        drop_pending_updates=False,
    )

    await register_commands()

    return {
        "ok": True,
        "webhook": webhook_url,
    }


@app.post("/{path:path}")
async def telegram_webhook(request: Request, path: str):
    if path != WEBHOOK_PATH:
        raise HTTPException(status_code=404, detail="Not found")

    if not WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="WEBHOOK_SECRET missing")

    telegram_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")

    if telegram_secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret token")

    if not bot or not dp:
        raise HTTPException(status_code=500, detail="Bot not initialized")

    await ensure_db()

    try:
        data = await request.json()
        update = Update.model_validate(data)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid update payload")

    await dp.feed_update(bot=bot, update=update)

    return {"ok": True}


# Vercel compatibility
handler = app