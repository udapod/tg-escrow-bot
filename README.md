# 🤝 HandshakeDealBot

A Telegram bot for secure P2P deals with a built-in **escrow guarantor**. Buy and sell goods and services between users — all transactions via **USDT (TRC-20)**, funds are held in escrow until the deal is completed.

## 🔐 Core Principle — Security

**The bot acts as a smart contract:** the buyer's funds are frozen on the bot's wallet and released to the seller **only after the buyer confirms receipt of the goods/services**. No one can cheat — funds are protected.

## 📋 Features

- **Escrow Guarantor** — funds held on the bot's wallet until the deal is complete
- **Automated Flow** — no admin intervention needed for standard deals
- **Auto-Completion** — deal auto-completes 72h after delivery if no dispute is raised
- **Dispute System** — funds remain frozen until the admin resolves the dispute
- **Listings Catalog** — goods and services with categories
- **Ratings & Reviews** — 1–5 star rating after each deal
- **Admin Panel** — statistics, bans, disputes, escrow monitoring

## 🔄 How a Deal Works (Automated Flow)

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
  │<── Order delivered! ─────────│                              │
  │                              │                              │
  │── ✅ Confirm receipt ───────>│                              │
  │                              │── 💵 Payout to seller ──────>│
  │                              │                              │
  │── ⭐ Review ────────────────>│<── ⭐ Review ────────────────│
```

### Fraud Protection:
- **Seller won't receive funds** until the buyer confirms receipt
- **Buyer won't lose funds** — in case of a dispute, funds stay frozen
- **72h auto-timer** — if the buyer is silent and doesn't dispute, the deal completes automatically
- **Admin resolves disputes** — both parties are protected in case of conflict

## 🚀 Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configuration
Copy `.env.example` → `.env` and fill in the values:

```env
BOT_TOKEN=123456:ABC-DEF...       # Token from @BotFather
ADMIN_ID=123456789                 # Your Telegram ID
BOT_COMMISSION=2                   # Commission in % (2 = 2%)
BOT_WALLET=T...                    # TRC-20 wallet for escrow
AUTO_COMPLETE_HOURS=72             # Auto-completion (hours)
```

### 3. Run
```bash
python bot.py
```

## 📂 Project Structure

```
HandshakeDealBot/
├── bot.py              # Entry point + auto-completion background task
├── config.py           # Configuration, escrow statuses
├── database.py         # SQLite: users, listings, deals, reviews
├── keyboards.py        # Inline and Reply keyboards
├── handlers/
│   ├── common.py       # /start, /help, profile, admin, wallet
│   ├── listings.py     # Create/browse/delete listings
│   └── deals.py        # Escrow deals, disputes, reviews, auto-completion
├── requirements.txt
├── .env.example
└── README.md
```

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Register and open the main menu |
| `/help` | Help on escrow and usage |
| `/wallet T...` | Set your USDT wallet (TRC-20) |
| `/admin` | Admin panel (admin only) |
| `/ban ID` | Ban a user |
| `/unban ID` | Unban a user |
| `/resolve ID seller` | Resolve dispute — pay the seller |
| `/resolve ID buyer` | Resolve dispute — refund the buyer |

## ⚠️ Important

- The bot acts as an **escrow guarantor** — all funds pass through the bot's wallet
- The seller receives payout **only after confirmation** by the buyer
- In case of a dispute — funds are **frozen** until the admin's decision
- Auto-completion after 72h protects the seller from buyer inactivity
- Network: **TRC-20** (TRON) for USDT
