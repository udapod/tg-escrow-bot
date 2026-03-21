import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
BOT_COMMISSION = float(os.getenv("BOT_COMMISSION", "3"))
BOT_WALLET = os.getenv("BOT_WALLET", "")
TRONGRID_API_KEY = os.getenv("TRONGRID_API_KEY", "")
MIN_DEAL_AMOUNT = float(os.getenv("MIN_DEAL_AMOUNT", "20"))

# VIP-подписка
VIP_PRICE = float(os.getenv("VIP_PRICE", "10"))          # стоимость VIP в USDT/мес.
VIP_DAYS = int(os.getenv("VIP_DAYS", "30"))               # срок действия в днях
VIP_COMMISSION = float(os.getenv("VIP_COMMISSION", "1.5")) # комиссия для VIP (вместо 3%)

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
    "goods": "🛒 Товары",
    "services": "🔧 Услуги",
}

# Страны и основные города
COUNTRIES = {
    "uz": {"flag": "🇺🇿", "name": "Узбекистан"},
    "kz": {"flag": "🇰🇿", "name": "Казахстан"},
    "ru": {"flag": "🇷🇺", "name": "Россия"},
    "kg": {"flag": "🇰🇬", "name": "Кыргызстан"},
    "tj": {"flag": "🇹🇯", "name": "Таджикистан"},
    "tr": {"flag": "🇹🇷", "name": "Турция"},
}

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
