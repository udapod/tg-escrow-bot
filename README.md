

```markdown
# 🕊 YEETOP ESCROW BOT

**Telegram group-chat escrow bot for safe USDT (TRC-20) and Litecoin trades.**

A fully automated Telegram bot that acts as an escrow guarantor for peer-to-peer deals inside group chats. Buyers and sellers trade goods & services while crypto funds are frozen in the bot's wallet until the deal is confirmed. No trust needed — the blockchain verifies everything.

---

## 🔐 How It Works

```
Buyer                         Bot (Escrow)                  Seller
  │                              │                              │
  │── /buyer LTC wallet ────────>│                              │
  │                              │<── /seller LTC wallet ───────│
  │                              │── 🤝 DEAL ACTIVE ───────────>│
  │                              │── Escrow address ───────────>│
  │                              │                              │
  │── Crypto → escrow ──────────>│ 🔐 Funds frozen              │
  │                              │                              │
  │                              │<── Product delivered ────────│
  │<── Received! ────────────────│                              │
  │                              │                              │
  │── /payseller ───────────────>│                              │
  │   [✅ Confirm & Release]     │                              │
  │                              │── 💵 Payout to seller ──────>│
  │                              │                              │
  │── ⭐ Reply to review ───────>│<── ⭐ Reply to review ───────│
```

1. Seller and buyer add the bot to a group chat and promote it to admin
2. Both register their roles and wallet addresses via `/seller` and `/buyer` commands
3. Bot locks the deal to the matching currency and displays the escrow address
4. Buyer sends funds to the escrow address, seller delivers the product/service
5. Buyer types `/payseller` to release funds (with confirmation gate)
6. Bot prompts both parties for reviews, which are forwarded to the review channel

**5% escrow fee, minimum $5**

---

## ✨ Features

### Core
- **Group-Chat Escrow** — deals happen inside private group chats, not public catalogs
- **Multi-Currency** — USDT (TRC-20) and Litecoin (LTC) with auto-detection
- **Address Validation** — regex validation prevents invalid wallet submissions
- **Currency Locking** — once first party registers, the other must match the network
- **Role Locking** — users cannot switch between buyer and seller mid-deal
- **Confirmation Gates** — irreversible actions require explicit confirmation with warning

### Trust & Security
- **Bot-As-Admin Required** — bot refuses to operate unless promoted to admin in the group
- **Dispute Intervention** — admins can force-release or force-refund when parties disagree
- **Ban System** — admins can ban users from using the bot globally
- **Terms of Service** — built-in TOS with liability disclaimers and evidence requirements
- **Scam Education** — `/avoidscam` command with educational GIF

### Admin Override
- **Dynamic Admins** — root admin can add other admins via `/addadmin`
- **Force Commands** — `/forcepay` and `/forcerefund` work directly in the deal group
- **Active Deal Monitor** — `/active` shows all ongoing deals with quick-action buttons
- **Review Channel** — user reviews automatically forwarded to designated channel

### User Experience
- **Inline Buttons** — clickable confirmation cards instead of text-only prompts
- **QR Codes** — `/qr` generates QR for the active deal's escrow address
- **Group Review System** — bot posts review prompt in group, users reply to submit feedback
- **Clear Error Messages** — descriptive errors for invalid addresses, currency mismatches, role conflicts

---

## 💰 Fee Structure

| Condition | Fee |
|-----------|-----|
| All deals | **5%** of transaction amount |
| Minimum fee | **$5** (for deals under $100) |

No VIP tiers, no referral discounts, no progressive scales. Simple and transparent.

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/udapod/tg-escrow-bot.git
cd tg-escrow-bot
pip install -r requirements.txt
```

### 2. Configure
Copy `.env.example` → `.env` and fill in:

```env
BOT_TOKEN=123456:ABC-DEF...           # Token from @BotFather
ADMIN_ID=123456789                     # Your Telegram user ID
ADMIN_GROUP_ID=-1001234567890          # Your admin group chat ID
REVIEW_CHANNEL_ID=-1009876111110       # Your review channel ID
BOT_WALLET=T...                        # TRC-20 wallet for USDT escrow
BOT_WALLET_LTC=L...                    # Litecoin wallet for LTC escrow
DATABASE_URL=postgresql://...          # Supabase connection string
REDIS_URL=rediss://...                 # Upstash Redis connection string
```

### 3. Deploy to Vercel
```bash
vercel --prod
```

### Docker (optional)
```bash
docker-compose up -d
```

---

## 📂 Project Structure

```
tg-escrow-bot/
├── api/
│   └── index.py              # FastAPI webhook endpoint, bot initialization
├── db/
│   └── core.py               # PostgreSQL schema, connection pool, query helpers
├── handlers/
│   ├── common.py             # /start, /terms, /contactadmin, /ban, /unban, /addadmin, /avoidscam
│   └── group_escrow.py       # /seller, /buyer, /payseller, /refundbuyer, /forcepay, /forcerefund
├── config.py                 # Environment variables, wallet addresses, admin IDs
├── database.py               # High-level database functions (get_user, create_deal, etc.)
├── languages.py              # Single-language text strings (English)
├── yee.gif                   # Educational "How to Avoid Scam" GIF
├── requirements.txt          # Python dependencies
├── vercel.json               # Vercel deployment configuration
├── .env.example              # Environment variable template
├── Dockerfile                # Docker container definition
└── README.md                 # This file
```

---

## 🤖 Bot Commands

### User Commands (Group Chat Only)

| Command | Description |
|---------|-------------|
| `/start` | Display welcome message with Terms and Contact buttons |
| `/seller USDT WALLET` | Register as seller with USDT TRC-20 wallet |
| `/seller LTC WALLET` | Register as seller with Litecoin wallet |
| `/buyer USDT WALLET` | Register as buyer with USDT TRC-20 wallet |
| `/buyer LTC WALLET` | Register as buyer with Litecoin wallet |
| `/payseller` | Release escrow funds to seller (buyer only, requires confirmation) |
| `/refundbuyer` | Refund escrow funds to buyer (seller only, requires confirmation) |
| `/qr` | Generate QR code for active deal's escrow address |
| `/terms` | Display full Terms of Service |
| `/contactadmin` | Send support request to admin group |
| `/avoidscam` | Display educational scam-prevention GIF |

### Admin Commands

| Command | Description |
|---------|-------------|
| `/addadmin USER_ID` | Grant admin privileges to another user (root admin only) |
| `/ban USER_ID` | Ban user from using the bot globally |
| `/unban USER_ID` | Remove user ban |
| `/active` | View all active deals with force-action buttons |
| `/forcepay` | Force-release funds to seller (in deal group, admin only) |
| `/forcerefund` | Force-refund funds to buyer (in deal group, admin only) |
| `/chatid` | Display current chat/group ID |

---

## 🛡 Security Features

- **Bot-as-Admin Required** — refuses to operate unless promoted to admin in the group
- **Currency Locking** — prevents mismatched currency deals
- **Role Locking** — prevents users from switching buyer/seller roles
- **Confirmation Gates** — irreversible actions require explicit confirmation with "THIS ACTION CAN'T BE UNDONE" warning
- **Admin Override** — admins can force-resolve disputes when parties are uncooperative
- **Global Ban System** — banned users cannot use any bot commands
- **Address Validation** — regex prevents invalid wallet addresses from being registered
- **No Side Deals** — Terms of Service explicitly state bot is not liable for off-platform agreements

---

## 📝 Review System

When a deal completes (via `/payseller`, `/refundbuyer`, or admin override):
1. Bot posts a review prompt in the group chat
2. Tags both buyer and seller
3. Users reply directly to the bot's message with their feedback
4. Bot forwards the review to the designated review channel

No DMs, no spam, no ban risk.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

**Built with aiogram + FastAPI + PostgreSQL + Vercel**
```

