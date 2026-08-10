import qrcode
from io import BytesIO

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
import database as db
from languages import t
from config import ADMIN_GROUP_ID, BOT_WALLET, BOT_WALLET_LTC, ADMIN_ID, REVIEW_CHANNEL_ID

def display_currency(currency: str) -> str:
    if currency == "USDT":
        return "USDT (TRC20)"
    if currency == "LTC":
        return "LTC (Litecoin)"
    return currency

router = Router()

def is_group(message: Message) -> bool:
    return message.chat.type in ["group", "supergroup"]

async def dm_block(message: Message):
    await message.answer(
        "⛔ <b>You can only use this command inside a group chat.</b>\n\n"
        "Kindly make a group chat and add the bot.",
        parse_mode="HTML",
    )

# --- Helper for Terms ---
async def process_terms(message: Message):
    if not is_group(message):
        return await dm_block(message)
        
    text = (
        "<b>⚖️ TERMS OF SERVICE</b>\n\n"
        "<b>YEETOP ESCROW BOT</b>\n\n"
        "<b>Trust is earned, screenshots are evidence, and carelessness is not our liability.</b>\n\n"
        "YEETOP ESCROW BOT operates solely as an <b>automated escrow, verification, and notification service</b>. We facilitate the process; we do not guarantee the people, products, promises, or outcomes involved.\n\n"
        "<b>1. ⚠️ DEALS ARE YOUR RESPONSIBILITY</b>\n\n"
        "We are <b>not liable</b> for any agreement, product, service, account, digital asset, or transaction exchanged between users. If you enter a deal, you accept the risks that come with it.\n\n"
        "<b>2. 💀 RELEASED FUNDS STAY RELEASED</b>\n\n"
        "Once funds have been released or a refund has been processed, <b>do not expect us to turn back the clock</b>. We cannot reverse payments simply because you later regret the decision or discover a problem.\n\n"
        "<b>3. 🕳️ SIDE DEALS ARE YOUR PROBLEM</b>\n\n"
        "Any agreement, promise, payment, or arrangement made <b>outside the bot's visible escrow commands</b> exists strictly between the parties involved. If you take the deal off the record, you take the risk with it.\n\n"
        "<b>4. 📸 EVIDENCE IS YOUR SHIELD</b>\n\n"
        "Disputes are settled based on the agreement and evidence available to us. <b>Keep screenshots of your conversations, payment records, usernames, and agreed terms.</b>\n\n"
        "Telegram messages can disappear. Users can delete messages. Usernames can change. Stories can change even faster.\n\n"
        "<b>If there is no evidence, there may be nothing for us to enforce.</b>\n\n"
        "Be precise. Be thorough. Put important terms in writing <b>before</b> money or goods change hands.\n\n"
        "<b>5. 🕵️ IMPOSTORS EXIST</b>\n\n"
        "If an administrator contacts you, <b>verify that they are actually an authorized YEETOP administrator before taking any action.</b>\n\n"
        "Impostors may attempt to impersonate staff, request payments, or redirect transactions.\n\n"
        "<b>We are not responsible for losses caused by trusting an impersonator or acting outside the bot's official procedures.</b>\n\n"
        "<b>6. 💰 THE PRICE OF THE ESCROW</b>\n\n"
        "By using YEETOP ESCROW BOT, you acknowledge and agree to our <b>5% escrow fee</b>, subject to a <b>minimum fee of $5</b>.\n\n"
        "If you proceed with a transaction, you are confirming that you understand and accept these terms.\n\n"
        "➖➖➖➖➖➖➖➖➖\n\n"
        "<b>☠️ FINAL WARNING</b>\n\n"
        "<b>Read before you trust.\n"
        "Verify before you pay.\n"
        "Document before you deal.</b>\n\n"
        "The bot can provide a system.\n"
        "<b>It cannot protect you from your own negligence.</b>\n\n"
        "By using YEETOP ESCROW BOT, you acknowledge that you have read, understood, and accepted these Terms of Service."
    )
    await message.answer(text, parse_mode="HTML")

# --- Helper for Contact Admin ---
async def process_contact_admin(message: Message, bot: Bot):
    if not is_group(message):
        return await dm_block(message)

    if not ADMIN_GROUP_ID:
        return await message.answer("⛔ Admin contact not configured.", parse_mode="HTML")

    group_ref = f"🏷 {message.chat.title}"
    try:
        link = await bot.export_chat_invite_link(message.chat.id)
        group_ref = f"<a href='{link}'>{message.chat.title}</a>"
    except Exception:
        group_ref = f"🏷 {message.chat.title} <i>(make the bot a group admin to enable invite links)</i>"

    try:
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"🚨 <b>SUPPORT REQUEST</b>\n\n"
            f"Group: {group_ref}\n"
            f"Chat ID: <code>{message.chat.id}</code>\n"
            f"Requested by: {message.from_user.mention_html()}",
            parse_mode="HTML",
        )
        await message.answer("✅ Admins have been notified.", parse_mode="HTML")
    except Exception:
        await message.answer(
            "⛔ Could not reach the admin group.\n\n"
            "The admins must add this bot to their admin group and set the correct "
            "<code>ADMIN_GROUP_ID</code> (use /chatid in that group to get it).",
            parse_mode="HTML",
        )

# ————— /start —————

@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    if is_group(message):
        deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1", message.chat.id)
        if deal and deal['status'] in ('setup', 'active'):
            return await message.answer(
                "⚠️ <b>A deal is already in progress in this group.</b>\n\n"
                "Please finish or cancel the current deal before starting a new one.",
                parse_mode="HTML",
            )
            
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⚖️ Terms of Service", callback_data="btn_terms"),
            InlineKeyboardButton(text="🚨 Contact Admin", callback_data="btn_contact_admin"),
        ]
    ])
    
    await message.answer(t(message.from_user.language_code or "en", "welcome"), parse_mode="HTML", reply_markup=kb)

# ————— /chatid —————

@router.message(Command("chatid"))
async def cmd_chatid(message: Message):
    await message.answer(f" Chat ID: <code>{message.chat.id}</code>", parse_mode="HTML")

# ————— /addadmin —————

@router.message(Command("addadmin"))
async def cmd_addadmin(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Root admin access required.", parse_mode="HTML")
    
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("Usage: <code>/addadmin USER_ID</code>", parse_mode="HTML")
    
    uid = int(parts[1])
    await db.execute("INSERT INTO bot_admins (user_id) VALUES ($1) ON CONFLICT DO NOTHING", uid)
    await message.answer(f"✅ Admin <code>{uid}</code> added successfully.", parse_mode="HTML")

# ————— /qr —————

@router.message(Command("qr"))
async def cmd_qr(message: Message, bot: Bot):
    if not is_group(message):
        return await dm_block(message)

    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", message.chat.id)

    if not deal:
        return await message.answer("⛔ No active deal found here, press /start to start a new deal.", parse_mode="HTML")

    currency = deal['currency']
    escrow_addr = BOT_WALLET_LTC if currency == 'LTC' else BOT_WALLET

    if not escrow_addr:
        return await message.answer("⛔ Escrow wallet not configured by the admins.", parse_mode="HTML")

    img = qrcode.make(escrow_addr)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    await message.answer_photo(
        BufferedInputFile(buf.read(), filename="escrow_qr.png"),
        caption=(
            f"💰 <b>Escrow Address QR</b>\n"
            f"⚠️ Network: <b>{display_currency(currency)}</b>\n"
            f"<code>{escrow_addr}</code>"
        ),
        parse_mode="HTML",
    )

# ————— /terms & Button —————

@router.message(Command("terms"))
async def cmd_terms(message: Message):
    await process_terms(message)

@router.callback_query(F.data == "btn_terms")
async def cb_terms(callback: CallbackQuery):
    await process_terms(callback.message)
    await callback.answer()

# ————— /contactadmin & Button —————

@router.message(Command("contactadmin"))
async def cmd_contact(message: Message, bot: Bot):
    await process_contact_admin(message, bot)

@router.callback_query(F.data == "btn_contact_admin")
async def cb_contact_admin(callback: CallbackQuery, bot: Bot):
    await process_contact_admin(callback.message, bot)
    await callback.answer()