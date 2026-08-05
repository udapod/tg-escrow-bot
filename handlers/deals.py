from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
import html as html_lib
import logging

import database as db
from keyboards import (
    deal_pay_escrow_kb,
    deal_seller_deliver_kb,
    deal_buyer_confirm_kb,
    deal_complete_review_kb,
    review_rating_kb,
    main_menu_kb,
)
from config import BOT_WALLET, ADMIN_ID, DealStatus, AUTO_COMPLETE_HOURS, MIN_DEAL_AMOUNT, CANCEL_PENALTY, calc_commission
from languages import t, all_btn_texts
from payments.verify import verify_payment  # <-- Replaced tron.verify_tx
from contact_filter import contains_contact

# Fallback for LTC wallet if you haven't added it to config.py yet
try:
    from config import BOT_WALLET_LTC
except ImportError:
    BOT_WALLET_LTC = BOT_WALLET

logger = logging.getLogger(__name__)

router = Router()

MAX_CHAT_MESSAGE_LEN = 2000


class TxHashState(StatesGroup):
    waiting_tx_hash = State()


class ReviewState(StatesGroup):
    waiting_comment = State()
    waiting_photo = State()


class DealChat(StatesGroup):
    chatting = State()
    meet_location = State()
    meet_datetime = State()


# ————— Начало сделки —————

@router.callback_query(F.data.startswith("buy_"))
async def cb_start_deal(callback: CallbackQuery, bot: Bot):
    buyer_lang = await db.get_user_lang(callback.from_user.id)
    listing_id = int(callback.data.split("_")[1])
    listing = await db.get_listing(listing_id)

    if not listing or not listing["is_active"]:
        await callback.answer(t(buyer_lang, "listing_unavailable"), show_alert=True)
        return

    buyer = await db.get_user(callback.from_user.id)
    if not buyer:
        await callback.answer(t(buyer_lang, "press_start_first"), show_alert=True)
        return
    if buyer["is_banned"]:
        await callback.answer(t(buyer_lang, "account_banned"), show_alert=True)
        return

    if listing["seller_id"] == callback.from_user.id:
        await callback.answer(t(buyer_lang, "cant_buy_own"), show_alert=True)
        return

    if listing["price"] < MIN_DEAL_AMOUNT:
        await callback.answer(
            t(buyer_lang, "min_deal_amount", amount=MIN_DEAL_AMOUNT),
            show_alert=True,
        )
        return

    seller = await db.get_user(listing["seller_id"])
    if not seller or not seller["wallet"]:
        await callback.answer(t(buyer_lang, "seller_no_wallet"), show_alert=True)
        return

    price = listing["price"]
    seller_is_vip = await db.is_vip(listing["seller_id"])

    # Первая сделка бесплатно (0% комиссии)
    if buyer["deals_count"] == 0:
        rate = 0
        commission = 0.0
    else:
        rate, commission = calc_commission(price, is_vip=seller_is_vip, deals_count=buyer["deals_count"])

    total = round(price + commission, 2)
    
    # Determine currency and correct escrow wallet
    currency = listing.get("currency", "USDT_TRC20")
    pay_wallet = BOT_WALLET_LTC if currency == "LTC" else BOT_WALLET

    deal_id = await db.create_deal_atomic(
        listing_id=listing_id,
        seller_id=listing["seller_id"],
        buyer_id=callback.from_user.id,
        amount=price,
        commission=commission,
        total_escrow=total,
        seller_wallet=seller["wallet"],
    )

    if not deal_id:
        await callback.answer(t(buyer_lang, "listing_unavailable"), show_alert=True)
        return

    logger.info(
        "Deal #%d created: buyer=%d seller=%d amount=%.2f escrow=%.2f listing=%d",
        deal_id, callback.from_user.id, listing["seller_id"], price, total, listing_id,
    )

    if buyer["deals_count"] == 0:
        vip_note = t(buyer_lang, "first_deal_free_note")
    elif seller_is_vip:
        vip_note = t(buyer_lang, "vip_seller_note")
    else:
        vip_note = ""

    # Сообщение покупателю
    await callback.message.answer(
        t(buyer_lang, "deal_created",
          id=deal_id, vip_note=vip_note, title=listing["title"],
          price=price, rate=rate, commission=commission,
          total=total, wallet=pay_wallet),
        parse_mode="HTML",
        reply_markup=deal_pay_escrow_kb(deal_id, buyer_lang, currency),
    )

    # QR-код кошелька для удобной оплаты
    from qr_utils import generate_qr
    from aiogram.types import BufferedInputFile
    qr_buf = generate_qr(pay_wallet)
    photo = BufferedInputFile(qr_buf.read(), filename="wallet_qr.png")
    await callback.message.answer_photo(
        photo,
        caption=t(buyer_lang, "qr_wallet_caption", id=deal_id),
    )

    # Уведомление продавцу (на языке продавца)
    seller_lang = await db.get_user_lang(listing["seller_id"])
    await bot.send_message(
        listing["seller_id"],
        t(seller_lang, "deal_new_seller_notify",
          id=deal_id, title=listing["title"],
          price=price, buyer=buyer["full_name"]),
        parse_mode="HTML",
    )

    await callback.answer()


# ————— Покупатель подтверждает отправку на эскроу —————

@router.callback_query(F.data.startswith("funded_"))
async def cb_buyer_funded_escrow(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_lang(callback.from_user.id)
    deal_id = int(callback.data.split("_")[1])
    deal = await db.get_deal(deal_id)

    if not deal or deal["buyer_id"] != callback.from_user.id:
        await callback.answer(t(lang, "deal_not_found"), show_alert=True)
        return

    if deal["status"] != DealStatus.CREATED:
        await callback.answer(t(lang, "deal_status_locked"), show_alert=True)
        return

    await state.update_data(escrow_deal_id=deal_id)
    await callback.message.edit_text(
        t(lang, "enter_tx_hash", id=deal_id),
        parse_mode="HTML",
    )
    await state.set_state(TxHashState.waiting_tx_hash)
    await callback.answer()


MAX_TX_ATTEMPTS = 3


@router.message(TxHashState.waiting_tx_hash)
async def tx_hash_entered(message: Message, state: FSMContext, bot: Bot):
    lang = await db.get_user_lang(message.from_user.id)
    tx_hash = message.text.strip()

    if len(tx_hash) < 20 or len(tx_hash) > 128:
        await message.answer(t(lang, "tx_hash_invalid"))
        return

    data = await state.get_data()
    deal_id = data.get("escrow_deal_id")
    attempts = data.get("tx_attempts", 0)
    if not deal_id:
        await state.clear()
        await message.answer(t(lang, "error_try_again"))
        return

    deal = await db.get_deal(deal_id)
    if not deal or deal["status"] != DealStatus.CREATED:
        await state.clear()
        await message.answer(t(lang, "deal_status_changed"))
        return

    # Защита от переиспользования tx hash
    if await db.is_tx_hash_used(tx_hash):
        await message.answer(t(lang, "tx_already_used"))
        return

    listing = await db.get_listing(deal["listing_id"])
    title = listing["title"] if listing else "—"
    price = deal["amount"]

    # --- Автопроверка TxHash (TRC20 / LTC) ---
    verifying_msg = await message.answer(t(lang, "tx_verifying"))
    
    currency = deal.get("currency", "USDT_TRC20")
    is_valid = await verify_payment(
        currency=currency,
        tx_hash=tx_hash,
        amount=deal["total_escrow"]
    )
    
    # Map to original expected result format to preserve error handling logic
    result = {"ok": True} if is_valid else {"ok": False, "error": "tx_network_error"}

    if not result["ok"]:
        attempts += 1
        await state.update_data(tx_attempts=attempts)
        error_key = result.get("error", "tx_network_error")
        kwargs = {}
        if error_key == "tx_amount_mismatch":
            kwargs = {"expected": deal["total_escrow"], "received": result.get("received", "?")}
        await verifying_msg.delete()

        # Уведомление админу о неудачной попытке
        reason = t("ru", error_key, **kwargs)
        try:
            await bot.send_message(
                ADMIN_ID,
                t("ru", "tx_admin_failed",
                  id=deal_id, title=title,
                  buyer_id=message.from_user.id,
                  seller_id=deal["seller_id"],
                  amount=deal["total_escrow"],
                  reason=reason, tx=tx_hash, attempt=attempts),
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error("Failed to notify admin about tx fail: %s", e)

        # Блокировка после 3 неудачных попыток
        if attempts >= MAX_TX_ATTEMPTS:
            await state.clear()
            await db.update_deal_status(deal_id, DealStatus.CANCELLED)
            # Возвращаем объявление в активное
            await db.activate_listing(deal["listing_id"])
            await message.answer(t(lang, "tx_blocked"))
            try:
                await bot.send_message(
                    ADMIN_ID,
                    t("ru", "tx_admin_blocked",
                      id=deal_id, title=title,
                      buyer_id=message.from_user.id,
                      seller_id=deal["seller_id"],
                      amount=deal["total_escrow"]),
                    parse_mode="HTML",
                )
            except Exception as e:
                logger.error("Failed to notify admin about tx block: %s", e)
            return

        await message.answer(t(lang, error_key, **kwargs))
        return  # остаёмся в FSM, buyer может ввести заново

    await verifying_msg.delete()
    if not result.get("skipped"):
        await message.answer(t(lang, "tx_verified"))

    # Уведомление админу об успешной верификации
    try:
        await bot.send_message(
            ADMIN_ID,
            t("ru", "tx_admin_verified",
              id=deal_id, title=title,
              buyer_id=message.from_user.id,
              seller_id=deal["seller_id"],
              price=price,
              amount=deal["total_escrow"], tx=tx_hash),
            parse_mode="HTML",
        )
    except Exception as e:
        logger.error("Failed to notify admin about tx verify: %s", e)
    # --- конец автопроверки ---

    await db.set_buyer_tx_hash(deal_id, tx_hash)
    await db.update_deal_status(deal_id, DealStatus.PAID)
    logger.info("Deal #%d PAID: tx=%s buyer=%d amount=%.2f", deal_id, tx_hash, message.from_user.id, deal["total_escrow"])
    await state.clear()

    await message.answer(
        t(lang, "deal_paid", id=deal_id, title=title,
          total=deal["total_escrow"], tx=tx_hash),
        parse_mode="HTML",
    )

    # Уведомление о разблокировке контактов
    await message.answer(t(lang, "chat_contacts_unlocked"))

    # Уведомление продавцу
    seller_lang = await db.get_user_lang(deal["seller_id"])
    await bot.send_message(
        deal["seller_id"],
        t(seller_lang, "deal_escrow_seller_notify",
          id=deal_id, title=title,
          total=deal["total_escrow"], tx=tx_hash),
        parse_mode="HTML",
        reply_markup=deal_seller_deliver_kb(deal_id, seller_lang),
    )
    # Уведомление продавцу о разблокировке контактов
    await bot.send_message(
        deal["seller_id"],
        t(seller_lang, "chat_contacts_unlocked"),
    )


# ————— Продавец отмечает выполнение —————

@router.callback_query(F.data.startswith("delivered_"))
async def cb_seller_delivered(callback: CallbackQuery, bot: Bot):
    lang = await db.get_user_lang(callback.from_user.id)
    deal_id = int(callback.data.split("_")[1])
    deal = await db.get_deal(deal_id)

    if not deal or deal["seller_id"] != callback.from_user.id:
        await callback.answer(t(lang, "deal_not_found"), show_alert=True)
        return

    if deal["status"] != DealStatus.PAID:
        await callback.answer(t(lang, "deal_not_at_execution"), show_alert=True)
        return

    await db.mark_delivered(deal_id)

    listing = await db.get_listing(deal["listing_id"])
    title = listing["title"] if listing else "—"

    await callback.message.edit_text(
        t(lang, "deal_delivered_seller", id=deal_id, hours=AUTO_COMPLETE_HOURS),
        parse_mode="HTML",
    )

    # Уведомление покупателю
    buyer_lang = await db.get_user_lang(deal["buyer_id"])
    seller = await db.get_user(deal["seller_id"])
    await bot.send_message(
        deal["buyer_id"],
        t(buyer_lang, "deal_delivered_buyer_notify",
          id=deal_id, title=title,
          seller=seller["full_name"], hours=AUTO_COMPLETE_HOURS),
        parse_mode="HTML",
        reply_markup=deal_buyer_confirm_kb(deal_id, buyer_lang),
    )

    await callback.answer()


# ————— Покупатель подтверждает получение → АВТОЗАВЕРШЕНИЕ —————

@router.callback_query(F.data.startswith("confirm_"))
async def cb_buyer_confirm(callback: CallbackQuery, bot: Bot):
    lang = await db.get_user_lang(callback.from_user.id)
    deal_id = int(callback.data.split("_")[1])
    deal = await db.get_deal(deal_id)

    if not deal or deal["buyer_id"] != callback.from_user.id:
        await callback.answer(t(lang, "deal_not_found"), show_alert=True)
        return

    if deal["status"] not in (DealStatus.PAID, DealStatus.DELIVERED):
        await callback.answer(t(lang, "cant_confirm_now"), show_alert=True)
        return

    await db.update_deal_status(deal_id, DealStatus.COMPLETED)
    logger.info("Deal #%d COMPLETED: buyer=%d seller=%d payout=%.2f", deal_id, deal["buyer_id"], deal["seller_id"], deal["amount"])
    await db.increment_deals_count(deal["seller_id"])
    await db.increment_deals_count(deal["buyer_id"])

    listing = await db.get_listing(deal["listing_id"])
    title = listing["title"] if listing else "—"
    payout = round(deal["amount"], 2)
    currency = deal.get("currency", "USDT")

    await callback.message.edit_text(
        t(lang, "deal_completed_buyer",
          id=deal_id, title=title, payout=payout, commission=deal["commission"]),
        parse_mode="HTML",
        reply_markup=deal_complete_review_kb(deal_id, lang),
    )

    # Уведомление продавцу
    seller_lang = await db.get_user_lang(deal["seller_id"])
    await bot.send_message(
        deal["seller_id"],
        t(seller_lang, "deal_completed_seller_notify",
          id=deal_id, title=title, payout=payout,
          wallet=deal["seller_wallet"]),
        parse_mode="HTML",
        reply_markup=deal_complete_review_kb(deal_id, seller_lang),
    )

    # Уведомление админу о выплате
    buyer = await db.get_user(deal["buyer_id"])
    seller = await db.get_user(deal["seller_id"])
    await bot.send_message(
        ADMIN_ID,
        f"💸 <b>ВЫПЛАТА — Сделка #{deal_id}</b>\n\n"
        f"Продавец: {html_lib.escape(seller['full_name'])} (ID: {deal['seller_id']})\n"
        f"Покупатель: {html_lib.escape(buyer['full_name'])} (ID: {deal['buyer_id']})\n"
        f"💵 Отправить продавцу: <b>{payout} {currency}</b>\n"
        f"📊 Комиссия бота: {deal['commission']} {currency}\n"
        f"🏦 Кошелёк продавца: <code>{deal['seller_wallet']}</code>",
        parse_mode="HTML",
    )

    await callback.answer()


# ————— Отмена сделки —————

@router.callback_query(F.data.startswith("cancel_deal_"))
async def cb_cancel_deal(callback: CallbackQuery, bot: Bot):
    lang = await db.get_user_lang(callback.from_user.id)
    deal_id = int(callback.data.split("_")[-1])
    deal = await db.get_deal(deal_id)

    if not deal or deal["buyer_id"] != callback.from_user.id:
        await callback.answer(t(lang, "deal_not_found"), show_alert=True)
        return

    # До оплаты — отмена бесплатная
    if deal["status"] == DealStatus.CREATED:
        await db.update_deal_status(deal_id, DealStatus.CANCELLED)
        # Возвращаем объявление в активное состояние
        await db.activate_listing(deal["listing_id"])
        await callback.message.edit_text(t(lang, "deal_cancelled", id=deal_id))

        seller_lang = await db.get_user_lang(deal["seller_id"])
        await bot.send_message(
            deal["seller_id"],
            t(seller_lang, "deal_cancelled_seller_notify", id=deal_id),
        )
        await callback.answer()
        return

    # После оплаты — отмена со штрафом
    if deal["status"] in (DealStatus.PAID, DealStatus.DELIVERED):
        currency = deal.get("currency", "USDT")
        penalty = round(deal["amount"] * CANCEL_PENALTY / 100, 2)
        if penalty < MIN_COMMISSION:
            penalty = MIN_COMMISSION
        # Штраф не может превышать сумму на эскроу
        if penalty > deal["total_escrow"]:
            penalty = deal["total_escrow"]
        refund = round(deal["total_escrow"] - penalty, 2)

        await db.update_deal_status(deal_id, DealStatus.REFUNDED)
        await db.activate_listing(deal["listing_id"])

        listing = await db.get_listing(deal["listing_id"])
        title = listing["title"] if listing else "—"

        await callback.message.edit_text(
            t(lang, "deal_cancelled_penalty",
              id=deal_id, penalty_pct=CANCEL_PENALTY,
              penalty=penalty, refund=refund),
            parse_mode="HTML",
        )

        seller_lang = await db.get_user_lang(deal["seller_id"])
        await bot.send_message(
            deal["seller_id"],
            t(seller_lang, "deal_cancelled_seller_after_pay", id=deal_id, title=title),
        )

        # Уведомление админу о штрафе
        buyer = await db.get_user(deal["buyer_id"])
        await bot.send_message(
            ADMIN_ID,
            f"⚠️ <b>ОТМЕНА СО ШТРАФОМ — Сделка #{deal_id}</b>\n\n"
            f"📌 {title}\n"
            f"Покупатель: {html_lib.escape(buyer['full_name'])} (ID: {deal['buyer_id']})\n"
            f"💰 На эскроу: {deal['total_escrow']} {currency}\n"
            f"🔻 Штраф ({CANCEL_PENALTY}%): <b>{penalty} {currency}</b>\n"
            f"💸 Возврат покупателю: <b>{refund} {currency}</b>",
            parse_mode="HTML",
        )

        await callback.answer()
        return

    await callback.answer(t(lang, "cancel_not_available"), show_alert=True)


# ————— Спор —————

@router.callback_query(F.data.startswith("dispute_"))
async def cb_open_dispute(callback: CallbackQuery, bot: Bot):
    lang = await db.get_user_lang(callback.from_user.id)
    deal_id = int(callback.data.split("_")[1])
    deal = await db.get_deal(deal_id)

    if not deal:
        await callback.answer(t(lang, "deal_not_found"), show_alert=True)
        return

    if callback.from_user.id not in (deal["seller_id"], deal["buyer_id"]):
        await callback.answer(t(lang, "no_access"), show_alert=True)
        return

    if deal["status"] not in (DealStatus.PAID, DealStatus.DELIVERED):
        await callback.answer(t(lang, "dispute_only_escrow"), show_alert=True)
        return

    await db.update_deal_status(deal_id, DealStatus.DISPUTED)

    await callback.message.edit_text(
        t(lang, "dispute_opened", id=deal_id),
        parse_mode="HTML",
    )

    # Уведомление второй стороне
    other_id = deal["buyer_id"] if callback.from_user.id == deal["seller_id"] else deal["seller_id"]
    other_lang = await db.get_user_lang(other_id)
    await bot.send_message(
        other_id,
        t(other_lang, "dispute_other_notify", id=deal_id),
    )

    # Уведомление админу (на русском)
    buyer = await db.get_user(deal["buyer_id"])
    seller = await db.get_user(deal["seller_id"])
    initiator = "Покупатель" if callback.from_user.id == deal["buyer_id"] else "Продавец"
    listing = await db.get_listing(deal["listing_id"])
    title = listing["title"] if listing else "—"
    currency = deal.get("currency", "USDT")

    await bot.send_message(
        ADMIN_ID,
        f"🚨 <b>СПОР по сделке #{deal_id}</b>\n\n"
        f"📌 {html_lib.escape(title)}\n"
        f"Инициатор: {initiator}\n"
        f"👤 Продавец: {html_lib.escape(seller['full_name'])} (ID: {deal['seller_id']})\n"
        f"👤 Покупатель: {html_lib.escape(buyer['full_name'])} (ID: {deal['buyer_id']})\n"
        f"💰 На эскроу: {deal['total_escrow']} {currency}\n"
        f"🔗 TxID: <code>{deal['buyer_tx_hash']}</code>\n"
        f"🏦 Кошелёк продавца: <code>{deal['seller_wallet']}</code>\n\n"
        f"<b>Команды:</b>\n"
        f"/resolve {deal_id} seller — выплатить продавцу\n"
        f"/resolve {deal_id} buyer — вернуть покупателю\n"
        f"/chatlog {deal_id} — история переписки",
        parse_mode="HTML",
    )

    await callback.answer()


# ————— Админ: разрешение спора —————

@router.message(F.text.startswith("/resolve"))
async def cmd_resolve_deal(message: Message, bot: Bot):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()
    if len(parts) < 3:
        await message.answer(
            "Использование:\n"
            "/resolve <ID> <b>seller</b> — выплатить продавцу\n"
            "/resolve <ID> <b>buyer</b> — вернуть покупателю",
            parse_mode="HTML",
        )
        return

    if not parts[1].isdigit():
        await message.answer("ID сделки должен быть числом.")
        return

    deal_id = int(parts[1])
    action = parts[2].lower()

    deal = await db.get_deal(deal_id)
    if not deal or deal["status"] != DealStatus.DISPUTED:
        await message.answer("Сделка не найдена или не в статусе спора.")
        return

    listing = await db.get_listing(deal["listing_id"])
    title = listing["title"] if listing else "—"

    if action not in ("seller", "buyer"):
        await message.answer("Действие: <b>seller</b> или <b>buyer</b>", parse_mode="HTML")
        return

    # Подтверждение перед выполнением
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    if action == "seller":
        payout = round(deal["amount"], 2)
        confirm_text = t("ru", "resolve_confirm_seller",
                         id=deal_id, payout=payout, wallet=deal["seller_wallet"])
    else:
        confirm_text = t("ru", "resolve_confirm_buyer",
                         id=deal_id, total=deal["total_escrow"])

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да", callback_data=f"resolve_yes_{deal_id}_{action}"),
            InlineKeyboardButton(text="❌ Нет", callback_data="resolve_no"),
        ]
    ])
    await message.answer(confirm_text, parse_mode="HTML", reply_markup=kb)


@router.callback_query(F.data == "resolve_no")
async def cb_resolve_no(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    await callback.message.edit_text("❌ Отменено.")
    await callback.answer()


@router.callback_query(F.data.startswith("resolve_yes_"))
async def cb_resolve_yes(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id != ADMIN_ID:
        return

    parts = callback.data.split("_")
    deal_id = int(parts[2])
    action = parts[3]

    deal = await db.get_deal(deal_id)
    if not deal or deal["status"] != DealStatus.DISPUTED:
        await callback.message.edit_text("Сделка не найдена или уже разрешена.")
        await callback.answer()
        return

    listing = await db.get_listing(deal["listing_id"])
    title = listing["title"] if listing else "—"

    if action == "seller":
        await db.update_deal_status(deal_id, DealStatus.COMPLETED)
        logger.info("Dispute #%d resolved SELLER by admin, deal=%d", deal_id, deal_id)
        await db.increment_deals_count(deal["seller_id"])
        await db.increment_deals_count(deal["buyer_id"])
        payout = round(deal["amount"], 2)

        await callback.message.edit_text(
            f"✅ Спор #{deal_id} решён в пользу продавца.\n"
            f"💵 Отправьте {payout} USDT → <code>{deal['seller_wallet']}</code>",
            parse_mode="HTML",
        )

        seller_lang = await db.get_user_lang(deal["seller_id"])
        buyer_lang = await db.get_user_lang(deal["buyer_id"])

        await bot.send_message(
            deal["seller_id"],
            t(seller_lang, "deal_completed_seller_notify",
              id=deal_id, title=title, payout=payout, wallet=deal["seller_wallet"]),
            parse_mode="HTML",
            reply_markup=deal_complete_review_kb(deal_id, seller_lang),
        )
        await bot.send_message(
            deal["buyer_id"],
            t(buyer_lang, "deal_cancelled", id=deal_id),
            reply_markup=deal_complete_review_kb(deal_id, buyer_lang),
        )

    elif action == "buyer":
        await db.update_deal_status(deal_id, DealStatus.REFUNDED)
        logger.info("Dispute #%d resolved BUYER by admin, deal=%d refund=%.2f", deal_id, deal_id, deal["total_escrow"])
        await db.activate_listing(deal["listing_id"])

        await callback.message.edit_text(
            f"💸 Спор #{deal_id} решён в пользу покупателя.\n"
            f"Верните {deal['total_escrow']} USDT покупателю.",
        )

        buyer_lang = await db.get_user_lang(deal["buyer_id"])
        seller_lang = await db.get_user_lang(deal["seller_id"])

        await bot.send_message(
            deal["buyer_id"],
            t(buyer_lang, "deal_completed_buyer",
              id=deal_id, title=title, payout=deal["total_escrow"], commission=0),
            parse_mode="HTML",
        )
        await bot.send_message(
            deal["seller_id"],
            t(seller_lang, "deal_cancelled", id=deal_id),
        )

    await callback.answer()


# ————— Мои сделки —————

@router.message(F.text.in_(all_btn_texts("btn_my_deals")))
async def cmd_my_deals(message: Message):
    lang = await db.get_user_lang(message.from_user.id)
    deals = await db.get_user_deals(message.from_user.id)
    if not deals:
        await message.answer(t(lang, "no_deals"))
        return

    status_map = {
        DealStatus.CREATED: "deal_status_created",
        DealStatus.PAID: "deal_status_paid",
        DealStatus.DELIVERED: "deal_status_delivered",
        DealStatus.COMPLETED: "deal_status_completed",
        DealStatus.DISPUTED: "deal_status_disputed",
        DealStatus.CANCELLED: "deal_status_cancelled",
        DealStatus.REFUNDED: "deal_status_refunded",
    }

    text_parts = [t(lang, "my_deals_title") + "\n"]
    for d in deals[:15]:
        listing = await db.get_listing(d["listing_id"])
        title = listing["title"] if listing else "—"
        role = t(lang, "role_buyer") if d["buyer_id"] == message.from_user.id else t(lang, "role_seller")
        status_key = status_map.get(d["status"], "deal_status_created")
        status = t(lang, status_key)
        currency = d.get("currency", "USDT")

        text_parts.append(
            f"\n#{d['id']} — <b>{title}</b>\n"
            f"  {role} | {status}\n"
            f"  💰 {d['amount']} {currency} | 📅 {d['created_at']}"
        )

    await message.answer("\n".join(text_parts), parse_mode="HTML")


# ————— Отзывы —————

@router.callback_query(F.data.startswith("review_"))
async def cb_start_review(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    deal_id = int(callback.data.split("_")[1])
    deal = await db.get_deal(deal_id)

    if not deal or deal["status"] not in (DealStatus.COMPLETED, DealStatus.REFUNDED):
        await callback.answer(t(lang, "review_only_completed"), show_alert=True)
        return

    if callback.from_user.id not in (deal["buyer_id"], deal["seller_id"]):
        await callback.answer(t(lang, "review_not_participant"), show_alert=True)
        return

    await callback.message.answer(
        t(lang, "review_rate", id=deal_id),
        reply_markup=review_rating_kb(deal_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("rate_"))
async def cb_rate_deal(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_lang(callback.from_user.id)
    parts = callback.data.split("_")
    deal_id = int(parts[1])
    rating = int(parts[2])

    deal = await db.get_deal(deal_id)
    if not deal or deal["status"] not in (DealStatus.COMPLETED, DealStatus.REFUNDED):
        await callback.answer(t(lang, "error_try_again"), show_alert=True)
        return

    if callback.from_user.id == deal["buyer_id"]:
        target_id = deal["seller_id"]
    else:
        target_id = deal["buyer_id"]

    await state.update_data(review_deal_id=deal_id, review_target_id=target_id, review_rating=rating)
    await callback.message.edit_text(
        f"{'⭐' * rating}\n\n{t(lang, 'review_comment')}"
    )
    await state.set_state(ReviewState.waiting_comment)
    await callback.answer()


@router.message(ReviewState.waiting_comment)
async def review_comment_entered(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    data = await state.get_data()
    comment = message.text.strip() if message.text.strip() != "-" else ""

    if len(comment) > 300:
        await message.answer(t(lang, "review_comment_too_long"))
        return

    await state.update_data(review_comment=comment)
    await message.answer(t(lang, "review_photo_prompt"))
    await state.set_state(ReviewState.waiting_photo)


@router.message(ReviewState.waiting_photo, F.photo)
async def review_photo_received(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    photo_id = message.photo[-1].file_id
    await _save_review(message, state, lang, photo_id)


@router.message(Command("skip"), ReviewState.waiting_photo)
async def review_photo_skip(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await _save_review(message, state, lang, "")


@router.message(ReviewState.waiting_photo)
async def review_photo_invalid(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await message.answer(t(lang, "review_photo_prompt"))


async def _save_review(message: Message, state: FSMContext, lang: str, photo_id: str):
    data = await state.get_data()
    comment = data.get("review_comment", "")

    await db.create_review(
        deal_id=data["review_deal_id"],
        reviewer_id=message.from_user.id,
        target_id=data["review_target_id"],
        rating=data["review_rating"],
        comment=comment,
        photo_id=photo_id,
    )

    await state.clear()
    review_text = (
        f"{t(lang, 'review_saved')} {'⭐' * data['review_rating']}\n"
        f"{'💬 ' + comment if comment else ''}"
    )
    if photo_id:
        review_text += "\n📸 Фото прикреплено"
    await message.answer(review_text, reply_markup=main_menu_kb(lang))


# ————— Админ: просмотр споров —————

@router.callback_query(F.data == "admin_disputes")
async def cb_admin_disputes(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

     disputes = await db.fetch(
        "SELECT * FROM deals WHERE status = 'disputed' ORDER BY updated_at DESC"
    )

    if not disputes:
        await callback.message.edit_text("✅ Активных споров нет.")
        await callback.answer()
        return

    text_parts = ["⚖️ <b>Активные споры:</b>\n"]
    for d in disputes:
        currency = d.get("currency", "USDT")
        text_parts.append(
            f"\n#{d['id']} | 💰 {d['total_escrow']} {currency}\n"
            f"  Продавец: {d['seller_id']} | Покупатель: {d['buyer_id']}\n"
            f"  🔗 TxID: <code>{d['buyer_tx_hash']}</code>\n"
            f"  /resolve {d['id']} seller | buyer"
        )

    await callback.message.edit_text("\n".join(text_parts), parse_mode="HTML")
    await callback.answer()


# ————— Админ: просмотр эскроу-сделок —————

@router.callback_query(F.data == "admin_escrow")
async def cb_admin_escrow(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    escrow_deals = await db.get_active_escrow_deals()

    if not escrow_deals:
        await callback.message.edit_text("✅ Нет активных эскроу-сделок.")
        await callback.answer()
        return

    status_map = {
        DealStatus.PAID: "🔐 На эскроу",
        DealStatus.DELIVERED: "📦 Доставлено",
        DealStatus.DISPUTED: "⚠️ Спор",
    }
    text_parts = ["🔒 <b>Эскроу-сделки (средства заморожены):</b>\n"]
    for d in escrow_deals[:20]:
        st = status_map.get(d["status"], d["status"])
        currency = d.get("currency", "USDT")
        text_parts.append(
            f"\n#{d['id']} | {st} | 💰 {d['total_escrow']} {currency}\n"
            f"  🏦 → <code>{d['seller_wallet']}</code>"
        )

    await callback.message.edit_text("\n".join(text_parts), parse_mode="HTML")
    await callback.answer()


# ————— Фоновая задача: авто-завершение по таймеру —————

async def auto_complete_expired_deals(bot: Bot):
    """Автоматически завершает сделки в статусе 'delivered',
    у которых покупатель не подтвердил и не открыл спор за AUTO_COMPLETE_HOURS."""
    expired = await db.get_expired_delivered_deals(AUTO_COMPLETE_HOURS)

    for deal in expired:
        deal_id = deal["id"]
        await db.update_deal_status(deal_id, DealStatus.COMPLETED)
        await db.increment_deals_count(deal["seller_id"])
        await db.increment_deals_count(deal["buyer_id"])

        listing = await db.get_listing(deal["listing_id"])
        title = listing["title"] if listing else "—"
        payout = round(deal["amount"], 2)
        currency = deal.get("currency", "USDT")

        # Уведомление покупателю
        try:
            buyer_lang = await db.get_user_lang(deal["buyer_id"])
            await bot.send_message(
                deal["buyer_id"],
                t(buyer_lang, "deal_completed_buyer",
                  id=deal_id, title=title, payout=payout, commission=deal["commission"]),
                parse_mode="HTML",
                reply_markup=deal_complete_review_kb(deal_id, buyer_lang),
            )
        except Exception as e:
            logger.error("Auto-complete notify buyer error deal #%d: %s", deal_id, e)

        # Уведомление продавцу
        try:
            seller_lang = await db.get_user_lang(deal["seller_id"])
            await bot.send_message(
                deal["seller_id"],
                t(seller_lang, "deal_completed_seller_notify",
                  id=deal_id, title=title, payout=payout,
                  wallet=deal["seller_wallet"]),
                parse_mode="HTML",
                reply_markup=deal_complete_review_kb(deal_id, seller_lang),
            )
        except Exception as e:
            logger.error("Auto-complete notify seller error deal #%d: %s", deal_id, e)

        # Уведомление админу (русский)
        try:
            seller = await db.get_user(deal["seller_id"])
            await bot.send_message(
                ADMIN_ID,
                f"💸 <b>АВТО-ВЫПЛАТА — Сделка #{deal_id}</b>\n\n"
                f"Продавец: {html_lib.escape(seller['full_name']) if seller else deal['seller_id']}\n"
                f"💵 Отправить: <b>{payout} {currency}</b>\n"
                f"🏦 Кошелёк: <code>{deal['seller_wallet']}</code>",
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error("Auto-complete notify admin error deal #%d: %s", deal_id, e)


# ————— Чат сделки —————

@router.callback_query(F.data.startswith("dealchat_"))
async def cb_deal_chat(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_lang(callback.from_user.id)
    deal_id = int(callback.data.split("_")[1])
    deal = await db.get_deal(deal_id)

    if not deal:
        await callback.answer(t(lang, "deal_not_found"), show_alert=True)
        return

    uid = callback.from_user.id
    if uid not in (deal["seller_id"], deal["buyer_id"]):
        await callback.answer(t(lang, "no_access"), show_alert=True)
        return

    active_statuses = (DealStatus.CREATED, DealStatus.PAID, DealStatus.DELIVERED, DealStatus.DISPUTED)
    if deal["status"] not in active_statuses:
        await callback.answer(t(lang, "chat_no_deal"), show_alert=True)
        return

    role = "seller" if uid == deal["seller_id"] else "buyer"
    role_label = t(lang, f"chat_role_{role}")
    other_id = deal["buyer_id"] if role == "seller" else deal["seller_id"]

    await state.set_state(DealChat.chatting)
    await state.update_data(chat_deal_id=deal_id, chat_role=role, chat_other_id=other_id)

    await callback.message.answer(
        t(lang, "chat_enter", id=deal_id, role=role_label),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(DealChat.chatting, F.text == "/endchat")
async def cmd_end_chat(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.clear()
    await message.answer(t(lang, "chat_exited"), reply_markup=main_menu_kb(lang))


# ————— /meet — предложить встречу —————

@router.message(DealChat.chatting, F.text == "/meet")
async def cmd_meet_start(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.set_state(DealChat.meet_location)
    await message.answer(t(lang, "meet_enter_location"))


@router.message(DealChat.meet_location, F.text == "/endchat")
async def cmd_end_chat_from_meet_loc(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.clear()
    await message.answer(t(lang, "chat_exited"), reply_markup=main_menu_kb(lang))


@router.message(DealChat.meet_location, F.text == "/cancel")
async def cmd_cancel_meet_loc(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.set_state(DealChat.chatting)
    await message.answer(t(lang, "meet_cancelled"))


@router.message(DealChat.meet_location)
async def meet_location_entered(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    text = (message.text or "").strip()
    if not text:
        return
    # Фильтр контактов в предложении встречи только до оплаты
    data_pre = await state.get_data()
    deal_pre = await db.get_deal(data_pre.get("chat_deal_id"))
    if deal_pre and deal_pre["status"] == DealStatus.CREATED and contains_contact(text):
        await message.answer(t(lang, "chat_contact_blocked"))
        return
    await state.update_data(meet_location=text)
    await state.set_state(DealChat.meet_datetime)
    await message.answer(t(lang, "meet_enter_datetime"))


@router.message(DealChat.meet_datetime, F.text == "/endchat")
async def cmd_end_chat_from_meet_dt(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.clear()
    await message.answer(t(lang, "chat_exited"), reply_markup=main_menu_kb(lang))


@router.message(DealChat.meet_datetime, F.text == "/cancel")
async def cmd_cancel_meet_dt(message: Message, state: FSMContext):
    lang = await db.get_user_lang(message.from_user.id)
    await state.set_state(DealChat.chatting)
    await message.answer(t(lang, "meet_cancelled"))


@router.message(DealChat.meet_datetime)
async def meet_datetime_entered(message: Message, state: FSMContext, bot: Bot):
    lang = await db.get_user_lang(message.from_user.id)
    dt_text = (message.text or "").strip()
    if not dt_text:
        return
    data = await state.get_data()
    deal_pre = await db.get_deal(data.get("chat_deal_id"))
    if deal_pre and deal_pre["status"] == DealStatus.CREATED and contains_contact(dt_text):
        await message.answer(t(lang, "chat_contact_blocked"))
        return
    deal_id = data.get("chat_deal_id")
    role = data.get("chat_role")
    other_id = data.get("chat_other_id")
    location = data.get("meet_location", "—")

    # Save as a deal message for history
    meet_text = f"📍 Встреча: {location} | 🕐 {dt_text}"
    await db.save_deal_message(deal_id, message.from_user.id, role, meet_text)

    # Send proposal card to both parties
    card_self = t(lang, "meet_proposal_card", id=deal_id, location=location, datetime=dt_text)
    await message.answer(card_self, parse_mode="HTML")

    other_lang = await db.get_user_lang(other_id)
    card_other = t(other_lang, "meet_proposal_card", id=deal_id, location=location, datetime=dt_text)
    try:
        await bot.send_message(other_id, card_other, parse_mode="HTML")
    except Exception as e:
        logger.error("Failed to send meet proposal to %d: %s", other_id, e)

    await message.answer(t(lang, "meet_proposal_sent"))
    await state.set_state(DealChat.chatting)


@router.message(DealChat.chatting)
async def deal_chat_message(message: Message, state: FSMContext, bot: Bot):
    lang = await db.get_user_lang(message.from_user.id)
    data = await state.get_data()
    deal_id = data.get("chat_deal_id")
    role = data.get("chat_role")
    other_id = data.get("chat_other_id")

    if not deal_id or not other_id:
        await state.clear()
        await message.answer(t(lang, "error_try_again"), reply_markup=main_menu_kb(lang))
        return

    deal = await db.get_deal(deal_id)
    active_statuses = (DealStatus.CREATED, DealStatus.PAID, DealStatus.DELIVERED, DealStatus.DISPUTED)
    if not deal or deal["status"] not in active_statuses:
        await state.clear()
        await message.answer(t(lang, "chat_no_deal"), reply_markup=main_menu_kb(lang))
        return

    text = message.text or ""
    if not text.strip():
        return

    if len(text) > MAX_CHAT_MESSAGE_LEN:
        await message.answer(t(lang, "message_too_long"))
        return

    # Контакты разрешены только после оплаты (PAID, DELIVERED, DISPUTED)
    if deal["status"] == DealStatus.CREATED and contains_contact(text):
        await message.answer(t(lang, "chat_contact_blocked"))
        return

    await db.save_deal_message(deal_id, message.from_user.id, role, text)

    safe_text = html_lib.escape(text)
    other_lang = await db.get_user_lang(other_id)
    msg_key = "chat_msg_from_seller" if role == "seller" else "chat_msg_from_buyer"
    try:
        await bot.send_message(
            other_id,
            t(other_lang, msg_key, id=deal_id, text=safe_text),
            parse_mode="HTML",
        )
    except Exception as e:
        logger.error("Failed to forward chat msg deal #%s to %s: %s", deal_id, other_id, e)

    await message.answer(t(lang, "chat_sent"))


# ————— Админ: история переписки —————

@router.message(F.text.startswith("/chatlog"))
async def cmd_chatlog(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer(
            "Использование: /chatlog <ID сделки>",
        )
        return

    deal_id = int(parts[1])
    deal = await db.get_deal(deal_id)
    if not deal:
        await message.answer("Сделка не найдена.")
        return

    messages = await db.get_deal_messages(deal_id)
    if not messages:
        await message.answer(f"💬 Переписка по сделке #{deal_id} пуста.")
        return

    lines = [f"💬 <b>Переписка — Сделка #{deal_id}</b>\n"]
    for m in messages:
        role_emoji = "🟢" if m["role"] == "buyer" else "🔵"
        role_name = "Покупатель" if m["role"] == "buyer" else "Продавец"
        lines.append(
            f"{role_emoji} <b>{role_name}</b> ({m['sender_id']}) [{m['created_at']}]:\n{m['text']}\n"
        )

    full_text = "\n".join(lines)
    # Telegram limit ~4096 chars, split if needed
    for i in range(0, len(full_text), 4000):
        await message.answer(full_text[i:i + 4000], parse_mode="HTML")
