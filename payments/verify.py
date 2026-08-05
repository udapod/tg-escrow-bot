import os
from decimal import Decimal

import aiohttp

USDT_TRC20_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=8)


def _decimal_to_int(value, decimals: int) -> int:
    return int((Decimal(str(value)) * Decimal(10) ** decimals).to_integral_value())


async def _trongrid_get(session: aiohttp.ClientSession, url: str):
    headers = {}

    api_key = os.getenv("TRONGRID_API_KEY")
    if api_key:
        headers["TRON-PRO-API-KEY"] = api_key

    async with session.get(url, headers=headers, timeout=DEFAULT_TIMEOUT) as resp:
        if resp.status != 200:
            return None

        try:
            return await resp.json()
        except Exception:
            return None


async def _get_current_tron_block(session: aiohttp.ClientSession):
    data = await _trongrid_get(
        session,
        "https://api.trongrid.io/v1/blocks/current",
    )

    if not data:
        return None

    try:
        return data["data"][0]["block_header"]["raw_data"]["number"]
    except Exception:
        return None


async def verify_usdt_trc20(tx_hash: str, amount, receiver_address: str) -> bool:
    tx_hash = tx_hash.strip()
    receiver_address = receiver_address.strip()

    if not tx_hash or not receiver_address:
        return False

    expected_amount = _decimal_to_int(amount, 6)
    min_confirmations = int(os.getenv("MIN_TRC20_CONFIRMATIONS", "1"))

    async with aiohttp.ClientSession() as session:
        tx_data = await _trongrid_get(
            session,
            f"https://api.trongrid.io/v1/transactions/{tx_hash}",
        )

        if not tx_data or not tx_data.get("success"):
            return False

        tx_items = tx_data.get("data", [])
        if not tx_items:
            return False

        tx = tx_items[0]

        try:
            contract_result = tx["ret"][0]["contractRet"]
        except Exception:
            return False

        if contract_result != "SUCCESS":
            return False

        block_number = tx.get("blockNumber")

        if block_number:
            current_block = await _get_current_tron_block(session)

            if current_block:
                confirmations = current_block - block_number + 1

                if confirmations < min_confirmations:
                    return False

        events_data = await _trongrid_get(
            session,
            f"https://api.trongrid.io/v1/transactions/{tx_hash}/events",
        )

        if not events_data:
            return False

        events = events_data.get("data", [])

        for event in events:
            if event.get("event_name") != "Transfer":
                continue

            if event.get("contract_address") != USDT_TRC20_CONTRACT:
                continue

            result = event.get("result", {})

            to_address = str(result.get("to", "")).strip()

            if to_address != receiver_address:
                continue

            try:
                value = int(result.get("value", 0))
            except Exception:
                continue

            if value == expected_amount:
                return True

    return False


async def verify_ltc(tx_hash: str, amount, receiver_address: str) -> bool:
    tx_hash = tx_hash.strip()
    receiver_address = receiver_address.strip()

    if not tx_hash or not receiver_address:
        return False

    expected_satoshis = _decimal_to_int(amount, 8)
    min_confirmations = int(os.getenv("MIN_LTC_CONFIRMATIONS", "3"))

    url = f"https://api.blockcypher.com/v1/ltc/main/txs/{tx_hash}"
    params = {}

    token = os.getenv("BLOCKCYPHER_TOKEN")
    if token:
        params["token"] = token

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, timeout=DEFAULT_TIMEOUT) as resp:
            if resp.status != 200:
                return False

            try:
                data = await resp.json()
            except Exception:
                return False

    if data.get("double_spend"):
        return False

    confirmations = data.get("confirmations", 0)

    if confirmations < min_confirmations:
        return False

    outputs = data.get("outputs", [])

    for output in outputs:
        addresses = output.get("addresses") or []

        if receiver_address not in addresses:
            continue

        value = output.get("value", 0)

        if value >= expected_satoshis:
            return True

    return False


async def verify_payment(currency: str, tx_hash: str, amount) -> bool:
    if not currency or not tx_hash:
        return False

    currency = currency.upper().strip()

    if currency in {"USDT", "TRC20", "USDT_TRC20"}:
        receiver = os.getenv("TRC20_ESCROW_ADDRESS", "").strip()
        return await verify_usdt_trc20(tx_hash, amount, receiver)

    if currency in {"LTC", "LITECOIN"}:
        receiver = os.getenv("LTC_ESCROW_ADDRESS", "").strip()
        return await verify_ltc(tx_hash, amount, receiver)

    return False