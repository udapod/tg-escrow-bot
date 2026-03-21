from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import time

import database as db
from keyboards import main_menu_kb, admin_kb, back_to_menu_kb, lang_select_kb, country_select_kb, city_select_kb
from config import ADMIN_ID, COUNTRIES, CITIES, get_reputation_level
from languages import t, all_btn_texts, btn

router = Router()


class SetLocation(StatesGroup):
    waiting_city_manual = State()


class SupportState(StatesGroup):
    waiting_message = State()


# Rate-limit для /support: user_id -> timestamp
_support_cooldowns: dict[int, float] = {}
_support_cooldowns_cleanup = 0  # время последней очистки
SUPPORT_COOLDOWN_SEC = 60


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, bot: Bot):
    """Регистрация и приветствие. Поддержка deep link: /start ref_123."""
    user = await db.get_user(message.from_user.id)
    is_new = user is None

    # Парсинг реферальной ссылки
    referred_by = 0
    if is_new and command.args and command.args.startswith("ref_"):
        try:
            ref_id = int(command.args[4:])
            if ref_id != message.from_user.id:  # нельзя пригласить себя
                referrer = await db.get_user(ref_id)
                if referrer:
                    referred_by = ref_id
        except (ValueError, TypeError):
            pass

    await db.register_user(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name,
        referred_by=referred_by,
    )

    if is_new:
        # Уведомляем реферера
        if referred_by:
            try:
                ref_lang = await db.get_user_lang(referred_by)
                await bot.send_message(
                    referred_by,
                    t(ref_lang, "referral_new_user_notify", name=message.from_user.full_name),
                    parse_mode="HTML",
                )
            except Exception as e:
                logger.warning(f"Не удалось уведомить реферера {referred_by}: {e}")

        # Новый пользователь — показываем выбор языка
        await message.answer(
            t("ru", "choose_lang"),
            reply_markup=lang_select_kb(),
        )
        return

    lang = await db.get_user_lang(message.from_user.id)
    await message.answer(
        t(lang, "welcome"),
        parse_mode="HTML",
        reply_markup=main_menu_kb(lang),
    )


# ————— Выбор / смена языка —————

@router.message(Command("lang"))
async def cmd_lang(message: Message):
    await message.answer(
        t("ru", "choose_lang"),
        reply_markup=lang_select_kb(),
    )


@router.callback_query(F.data.startswith("setlang_"))
async def cb_set_language(callback: CallbackQuery):
    lang_code = callback.data.split("_", 1)[1]
    if lang_code not in ("ru", "uz", "kk", "tr", "tg", "ky"):
        await callback.answer("Unknown language", show_alert=True)
        return

    # Регистрируем на случай, если пользователь новый
    await db.register_user(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        full_name=callback.from_user.full_name,
    )
    await db.set_user_lang(callback.from_user.id, lang_code)

    # Проверяем, указано ли уже местоположение
    country, city = await db.get_user_location(callback.from_user.id)
    if not country or not city:
        # Новый пользователь — после языка показываем выбор страны
        await callback.message.edit_text(
            t(lang_code, "lang_set") + "\n\n" + t(lang_code, "choose_country"),
            reply_markup=country_select_kb(),
        )
        await callback.answer()
        return

    await callback.message.edit_text(t(lang_code, "lang_set"))
    await callback.message.answer(
        t(lang_code, "welcome"),
        parse_mode="HTML",
        reply_markup=main_menu_kb(lang_code),
    )
    await callback.answer()


# ————— Выбор страны —————

@router.callback_query(F.data.startswith("setcountry_"))
async def cb_set_country(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    country_code = callback.data.split("_", 1)[1]
    if country_code not in COUNTRIES:
        await callback.answer("❌", show_alert=True)
        return

    # Сохраняем страну (город пока пустой)
    await db.set_user_location(callback.from_user.id, country_code, "")
    country_name = f"{COUNTRIES[country_code]['flag']} {COUNTRIES[country_code]['name']}"

    await callback.message.edit_text(
        t(lang, "choose_city", country=country_name),
        reply_markup=city_select_kb(country_code, lang),
    )
    await callback.answer()


# ————— Выбор города —————

@router.callback_query(F.data.startswith("setcity_"))
async def cb_set_city(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_lang(callback.from_user.id)
    city_value = callback.data.split("_", 1)[1]

    if city_value == "other":
        # Пользователь хочет ввести город вручную
        await callback.message.edit_text(t(lang, "enter_city_manual"))
        await state.set_state(SetLocation.waiting_city_manual)
        await callback.answer()
        return

    country, _ = await db.get_user_location(callback.from_user.id)
    await db.set_user_location(callback.from_user.id, country, city_value)

    country_name = COUNTRIES.get(country, {}).get("name", country)
    await callback.message.edit_text(
        t(lang, "location_set", country=country_name, city=city_value),
    )
    await callback.message.answer(
        t(lang, "welcome"),
        parse_mode="HTML",
        reply_markup=main_menu_kb(lang),
    )
    await callback.answer()


@router.message(SetLocation.waiting_city_manual)
async def city_manual_entered(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    text = message.text or ""
    # Отмена
    if text.strip().startswith("/"):
        await state.clear()
        await message.answer(t(lang, "city_input_cancelled"), reply_markup=main_menu_kb(lang))
        return
    city = text.strip()
    if len(city) < 2 or len(city) > 50:
        await message.answer(t(lang, "city_too_short"))
        return

    country, _ = await db.get_user_location(message.from_user.id)
    await db.set_user_location(message.from_user.id, country, city)
    await state.clear()

    country_name = COUNTRIES.get(country, {}).get("name", country)
    await message.answer(
        t(lang, "location_set", country=country_name, city=city),
    )
    await message.answer(
        t(lang, "welcome"),
        parse_mode="HTML",
        reply_markup=main_menu_kb(lang),
    )


# ————— Смена местоположения (кнопка / команда) —————

@router.message(Command("location"))
@router.message(F.text.in_(all_btn_texts("btn_change_location")))
async def cmd_change_location(message: Message):
    lang = await db.get_user_lang(message.from_user.id)
    await message.answer(
        t(lang, "choose_country"),
        reply_markup=country_select_kb(),
    )


# ————— Помощь —————

@router.message(Command("help"))
@router.message(F.text.in_(all_btn_texts("btn_help")))
async def cmd_help(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    # Очищаем FSM, чтобы /help не ломал текущее состояние
    await state.clear()
    await message.answer(t(lang, "help"), parse_mode="HTML", reply_markup=main_menu_kb(lang))


# ————— QR-код бота —————

@router.message(Command("qr"))
async def cmd_qr(message: Message, bot: Bot):
    lang = await db.get_user_lang(message.from_user.id)
    me = await bot.get_me()
    link = f"https://t.me/{me.username}"
    from qr_utils import generate_qr
    from aiogram.types import BufferedInputFile
    qr_buf = generate_qr(link)
    photo = BufferedInputFile(qr_buf.read(), filename="bot_qr.png")
    await message.answer_photo(photo, caption=t(lang, "qr_bot_caption"))


# ————— Профиль —————

@router.message(F.text.in_(all_btn_texts("btn_profile")))
async def cmd_profile(message: Message):
    lang = await db.get_user_lang(message.from_user.id)
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer(t(lang, "press_start_first"))
        return

    wallet_display = user["wallet"] if user["wallet"] else t(lang, "wallet_not_set")
    reviews = await db.get_user_reviews(message.from_user.id)
    vip_info = await db.get_vip_info(message.from_user.id)
    vip_line = t(lang, "profile_vip_status") + "\n" if vip_info else ""
    country_code = user.get("country", "")
    city = user.get("city", "")
    if country_code and city:
        country_name = COUNTRIES.get(country_code, {}).get("name", country_code)
        location_display = f"{country_name}, {city}"
    else:
        location_display = t(lang, "location_not_set")

    # Репутация
    rep_name, rep_emoji, rep_discount = get_reputation_level(user["deals_count"])
    rep_line = t(lang, "reputation_level", emoji=rep_emoji, name=rep_name) + "\n"
    if rep_discount > 0:
        rep_line += t(lang, "reputation_discount_note", discount=rep_discount) + "\n"

    # Рефералы
    ref_count = await db.get_referral_count(message.from_user.id)
    ref_line = f"{t(lang, 'profile_referrals')}: {ref_count}\n" if ref_count > 0 else ""

    # Подписчики
    followers_count = await db.get_favorites_count(message.from_user.id)
    followers_line = f"{t(lang, 'profile_followers')}: {followers_count}\n" if followers_count > 0 else ""

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    buttons = [
        [InlineKeyboardButton(text=t(lang, "btn_delete_account"), callback_data="delete_account")],
        [InlineKeyboardButton(text=t(lang, "btn_change_lang"), callback_data="profile_change_lang")],
    ]
    delete_kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(
        f"{t(lang, 'profile_title')}\n\n"
        f"{vip_line}"
        f"{rep_line}"
        f"{t(lang, 'profile_id')}: <code>{user['user_id']}</code>\n"
        f"{t(lang, 'profile_name')}: {user['full_name']}\n"
        f"{t(lang, 'profile_location')}: {location_display}\n"
        f"{t(lang, 'profile_rating')}: {user['rating']:.1f}/5.0\n"
        f"{t(lang, 'profile_deals')}: {user['deals_count']}\n"
        f"{t(lang, 'profile_wallet')}: <code>{wallet_display}</code>\n"
        f"{t(lang, 'profile_reviews')}: {len(reviews)}\n"
        f"{ref_line}"
        f"{followers_line}\n"
        f"{t(lang, 'wallet_hint')}",
        parse_mode="HTML",
        reply_markup=delete_kb,
    )


# ————— Удаление аккаунта —————

@router.callback_query(F.data == "delete_account")
async def cb_delete_account_prompt(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)

    # Проверяем активные сделки
    has_active = await db.has_active_deals(callback.from_user.id)
    if has_active:
        await callback.answer(t(lang, "delete_account_has_active_deals"), show_alert=True)
        return

    from keyboards import confirm_cancel_kb
    await callback.message.answer(
        t(lang, "delete_account_confirm"),
        parse_mode="HTML",
        reply_markup=confirm_cancel_kb("delacc", callback.from_user.id, lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("yes_delacc_"))
async def cb_confirm_delete_account(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    target_id = int(callback.data.split("_")[-1])

    # Безопасность: только сам пользователь может удалить свой аккаунт
    if target_id != callback.from_user.id:
        await callback.answer("⛔", show_alert=True)
        return

    has_active = await db.has_active_deals(callback.from_user.id)
    if has_active:
        await callback.answer(t(lang, "delete_account_has_active_deals"), show_alert=True)
        return

    await db.delete_user_account(callback.from_user.id)
    await callback.message.edit_text(t(lang, "account_deleted"))
    await callback.answer()


@router.callback_query(F.data.startswith("no_delacc_"))
async def cb_cancel_delete_account(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_text(t(lang, "action_cancelled"))
    await callback.answer()


@router.message(Command("wallet"))
async def cmd_set_wallet(message: Message):
    lang = await db.get_user_lang(message.from_user.id)
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or len(parts[1].strip()) < 30:
        await message.answer(t(lang, "wallet_prompt"), parse_mode="HTML")
        return

    wallet = parts[1].strip()
    if not wallet.startswith("T") or len(wallet) != 34:
        await message.answer(t(lang, "wallet_invalid"))
        return

    # Base58 валидация чек-суммы TRC-20 адреса
    try:
        import base58
        decoded = base58.b58decode_check(wallet)
        if decoded[0] != 0x41:  # TRON prefix
            raise ValueError
    except Exception:
        await message.answer(t(lang, "wallet_invalid"))
        return

    await db.update_wallet(message.from_user.id, wallet)
    await message.answer(
        f"{t(lang, 'wallet_saved')}: <code>{wallet}</code>",
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("profile_"))
async def cb_view_profile(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    # Проверка бана просматривающего
    viewer = await db.get_user(callback.from_user.id)
    if viewer and viewer["is_banned"]:
        await callback.answer(t(lang, "account_banned"), show_alert=True)
        return
    user_id = int(callback.data.split("_")[1])
    user = await db.get_user(user_id)
    if not user:
        await callback.answer(t(lang, "deal_not_found"), show_alert=True)
        return

    reviews = await db.get_user_reviews(user_id)
    vip_badge = "👑 " if await db.is_vip(user_id) else ""

    # Репутация
    rep_name, rep_emoji, _ = get_reputation_level(user["deals_count"])

    # Подписчики
    followers_count = await db.get_favorites_count(user_id)

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    buttons = []
    if reviews:
        buttons.append([InlineKeyboardButton(
            text=t(lang, "btn_view_reviews") + f" ({len(reviews)})",
            callback_data=f"viewreviews_{user_id}",
        )])
    # Кнопка подписки/отписки (не для себя)
    if user_id != callback.from_user.id:
        is_fav = await db.is_favorite(callback.from_user.id, user_id)
        if is_fav:
            buttons.append([InlineKeyboardButton(
                text=t(lang, "btn_unfollow_seller"),
                callback_data=f"unfollow_{user_id}",
            )])
        else:
            buttons.append([InlineKeyboardButton(
                text=t(lang, "btn_follow_seller"),
                callback_data=f"follow_{user_id}",
            )])
    buttons.append([InlineKeyboardButton(text=btn(lang, "btn_back_menu"), callback_data="back_menu")])

    await callback.message.answer(
        f"{t(lang, 'profile_view_title')}\n\n"
        f"{t(lang, 'profile_name')}: {vip_badge}{user['full_name']}\n"
        f"{rep_emoji} {rep_name}\n"
        f"{t(lang, 'profile_rating')}: {user['rating']:.1f}/5.0\n"
        f"{t(lang, 'profile_deals_count')}: {user['deals_count']}\n"
        f"{t(lang, 'profile_reviews')}: {len(reviews)}\n"
        f"{t(lang, 'profile_followers')}: {followers_count}\n"
        f"{t(lang, 'profile_since')}: {user['registered_at']}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("viewreviews_"))
async def cb_view_reviews(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    target_id = int(callback.data.split("_")[1])
    user = await db.get_user(target_id)
    if not user:
        await callback.answer("❌", show_alert=True)
        return

    reviews = await db.get_user_reviews(target_id)
    if not reviews:
        await callback.answer(t(lang, "no_reviews"), show_alert=True)
        return

    text = t(lang, "reviews_title", name=user["full_name"], rating=f"{user['rating']:.1f}")
    for r in reviews[:20]:
        stars = "⭐" * r["rating"]
        comment = r["comment"] if r["comment"] else "—"
        date = r["created_at"][:10] if r.get("created_at") else ""
        photo_mark = " 📸" if r.get("photo_id") else ""
        text += f"{stars}{photo_mark}  — <i>{comment}</i>\n📅 {date}\n\n"

    await callback.message.answer(text, parse_mode="HTML")

    # Отправляем фото отзывов отдельно
    from aiogram.types import InputMediaPhoto
    photo_reviews = [r for r in reviews[:20] if r.get("photo_id")]
    for r in photo_reviews[:5]:
        stars = "⭐" * r["rating"]
        await callback.message.answer_photo(
            photo=r["photo_id"],
            caption=f"{stars} — {r.get('comment', '') or '—'}",
        )

    await callback.answer()


# ————— Подписка / отписка от продавца —————

@router.callback_query(F.data.startswith("follow_"))
async def cb_follow_seller(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    seller_id = int(callback.data.split("_")[1])

    if seller_id == callback.from_user.id:
        await callback.answer(t(lang, "cant_follow_self"), show_alert=True)
        return

    seller = await db.get_user(seller_id)
    if not seller:
        await callback.answer("❌", show_alert=True)
        return

    await db.add_favorite(callback.from_user.id, seller_id)
    await callback.answer(
        t(lang, "followed_seller", name=seller["full_name"]),
        show_alert=True,
    )


@router.callback_query(F.data.startswith("unfollow_"))
async def cb_unfollow_seller(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    seller_id = int(callback.data.split("_")[1])

    seller = await db.get_user(seller_id)
    name = seller["full_name"] if seller else "—"

    await db.remove_favorite(callback.from_user.id, seller_id)
    await callback.answer(
        t(lang, "unfollowed_seller", name=name),
        show_alert=True,
    )


# ————— Избранное (кнопка) —————

@router.message(F.text.in_(all_btn_texts("btn_favorites")))
async def cmd_favorites(message: Message):
    lang = await db.get_user_lang(message.from_user.id)
    favorites = await db.get_favorites(message.from_user.id)

    if not favorites:
        await message.answer(t(lang, "favorites_empty"))
        return

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    text = t(lang, "favorites_list_title")
    buttons = []
    for seller in favorites[:20]:
        vip_badge = "👑 " if await db.is_vip(seller["user_id"]) else ""
        rep_name, rep_emoji, _ = get_reputation_level(seller["deals_count"])
        text += (
            f"\n{vip_badge}{seller['full_name']} {rep_emoji}\n"
            f"  ⭐ {seller['rating']:.1f} | 📦 {seller['deals_count']}\n"
        )
        buttons.append([
            InlineKeyboardButton(
                text=f"👤 {seller['full_name']}",
                callback_data=f"profile_{seller['user_id']}",
            ),
            InlineKeyboardButton(
                text=t(lang, "btn_unfollow_seller"),
                callback_data=f"unfollow_{seller['user_id']}",
            ),
        ])

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None,
    )


# ————— Реферальная программа (кнопка) —————

@router.message(F.text.in_(all_btn_texts("btn_referral")))
async def cmd_referral(message: Message, bot: Bot):
    lang = await db.get_user_lang(message.from_user.id)
    me = await bot.get_me()
    ref_link = f"https://t.me/{me.username}?start=ref_{message.from_user.id}"
    total = await db.get_referral_count(message.from_user.id)
    active = await db.get_referral_active_count(message.from_user.id)

    await message.answer(
        t(lang, "referral_info", link=ref_link, total=total, active=active),
        parse_mode="HTML",
    )


# ————— Админ —————

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("🔧 <b>Админ-панель</b>", parse_mode="HTML", reply_markup=admin_kb())


@router.callback_query(F.data == "admin_stats")
async def cb_admin_stats(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    stats = await db.get_stats()
    ref_stats = await db.get_referral_stats_admin()
    ref_line = ""
    if ref_stats:
        total_refs = sum(r["ref_count"] for r in ref_stats)
        ref_line = f"\n👥 Рефералов всего: {total_refs}"

    await callback.message.edit_text(
        f"📊 <b>Статистика бота</b>\n\n"
        f"👥 Пользователей: {stats['users']}\n"
        f"📋 Активных объявлений: {stats['active_listings']}\n"
        f"📦 Всего сделок: {stats['total_deals']}\n"
        f"✅ Завершённых: {stats['completed_deals']}\n"
        f"💰 Комиссия: {stats['total_commission']} USDT\n"
        f"🔒 Заморожено на эскроу: {stats['frozen_funds']} USDT\n"
        f"⚠️ Активных споров: {stats['active_disputes']}"
        f"{ref_line}",
        parse_mode="HTML",
        reply_markup=admin_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "admin_ban")
async def cb_admin_ban_prompt(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return
    await callback.message.answer(
        "Отправьте команду:\n/ban <code>USER_ID</code>",
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin_unban")
async def cb_admin_unban_prompt(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return
    await callback.message.answer(
        "Отправьте команду:\n/unban <code>USER_ID</code>",
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(Command("ban"))
async def cmd_ban(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Использование: /ban <code>USER_ID</code>", parse_mode="HTML")
        return
    target_id = int(parts[1])
    await db.ban_user(target_id, ban=True)
    await message.answer(f"🚫 Пользователь {target_id} заблокирован.")


@router.message(Command("unban"))
async def cmd_unban(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Использование: /unban <code>USER_ID</code>", parse_mode="HTML")
        return
    target_id = int(parts[1])
    await db.ban_user(target_id, ban=False)
    await message.answer(f"✅ Пользователь {target_id} разблокирован.")


@router.callback_query(F.data == "back_menu")
async def cb_back_menu(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.answer(t(lang, "main_menu"), reply_markup=main_menu_kb(lang))
    await callback.answer()


@router.callback_query(F.data == "profile_change_lang")
async def cb_profile_change_lang(callback: CallbackQuery):
    from keyboards import lang_select_kb
    await callback.message.answer(
        t("ru", "choose_lang"),
        reply_markup=lang_select_kb(),
    )
    await callback.answer()


# ————— Админ: реферальная статистика —————

@router.callback_query(F.data == "admin_referrals")
async def cb_admin_referrals(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    top = await db.get_referral_stats_admin()
    if not top:
        await callback.message.edit_text(
            "👥 Реферальных приглашений пока нет.",
            reply_markup=admin_kb(),
        )
        await callback.answer()
        return

    text_parts = ["👥 <b>Топ рефереров:</b>\n"]
    for i, r in enumerate(top, 1):
        text_parts.append(f"{i}. {r['full_name']} — <b>{r['ref_count']}</b> приглашений")

    await callback.message.edit_text(
        "\n".join(text_parts),
        parse_mode="HTML",
        reply_markup=admin_kb(),
    )
    await callback.answer()


# ————— Поддержка /support —————

@router.message(Command("support"))
async def cmd_support(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    # Rate-limit
    global _support_cooldowns_cleanup
    now = time.time()
    # Очистка старых записей раз в час
    if now - _support_cooldowns_cleanup > 3600:
        _support_cooldowns_cleanup = now
        cutoff = now - 86400
        for uid in [k for k, v in _support_cooldowns.items() if v < cutoff]:
            _support_cooldowns.pop(uid, None)
    last = _support_cooldowns.get(message.from_user.id, 0)
    if now - last < SUPPORT_COOLDOWN_SEC:
        await message.answer(t(lang, "support_rate_limit"))
        return
    await message.answer(t(lang, "support_prompt"))
    await state.set_state(SupportState.waiting_message)


@router.message(SupportState.waiting_message)
async def support_message_entered(message: Message, state: FSMContext, bot: Bot):
    lang = await db.get_user_lang(message.from_user.id)
    text = (message.text or "").strip()

    if not text:
        return

    if text.startswith("/"):
        await state.clear()
        await message.answer(t(lang, "support_cancelled"), reply_markup=main_menu_kb(lang))
        return

    if len(text) > 1000:
        await message.answer(t(lang, "support_too_long"))
        return

    user = await db.get_user(message.from_user.id)
    full_name = user["full_name"] if user else message.from_user.full_name
    username = user["username"] if user else (message.from_user.username or "")

    await db.save_support_message(
        user_id=message.from_user.id,
        username=username,
        full_name=full_name,
        message_text=text,
    )

    await state.clear()
    _support_cooldowns[message.from_user.id] = time.time()
    await message.answer(t(lang, "support_sent"), reply_markup=main_menu_kb(lang))

    # Пересылаем администратору
    try:
        await bot.send_message(
            ADMIN_ID,
            f"📩 <b>Новое обращение в поддержку</b>\n\n"
            f"👤 {full_name} (@{username})\n"
            f"🆔 ID: <code>{message.from_user.id}</code>\n\n"
            f"💬 {text}",
            parse_mode="HTML",
        )
    except Exception:
        pass


# ————— Админ: просмотр сообщений поддержки —————

@router.callback_query(F.data == "admin_support")
async def cb_admin_support(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    messages = await db.get_support_messages(limit=20)

    if not messages:
        await callback.message.edit_text(
            "📩 Нет обращений в поддержку.",
            reply_markup=admin_kb(),
        )
        await callback.answer()
        return

    unread = await db.get_unread_support_count()
    text_parts = [f"📩 <b>Обращения в поддержку</b> (непрочитанных: {unread})\n"]
    for m in messages:
        read_mark = "✅" if m["is_read"] else "🆕"
        text_parts.append(
            f"\n{read_mark} <b>{m['full_name']}</b> (@{m['username']})\n"
            f"🆔 <code>{m['user_id']}</code> | {m['created_at']}\n"
            f"💬 {m['message'][:200]}"
        )

    await db.mark_support_read()

    full_text = "\n".join(text_parts)
    if len(full_text) > 4000:
        full_text = full_text[:4000] + "\n\n..."

    await callback.message.edit_text(full_text, parse_mode="HTML", reply_markup=admin_kb())
    await callback.answer()
