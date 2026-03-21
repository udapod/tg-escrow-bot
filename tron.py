"""
Модуль проверки USDT TRC-20 транзакций через TronGrid API.
"""
import logging

import aiohttp
from config import BOT_WALLET, TRONGRID_API_KEY

logger = logging.getLogger(__name__)

# Адрес USDT-контракта в сети TRON
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

TRONGRID_URL = "https://api.trongrid.io"


async def verify_tx(tx_hash: str, expected_amount: float) -> dict:
    """
    Проверяет транзакцию по TxID:
    - Существует ли
    - Это USDT TRC-20 перевод
    - Получатель — кошелёк бота (BOT_WALLET)
    - Сумма >= expected_amount

    Возвращает:
        {"ok": True, "amount": float, "from": str}
        или {"ok": False, "error": str}
    """
    if not TRONGRID_API_KEY:
        # Без API-ключа пропускаем проверку (обратная совместимость)
        logger.warning("TRONGRID_API_KEY не задан! Верификация транзакций ОТКЛЮЧЕНА.")
        return {"ok": True, "amount": expected_amount, "from": "unknown", "skipped": True}

    headers = {"TRON-PRO-API-KEY": TRONGRID_API_KEY}

    try:
        async with aiohttp.ClientSession() as session:
            # 1. Получаем информацию о транзакции
            url = f"{TRONGRID_URL}/v1/transactions/{tx_hash}/events"
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return {"ok": False, "error": "tx_network_error"}
                data = await resp.json()

            events = data.get("data", [])
            if not events:
                return {"ok": False, "error": "tx_not_found"}

            # 2. Ищем событие Transfer USDT
            found_usdt_transfer = False
            for event in events:
                contract = event.get("contract_address", "")
                event_name = event.get("event_name", "")

                if contract != USDT_CONTRACT or event_name != "Transfer":
                    continue

                found_usdt_transfer = True
                result = event.get("result", {})
                to_addr = result.get("to", "")
                from_addr = result.get("from", "")
                value_raw = int(result.get("value", "0"))

                # USDT имеет 6 десятичных знаков
                amount = value_raw / 1_000_000

                # 3. Проверяем получателя
                # TronGrid возвращает адреса в hex — конвертируем BOT_WALLET в hex для сравнения
                bot_wallet_hex = _tron_address_to_hex(BOT_WALLET)

                if to_addr.lower() != bot_wallet_hex.lower():
                    continue

                # 4. Проверяем сумму (допускаем погрешность 0.01 USDT)
                if amount < expected_amount - 0.01:
                    return {
                        "ok": False,
                        "error": "tx_amount_mismatch",
                        "expected": expected_amount,
                        "received": amount,
                    }

                return {"ok": True, "amount": amount, "from": from_addr}

            if found_usdt_transfer:
                return {"ok": False, "error": "tx_wrong_wallet"}
            return {"ok": False, "error": "tx_not_usdt"}

    except aiohttp.ClientError:
        return {"ok": False, "error": "tx_network_error"}
    except Exception:
        return {"ok": False, "error": "tx_network_error"}


def _tron_address_to_hex(address: str) -> str:
    """Конвертирует TRON Base58 адрес в hex (без префикса 41)."""
    import base58
    decoded = base58.b58decode_check(address)
    # decoded[0] = 0x41 (TRON prefix), остальное — 20 байт адреса
    return decoded[1:].hex()
