# Self-contained language file for Yeetop Escrow Bot

TEXTS = {
    "welcome": {
        "en": (
            "🕊 <b>YEETOP ESCROW BOT</b> 🕊\n"
            "Automated Escrow for Safe Transactions\n\n"
            "Yo, welcome to YeeTopEscrowBot—your ultimate shield in these gritty streets of Telegram deals. We put your money on lockdown with military-grade security— no switch-ups. Your bread stays safe till the deal is done.\n\n"
            "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
            "💰 <b>ESCROW FEE:</b>\n"
            "5% for amounts over $100\n"
            "$5 for amounts under $100\n\n"
            "ℹ️ <b>How To Use YEETOP ESCROW BOT?</b>\n\n"
            "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
            "1️⃣ Create a new Group Chat with seller / buyer and add the bot.\n\n"
            "2️⃣ Seller: Declare your role by using the command <code>/seller LTC/USDT(trc20) ADDRESS</code>, replacing LTC/USDT(trc20) ADDRESS with your respective wallet address.\n\n"
            "3️⃣ Buyer: Declare your role by using the command <code>/buyer LTC/USDT(trc20) ADDRESS</code>, replacing LTC/USDT(trc20) ADDRESS with your respective wallet address.\n\n"
            "4️⃣ The bot will generate an escrow address automatically.\n\n"
            "5️⃣ Both buyer and seller verify the generated escrow address in @YeetopVerifyBot.\n\n"
            "6️⃣ The buyer sends the agreed amount to the ESCROW address.\n\n"
            "7️⃣ Check the balance using the command <code>/balance</code>.\n\n"
            "8️⃣ The seller releases the product/service to the buyer once the balance is confirmed.\n\n"
            "9️⃣ When the buyer is satisfied, release the payment using <code>/payseller</code>. Alternatively, the seller can initiate a refund to the buyer using <code>/refundbuyer</code>.\n\n"
            "🔟 Got beef with a deal? Hit <code>/contact Invite/Group chat link</code> and our arbitrators will slide into your chat within 24 hours to settle it. No runnin', no duckin'—just fair play."
        )
    }
}

def t(lang: str, key: str, **kwargs) -> str:
    """Get translation by key and language."""
    entry = TEXTS.get(key, {})
    # Default to English if the language isn't found
    text = entry.get(lang, entry.get("en", key))
    if kwargs:
        text = text.format(**kwargs)
    return text