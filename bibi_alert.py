import requests
from web3 import Web3
import time

# --- הגדרות ---
ALCHEMY_API_KEY = 'zq_ZbyEWvCD5sCMzN_MsL' https://eth-mainnet.g.alchemy.com/v2/zq_ZbyEWvCD5sCMzN_MsL
ALCHEMY_URL = f'https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}'

web3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

TOKEN_ADDRESS = Web3.to_checksum_address('0xfA21cc13462fD156a2d11EB7b5c4812154C6f485')
UNISWAP_V3_FACTORY = Web3.to_checksum_address('0x1F98431c8aD98523631AE4a59f267346ea31F984')

# טלגרם
TELEGRAM_BOT_TOKEN = '8425080568:AAEBS05iTDNkp6TzGgJ-QJp156dzMpVdMB4'
TELEGRAM_CHAT_ID = '@bibicoinradar'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    print(response.json())

# התחברות
if not web3.is_connected():
    raise Exception("❌ חיבור ל־Ethereum נכשל")

send_telegram_message("✅ BIBI Bot התחיל לעקוב אחרי עסקאות Uniswap V3...")

def is_bibi_swap_v3(tx):
    if tx.to is None:
        return False

    try:
        tx_receipt = web3.eth.get_transaction_receipt(tx.hash)
        for log in tx_receipt.logs:
            if TOKEN_ADDRESS.lower() in log['address'].lower():
                return True
    except Exception as e:
        print("⚠️ שגיאה בקריאת טרנזקציה:", e)
    return False

latest = web3.eth.block_number

while True:
    try:
        current = web3.eth.block_number

        if current > latest:
            for block_number in range(latest + 1, current + 1):
                block = web3.eth.get_block(block_number, full_transactions=True)

                for tx in block.transactions:
                    if is_bibi_swap_v3(tx):
                        msg = f"🚨 BIBI Token נרשם בטרנזקציה (Uniswap V3)!\nמאת: {tx['from']}\nBlock: {block_number}"
                        print(msg)
                        send_telegram_message(msg)

            latest = current

        time.sleep(10)

    except Exception as e:
        print("שגיאה:", e)
        time.sleep(5)
