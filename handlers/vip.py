from datetime import datetime
import html as html_lib

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database as db
from keyboards import vip_buy_kb, vip_paid_kb, main_menu_kb, admin_kb
from config import VIP_PRICE, VIP_DAYS, VIP_COMMISSION, BOT_COMMISSION, BOT_WALLET, ADMIN_ID
from languages import t, all_btn_texts
from tron import verify_tx

router = Router()


class VipTxState(StatesGroup):
    waiting_tx_hash = State()


# ————— Кнопка VIP-подписка —————

@router.message(F.text.in_(all_btn_texts("btn_vip")))
async def cmd_vip(message: Message):
    lang = await db.get_user_lang(message.from_user.id)
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer(t(lang, "press_start_first"))
        return

    vip_info = await db.get_vip_info(message.from_user.id)

    if vip_info:
        expires = datetime.fromisoformat(vip_info["expires_at"])
        days_left = max(0, (expires - datetime.now()).days)
        text = t(lang, "vip_active",
                 expires=vip_info["expires_at"],
                 vip_rate=VIP_COMMISSION, rate=BOT_COMMISSION)
        text += "\n" + t(lang, "vip_days_left", days=days_left)
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer(
            t(lang, "vip_offer",
              vip_rate=VIP_COMMISSION, rate=BOT_COMMISSION,
              price=VIP_PRICE, days=VIP_DAYS),
            parse_mode="HTML",
            reply_markup=vip_buy_kb(lang),
        )


# ————— Покупка VIP —————

@router.callback_query(F.data == "vip_buy")
async def cb_vip_buy(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    user = await db.get_user(callback.from_user.id)
    if not user:
        await callback.answer(t(lang, "press_start_first"), show_alert=True)
        return

    vip_info = await db.get_vip_info(callback.from_user.id)
    if vip_info:
        await callback.answer(t(lang, "vip_already_active"), show_alert=True)
        return

    sub_id = await db.create_vip_subscription(
        user_id=callback.from_user.id,
        amount=VIP_PRICE,
        days=VIP_DAYS,
    )

    await callback.message.edit_text(
        t(lang, "vip_payment",
          price=VIP_PRICE, days=VIP_DAYS, wallet=BOT_WALLET),
        parse_mode="HTML",
        reply_markup=vip_paid_kb(sub_id, lang),
    )
    await callback.answer()


# ————— Подтверждение оплаты VIP —————

@router.callback_query(F.data.startswith("vip_paid_"))
async def cb_vip_paid(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_lang(callback.from_user.id)
    sub_id = int(callback.data.split("_")[-1])

    await state.update_data(vip_sub_id=sub_id)
    await callback.message.edit_text(
        t(lang, "vip_enter_tx"),
        parse_mode="HTML",
    )
    await state.set_state(VipTxState.waiting_tx_hash)
    await callback.answer()


@router.message(VipTxState.waiting_tx_hash)
async def vip_tx_hash_entered(message: Message, state: FSMContext, bot: Bot):
    lang = await db.get_user_lang(message.from_user.id)
    tx_hash = message.text.strip()

    if len(tx_hash) < 20 or len(tx_hash) > 128:
        await message.answer(t(lang, "tx_hash_invalid"))
        return

    data = await state.get_data()
    sub_id = data.get("vip_sub_id")
    if not sub_id:
        await state.clear()
        await message.answer(t(lang, "error_try_again"))
        return

    # Проверка транзакции через TronGrid
    verifying_msg = await message.answer(t(lang, "tx_verifying"))
    result = await verify_tx(tx_hash, VIP_PRICE)
    await verifying_msg.delete()

    if not result["ok"]:
        error_key = result.get("error", "tx_network_error")
        await message.answer(t(lang, error_key))
        return

    await db.activate_vip_simple(sub_id, tx_hash, VIP_DAYS)
    await state.clear()

    user = await db.get_user(message.from_user.id)

    await message.answer(
        t(lang, "vip_activated",
          days=VIP_DAYS, vip_rate=VIP_COMMISSION, tx=tx_hash),
        parse_mode="HTML",
        reply_markup=main_menu_kb(lang),
    )

    # Уведомление админу (русский)
    await bot.send_message(
        ADMIN_ID,
        f"👑 <b>НОВАЯ VIP-ПОДПИСКА</b>\n\n"
        f"👤 {html_lib.escape(user['full_name'])} (ID: {message.from_user.id})\n"
        f"💵 {VIP_PRICE} USDT\n"
        f"🔗 TxID: <code>{tx_hash}</code>\n"
        f"📅 Срок: {VIP_DAYS} дней",
        parse_mode="HTML",
    )


@router.callback_query(F.data == "vip_cancel")
async def cb_vip_cancel(callback: CallbackQuery):
    lang = await db.get_user_lang(callback.from_user.id)
    await callback.message.edit_text(t(lang, "vip_cancelled"))
    await callback.answer()


# ————— Админ: VIP-заявки —————

@router.callback_query(F.data == "admin_vip")
async def cb_admin_vip(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    vip_stats = await db.get_vip_stats()
    await callback.message.edit_text(
        f"👑 <b>VIP-статистика</b>\n\n"
        f"✅ Активных VIP: {vip_stats['active_vips']}\n"
        f"💵 Доход от VIP: {vip_stats['total_vip_revenue']} USDT",
        parse_mode="HTML",
        reply_markup=admin_kb(),
    )
    await callback.answer()
