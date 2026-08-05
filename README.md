# 🤝 HandshakeDeal Bot

**Telegram P2P escrow bot for safe USDT TRC-20 trades.**

A fully automated Telegram bot that acts as an escrow guarantor for peer-to-peer deals. Buyers and sellers trade goods & services while USDT funds are frozen in the bot's wallet until delivery is confirmed. No trust needed — the blockchain verifies everything.

[![Open Source](https://img.shields.io/badge/Open%20Source-yes-brightgreen)](#license)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-0088cc)](https://core.telegram.org/bots)
[![USDT TRC-20](https://img.shields.io/badge/USDT-TRC--20-26A17B)](https://tron.network)

---

## 🔐 How It Works

```
Buyer                         Bot (Escrow)                  Seller
  │                              │                              │
  │── Start deal ───────────────>│                              │
  │                              │── Notification ─────────────>│
  │── USDT → bot wallet ────────>│                              │
  │── Submit TxID ──────────────>│ 🔐 Funds frozen              │
  │                              │── Funds in escrow! ─────────>│
  │                              │                              │
  │                              │<── Order fulfilled ──────────│
  │<── Delivered! ───────────────│                              │
  │                              │                              │
  │── ✅ Confirm receipt ───────>│                              │
  │                              │── 💵 Payout to seller ──────>│
  │                              │                              │
  │── ⭐ Review ────────────────>│<── ⭐ Review ────────────────│
```

1. Seller creates a listing (goods or services)
2. Buyer starts a deal → sends USDT to the bot's escrow wallet
3. Bot verifies the transaction on TRON blockchain (TxHash)
4. Contacts are unlocked → anonymous deal chat becomes open
5. Buyer confirms receipt → funds released to seller
6. Both parties leave reviews

**First deal is commission-free!**

---

## ✨ Features

### Core
- **Escrow Protection** — USDT frozen on bot wallet until buyer confirms receipt
- **Blockchain Verification** — TxHash checked via TronGrid API (amount, recipient, token)
- **Auto-Completion** — deal auto-completes 72h after delivery if no dispute
- **Dispute System** — funds stay frozen until admin resolves the conflict

### Trading
- **Listings Catalog** — goods & services with categories, search, pagination
- **Location-Based** — 6 countries, 50+ cities, localized country names
- **Deal Chat** — anonymous messaging before payment, contacts unlocked after
- **Meeting Proposals** — suggest time & place for in-person deals

### Trust & Reputation
- **Star Ratings** — 1–5 stars after each deal with text & photo reviews
- **Reputation Levels** — Bronze → Silver → Gold with commission discounts
- **VIP Subscriptions** — verified seller badge, priority in catalog, lower fees
- **Seller Favorites** — follow sellers, get notified about new listings

### Growth
- **Referral Program** — invite link + tracking, first deal free for referrals
- **QR Codes** — shareable QR for bot link and escrow payment wallets
- **7 Languages** — English, Russian, Turkish, Uzbek, Kazakh, Kyrgyz, Tajik

### Admin
- **Admin Panel** — `/admin` with statistics, user management, dispute resolution
- **Ban/Unban** — block fraudulent users
- **Dispute Resolution** — pay seller or refund buyer with confirmation
- **Escrow Monitoring** — track all active deals and frozen funds

---

## 💰 Commission Structure

| Deal Amount | Standard | VIP (50% off) |
|-------------|----------|----------------|
| First deal  | **0% (free!)** | **0% (free!)** |
| 20–100 USDT | 3% (min 2 USDT) | 1.5% |
| 100–500 USDT | 2% | 1% |
| 500+ USDT | 1.5% | 0.75% |
| Cancellation after payment | 2% penalty | 2% penalty |

**VIP subscription:** 10 USDT / 30 days

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/GrossBuilder/HandshakeDealBot.git
cd HandshakeDealBot
pip install -r requirements.txt
```

### 2. Configure
Copy `.env.example` → `.env` and fill in:

```env
BOT_TOKEN=123456:ABC-DEF...       # Token from @BotFather
ADMIN_ID=123456789                 # Your Telegram user ID
BOT_WALLET=T...                    # TRC-20 wallet for escrow
TRONGRID_API_KEY=...               # TronGrid API key
AUTO_COMPLETE_HOURS=72             # Auto-completion timer
```

### 3. Run
```bash
python bot.py
```

### Docker (optional)
```bash
docker-compose up -d
```

---

## 📂 Project Structure

```
HandshakeDealBot/
├── bot.py                # Entry point, background tasks
├── config.py             # Configuration, commission calc, statuses
├── database.py           # SQLite: users, listings, deals, reviews
├── keyboards.py          # Inline & Reply keyboards
├── languages.py          # Translation system (222 keys × 7 langs)
├── tron.py               # TronGrid API — blockchain verification
├── qr_utils.py           # QR code generation
├── contact_filter.py     # Contact info filtering for chat
├── _lang_en.py           # English translations
├── _lang_tr.py           # Turkish translations
├── _lang_tg.py           # Tajik translations
├── _lang_ky.py           # Kyrgyz translations
├── handlers/
│   ├── common.py         # /start, /help, profile, admin, wallet, lang
│   ├── listings.py       # Create/browse/search/delete listings
│   ├── deals.py          # Escrow deals, disputes, reviews, chat
│   └── vip.py            # VIP subscriptions & payment
├── docker-compose.yml    # Docker deployment
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Register and open the main menu |
| `/lang` | Change interface language |
| `/location` | Set your city |
| `/help` | Rules, commissions, how escrow works |
| `/wallet T...` | Set your USDT wallet (TRC-20) |
| `/qr` | Get QR code to share the bot |
| `/support` | Contact admin support |
| `/meet` | Propose a meeting (in deal chat) |
| `/admin` | Admin panel (admin only) |
| `/resolve ID seller/buyer` | Resolve dispute (admin only) |
| `/ban ID` / `/unban ID` | Ban/unban user (admin only) |

---

## 🌍 Supported Languages

| Flag | Language | Code |
|------|----------|------|
| 🇺🇸 | English | `en` |
| 🇷🇺 | Русский | `ru` |
| 🇹🇷 | Türkçe | `tr` |
| 🇺🇿 | O'zbek | `uz` |
| 🇰🇿 | Қазақша | `kk` |
| 🇰🇬 | Кыргызча | `ky` |
| 🇹🇯 | Тоҷикӣ | `tg` |

All 222 UI strings are fully translated for every language. No mixed-language interfaces.

---

## 🛡 Fraud Protection

- **Seller can't steal** — funds released only after buyer confirmation
- **Buyer can't scam** — funds frozen in escrow, visible on blockchain
- **72h auto-timer** — protects seller from unresponsive buyers
- **TxHash verification** — bot checks amount, recipient, and token on-chain
- **3 attempt limit** — deal blocked after 3 failed payment verifications
- **Contact filtering** — phone numbers and links blocked before escrow payment
- **Admin disputes** — manual resolution when parties disagree
 **Admin disputes** — manual resolution when parties disagree

---

## 📄 License

[MIT License](LICENSE) — free to use, modify, and distribute.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

**Built with [aiogram](https://docs.aiogram.dev/) + [TronGrid API](https://www.trongrid.io/) + [aiosqlite](https://aiosqlite.omnilib.dev/)**
