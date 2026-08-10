import re

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import database as db
from config import BOT_WALLET, BOT_WALLET_LTC, ADMIN_GROUP_ID, ADMIN_ID

router = Router()

# ————— WALLET VALIDATION —————

TRC20_RE = re.compile(r"^T[1-9A-HJ-NP-Za-km-z]{33}$")
LTC_LEGACY_RE = re.compile(r"^[LM][1-9A-HJ-NP-Za-km-z]{26,33}$")
LTC_SEGWIT_RE = re.compile(r"^ltc1[02-9ac-hj-np-z]{20,60}$")

def normalize_currency(raw: str):
    c = (raw or "").upper().strip()
    if c in ("USDT", "TRC20", "USDT_TRC20", "TRON", "TETHER"):
        return "USDT"
    if c in ("LTC", "LITECOIN"):
        return "LTC"
    return None

def validate_wallet(currency: str, wallet: str) -> bool:
    if currency == "USDT":
        return bool(TRC20_RE.match(wallet))
    if currency == "LTC":
        return bool(LTC_LEGACY_RE.match(wallet)) or bool(LTC_SEGWIT_RE.match(wallet.lower()))
    return False

def detect_currency(wallet: str):
    if TRC20_RE.match(wallet):
        return "USDT"
    if LTC_LEGACY_RE.match(wallet) or LTC_SEGWIT_RE.match(wallet.lower()):
        return "LTC"
    return None

def display_currency(currency: str) -> str:
    if currency == "USDT":
        return "USDT (TRC20)"
    if currency == "LTC":
        return "LTC (Litecoin)"
    return currency

def parse_role_args(message: Message):
    parts = message.text.split()

    if len(parts) >= 3:
        currency = normalize_currency(parts[1])
        wallet = parts[2].strip()
        if currency is None:
            return ("ERR", f"⛔ Unsupported currency <b>{parts[1]}</b>.\nUse <b>USDT</b> or <b>LTC</b>.")
        if not validate_wallet(currency, wallet):
            return ("ERR", f"⛔ That is <b>NOT a valid {display_currency(currency)} address</b>.\nDouble-check the address and try again.")
        return (currency, wallet)

    if len(parts) == 2:
        wallet = parts[1].strip()
        currency = detect_currency(wallet)
        if currency is None:
            return ("ERR", "⛔ That is <b>NOT a valid USDT (TRC20) or LTC address</b>.\nDouble-check the address and try again.")
        return (currency, wallet)

    return ("ERR", (
        "Usage: <code>/seller CURRENCY WALLET_ADDRESS</code>\n"
        "Example: <code>/seller USDT TR7Nh...</code>\n"
        "Or simply: <code>/seller YOUR_WALLET_ADDRESS</code> (auto-detect)"
    ))

# ————— SECURITY & GROUP CHECKS —————

def is_group(message: Message) -> bool:
    return message.chat.type in ["group", "supergroup"]

async def dm_block(message: Message):
    await message.answer(
        "⛔ <b>You can only use this command inside a group chat.</b>\n\n"
        "Kindly make a group chat and add the bot.",
        parse_mode="HTML",
    )

async def check_bot_is_admin(bot: Bot, chat_id: int) -> bool:
    """Checks if the bot has admin or creator status in the group."""
    try:
        member = await bot.get_chat_member(chat_id, bot.id)
        return member.status in ('administrator', 'creator')
    except Exception:
        return False

async def not_admin_block(message: Message):
    await message.answer(
        "⛔ <b>Bot is not an admin.</b>\n\n"
        "For security and dispute resolution, this bot must be promoted to an Admin in this group before a deal can begin.\n\n"
        "<i>Please ask the group owner to grant admin rights to the bot.</i>",
        parse_mode="HTML",
    )

def mismatch_error(locked: str, other_role: str) -> str:
    return (
        f"⛔ <b>CURRENCY MISMATCH.</b>\n"
        f"The {other_role} locked this deal to <b>{display_currency(locked)}</b>.\n"
        f"You must also use <b>{display_currency(locked)}</b>."
    )

# ————— /seller —————

@router.message(Command("seller"))
async def cmd_seller(message: Message, bot: Bot):
    if not is_group(message):
        return await dm_block(message)
    if not await check_bot_is_admin(bot, message.chat.id):
        return await not_admin_block(message)

    currency, wallet = parse_role_args(message)
    if currency == "ERR":
        return await message.answer(wallet, parse_mode="HTML")

    chat_id = message.chat.id
    user_id = message.from_user.id
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1", chat_id)

    if deal:
        locked = deal['currency']

        if deal['buyer_id'] == user_id:
            return await message.answer("⛔ You are already the <b>Buyer</b> in this deal. You cannot switch roles.", parse_mode="HTML")

        if deal['seller_id'] == user_id:
            if deal['buyer_id'] is not None and locked and currency != locked:
                return await message.answer(f"⛔ This deal is locked to <b>{display_currency(locked)}</b> by the buyer. You cannot change the network.", parse_mode="HTML")
            await db.execute("UPDATE group_deals SET seller_wallet = $1, currency = $2 WHERE chat_id = $3", wallet, currency, chat_id)
            await message.answer(f"✅ <b>Seller wallet updated.</b>\n💳 Network: {display_currency(currency)}\n🏦 <code>{wallet}</code>", parse_mode="HTML")
            await check_deal_ready(message, bot)
            return

        if deal['seller_id'] is not None:
            return await message.answer("⛔ A seller is already registered for this deal. You cannot override them.", parse_mode="HTML")

        if locked and currency != locked:
            return await message.answer(mismatch_error(locked, "buyer"), parse_mode="HTML")

        await db.execute("UPDATE group_deals SET seller_id = $1, seller_wallet = $2, currency = $3 WHERE chat_id = $4", user_id, wallet, currency, chat_id)
    else:
        await db.execute("INSERT INTO group_deals (chat_id, seller_id, seller_wallet, currency) VALUES ($1, $2, $3, $4)", chat_id, user_id, wallet, currency)

    await message.answer(
        f"✅ <b>Seller registered & role locked.</b>\n"
        f"👤 {message.from_user.mention_html()}\n"
        f"💳 Network: {display_currency(currency)}\n"
        f"🏦 Wallet: <code>{wallet}</code>",
        parse_mode="HTML",
    )
    await check_deal_ready(message, bot)

# ————— /buyer —————

@router.message(Command("buyer"))
async def cmd_buyer(message: Message, bot: Bot):
    if not is_group(message):
        return await dm_block(message)
    if not await check_bot_is_admin(bot, message.chat.id):
        return await not_admin_block(message)

    currency, wallet = parse_role_args(message)
    if currency == "ERR":
        return await message.answer(wallet, parse_mode="HTML")

    chat_id = message.chat.id
    user_id = message.from_user.id
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1", chat_id)

    if deal:
        locked = deal['currency']

        if deal['seller_id'] == user_id:
            return await message.answer("⛔ You are already the <b>Seller</b> in this deal. You cannot switch roles.", parse_mode="HTML")

        if deal['buyer_id'] == user_id:
            if deal['seller_id'] is not None and locked and currency != locked:
                return await message.answer(f"⛔ This deal is locked to <b>{display_currency(locked)}</b> by the seller. You cannot change the network.", parse_mode="HTML")
            await db.execute("UPDATE group_deals SET buyer_wallet = $1, currency = $2 WHERE chat_id = $3", wallet, currency, chat_id)
            await message.answer(f"✅ <b>Buyer wallet updated.</b>\n💳 Network: {display_currency(currency)}\n🏦 <code>{wallet}</code>", parse_mode="HTML")
            await check_deal_ready(message, bot)
            return

        if deal['buyer_id'] is not None:
            return await message.answer("⛔ A buyer is already registered for this deal. You cannot override them.", parse_mode="HTML")

        if locked and currency != locked:
            return await message.answer(mismatch_error(locked, "seller"), parse_mode="HTML")

        await db.execute("UPDATE group_deals SET buyer_id = $1, buyer_wallet = $2, currency = $3 WHERE chat_id = $4", user_id, wallet, currency, chat_id)
    else:
        await db.execute("INSERT INTO group_deals (chat_id, buyer_id, buyer_wallet, currency) VALUES ($1, $2, $3, $4)", chat_id, user_id, wallet, currency)

    await message.answer(
        f"✅ <b>Buyer registered & role locked.</b>\n"
        f"👤 {message.from_user.mention_html()}\n"
        f"💳 Network: {display_currency(currency)}\n"
        f"🏦 Wallet: <code>{wallet}</code>",
        parse_mode="HTML",
    )
    await check_deal_ready(message, bot)

# ————— DEAL ACTIVATION —————

async def check_deal_ready(message: Message, bot: Bot):
    chat_id = message.chat.id
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1", chat_id)

    if deal and deal['seller_id'] and deal['buyer_id'] and deal['status'] == 'setup':
        await db.execute("UPDATE group_deals SET status = 'active' WHERE chat_id = $1", chat_id)

        currency = deal['currency']
        escrow_addr = BOT_WALLET_LTC if currency == 'LTC' else BOT_WALLET

        text = (
            f"🤝 <b>DEAL ACTIVE</b>\n\n"
            f"👤 Seller: <a href='tg://user?id={deal['seller_id']}'>Seller</a>\n"
            f"👤 Buyer: <a href='tg://user?id={deal['buyer_id']}'>Buyer</a>\n\n"
            f"💰 <b>Send funds to Escrow Address:</b>\n"
            f"<code>{escrow_addr}</code>\n\n"
            f"⚠️ Network: <b>{display_currency(currency)}</b>\n\n"
            f"Once funds are sent and product received:\n"
            f"• Buyer types <code>/payseller</code> to release funds.\n"
            f"• Seller types <code>/refundbuyer</code> to cancel."
        )
        await message.answer(text, parse_mode="HTML")

# ————— /payseller — SHOWS CONFIRMATION CARD —————

@router.message(Command("payseller"))
async def cmd_pay_seller(message: Message, bot: Bot):
    if not is_group(message):
        return await dm_block(message)
    if not await check_bot_is_admin(bot, message.chat.id):
        return await not_admin_block(message)

    chat_id = message.chat.id
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", chat_id)

    if not deal:
        return await message.answer("⛔ No active deal found in this group.")
    if deal['buyer_id'] != message.from_user.id:
        return await message.answer("⛔ Only the registered buyer can release funds.")

    # Build the confirmation card
    confirm_text = (
        "⚠️ <b>CONFIRM PAYMENT RELEASE</b>\n\n"
        "You are about to release the escrow funds to the seller.\n\n"
        f"👤 Seller: <a href='tg://user?id={deal['seller_id']}'>Seller</a>\n"
        f"💳 Network: <b>{display_currency(deal['currency'])}</b>\n"
        f"🏦 Seller Wallet: <code>{deal['seller_wallet']}</code>\n\n"
        "🚨 <b>THIS ACTION CAN'T BE UNDONE.</b>\n"
        "Once released, funds cannot be reversed or recalled by YEETOP ESCROW BOT."
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Confirm & Release", callback_data=f"confirm_pay_{chat_id}"),
            InlineKeyboardButton(text="❌ Cancel", callback_data=f"cancel_confirm_{chat_id}"),
        ]
    ])

    await message.answer(confirm_text, parse_mode="HTML", reply_markup=kb)

# ————— /refundbuyer — SHOWS CONFIRMATION CARD —————

@router.message(Command("refundbuyer"))
async def cmd_refund(message: Message, bot: Bot):
    if not is_group(message):
        return await dm_block(message)
    if not await check_bot_is_admin(bot, message.chat.id):
        return await not_admin_block(message)

    chat_id = message.chat.id
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", chat_id)

    if not deal:
        return await message.answer("⛔ No active deal found in this group.")
    if deal['seller_id'] != message.from_user.id:
        return await message.answer("⛔ Only the registered seller can initiate a refund.")

    # Build the confirmation card
    confirm_text = (
        "⚠️ <b>CONFIRM REFUND</b>\n\n"
        "You are about to refund the escrow funds back to the buyer.\n\n"
        f"👤 Buyer: <a href='tg://user?id={deal['buyer_id']}'>Buyer</a>\n"
        f"💳 Network: <b>{display_currency(deal['currency'])}</b>\n"
        f"🏦 Buyer Wallet: <code>{deal['buyer_wallet']}</code>\n\n"
        "🚨 <b>THIS ACTION CAN'T BE UNDONE.</b>\n"
        "Once refunded, funds cannot be reversed or recalled by YEETOP ESCROW BOT."
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Confirm & Refund", callback_data=f"confirm_refund_{chat_id}"),
            InlineKeyboardButton(text="❌ Cancel", callback_data=f"cancel_confirm_{chat_id}"),
        ]
    ])

    await message.answer(confirm_text, parse_mode="HTML", reply_markup=kb)

# ————— CALLBACK: CONFIRM PAYMENT RELEASE —————

@router.callback_query(F.data.startswith("confirm_pay_"))
async def cb_confirm_pay(callback: CallbackQuery, bot: Bot):
    chat_id = int(callback.data.split("_")[-1])
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", chat_id)

    if not deal:
        await callback.message.edit_text("⛔ Deal no longer active.", parse_mode="HTML")
        await callback.answer()
        return

    # Security: only the original buyer can confirm
    if deal['buyer_id'] != callback.from_user.id:
        await callback.answer("⛔ Only the buyer can confirm this payment.", show_alert=True)
        return

    # Execute the release
    await db.execute("UPDATE group_deals SET status = 'completed' WHERE chat_id = $1", chat_id)

    await callback.message.edit_text(
        "✅ <b>PAYMENT RELEASED</b>\n\n"
        "Funds should now be sent to the seller's wallet.\n"
        "This action cannot be undone.",
        parse_mode="HTML",
    )
    await callback.answer("Payment released.")

    if ADMIN_GROUP_ID:
        try:
            link = await bot.export_chat_invite_link(chat_id)
            await bot.send_message(
                ADMIN_GROUP_ID,
                f"💸 <b>PAYOUT REQUIRED</b>\n\n"
                f"Group: <a href='{link}'>{callback.message.chat.title}</a>\n"
                f"Seller Wallet: <code>{deal['seller_wallet']}</code>\n"
                f"Currency: {display_currency(deal['currency'])}",
                parse_mode="HTML",
            )
        except Exception as e:
            print(f"Failed to notify admin: {e}")

# ————— CALLBACK: CONFIRM REFUND —————

@router.callback_query(F.data.startswith("confirm_refund_"))
async def cb_confirm_refund(callback: CallbackQuery, bot: Bot):
    chat_id = int(callback.data.split("_")[-1])
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", chat_id)

    if not deal:
        await callback.message.edit_text("⛔ Deal no longer active.", parse_mode="HTML")
        await callback.answer()
        return

    # Security: only the original seller can confirm
    if deal['seller_id'] != callback.from_user.id:
        await callback.answer("⛔ Only the seller can confirm this refund.", show_alert=True)
        return

    # Execute the refund
    await db.execute("UPDATE group_deals SET status = 'refunded' WHERE chat_id = $1", chat_id)

    await callback.message.edit_text(
        "✅ <b>DEAL REFUNDED</b>\n\n"
        "Funds should now be returned to the buyer.\n"
        "This action cannot be undone.",
        parse_mode="HTML",
    )
    await callback.answer("Refund issued.")

    if ADMIN_GROUP_ID:
        try:
            link = await bot.export_chat_invite_link(chat_id)
            await bot.send_message(
                ADMIN_GROUP_ID,
                f"↩️ <b>REFUND REQUIRED</b>\n\n"
                f"Group: <a href='{link}'>{callback.message.chat.title}</a>\n"
                f"Buyer Wallet: <code>{deal['buyer_wallet']}</code>\n"
                f"Currency: {display_currency(deal['currency'])}",
                parse_mode="HTML",
            )
        except Exception as e:
            print(f"Failed to notify admin: {e}")

# ————— CALLBACK: CANCEL —————

@router.callback_query(F.data.startswith("cancel_confirm_"))
async def cb_cancel_confirm(callback: CallbackQuery):
    chat_id = int(callback.data.split("_")[-1])
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1", chat_id)

    # Security: only the buyer (for pay) or seller (for refund) can cancel their own prompt
    if not deal or (callback.from_user.id not in (deal['buyer_id'], deal['seller_id'])):
        await callback.answer("⛔ You cannot cancel this.", show_alert=True)
        return

    await callback.message.edit_text(
        "❌ <b>Action cancelled.</b>\n\n"
        "The deal remains active. You can try again when ready.",
        parse_mode="HTML",
    )
    await callback.answer("Cancelled.")

# ————— ADMIN: VIEW ALL ACTIVE DEALS —————

@router.message(Command("active"))
async def cmd_active(message: Message, bot: Bot):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Admin access required.", parse_mode="HTML")

    deals = await db.fetch("SELECT * FROM group_deals WHERE status = 'active'")

    if not deals:
        return await message.answer("✅ No active deals found.", parse_mode="HTML")

    await message.answer(f"📋 <b>Active Deals ({len(deals)})</b>", parse_mode="HTML")

    for deal in deals:
        chat_id = deal['chat_id']
        currency = deal['currency']

        text = (
            f"💼 <b>Deal in Chat {chat_id}</b>\n"
            f"💳 Network: <b>{display_currency(currency)}</b>\n"
            f"👤 Seller ID: <code>{deal['seller_id']}</code>\n"
            f"🏦 Seller Wallet: <code>{deal['seller_wallet']}</code>\n"
            f"👤 Buyer ID: <code>{deal['buyer_id']}</code>\n"
            f"🏦 Buyer Wallet: <code>{deal['buyer_wallet']}</code>"
        )

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Force Release to Seller", callback_data=f"admin_force_pay_{chat_id}"),
                InlineKeyboardButton(text="↩️ Force Refund to Buyer", callback_data=f"admin_force_refund_{chat_id}"),
            ]
        ])

        await message.answer(text, parse_mode="HTML", reply_markup=kb)

# ————— ADMIN: FORCE RELEASE TO SELLER (CONFIRMATION) —————

@router.callback_query(F.data.startswith("admin_force_pay_"))
async def cb_admin_force_pay(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Admin access required.", show_alert=True)
        return

    chat_id = int(callback.data.split("_")[-1])
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", chat_id)

    if not deal:
        await callback.message.edit_text("⛔ Deal no longer active.", parse_mode="HTML")
        await callback.answer()
        return

    confirm_text = (
        "⚠️ <b>ADMIN: FORCE PAYMENT RELEASE</b>\n\n"
        "You are about to override the buyer and force-release funds to the seller.\n\n"
        f"💳 Network: <b>{display_currency(deal['currency'])}</b>\n"
        f"🏦 Seller Wallet: <code>{deal['seller_wallet']}</code>\n\n"
        "🚨 <b>THIS ACTION CAN'T BE UNDONE.</b>\n"
        "Once released, funds cannot be reversed or recalled by YEETOP ESCROW BOT."
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Confirm & Force Release", callback_data=f"admin_confirm_pay_{chat_id}"),
            InlineKeyboardButton(text="❌ Cancel", callback_data=f"admin_cancel_{chat_id}"),
        ]
    ])

    await callback.message.edit_text(confirm_text, parse_mode="HTML", reply_markup=kb)
    await callback.answer()

# ————— ADMIN: FORCE REFUND TO BUYER (CONFIRMATION) —————

@router.callback_query(F.data.startswith("admin_force_refund_"))
async def cb_admin_force_refund(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Admin access required.", show_alert=True)
        return

    chat_id = int(callback.data.split("_")[-1])
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", chat_id)

    if not deal:
        await callback.message.edit_text("⛔ Deal no longer active.", parse_mode="HTML")
        await callback.answer()
        return

    confirm_text = (
        "⚠️ <b>ADMIN: FORCE REFUND</b>\n\n"
        "You are about to override the seller and force-refund funds to the buyer.\n\n"
        f"💳 Network: <b>{display_currency(deal['currency'])}</b>\n"
        f"🏦 Buyer Wallet: <code>{deal['buyer_wallet']}</code>\n\n"
        "🚨 <b>THIS ACTION CAN'T BE UNDONE.</b>\n"
        "Once refunded, funds cannot be reversed or recalled by YEETOP ESCROW BOT."
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Confirm & Force Refund", callback_data=f"admin_confirm_refund_{chat_id}"),
            InlineKeyboardButton(text="❌ Cancel", callback_data=f"admin_cancel_{chat_id}"),
        ]
    ])

    await callback.message.edit_text(confirm_text, parse_mode="HTML", reply_markup=kb)
    await callback.answer()

# ————— ADMIN: CONFIRM FORCE RELEASE —————

@router.callback_query(F.data.startswith("admin_confirm_pay_"))
async def cb_admin_confirm_pay(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Admin access required.", show_alert=True)
        return

    chat_id = int(callback.data.split("_")[-1])
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", chat_id)

    if not deal:
        await callback.message.edit_text("⛔ Deal no longer active.", parse_mode="HTML")
        await callback.answer()
        return

    await db.execute("UPDATE group_deals SET status = 'completed' WHERE chat_id = $1", chat_id)

    await callback.message.edit_text(
        "✅ <b>ADMIN OVERRIDE: PAYMENT RELEASED</b>\n\n"
        "Funds should now be sent to the seller's wallet.\n"
        "This action cannot be undone.",
        parse_mode="HTML",
    )
    await callback.answer("Force release executed.")

    # Notify the deal group
    try:
        await bot.send_message(
            chat_id,
            "⚠️ <b>ADMIN INTERVENTION</b>\n\n"
            "An administrator has force-released the escrow funds to the seller.",
            parse_mode="HTML",
        )
    except Exception:
        pass

# ————— ADMIN: CONFIRM FORCE REFUND —————

@router.callback_query(F.data.startswith("admin_confirm_refund_"))
async def cb_admin_confirm_refund(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Admin access required.", show_alert=True)
        return

    chat_id = int(callback.data.split("_")[-1])
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", chat_id)

    if not deal:
        await callback.message.edit_text("⛔ Deal no longer active.", parse_mode="HTML")
        await callback.answer()
        return

    await db.execute("UPDATE group_deals SET status = 'refunded' WHERE chat_id = $1", chat_id)

    await callback.message.edit_text(
        "✅ <b>ADMIN OVERRIDE: DEAL REFUNDED</b>\n\n"
        "Funds should now be returned to the buyer.\n"
        "This action cannot be undone.",
        parse_mode="HTML",
    )
    await callback.answer("Force refund executed.")

    # Notify the deal group
    try:
        await bot.send_message(
            chat_id,
            "⚠️ <b>ADMIN INTERVENTION</b>\n\n"
            "An administrator has force-refunded the escrow funds to the buyer.",
            parse_mode="HTML",
        )
    except Exception:
        pass

# ————— ADMIN: CANCEL —————

@router.callback_query(F.data.startswith("admin_cancel_"))
async def cb_admin_cancel(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Admin access required.", show_alert=True)
        return

    await callback.message.edit_text("❌ <b>Action cancelled.</b>", parse_mode="HTML")
    await callback.answer("Cancelled.")