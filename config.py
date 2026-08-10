import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", "0"))
REVIEW_CHANNEL_ID = int(os.getenv("REVIEW_CHANNEL_ID", "0"))
BOT_COMMISSION = float(os.getenv("BOT_COMMISSION", "3"))
BOT_WALLET = os.getenv("BOT_WALLET", "")
BOT_WALLET_LTC = os.getenv("LTC_ESCROW_ADDRESS", "")
TRONGRID_API_KEY = os.getenv("TRONGRID_API_KEY", "")
MIN_DEAL_AMOUNT = float(os.getenv("MIN_DEAL_AMOUNT", "20"))

# VIP-подписка
VIP_PRICE = float(os.getenv("VIP_PRICE", "10"))          # стоимость VIP в USDT/мес.
VIP_DAYS = int(os.getenv("VIP_DAYS", "30"))               # срок действия в днях
VIP_COMMISSION = float(os.getenv("VIP_COMMISSION", "1.5")) # комиссия для VIP (вместо 3%)

# Прокси для подключения к Telegram API (например http://127.0.0.1:10808)
PROXY = os.getenv("PROXY", "")

# Штраф при отмене после оплаты (% от суммы на эскроу)
CANCEL_PENALTY = float(os.getenv("CANCEL_PENALTY", "2"))
# Минимальная комиссия (USDT)
MIN_COMMISSION = float(os.getenv("MIN_COMMISSION", "2"))
MIN_COMMISSION_VIP = float(os.getenv("MIN_COMMISSION_VIP", "1"))

# Прогрессивная шкала комиссий: (порог_USDT, %, VIP_%)
COMMISSION_TIERS = [
    (500, 1.5, 0.75),   # 500+ USDT
    (100, 2.0, 1.0),    # 100-500 USDT
    (0,   3.0, 1.5),    # 20-100 USDT (базовая)
]


def calc_commission(amount: float, is_vip: bool = False, deals_count: int = 0) -> tuple[float, float]:
    """Рассчитать комиссию по прогрессивной шкале с учётом репутации.
    Возвращает (rate%, commission_usdt)."""
    for threshold, rate, vip_rate in COMMISSION_TIERS:
        if amount >= threshold:
            r = vip_rate if is_vip else rate
            commission = round(amount * r / 100, 2)
            # Скидка за репутацию
            _, _, rep_discount = get_reputation_level(deals_count)
            if rep_discount > 0:
                commission = round(commission * (100 - rep_discount) / 100, 2)
            min_c = MIN_COMMISSION_VIP if is_vip else MIN_COMMISSION
            if commission < min_c:
                commission = min_c
            return r, commission
    # fallback
    r = 1.5 if is_vip else 3.0
    return r, round(amount * r / 100, 2)

DB_PATH = os.getenv("DB_PATH", "database.db")

# ————— Система репутации —————
# (мин. сделок, название_ru, эмодзи, скидка_на_комиссию_%)
REPUTATION_TIERS = [
    (20, "Золото", "🥇", 20),     # 20+ сделок → −20% от комиссии
    (5,  "Серебро", "🥈", 10),    # 5-19 сделок → −10% от комиссии
    (0,  "Бронза", "🥉", 0),      # 0-4 сделки → стандартная комиссия
]


def get_reputation_level(deals_count: int) -> tuple[str, str, int]:
    """Возвращает (название, эмодзи, скидка_%) по количеству сделок."""
    for threshold, name, emoji, discount in REPUTATION_TIERS:
        if deals_count >= threshold:
            return name, emoji, discount
    return "Бронза", "🥉", 0

# Время (в часах) после отметки доставки, через которое сделка
# автоматически завершается, если покупатель не открыл спор
AUTO_COMPLETE_HOURS = max(1, int(os.getenv("AUTO_COMPLETE_HOURS", "72")))

# Категории объявлений
CATEGORIES = {
    "goods": "🛒 Goods",
    "services": "🔧 Services",
}

# Страны и основные города
COUNTRIES = {
    "uz": {
        "flag": "🇺🇿",
        "name": {
            "ru": "Узбекистан", "uz": "O'zbekiston", "kk": "Өзбекстан",
            "tr": "Özbekistan", "tg": "Ӯзбекистон", "ky": "Өзбекстан", "en": "Uzbekistan",
        },
    },
    "kz": {
        "flag": "🇰🇿",
        "name": {
            "ru": "Казахстан", "uz": "Qozog'iston", "kk": "Қазақстан",
            "tr": "Kazakistan", "tg": "Қазоқистон", "ky": "Казакстан", "en": "Kazakhstan",
        },
    },
    "ru": {
        "flag": "🇷🇺",
        "name": {
            "ru": "Россия", "uz": "Rossiya", "kk": "Ресей",
            "tr": "Rusya", "tg": "Русия", "ky": "Россия", "en": "Russia",
        },
    },
    "kg": {
        "flag": "🇰🇬",
        "name": {
            "ru": "Кыргызстан", "uz": "Qirg'iziston", "kk": "Қырғызстан",
            "tr": "Kırgızistan", "tg": "Қирғизистон", "ky": "Кыргызстан", "en": "Kyrgyzstan",
        },
    },
    "tj": {
        "flag": "🇹🇯",
        "name": {
            "ru": "Таджикистан", "uz": "Tojikiston", "kk": "Тәжікстан",
            "tr": "Tacikistan", "tg": "Тоҷикистон", "ky": "Тажикстан", "en": "Tajikistan",
        },
    },
    "tr": {
        "flag": "🇹🇷",
        "name": {
            "ru": "Турция", "uz": "Turkiya", "kk": "Түркия",
            "tr": "Türkiye", "tg": "Туркия", "ky": "Түркия", "en": "Turkey",
        },
    },
}


def get_country_name(country_code: str, lang: str = "en") -> str:
    """Get country name in the requested language."""
    info = COUNTRIES.get(country_code, {})
    names = info.get("name", {})
    if isinstance(names, dict):
        return names.get(lang, names.get("en", country_code))
    return names  # fallback for old format


CITIES = {
    "uz": [
        "Ташкент", "Самарканд", "Бухара", "Наманган", "Андижан",
        "Фергана", "Нукус", "Карши", "Навои", "Ургенч",
    ],
    "kz": [
        "Алматы", "Астана", "Шымкент", "Караганда", "Актобе",
        "Тараз", "Павлодар", "Усть-Каменогорск", "Семей", "Атырау",
    ],
    "ru": [
        "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург",
        "Казань", "Нижний Новгород", "Красноярск", "Челябинск",
        "Самара", "Ростов-на-Дону",
    ],
    "kg": [
        "Бишкек", "Ош", "Джалал-Абад", "Каракол", "Токмок",
    ],
    "tj": [
        "Душанбе", "Худжанд", "Бохтар", "Куляб", "Истаравшан",
    ],
    "tr": [
        "Стамбул", "Анкара", "Измир", "Анталья", "Бурса",
    ],
}

# Статусы сделки — полностью автоматический эскроу-гарант
class DealStatus:
    CREATED = "created"           # Сделка создана — ждём оплату на эскроу-кошелёк бота
    PAID = "paid"                 # 💰 Покупатель отправил USDT на эскроу (указал tx hash)
    DELIVERED = "delivered"       # 📦 Продавец выполнил заказ / отправил товар
    COMPLETED = "completed"       # 🎉 Сделка завершена — средства выплачиваются продавцу
    DISPUTED = "disputed"         # ⚠️ Спор — средства заморожены, решает админ
    CANCELLED = "cancelled"       # ❌ Отменена до оплаты
    REFUNDED = "refunded"         # 💸 Отменена после оплаты — возврат покупателю
