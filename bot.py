import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, ADMIN_ID, TRONGRID_API_KEY
from database import init_db, cleanup_old_data
from handlers.common import router as common_router
from handlers.listings import router as listings_router
from handlers.deals import router as deals_router
from handlers.vip import router as vip_router
from handlers.deals import auto_complete_expired_deals

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

if not TRONGRID_API_KEY:
    logger.warning("⚠️ TRONGRID_API_KEY не задан! Верификация транзакций ОТКЛЮЧЕНА. Установите ключ для безопасной работы.")


async def scheduler(bot: Bot):
    """Фоновая задача: каждый час проверяет и авто-завершает сделки + очищает старые данные."""
    while True:
        try:
            await auto_complete_expired_deals(bot)
        except Exception as e:
            logger.error(f"Ошибка в авто-завершении: {e}")
        try:
            await cleanup_old_data()
        except Exception as e:
            logger.error(f"Ошибка при очистке старых данных: {e}")
        await asyncio.sleep(3600)  # проверять раз в час


async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не указан! Создайте .env файл (см. .env.example)")
        return

    await init_db()
    logger.info("База данных инициализирована")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(common_router)
    dp.include_router(listings_router)
    dp.include_router(deals_router)
    dp.include_router(vip_router)

    # Запускаем фоновую задачу авто-завершения
    scheduler_task = asyncio.create_task(scheduler(bot))
    logger.info("Фоновая задача авто-завершения запущена")

    # Graceful shutdown
    async def on_shutdown():
        logger.info("Завершение работы бота...")
        scheduler_task.cancel()
        await bot.session.close()
        logger.info("Бот остановлен корректно")

    dp.shutdown.register(on_shutdown)

    # Команды для всех пользователей
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск / Перезапуск бота"),
        BotCommand(command="help", description="Помощь — как пользоваться"),
        BotCommand(command="wallet", description="Указать USDT-кошелёк (TRC-20)"),
        BotCommand(command="lang", description="Сменить язык / Tilni o'zgartirish"),
        BotCommand(command="location", description="Сменить город"),
        BotCommand(command="support", description="Написать в поддержку"),        BotCommand(command="cancel", description="Отменить текущее действие"),        BotCommand(command="qr", description="QR-код для перехода в бот"),
    ])
    # Дополнительные команды только для админа
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запуск / Перезапуск бота"),
            BotCommand(command="help", description="Помощь — как пользоваться"),
            BotCommand(command="wallet", description="Указать USDT-кошелёк (TRC-20)"),
            BotCommand(command="lang", description="Сменить язык / Tilni o'zgartirish"),
            BotCommand(command="location", description="Сменить город"),
            BotCommand(command="support", description="Написать в поддержку"),            BotCommand(command="cancel", description="Отменить текущее действие"),            BotCommand(command="qr", description="QR-код для перехода в бот"),
            BotCommand(command="admin", description="Админ-панель"),
            BotCommand(command="chatlog", description="История переписки сделки"),
        ],
        scope=BotCommandScopeChat(chat_id=ADMIN_ID),
    )
    logger.info("Команды бота зарегистрированы")

    logger.info("Бот запускается...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
