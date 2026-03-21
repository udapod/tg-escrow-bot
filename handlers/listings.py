from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
import html as html_lib

import database as db
from keyboards import (
    categories_kb,
    listing_card_kb,
    my_listing_kb,
    main_menu_kb,
    confirm_cancel_kb,
)
from config import CATEGORIES, MIN_DEAL_AMOUNT, COUNTRIES, get_reputation_level
from languages import t, all_btn_texts, get_category_name

router = Router()


class CreateListing(StatesGroup):
    category = State()
    title = State()
    description = State()
    price = State()
    photo = State()


class SearchState(StatesGroup):
    waiting_query = State()


# ————— Отмена создания объявления —————

@router.message(Command("cancel"), CreateListing.title)
@router.message(Command("cancel"), CreateListing.description)
@router.message(Command("cancel"), CreateListing.price)
@router.message(Command("cancel"), CreateListing.photo)
@router.message(Command("cancel"), CreateListing.category)
async def cancel_create_listing(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.clear()
    await message.answer(t(lang, "create_listing_cancelled"), reply_markup=main_menu_kb(lang))


# ————— Создание объявления —————

@router.message(F.text.in_(all_btn_texts("btn_create_listing")))
async def start_create_listing(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer(t(lang, "press_start_first"))
        return
    if user["is_banned"]:
        await message.answer(t(lang, "account_banned"))
        return
    if not user["wallet"]:
        await message.answer(t(lang, "set_wallet_first"), parse_mode="HTML")
        return
    if not user.get("country") or not user.get("city"):
        await message.answer(t(lang, "set_location_first"))
        return

    await message.answer(t(lang, "choose_category"), reply_markup=categories_kb("cat", lang))
    await state.set_state(CreateListing.category)


@router.callback_query(F.data.startswith("cat_"), CreateListing.category)
async def listing_category_chosen(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_lang(callback.from_user.id)
    category = callback.data.split("_", 1)[1]
    if category not in CATEGORIES:
        await callback.answer(t(lang, "invalid_category"), show_alert=True)
        return

    await state.update_data(category=category)
    cat_name = get_category_name(category, lang)
    await callback.message.edit_text(
        f"{cat_name}\n\n{t(lang, 'enter_title')}",
        parse_mode="HTML",
    )
    await state.set_state(CreateListing.title)
    await callback.answer()


@router.message(CreateListing.title)
async def listing_title_entered(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    title = message.text.strip()
    # Защита от команд как названия
    if title.startswith("/"):
        await message.answer(t(lang, "title_error"))
        return
    if len(title) < 3 or len(title) > 100:
        await message.answer(t(lang, "title_error"))
        return

    await state.update_data(title=title)
    await message.answer(t(lang, "enter_description"))
    await state.set_state(CreateListing.description)


@router.message(CreateListing.description)
async def listing_desc_entered(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    desc = message.text.strip()
    if len(desc) < 10 or len(desc) > 500:
        await message.answer(t(lang, "desc_error"))
        return

    await state.update_data(description=desc)
    await message.answer(t(lang, "enter_price"))
    await state.set_state(CreateListing.price)


@router.message(CreateListing.price)
async def listing_price_entered(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    try:
        raw = message.text.strip().lower().replace("usdt", "").replace(" ", "").replace(",", ".")
        price = float(raw)
        if price <= 0 or price > 1_000_000:
            raise ValueError
        if price < MIN_DEAL_AMOUNT:
            await message.answer(t(lang, "price_min_error", amount=MIN_DEAL_AMOUNT))
            return
    except ValueError:
        await message.answer(t(lang, "price_error"))
        return

    await state.update_data(price=price)
    await message.answer(t(lang, "enter_photo"))
    await state.set_state(CreateListing.photo)


@router.message(CreateListing.photo, F.photo)
async def listing_photo_received(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await _save_listing(message, state, lang)


@router.message(Command("skip"), CreateListing.photo)
async def listing_photo_skip(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.update_data(photo_id="")
    await _save_listing(message, state, lang)


@router.message(CreateListing.photo)
async def listing_photo_invalid(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await message.answer(t(lang, "enter_photo"))


async def _save_listing(message: Message, state: FSMContext, lang: str):
    data = await state.get_data()
    price = data["price"]
    country, city = await db.get_user_location(message.from_user.id)
    listing_id = await db.create_listing(
        seller_id=message.from_user.id,
        category=data["category"],
        title=data["title"],
        description=data["description"],
        price=price,
        photo_id=data.get("photo_id", ""),
        country=country,
        city=city,
    )
    await state.clear()

    cat_name = get_category_name(data["category"], lang)
    await message.answer(
        t(lang, "listing_created", id=listing_id, cat=cat_name, title=data["title"], price=price),
        parse_mode="HTML",
        reply_markup=main_menu_kb(lang),
    )

    # Уведомить подписчиков продавца
    bot: Bot = message.bot
    seller = await db.get_user(message.from_user.id)
    seller_name = seller["full_name"] if seller else "—"
    followers = await db.get_seller_followers(message.from_user.id)
    notified_count = 0
    for follower_id in followers:
        try:
            f_lang = await db.get_user_lang(follower_id)
            notify_text = t(f_lang, "new_listing_notify_follower",
                            seller=html_lib.escape(seller_name),
                            title=html_lib.escape(data["title"]),
                            price=price, city=city or "—")
            kb = listing_card_kb(listing_id, message.from_user.id, f_lang)
            if data.get("photo_id"):
                await bot.send_photo(
                    follower_id, photo=data["photo_id"],
                    caption=notify_text, parse_mode="HTML", reply_markup=kb,
                )
            else:
                await bot.send_message(
                    follower_id, notify_text,
                    parse_mode="HTML", reply_markup=kb,
                )
            notified_count += 1
        except Exception:
            pass
    if notified_count > 0:
        await message.answer(t(lang, "followers_notified", count=notified_count))


# ————— Поиск —————

@router.message(F.text.in_(all_btn_texts("btn_search")))
async def cmd_search(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await message.answer(t(lang, "search_prompt"), parse_mode="HTML")
    await state.set_state(SearchState.waiting_query)


@router.message(SearchState.waiting_query)
async def search_query_entered(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    query = message.text.strip() if message.text else ""

    if len(query) < 2:
        await message.answer(t(lang, "search_too_short"))
        return

    await state.clear()

    listings = await db.search_listings(query)

    if not listings:
        await message.answer(
            t(lang, "search_no_results", query=query),
            parse_mode="HTML",
            reply_markup=main_menu_kb(lang),
        )
        return

    # Показываем первую страницу результатов
    await _show_search_results(message, listings, query, 0, lang)


async def _show_search_results(message: Message, listings: list, query: str, page: int, lang: str):
    """Показать страницу результатов поиска."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    total = len(listings)
    total_pages = (total + LISTINGS_PER_PAGE - 1) // LISTINGS_PER_PAGE
    page = min(page, total_pages - 1)
    start = page * LISTINGS_PER_PAGE
    end = start + LISTINGS_PER_PAGE
    page_listings = listings[start:end]

    header = t(lang, "search_results", query=query, count=total)
    if total_pages > 1:
        header += f"  ({t(lang, 'page_label')} {page + 1}/{total_pages})"

    await message.answer(header, parse_mode="HTML", reply_markup=main_menu_kb(lang))

    for lst in page_listings:
        seller = await db.get_user(lst["seller_id"])
        seller_name = seller["full_name"] if seller else t(lang, "unknown_seller")
        seller_rating = f"{seller['rating']:.1f}" if seller else "—"
        vip_badge = "👑 " if seller and await db.is_vip(lst["seller_id"]) else ""
        rep_name, rep_emoji, _ = get_reputation_level(seller["deals_count"] if seller else 0)
        listing_city = lst.get("city", "")

        card_text = (
            f"{vip_badge}📌 <b>{html_lib.escape(lst['title'])}</b>\n"
            f"📋 {html_lib.escape(lst['description'])}\n\n"
            f"💰 {t(lang, 'price_label')}: <b>{lst['price']} USDT</b>\n"
            f"📍 {t(lang, 'listing_city')}: {html_lib.escape(listing_city)}\n"
            f"👤 {t(lang, 'seller')}: {vip_badge}{rep_emoji} {html_lib.escape(seller_name)} (⭐ {seller_rating})\n"
            f"🆔 #{lst['id']}"
        )
        kb = listing_card_kb(lst["id"], lst["seller_id"], lang)

        if lst.get("photo_id"):
            await message.answer_photo(
                photo=lst["photo_id"],
                caption=card_text,
                parse_mode="HTML",
                reply_markup=kb,
            )
        else:
            await message.answer(
                card_text,
                parse_mode="HTML",
                reply_markup=kb,
            )

    # Кнопки навигации для поиска
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton(
                text="⬅️", callback_data=f"search_p{page - 1}"))
        nav_buttons.append(InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}", callback_data="noop"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton(
                text="➡️", callback_data=f"search_p{page + 1}"))
        await message.answer(
            t(lang, 'page_label') + f" {page + 1}/{total_pages}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[nav_buttons]),
        )


# ————— Каталог —————

@router.message(F.text.in_(all_btn_texts("btn_catalog")))
async def cmd_catalog(message: Message):
    lang = await db.get_user_lang(message.from_user.id)
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer(t(lang, "press_start_first"))
        return
    if user["is_banned"]:
        await message.answer(t(lang, "account_banned"))
        return
    await message.answer(t(lang, "choose_category"), reply_markup=categories_kb("browse", lang))


LISTINGS_PER_PAGE = 5


@router.callback_query(F.data.startswith("browse_"))
async def cb_browse_category(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    raw = callback.data.split("_", 1)[1]

    # Парсим номер страницы: browse_{category}_p{page}
    import re
    page_match = re.search(r'_p(\d+)$', raw)
    page = int(page_match.group(1)) if page_match else 0
    if page_match:
        raw = raw[:page_match.start()]

    # Формат: browse_{category} или browse_{category}_all (все города в стране)
    show_all_cities = raw.endswith("_all")
    category = raw.rsplit("_all", 1)[0] if show_all_cities else raw

    # Валидация категории
    if category not in CATEGORIES:
        await callback.answer(t(lang, "invalid_category"), show_alert=True)
        return

    country, city = await db.get_user_location(callback.from_user.id)

    if country and city and not show_all_cities:
        listings = await db.get_active_listings(category=category, country=country, city=city, limit=500)
    elif country:
        listings = await db.get_active_listings(category=category, country=country, limit=500)
    else:
        listings = await db.get_active_listings(category=category, limit=500)

    cat_name = get_category_name(category, lang)

    if not listings:
        if country and city and not show_all_cities:
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text=t(lang, "all_cities"),
                    callback_data=f"browse_{category}_all",
                )
            ]])
            await callback.message.edit_text(
                t(lang, "no_listings_in_cat", cat=cat_name)
                + f"\n\n📍 {city}",
                parse_mode="HTML",
                reply_markup=kb,
            )
        else:
            await callback.message.edit_text(
                t(lang, "no_listings_in_cat", cat=cat_name),
                parse_mode="HTML",
            )
        await callback.answer()
        return

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    total = len(listings)
    total_pages = (total + LISTINGS_PER_PAGE - 1) // LISTINGS_PER_PAGE
    page = min(page, total_pages - 1)
    start = page * LISTINGS_PER_PAGE
    end = start + LISTINGS_PER_PAGE
    page_listings = listings[start:end]

    browse_suffix = f"{category}_all" if show_all_cities else category

    location_label = city if (city and not show_all_cities) else COUNTRIES.get(country, {}).get("name", "")

    # Навигационные кнопки
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️", callback_data=f"browse_{browse_suffix}_p{page - 1}"))
    nav_buttons.append(InlineKeyboardButton(
        text=f"{page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="➡️", callback_data=f"browse_{browse_suffix}_p{page + 1}"))

    nav_kb = InlineKeyboardMarkup(inline_keyboard=[nav_buttons]) if total_pages > 1 else None

    header = t(lang, "listings_found", cat=cat_name, count=total)
    if location_label:
        header += f"  📍 {location_label}"
    if total_pages > 1:
        header += f"  ({t(lang, 'page_label')} {page + 1}/{total_pages})"

    await callback.message.edit_text(header, parse_mode="HTML", reply_markup=nav_kb)
    await callback.answer()

    for lst in page_listings:
        seller = await db.get_user(lst["seller_id"])
        seller_name = seller["full_name"] if seller else t(lang, "unknown_seller")
        seller_rating = f"{seller['rating']:.1f}" if seller else "—"
        vip_badge = "👑 " if seller and await db.is_vip(lst["seller_id"]) else ""
        rep_name, rep_emoji, _ = get_reputation_level(seller["deals_count"] if seller else 0)
        listing_city = lst.get("city", "")

        card_text = (
            f"{vip_badge}📌 <b>{html_lib.escape(lst['title'])}</b>\n"
            f"📋 {html_lib.escape(lst['description'])}\n\n"
            f"💰 {t(lang, 'price_label')}: <b>{lst['price']} USDT</b>\n"
            f"📍 {t(lang, 'listing_city')}: {html_lib.escape(listing_city)}\n"
            f"👤 {t(lang, 'seller')}: {vip_badge}{rep_emoji} {html_lib.escape(seller_name)} (⭐ {seller_rating})\n"
            f"🆔 #{lst['id']}"
        )
        kb = listing_card_kb(lst["id"], lst["seller_id"], lang)

        if lst.get("photo_id"):
            await callback.message.answer_photo(
                photo=lst["photo_id"],
                caption=card_text,
                parse_mode="HTML",
                reply_markup=kb,
            )
        else:
            await callback.message.answer(
                card_text,
                parse_mode="HTML",
                reply_markup=kb,
            )


@router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery):
    await callback.answer()


# ————— Мои объявления —————

@router.message(F.text.in_(all_btn_texts("btn_my_listings")))
async def cmd_my_listings(message: Message):
    lang = await db.get_user_lang(message.from_user.id)
    listings = await db.get_user_listings(message.from_user.id)
    if not listings:
        await message.answer(t(lang, "no_my_listings"))
        return

    for lst in listings:
        status = t(lang, "listing_active") if lst["is_active"] else t(lang, "listing_inactive")
        cat_name = get_category_name(lst["category"], lang)
        listing_city = lst.get("city", "")
        city_line = f"📍 {listing_city}\n" if listing_city else ""
        card_text = (
            f"📌 <b>{html_lib.escape(lst['title'])}</b>\n"
            f"💰 {lst['price']} USDT\n"
            f"📂 {cat_name}\n"
            f"{city_line}"
            f"{t(lang, 'status_label')}: {status}\n"
            f"🆔 #{lst['id']}"
        )
        kb = my_listing_kb(lst["id"], lang) if lst["is_active"] else None

        if lst.get("photo_id"):
            await message.answer_photo(
                photo=lst["photo_id"],
                caption=card_text,
                parse_mode="HTML",
                reply_markup=kb,
            )
        else:
            await message.answer(
                card_text,
                parse_mode="HTML",
                reply_markup=kb,
            )


@router.callback_query(F.data.startswith("del_listing_"))
async def cb_delete_listing(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    listing_id = int(callback.data.split("_")[-1])
    listing = await db.get_listing(listing_id)

    if not listing or listing["seller_id"] != callback.from_user.id:
        await callback.answer(t(lang, "listing_unavailable"), show_alert=True)
        return

    confirm_text = t(lang, "confirm_delete_listing", id=listing_id, title=listing["title"])
    kb = confirm_cancel_kb("dellst", listing_id, lang)

    if callback.message.photo:
        await callback.message.edit_caption(caption=confirm_text, reply_markup=kb)
    else:
        await callback.message.edit_text(confirm_text, reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data.startswith("yes_dellst_"))
async def cb_confirm_delete_listing(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    listing_id = int(callback.data.split("_")[-1])
    listing = await db.get_listing(listing_id)
    if listing and listing["seller_id"] == callback.from_user.id:
        await db.deactivate_listing(listing_id)
        if callback.message.photo:
            await callback.message.edit_caption(caption=t(lang, "listing_deleted"))
        else:
            await callback.message.edit_text(t(lang, "listing_deleted"))
    else:
        await callback.answer(t(lang, "listing_unavailable"), show_alert=True)
    await callback.answer()


@router.callback_query(F.data.startswith("no_dellst_"))
async def cb_cancel_delete_listing(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    if callback.message.photo:
        await callback.message.edit_caption(caption=t(lang, "action_cancelled"))
    else:
        await callback.message.edit_text(t(lang, "action_cancelled"))
    await callback.answer()
