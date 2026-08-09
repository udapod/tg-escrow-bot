import re

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
import database as db
from config import BOT_WALLET, BOT_WALLET_LTC, ADMIN_GROUP_ID

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

def parse_role_args(message: Message):
    parts = message.text.split()

    if len(parts) >= 3:
        currency = normalize_currency(parts[1])
        wallet = parts[2].strip()
        if currency is None:
            return ("ERR", f"⛔ Unsupported currency <b>{parts[1]}</b>.\nUse <b>USDT</b> or <b>LTC</b>.")
        if not validate_wallet(currency, wallet):
            return ("ERR", f"️ That is <b>NOT a valid {currency} address</b>.\nDouble-check the address and try again.")
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

def is_group(message: Message) -> bool:
    return message.chat.type in ["group", "supergroup"]

async def dm_block(message: Message):
    await message.answer(
        "⛔ <b>You can only use this command inside a group chat.</b>\n\n"
        "Kindly make a group chat and add the bot.",
        parse_mode="HTML",
    )

# ————— /seller —————

@router.message(Command("seller"))
async def cmd_seller(message: Message, bot: Bot):
    if not is_group(message):
        return await dm_block(message)

    currency, wallet = parse_role_args(message)
    if currency == "ERR":
        return await message.answer(wallet, parse_mode="HTML")

    chat_id = message.chat.id
    user_id = message.from_user.id
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1", chat_id)

    if deal:
        if deal['buyer_id'] == user_id:
            return await message.answer("⛔ You are already the <b>Buyer</b> in this deal. You cannot switch roles.", parse_mode="HTML")
        if deal['seller_id'] == user_id:
            await db.execute("UPDATE group_deals SET seller_wallet = $1, currency = $2 WHERE chat_id = $3", wallet, currency, chat_id)
            await message.answer(f"✅ <b>Seller wallet updated.</b>\n💳 Network: {currency}\n🏦 <code>{wallet}</code>", parse_mode="HTML")
            await check_deal_ready(message, bot)
            return
        if deal['seller_id'] is not None:
            return await message.answer("⛔ A seller is already registered for this deal. You cannot override them.", parse_mode="HTML")
        await db.execute("UPDATE group_deals SET seller_id = $1, seller_wallet = $2, currency = $3 WHERE chat_id = $4", user_id, wallet, currency, chat_id)
    else:
        await db.execute("INSERT INTO group_deals (chat_id, seller_id, seller_wallet, currency) VALUES ($1, $2, $3, $4)", chat_id, user_id, wallet, currency)

    await message.answer(
        f"✅ <b>Seller registered & role locked.</b>\n"
        f"👤 {message.from_user.mention_html()}\n"
        f"💳 Network: {currency}\n"
        f"🏦 Wallet: <code>{wallet}</code>",
        parse_mode="HTML",
    )
    await check_deal_ready(message, bot)

# ————— /buyer —————

@router.message(Command("buyer"))
async def cmd_buyer(message: Message, bot: Bot):
    if not is_group(message):
        return await dm_block(message)

    currency, wallet = parse_role_args(message)
    if currency == "ERR":
        return await message.answer(wallet, parse_mode="HTML")

    chat_id = message.chat.id
    user_id = message.from_user.id
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1", chat_id)

    if deal:
        if deal['seller_id'] == user_id:
            return await message.answer("⛔ You are already the <b>Seller</b> in this deal. You cannot switch roles.", parse_mode="HTML")
        if deal['buyer_id'] == user_id:
            await db.execute("UPDATE group_deals SET buyer_wallet = $1, currency = $2 WHERE chat_id = $3", wallet, currency, chat_id)
            await message.answer(f"✅ <b>Buyer wallet updated.</b>\n💳 Network: {currency}\n🏦 <code>{wallet}</code>", parse_mode="HTML")
            await check_deal_ready(message, bot)
            return
        if deal['buyer_id'] is not None:
            return await message.answer("⛔ A buyer is already registered for this deal. You cannot override them.", parse_mode="HTML")
        await db.execute("UPDATE group_deals SET buyer_id = $1, buyer_wallet = $2, currency = $3 WHERE chat_id = $4", user_id, wallet, currency, chat_id)
    else:
        await db.execute("INSERT INTO group_deals (chat_id, buyer_id, buyer_wallet, currency) VALUES ($1, $2, $3, $4)", chat_id, user_id, wallet, currency)

    await message.answer(
        f"✅ <b>Buyer registered & role locked.</b>\n"
        f"👤 {message.from_user.mention_html()}\n"
        f"💳 Network: {currency}\n"
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
            f"⚠️ Network: <b>{currency}</b>\n\n"
            f"Once funds are sent and product received:\n"
            f"• Buyer types <code>/payseller</code> to release funds.\n"
            f"• Seller types <code>/refundbuyer</code> to cancel."
        )
        await message.answer(text, parse_mode="HTML")

# ————— /payseller —————

@router.message(Command("payseller"))
async def cmd_pay_seller(message: Message, bot: Bot):
    if not is_group(message):
        return await dm_block(message)

    chat_id = message.chat.id
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", chat_id)

    if not deal:
        return await message.answer("⛔ No active deal found in this group.")
    if deal['buyer_id'] != message.from_user.id:
        return await message.answer("⛔ Only the registered buyer can release funds.")

    await db.execute("UPDATE group_deals SET status = 'completed' WHERE chat_id = $1", chat_id)
    await message.answer("✅ <b>Payment Released!</b>\nFunds should be sent to the seller's wallet.", parse_mode="HTML")

    if ADMIN_GROUP_ID:
        try:
            link = await bot.export_chat_invite_link(chat_id)
            await bot.send_message(
                ADMIN_GROUP_ID,
                f"💸 <b>PAYOUT REQUIRED</b>\n\n"
                f"Group: <a href='{link}'>{message.chat.title}</a>\n"
                f"Seller Wallet: <code>{deal['seller_wallet']}</code>\n"
                f"Currency: {deal['currency']}",
                parse_mode="HTML",
            )
        except Exception as e:
            print(f"Failed to notify admin: {e}")

# ————— /refundbuyer —————

@router.message(Command("refundbuyer"))
async def cmd_refund(message: Message, bot: Bot):
    if not is_group(message):
        return await dm_block(message)

    chat_id = message.chat.id
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", chat_id)

    if not deal:
        return await message.answer("⛔ No active deal found in this group.")
    if deal['seller_id'] != message.from_user.id:
        return await message.answer("⛔ Only the registered seller can initiate a refund.")

    await db.execute("UPDATE group_deals SET status = 'refunded' WHERE chat_id = $1", chat_id)
    await message.answer("✅ <b>Deal Refunded!</b>\nFunds should be returned to the buyer.", parse_mode="HTML")

    if ADMIN_GROUP_ID:
        try:
            link = await bot.export_chat_invite_link(chat_id)
            await bot.send_message(
                ADMIN_GROUP_ID,
                f"↩️ <b>REFUND REQUIRED</b>\n\n"
                f"Group: <a href='{link}'>{message.chat.title}</a>\n"
                f"Buyer Wallet: <code>{deal['buyer_wallet']}</code>\n"
                f"Currency: {deal['currency']}",
                parse_mode="HTML",
            )
        except Exception as e:
            print(f"Failed to notify admin: {e}")