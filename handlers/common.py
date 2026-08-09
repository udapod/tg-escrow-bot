from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from languages import t
from config import ADMIN_GROUP_ID

router = Router()

def is_group(message: Message) -> bool:
    return message.chat.type in ["group", "supergroup"]

async def dm_block(message: Message):
    await message.answer(
        "⛔ <b>You can only use this command inside a group chat.</b>\n\n"
        "Kindly make a group chat and add the bot.",
        parse_mode="HTML",
    )

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(t(message.from_user.language_code or "en", "welcome"), parse_mode="HTML")

@router.message(Command("terms"))
async def cmd_terms(message: Message):
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
        
        "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
        
        "<b>☠️ FINAL WARNING</b>\n\n"
        "<b>Read before you trust.\n"
        "Verify before you pay.\n"
        "Document before you deal.</b>\n\n"
        "The bot can provide a system.\n"
        "<b>It cannot protect you from your own negligence.</b>\n\n"
        "By using YEETOP ESCROW BOT, you acknowledge that you have read, understood, and accepted these Terms of Service."
    )
    await message.answer(text, parse_mode="HTML")

@router.message(Command("contactadmin"))
async def cmd_contact(message: Message, bot: Bot):
    if not is_group(message): 
        return await dm_block(message)
        
    if not ADMIN_GROUP_ID:
        return await message.answer("⛔ Admin contact not configured.", parse_mode="HTML")
        
    try:
        link = await bot.export_chat_invite_link(message.chat.id)
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"🚨 <b>SUPPORT REQUEST</b>\n\n"
            f"Group: <a href='{link}'>{message.chat.title}</a>\n"
            f"Requested by: {message.from_user.mention_html()}",
            parse_mode="HTML",
        )
        await message.answer("✅ Admins have been notified.", parse_mode="HTML")
    except Exception:
        await message.answer("⛔ Failed to contact admins.", parse_mode="HTML")