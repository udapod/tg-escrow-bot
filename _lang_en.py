"""English (en) translations — all 222 keys."""

EN = {
    # ===== MENU BUTTONS =====
    "btn_catalog": "📋 Catalog",
    "btn_create_listing": "➕ Create Listing",
    "btn_my_deals": "📦 My Deals",
    "btn_my_listings": "📝 My Listings",
    "btn_vip": "👑 VIP Subscription",
    "btn_profile": "👤 Profile",
    "btn_search": "🔍 Search",
    "btn_help": "ℹ️ Help",

    # ===== INLINE BUTTONS =====
    "btn_start_deal": "🤝 Start Deal",
    "btn_seller_profile": "👤 Seller Profile",
    "btn_i_sent_usdt": "💰 I Sent USDT to Escrow",
    "btn_cancel_deal": "❌ Cancel Deal",
    "btn_order_done": "📦 Order Fulfilled / Item Shipped",
    "btn_open_dispute": "⚠️ Open Dispute",
    "btn_confirm_received": "✅ Confirm Receipt",
    "btn_leave_review": "⭐ Leave Review",
    "btn_yes": "✅ Yes",
    "btn_no": "❌ No",
    "btn_delete_listing": "🗑 Delete Listing",
    "btn_back_menu": "⬅️ Back to Menu",
    "btn_buy_vip": "👑 Buy VIP Subscription",
    "btn_i_paid_vip": "💰 I Paid for VIP",
    "btn_cancel": "❌ Cancel",

    # ===== CATEGORIES =====
    "cat_goods": "🛒 Goods",
    "cat_services": "🔧 Services",

    # ===== /start =====
    "welcome": (
        "🤝 <b>Welcome to HandshakeDeal!</b>\n\n"
        "🔐 <b>Trusted escrow protection</b> for P2P deals.\n"
        "Buy and sell goods & services safely!\n\n"
        "🛡 <b>How it works:</b>\n"
        "1️⃣ Seller creates a listing\n"
        "2️⃣ Buyer sends USDT to the <b>bot's escrow wallet</b>\n"
        "3️⃣ 🔓 Contact details are revealed\n"
        "4️⃣ Buyer confirms receipt\n"
        "5️⃣ Funds are released to the seller ⭐\n\n"
        "🎁 <b>First deal is commission-free!</b>\n"
        "❗ 2% penalty if cancelled after payment.\n\n"
        "Use the menu below 👇"
    ),

    # ===== Language selection =====
    "choose_lang": "🌐 Choose language / Выберите язык / Tilni tanlang:",
    "lang_set": "✅ Language set: English",

    # ===== LOCATION =====
    "choose_country": "🌍 Choose your country:",
    "choose_city": "🏙 Choose your city ({country}):",
    "city_other": "📝 Other city",
    "enter_city_manual": "✏️ Enter your city name:",
    "city_too_short": "❗ Name too short. Enter city name (2–50 characters):",
    "location_set": "📍 Location set: {country}, {city}",
    "btn_change_location": "📍 Change City",
    "profile_location": "📍 City",
    "location_not_set": "not specified",
    "set_location_first": "📍 Please set your location first — /location",
    "listing_city": "📍 City",
    "all_cities": "🌐 All cities",

    # ===== DEAL CHAT =====
    "btn_chat": "💬 Deal Chat",
    "chat_role_seller": "seller",
    "chat_role_buyer": "buyer",
    "chat_msg_from_buyer": "💬 <b>Buyer</b> (deal #{id}):\n{text}",
    "chat_msg_from_seller": "💬 <b>Seller</b> (deal #{id}):\n{text}",
    "chat_contact_blocked": (
        "🚫 Contact information (phone, @username, links) is blocked until escrow payment.\n"
        "It will be unlocked automatically after payment."
    ),
    "chat_sent": "✅ Sent",
    "chat_exited": "👋 You left the deal chat.",
    "chat_no_deal": "❗ Deal not found or already completed.",
    "chat_history_title": "📜 <b>Chat history — deal #{id}</b>\n",
    "chat_history_empty": "📜 No messages in deal #{id}.",
    "btn_view_chat_history": "📜 Chat History",

    # ===== MEETING =====
    "btn_propose_meet": "📍 Propose Meeting",
    "meet_enter_location": "📍 Enter the meeting location (address, mall, etc.):",
    "meet_enter_datetime": "🕐 Enter the meeting date and time (e.g. tomorrow 3:00 PM):",
    "meet_proposal_sent": "✅ Meeting proposal sent!",
    "meet_proposal_card": (
        "📍 <b>Meeting proposal — deal #{id}</b>\n\n"
        "🏠 Location: <b>{location}</b>\n"
        "🕐 Time: <b>{datetime}</b>\n\n"
        "If you want to change the time/place, reply in the deal chat."
    ),
    "meet_cancelled": "❌ Meeting proposal cancelled. Return to chat.",
    "chat_enter": (
        "💬 <b>Deal chat #{id}</b>\n\n"
        "You are chatting anonymously with the {role}.\n"
        "Type a message — the bot will deliver it.\n\n"
        "📍 /meet — propose a meeting\n"
        "/endchat — leave chat"
    ),

    # ===== /help =====
    "help": (
        "📖 <b>HandshakeDeal Rules & Terms</b>\n\n"
        "📝 <b>Main features:</b>\n"
        "📋 <b>Catalog</b> — browse listings in your city\n"
        "➕ <b>Create Listing</b> — post a product or service\n"
        "📦 <b>My Deals</b> — current and completed deals\n"
        "👤 <b>Profile</b> — rating, wallet, statistics\n\n"
        "🔐 <b>Escrow protection:</b>\n"
        "• Buyer sends USDT to the bot's wallet\n"
        "• Funds are frozen until receipt is confirmed\n"
        "• Seller receives payment only after deal completion\n"
        "• Auto-completion after 72 hours\n"
        "• Dispute = funds frozen until admin decision\n\n"
        "💰 <b>Commissions:</b>\n"
        "• 🎁 First deal — <b>commission-free (0%)</b>\n"
        "• 20–100 USDT — <b>3%</b> (min 2 USDT)\n"
        "• 100–500 USDT — <b>2%</b>\n"
        "• 500+ USDT — <b>1.5%</b>\n"
        "• 👑 VIP — half the rate\n"
        "• 👑 VIP subscription — <b>10 USDT</b>/month\n"
        "• Minimum deal amount — <b>20 USDT</b>\n\n"
        "💬 <b>Deal chat:</b>\n"
        "• Before payment — anonymous chat\n"
        "• After payment — 🔓 contacts unlocked\n"
        "• Share phone numbers, addresses\n"
        "• 📍 /meet — propose a meeting\n\n"
        "⚠️ <b>Cancellation:</b>\n"
        "• Before payment — free\n"
        "• After payment — <b>2% penalty</b>\n"
        "• Remaining funds returned to buyer\n\n"
        "💱 All transactions in USDT (TRC-20).\n"
        "📱 /qr — QR code to invite friends\n"
        "Support: /support"
    ),

    # ===== Profile =====
    "profile_title": "👤 <b>Your Profile</b>",
    "profile_vip_status": "👑 Status: <b>Verified (VIP)</b>",
    "profile_id": "🆔 ID",
    "profile_name": "📛 Name",
    "profile_rating": "⭐ Rating",
    "profile_deals": "📦 Completed deals",
    "profile_wallet": "💰 USDT Wallet (TRC-20)",
    "profile_reviews": "📝 Reviews",
    "wallet_not_set": "❌ Not set",
    "wallet_hint": "Set or change your wallet:\n/wallet <code>YOUR_TRC20_ADDRESS</code>",
    "wallet_prompt": "❗ Enter your USDT TRC-20 wallet:\n/wallet <code>T...</code>",
    "wallet_invalid": "❌ Invalid TRC-20 address format. The address must start with T and be 34 characters long.",
    "wallet_saved": "✅ Wallet saved",

    # ===== Other user profile =====
    "profile_view_title": "👤 <b>User Profile</b>",
    "profile_since": "📅 Member since",
    "profile_deals_count": "📦 Deals",

    # ===== Listings =====
    "press_start_first": "Please press /start first",
    "account_banned": "🚫 Your account has been banned. Contact: /support",
    "set_wallet_first": "❗ Set your USDT wallet (TRC-20) first:\n/wallet <code>YOUR_ADDRESS</code>",
    "choose_category": "Choose a category:",
    "invalid_category": "❌ Invalid category.",
    "enter_title": "📝 Enter the title (up to 100 characters):",
    "title_error": "❗ Title must be 3–100 characters. Try again:",
    "enter_description": "📋 Enter the description (up to 500 characters):",
    "desc_error": "❗ Description must be 10–500 characters. Try again:",
    "enter_price": "💰 Enter the price in USDT (number):",
    "enter_photo": "📸 Send a photo of the item/service or press /skip to skip:",
    "price_min_error": "❗ Minimum deal amount is {amount} USDT. Enter a higher price:",
    "price_error": "❗ Enter a valid price (0.01–1,000,000 USDT):",
    "listing_created": "✅ Listing #{id} created!\n\n📂 {cat}\n📌 {title}\n💰 {price} USDT\n\nNow visible in the catalog.",
    "no_listings_in_cat": "No listings in <b>{cat}</b> yet.",
    "listings_found": "📋 <b>{cat}</b> — {count} found:",
    "seller": "Seller",
    "price_label": "Price",
    "unknown_seller": "Unknown",
    "no_my_listings": "You have no listings yet. Press «➕ Create Listing».",
    "listing_active": "✅ Active",
    "listing_inactive": "❌ Inactive",
    "status_label": "Status",
    "confirm_delete_listing": "Delete listing #{id} «{title}»?",
    "listing_deleted": "✅ Listing deleted.",
    "action_cancelled": "❌ Action cancelled.",

    # ===== Deals =====
    "listing_unavailable": "❌ This listing is not available.",
    "cant_buy_own": "You cannot buy from yourself!",
    "min_deal_amount": "⚠️ Minimum deal amount is {amount} USDT",
    "seller_no_wallet": "Seller has not set up a wallet",
    "deal_created": (
        "🤝 <b>Deal #{id} created!</b>\n\n"
        "{vip_note}"
        "📌 {title}\n"
        "💰 Price: {price} USDT\n"
        "📊 Bot commission ({rate}%): {commission} USDT\n"
        "💵 <b>Total payment: {total} USDT</b>\n\n"
        "🔐 <b>ESCROW PROTECTION:</b>\n"
        "Your funds are frozen in the bot's wallet until\n"
        "you confirm receipt of the item/service.\n\n"
        "📋 Send <b>{total} USDT</b> to the bot's escrow wallet:\n"
        "<code>{wallet}</code>\n\n"
        "⚠️ Network: <b>TRC-20</b>\n"
        "After sending, press «💰 I Sent USDT to Escrow»"
    ),
    "deal_new_seller_notify": (
        "🔔 <b>New deal #{id}!</b>\n\n"
        "📌 {title}\n💰 {price} USDT\n"
        "👤 Buyer: {buyer}\n\n"
        "🔐 Buyer is sending funds to bot escrow.\n"
        "You will be notified when funds are locked."
    ),
    "deal_not_found": "Deal not found",
    "deal_status_locked": "Cannot change the status of this deal",
    "enter_tx_hash": (
        "📋 <b>Deal #{id}</b>\n\n"
        "Enter the transaction hash (TxID) for verification:\n\n"
        "💡 Hash looks like:\n"
        "<code>a1b2c3d4e5f6...</code> (64 characters)"
    ),
    "tx_hash_invalid": "❗ Invalid TxID format.\nA TRON transaction hash is 64 characters:\n<code>a1b2c3d4e5f6...</code>\nEnter a valid TxID:",
    "tx_already_used": "🚫 This TxID has already been used in another deal. Enter a different TxID:",
    "message_too_long": "⚠️ Message is too long (max 2000 characters).",
    "tx_verifying": "⏳ Verifying transaction on the TRON blockchain...",
    "tx_not_found": "❌ Transaction not found on the blockchain.\nCheck the TxID and try again:",
    "tx_wrong_wallet": "❌ Transaction found, but the recipient is not the bot's wallet.\nSend USDT to the correct address and enter the new TxID:",
    "tx_amount_mismatch": "❌ Transaction amount ({received} USDT) is less than required ({expected} USDT).\nSend the exact amount and enter the new TxID:",
    "tx_not_usdt": "❌ This is not a USDT TRC-20 transfer to the bot's wallet.\nSend USDT (TRC-20) and enter the correct TxID:",
    "tx_network_error": "⚠️ Could not verify the transaction (network error). Try again in a minute:",
    "tx_verified": "✅ Transaction verified on the blockchain!",
    "tx_admin_verified": (
        "✅ <b>Payment verified</b>\n\n"
        "🆔 Deal: #{id}\n"
        "📋 Item: {title}\n"
        "👤 Buyer: {buyer_id}\n"
        "👥 Seller: {seller_id}\n"
        "💵 Item price: {price} USDT\n"
        "💰 Escrow (with commission): {amount} USDT\n"
        "🔗 TxHash: <code>{tx}</code>"
    ),
    "tx_admin_failed": (
        "⚠️ <b>TxHash verification failed</b>\n\n"
        "🆔 Deal: #{id}\n"
        "📋 Item: {title}\n"
        "👤 Buyer: {buyer_id}\n"
        "👥 Seller: {seller_id}\n"
        "💰 Escrow: {amount} USDT\n"
        "❌ Reason: {reason}\n"
        "🔗 TxHash: <code>{tx}</code>\n"
        "🔄 Attempt: {attempt}/3"
    ),
    "tx_blocked": "🚫 Too many failed attempts. Deal is blocked — contact the administrator.",
    "tx_admin_blocked": (
        "🚫 <b>Deal blocked</b>\n\n"
        "🆔 Deal: #{id}\n"
        "📋 Item: {title}\n"
        "👤 Buyer: {buyer_id}\n"
        "👥 Seller: {seller_id}\n"
        "💰 Escrow: {amount} USDT\n"
        "❌ 3 failed TxHash verifications\n"
        "⚡ Manual review required"
    ),
    "deal_paid": (
        "✅ <b>Deal #{id} — payment recorded!</b>\n\n"
        "📌 {title}\n"
        "💰 {total} USDT frozen in escrow\n"
        "🔗 TxID: <code>{tx}</code>\n\n"
        "⏳ Waiting for the seller to fulfill the order...\n\n"
        "After receiving the item/service, press «✅ Confirm Receipt»."
    ),
    "deal_escrow_seller_notify": (
        "💰 <b>Deal #{id} — funds in escrow!</b>\n\n"
        "📌 {title}\n"
        "💵 {total} USDT frozen in the bot's wallet.\n"
        "🔗 Buyer TxID: <code>{tx}</code>\n\n"
        "✅ Buyer has paid. Fulfill the order and\n"
        "press «📦 Order Fulfilled»."
    ),
    "deal_delivered_seller": (
        "📦 <b>Deal #{id} — order fulfilled!</b>\n\n"
        "Waiting for buyer confirmation.\n\n"
        "⏳ If the buyer doesn't confirm within <b>{hours} hours</b>\n"
        "and doesn't open a dispute — the deal will auto-complete\n"
        "and funds will be sent to you."
    ),
    "deal_delivered_buyer_notify": (
        "📦 <b>Deal #{id} — seller fulfilled the order!</b>\n\n"
        "📌 {title}\n👤 Seller: {seller}\n\n"
        "If you received the item/service — confirm,\n"
        "and funds will be automatically sent to the seller.\n\n"
        "⚠️ If there's a problem — open a dispute.\n"
        "⏳ Auto-completion in <b>{hours} hours</b> if no response."
    ),
    "deal_completed_buyer": (
        "🎉 <b>Deal #{id} completed!</b>\n\n"
        "📌 {title}\n"
        "💵 {payout} USDT will be sent to the seller.\n"
        "📊 {commission} USDT commission collected by the bot.\n\n"
        "Thank you for your trust! Please leave a review:"
    ),
    "deal_completed_seller_notify": (
        "🎉 <b>Deal #{id} completed!</b>\n\n"
        "📌 {title}\n"
        "✅ Buyer confirmed receipt.\n"
        "💵 <b>{payout} USDT</b> will be sent to your wallet:\n"
        "<code>{wallet}</code>\n\n"
        "Please leave a review for the buyer:"
    ),
    "deal_cancelled": "❌ Deal #{id} cancelled.",
    "deal_cancelled_seller_notify": "❌ Deal #{id} cancelled by the buyer (before payment).",
    "cancel_only_before_pay": "Cancellation is only possible before escrow payment",
    "cancel_not_available": "Cancellation is not available right now",
    "deal_cancelled_penalty": (
        "❌ <b>Deal #{id} cancelled after payment</b>\n\n"
        "🔻 Cancellation penalty ({penalty_pct}%): <b>{penalty} USDT</b>\n"
        "💸 Refund: <b>{refund} USDT</b>\n\n"
        "The administrator will deduct the penalty and return the funds."
    ),
    "deal_cancelled_seller_after_pay": "❌ Deal #{id} ({title}) cancelled by the buyer after payment. Funds are being returned to the buyer.",
    "first_deal_free_note": "🎁 <b>First deal is commission-free!</b>\n",
    "chat_contacts_unlocked": "🔓 Payment confirmed — contact sharing is now unlocked!\nYou can now exchange phone numbers and addresses.",

    # ===== Disputes =====
    "dispute_opened": (
        "⚠️ <b>Dispute opened for deal #{id}!</b>\n\n"
        "🔐 Funds are frozen in escrow.\n"
        "An administrator will review the dispute and make a decision.\n\n"
        "No one receives funds until the dispute is resolved."
    ),
    "dispute_other_notify": "⚠️ Dispute opened for deal #{id}.\n🔐 Funds frozen until admin decision.",
    "dispute_only_escrow": "Disputes can only be opened when funds are in escrow",
    "no_access": "Access denied",

    # ===== Reviews =====
    "review_only_completed": "Reviews can only be left after a deal is completed",
    "review_not_participant": "You are not a participant of this deal",
    "review_rate": "⭐ Rate deal #{id}:",
    "review_comment": "💬 Write a comment (or send «-» to skip):",
    "review_comment_too_long": "❗ Comment must be under 300 characters. Try again:",
    "review_saved": "✅ Review saved!",

    # ===== My deals =====
    "no_deals": "You have no deals yet.",
    "my_deals_title": "📦 <b>Your deals:</b>",
    "role_buyer": "🛒 Buyer",
    "role_seller": "🏪 Seller",
    "deal_status_created": "🕐 Awaiting escrow payment",
    "deal_status_paid": "🔐 Funds in escrow (in progress)",
    "deal_status_delivered": "📦 Delivered (awaiting confirmation)",
    "deal_status_completed": "🎉 Completed",
    "deal_status_disputed": "⚠️ Dispute (funds frozen)",
    "deal_status_cancelled": "❌ Cancelled",
    "deal_status_refunded": "💸 Refunded",

    # ===== VIP =====
    "vip_active": (
        "👑 <b>You have an active VIP subscription!</b>\n\n"
        "✅ Status: Verified Seller\n"
        "📅 Expires: <b>{expires}</b>\n"
        "💰 Your commission: <b>{vip_rate}%</b> (instead of {rate}%)\n\n"
        "🛡 Benefits:\n"
        "• ✅ «Verified» badge on your profile\n"
        "• 📌 Priority in the catalog\n"
        "• 💰 Reduced commission {vip_rate}%\n"
        "• ⭐ Higher trust from buyers"
    ),
    "vip_offer": (
        "👑 <b>VIP Subscription</b>\n\n"
        "Become a verified seller and get:\n\n"
        "✅ «Verified» badge next to your name\n"
        "📌 Priority in the catalog\n"
        "💰 Reduced commission: <b>{vip_rate}%</b> (instead of {rate}%)\n"
        "⭐ Higher trust from buyers\n\n"
        "💵 Price: <b>{price} USDT / {days} days</b>"
    ),
    "vip_already_active": "You already have an active VIP subscription!",
    "vip_payment": (
        "👑 <b>VIP Subscription Payment</b>\n\n"
        "💵 Amount: <b>{price} USDT</b>\n"
        "📅 Duration: {days} days\n\n"
        "📋 Send <b>{price} USDT</b> to the bot's wallet:\n"
        "<code>{wallet}</code>\n\n"
        "⚠️ Network: <b>TRC-20</b>\n\n"
        "After sending, press «💰 I Paid for VIP»"
    ),
    "vip_enter_tx": "📋 <b>VIP Subscription — payment verification</b>\n\nEnter the transaction hash (TxID):",
    "vip_activated": (
        "🎉 <b>VIP subscription activated!</b>\n\n"
        "👑 You are now a verified seller!\n"
        "📅 Valid for {days} days\n"
        "💰 Your commission: {vip_rate}%\n"
        "✅ Verified badge on your profile\n\n"
        "🔗 TxID: <code>{tx}</code>"
    ),
    "vip_cancelled": "❌ VIP purchase cancelled.",
    "vip_seller_note": "👑 Seller is verified (VIP)\n",

    # ===== Main menu =====
    "main_menu": "Main menu 👇",
    "error_try_again": "Error. Please try again.",
    "deal_status_changed": "Deal not found or status has changed.",
    "cant_confirm_now": "Confirmation is not possible at this stage",
    "deal_not_at_execution": "Cannot mark — deal is not in execution stage",

    # ===== Account deletion =====
    "btn_delete_account": "🗑 Delete Account",
    "delete_account_confirm": (
        "⚠️ <b>Are you sure you want to delete your account?</b>\n\n"
        "This will delete:\n"
        "• Your profile and wallet\n"
        "• All your listings\n"
        "• VIP subscription\n\n"
        "❗ Active deals will not be affected.\n"
        "This action is <b>irreversible</b>!"
    ),
    "account_deleted": "✅ Your account has been deleted. All data has been removed.\nPress /start to register again",
    "delete_account_has_active_deals": "❌ Cannot delete account — you have active deals. Complete or cancel them first.",

    # ===== Support =====
    "support_prompt": "📩 Write your message to support:",
    "support_sent": "✅ Your message has been sent to the administrator. Please wait for a reply.",
    "support_too_long": "❗ Message is too long (max 1000 characters).",
    "support_cancelled": "❌ Support request cancelled.",

    # ===== Pagination =====
    "page_label": "page",

    # ===== Search =====
    "search_prompt": "🔍 Enter your search query (product/service name or description):",
    "search_too_short": "❗ Query is too short. Enter at least 2 characters.",
    "search_results": "🔍 Found {count} for <b>{query}</b>:",
    "search_no_results": "🔍 Nothing found for <b>{query}</b>.",
    "search_cancelled": "↩️ Search cancelled.",

    # ===== Reviews (view) =====
    "btn_view_reviews": "📝 Reviews",
    "reviews_title": "📝 <b>Reviews for {name}</b>  (⭐ {rating})\n\n",
    "no_reviews": "This user has no reviews yet.",
    "review_item": "{'⭐' * rating}  — <i>{comment}</i>\n📅 {date}\n\n",

    # ===== QR =====
    "qr_bot_caption": "📱 QR code to access the bot\nScan or share with friends!",
    "qr_wallet_caption": "📋 Escrow wallet QR code for deal #{id} payment",

    # ===== Referral program =====
    "referral_welcome_bonus": "🎁 You were invited by a user! Welcome to HandshakeDeal!",
    "referral_new_user_notify": "🎉 A new user registered via your referral link: <b>{name}</b>!",
    "referral_info": (
        "👥 <b>Referral Program</b>\n\n"
        "Your link:\n<code>{link}</code>\n\n"
        "📊 Invited: <b>{total}</b>\n"
        "✅ Made a deal: <b>{active}</b>\n\n"
        "🎁 Invited users get their <b>first deal commission-free</b>.\n"
        "Share your link and grow the platform!"
    ),
    "btn_referral": "👥 Referral Program",

    # ===== Reputation =====
    "reputation_level": "{emoji} Level: <b>{name}</b>",
    "reputation_discount_note": "📉 Reputation commission discount: <b>−{discount}%</b>",
    "reputation_bronze": "Bronze",
    "reputation_silver": "Silver",
    "reputation_gold": "Gold",

    # ===== Photo reviews =====
    "review_photo_prompt": "📸 Attach a photo (product, result, etc.) or press /skip to skip:",

    # ===== Favorites =====
    "btn_follow_seller": "⭐ Follow",
    "btn_unfollow_seller": "💔 Unfollow",
    "btn_favorites": "⭐ Favorites",
    "followed_seller": "⭐ You are now following <b>{name}</b>. You'll be notified about new listings.",
    "unfollowed_seller": "💔 You unfollowed <b>{name}</b>.",
    "favorites_empty": "⭐ You're not following any sellers yet.\nFollow sellers from their profile in the catalog.",
    "favorites_list_title": "⭐ <b>Your subscriptions:</b>\n",
    "new_listing_notify_follower": (
        "🔔 New listing from a seller you follow!\n\n"
        "👤 {seller}\n"
        "📌 <b>{title}</b>\n"
        "💰 {price} USDT\n"
        "📍 {city}"
    ),
    "cant_follow_self": "❌ You cannot follow yourself",
    "profile_followers": "👥 Followers",
    "profile_referrals": "👥 Referrals",

    # ===== Miscellaneous =====
    "create_listing_cancelled": "❌ Listing creation cancelled.",
    "city_input_cancelled": "❌ City input cancelled.",
    "support_rate_limit": "⏳ Please wait a moment before submitting another request.",
    "resolve_confirm_seller": (
        "⚠️ <b>Confirm dispute resolution #{id}</b>\n\n"
        "Action: payment to seller\n"
        "💰 Amount: {payout} USDT → <code>{wallet}</code>\n\n"
        "Are you sure?"
    ),
    "resolve_confirm_buyer": (
        "⚠️ <b>Confirm dispute resolution #{id}</b>\n\n"
        "Action: refund to buyer\n"
        "💰 Amount: {total} USDT\n\n"
        "Are you sure?"
    ),
    "followers_notified": "📣 Followers notified: {count}",
    "btn_change_lang": "🌐 Change Language",
    "vip_days_left": "⏳ Days remaining: <b>{days}</b>",
}
