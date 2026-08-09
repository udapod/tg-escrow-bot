from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
import database as db
from config import BOT_WALLET, LTC_ESCROW_ADDRESS, ADMIN_GROUP_ID

router = Router()

def is_group(message: Message) -> bool:
    return message.chat.type in ["group", "supergroup"]

async def dm_block(message: Message):
    await message.answer("⛔ <b>Can't use bot in DM.</b>\n\nCreate a group chat, add the bot, and use commands there.", parse_mode="HTML")

@router.message(Command("seller"))
async def cmd_seller(message: Message, bot: Bot):
    if not is_group(message): return await dm_block(message)
    
    parts = message.text.split()
    if len(parts) < 3:
        return await message.answer("Usage: <code>/seller CURRENCY WALLET_ADDRESS</code>\nExample: <code>/seller USDT TR7Nh...</code>", parse_mode="HTML")
    
    currency = parts[1].upper()
    wallet = parts[2]
    chat_id = message.chat.id
    
    # Save seller
    await db.execute("""
        INSERT INTO group_deals (chat_id, seller_id, seller_wallet, currency) 
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (chat_id) DO UPDATE 
        SET seller_id = EXCLUDED.seller_id, seller_wallet = EXCLUDED.seller_wallet, currency = EXCLUDED.currency
    """, chat_id, message.from_user.id, wallet, currency)
    
    await message.answer(f"✅ Seller registered: {message.from_user.mention_html()}\nWallet: <code>{wallet}</code>", parse_mode="HTML")
    await check_deal_ready(message, bot)

@router.message(Command("buyer"))
async def cmd_buyer(message: Message, bot: Bot):
    if not is_group(message): return await dm_block(message)
    
    parts = message.text.split()
    if len(parts) < 3:
        return await message.answer("Usage: <code>/buyer CURRENCY WALLET_ADDRESS</code>\nExample: <code>/buyer LTC Lc1...</code>", parse_mode="HTML")
    
    currency = parts[1].upper()
    wallet = parts[2]
    chat_id = message.chat.id
    
    # Save buyer
    await db.execute("""
        INSERT INTO group_deals (chat_id, buyer_id, buyer_wallet, currency) 
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (chat_id) DO UPDATE 
        SET buyer_id = EXCLUDED.buyer_id, buyer_wallet = EXCLUDED.buyer_wallet, currency = EXCLUDED.currency
    """, chat_id, message.from_user.id, wallet, currency)
    
    await message.answer(f"✅ Buyer registered: {message.from_user.mention_html()}\nWallet: <code>{wallet}</code>", parse_mode="HTML")
    await check_deal_ready(message, bot)

async def check_deal_ready(message: Message, bot: Bot):
    chat_id = message.chat.id
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1", chat_id)
    
    if deal and deal['seller_id'] and deal['buyer_id'] and deal['status'] == 'setup':
        # Both registered -> Activate deal
        await db.execute("UPDATE group_deals SET status = 'active' WHERE chat_id = $1", chat_id)
        
        currency = deal['currency']
        escrow_addr = LTC_ESCROW_ADDRESS if currency == 'LTC' else BOT_WALLET
        
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

@router.message(Command("payseller"))
async def cmd_pay_seller(message: Message, bot: Bot):
    if not is_group(message): return await dm_block(message)
    
    chat_id = message.chat.id
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", chat_id)
    
    if not deal:
        return await message.answer("No active deal found.")
    if deal['buyer_id'] != message.from_user.id:
        return await message.answer("⛔ Only the buyer can release funds.")
        
    await db.execute("UPDATE group_deals SET status = 'completed' WHERE chat_id = $1", chat_id)
    await message.answer("✅ <b>Payment Released!</b>\nFunds should be sent to the seller's wallet.", parse_mode="HTML")
    
    # Notify Admin Group
    if ADMIN_GROUP_ID:
        try:
            link = await bot.export_chat_invite_link(chat_id)
            await bot.send_message(
                ADMIN_GROUP_ID, 
                f"💸 <b>PAYOUT REQUIRED</b>\n\n"
                f"Group: <a href='{link}'>{message.chat.title}</a>\n"
                f"Seller Wallet: <code>{deal['seller_wallet']}</code>\n"
                f"Currency: {deal['currency']}", 
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Failed to notify admin: {e}")

@router.message(Command("refundbuyer"))
async def cmd_refund(message: Message, bot: Bot):
    if not is_group(message): return await dm_block(message)
    
    chat_id = message.chat.id
    deal = await db.fetchrow("SELECT * FROM group_deals WHERE chat_id = $1 AND status = 'active'", chat_id)
    
    if not deal:
        return await message.answer("No active deal found.")
    if deal['seller_id'] != message.from_user.id:
        return await message.answer("⛔ Only the seller can initiate refund.")
        
    await db.execute("UPDATE group_deals SET status = 'refunded' WHERE chat_id = $1", chat_id)
    await message.answer("✅ <b>Deal Refunded!</b>\nFunds should be returned to the buyer.", parse_mode="HTML")
    
    # Notify Admin Group
    if ADMIN_GROUP_ID:
        try:
            link = await bot.export_chat_invite_link(chat_id)
            await bot.send_message(
                ADMIN_GROUP_ID, 
                f"↩️ <b>REFUND REQUIRED</b>\n\n"
                f"Group: <a href='{link}'>{message.chat.title}</a>\n"
                f"Buyer Wallet: <code>{deal['buyer_wallet']}</code>\n"
                f"Currency: {deal['currency']}", 
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Failed to notify admin: {e}")