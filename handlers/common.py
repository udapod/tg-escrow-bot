from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from languages import t
from config import ADMIN_GROUP_ID

router = Router()

def is_group(message: Message) -> bool:
    return message.chat.type in ["group", "supergroup"]

async def dm_block(message: Message):
    await message.answer("⛔ <b>You can only use this command inside a group chat.</b>\n\nKindly make a group chat and add the bot.", parse_mode="HTML")

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(t(message.from_user.language_code or "en", "welcome"), parse_mode="HTML")

@router.message(Command("terms"))
async def cmd_terms(message: Message):
    if not is_group(message): return await dm_block(message)
    text = (
        "⚖️ <b>TERMS OF SERVICE</b>\n\n"
        "YEETOP ESCROW BOT acts solely as an automated verifier and notification service.\n\n"
        "1. We are <b>NOT liable</b> for any agreements, product quality, or services exchanged between users.\n"
        "2. We do not hold private keys. We verify blockchain transactions and notify parties.\n"
        "3. Any side-deals or agreements made outside the bot's visible commands are strictly between the buyer and seller.\n"
        "4. Use at your own risk."
    )
    await message.answer(text, parse_mode="HTML")

@router.message(Command("contactadmin"))
async def cmd_contact(message: Message, bot: Bot):
    if not is_group(message): return await dm_block(message)
    if not ADMIN_GROUP_ID:
        return await message.answer("⛔ Admin contact not configured.")
        
    try:
        link = await bot.export_chat_invite_link(message.chat.id)
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"🚨 <b>SUPPORT REQUEST</b>\n\n"
            f"Group: <a href='{link}'>{message.chat.title}</a>\n"
            f"Requested by: {message.from_user.mention_html()}",
            parse_mode="HTML"
        )
        await message.answer("✅ Admins have been notified.")
    except Exception:
        await message.answer("⛔ Failed to contact admins.")