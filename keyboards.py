from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from languages import btn, get_category_name, LANGS


# ————— Reply-клавиатуры —————

def main_menu_kb(lang: str = "en") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=btn(lang, "btn_catalog")), KeyboardButton(text=btn(lang, "btn_create_listing"))],
            [KeyboardButton(text=btn(lang, "btn_my_deals")), KeyboardButton(text=btn(lang, "btn_my_listings"))],
            [KeyboardButton(text=btn(lang, "btn_search")), KeyboardButton(text=btn(lang, "btn_vip"))],
            [KeyboardButton(text=btn(lang, "btn_favorites")), KeyboardButton(text=btn(lang, "btn_referral"))],
            [KeyboardButton(text=btn(lang, "btn_profile")), KeyboardButton(text=btn(lang, "btn_help"))],
            [KeyboardButton(text=btn(lang, "btn_change_location"))],
        ],
        resize_keyboard=True,
    )


# ————— Выбор языка —————

def lang_select_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"setlang_{code}")]
        for code, label in LANGS.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def country_select_kb(lang: str = "en") -> InlineKeyboardMarkup:
    from config import COUNTRIES, get_country_name
    buttons = [
        [InlineKeyboardButton(
            text=f"{info['flag']} {get_country_name(code, lang)}",
            callback_data=f"setcountry_{code}",
        )]
        for code, info in COUNTRIES.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def city_select_kb(country_code: str, lang: str = "en") -> InlineKeyboardMarkup:
    from config import CITIES
    cities = CITIES.get(country_code, [])
    buttons = []
    # по 2 города в ряд
    for i in range(0, len(cities), 2):
        row = [InlineKeyboardButton(text=cities[i], callback_data=f"setcity_{cities[i]}")]
        if i + 1 < len(cities):
            row.append(InlineKeyboardButton(text=cities[i + 1], callback_data=f"setcity_{cities[i + 1]}"))
        buttons.append(row)
    # кнопка «Другой город»
    buttons.append([InlineKeyboardButton(text=btn(lang, "city_other"), callback_data="setcity_other")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ————— Inline-клавиатуры —————

def categories_kb(prefix: str = "cat", lang: str = "en") -> InlineKeyboardMarkup:
    from config import CATEGORIES
    buttons = [
        [InlineKeyboardButton(text=get_category_name(key, lang), callback_data=f"{prefix}_{key}")]
        for key in CATEGORIES
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# --- NEW: Currency Selection Keyboard ---
def currency_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="USDT TRC20", callback_data="currency:USDT_TRC20"),
                InlineKeyboardButton(text="Litecoin (LTC)", callback_data="currency:LTC")
            ]
        ]
    )


def listing_card_kb(listing_id: int, seller_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn(lang, "btn_start_deal"), callback_data=f"buy_{listing_id}")],
        [InlineKeyboardButton(text=btn(lang, "btn_seller_profile"), callback_data=f"profile_{seller_id}"),
         InlineKeyboardButton(text=btn(lang, "btn_follow_seller"), callback_data=f"follow_{seller_id}")],
    ])


# --- Эскроу-поток: кнопки по этапам ---

def deal_pay_escrow_kb(deal_id: int, lang: str = "en", currency: str = "USDT_TRC20") -> InlineKeyboardMarkup:
    # Dynamic button text based on currency
    if "LTC" in currency:
        pay_btn_text = "✅ I sent the LTC"
    else:
        pay_btn_text = btn(lang, "btn_i_sent_usdt")

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=pay_btn_text, callback_data=f"funded_{deal_id}")],
        [InlineKeyboardButton(text=btn(lang, "btn_chat"), callback_data=f"dealchat_{deal_id}")],
        [InlineKeyboardButton(text=btn(lang, "btn_cancel_deal"), callback_data=f"cancel_deal_{deal_id}")],
    ])


def deal_seller_deliver_kb(deal_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn(lang, "btn_order_done"), callback_data=f"delivered_{deal_id}")],
        [InlineKeyboardButton(text=btn(lang, "btn_chat"), callback_data=f"dealchat_{deal_id}")],
        [InlineKeyboardButton(text=btn(lang, "btn_open_dispute"), callback_data=f"dispute_{deal_id}")],
    ])


def deal_buyer_confirm_kb(deal_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn(lang, "btn_confirm_received"), callback_data=f"confirm_{deal_id}")],
        [InlineKeyboardButton(text=btn(lang, "btn_chat"), callback_data=f"dealchat_{deal_id}")],
        [InlineKeyboardButton(text=btn(lang, "btn_open_dispute"), callback_data=f"dispute_{deal_id}")],
        [InlineKeyboardButton(text=btn(lang, "btn_cancel_deal"), callback_data=f"cancel_deal_{deal_id}")],
    ])


def deal_complete_review_kb(deal_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn(lang, "btn_leave_review"), callback_data=f"review_{deal_id}")],
    ])


def review_rating_kb(deal_id: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=f"{'⭐' * i}", callback_data=f"rate_{deal_id}_{i}")
        for i in range(1, 6)
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def confirm_cancel_kb(action: str, item_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=btn(lang, "btn_yes"), callback_data=f"yes_{action}_{item_id}"),
            InlineKeyboardButton(text=btn(lang, "btn_no"), callback_data=f"no_{action}_{item_id}"),
        ]
    ])


def my_listing_kb(listing_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn(lang, "btn_delete_listing"), callback_data=f"del_listing_{listing_id}")],
    ])


def back_to_menu_kb(lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn(lang, "btn_back_menu"), callback_data="back_menu")],
    ])


# ————— Админ —————

def admin_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistics", callback_data="admin_stats")],
        [InlineKeyboardButton(text="💬 Support Messages", callback_data="admin_support")],
        [InlineKeyboardButton(text="🚫 Ban User", callback_data="admin_ban")],
        [InlineKeyboardButton(text="✅ Unban User", callback_data="admin_unban")],
        [InlineKeyboardButton(text="⚖️ Active Disputes", callback_data="admin_disputes")],
        [InlineKeyboardButton(text="🔒 Escrow Deals", callback_data="admin_escrow")],
        [InlineKeyboardButton(text="👑 VIP Requests", callback_data="admin_vip")],        
        [InlineKeyboardButton(text="👥 Referrals", callback_data="admin_referrals")],    
    ])


# ————— VIP —————

def vip_buy_kb(lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn(lang, "btn_buy_vip"), callback_data="vip_buy")],
    ])


def vip_paid_kb(sub_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn(lang, "btn_i_paid_vip"), callback_data=f"vip_paid_{sub_id}")],
        [InlineKeyboardButton(text=btn(lang, "btn_cancel"), callback_data="vip_cancel")],
    ])