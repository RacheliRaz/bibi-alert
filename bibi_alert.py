import requests
from web3 import Web3
import time

TELEGRAM_BOT_TOKEN = '8425080568:AAEBS05iTDNkp6TzGgJ-QJp156dzMpVdMB4'
TELEGRAM_CHAT_ID = '@BIBI_COIN_BOT'
BIBI_CONTRACT_ADDRESS = Web3.to_checksum_address('0xfA21cc13462fD156a2d11EB7b5c4812154C6f485')
INFURA_URL = 'https://mainnet.infura.io/v3/0d762f93f5ee42ab8198e2d6ceb9e475'

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not web3.is_connected():
    raise Exception("החיבור לבלוקצ'יין נכשל")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

latest_block = web3.eth.block_number
print(f"📡 מתחילים לבדוק בלוקים מ-{latest_block}")

while True:
    current_block = web3.eth.block_number
    if current_block > latest_block:
        for block_number in range(latest_block + 1, current_block + 1):
            block = web3.eth.get_block(block_number, full_transactions=True)
            for tx in block.transactions:
                if tx.to and tx.to.lower() == BIBI_CONTRACT_ADDRESS.lower():
                    value = web3.from_wei(tx.value, 'ether')
                    sender = tx['from']
                    msg = f"🚨 כתובת {sender} הרגע מכרה {value:.2f} ETH של $BIBI!"
                    print(msg)
                    send_telegram_message(msg)
        latest_block = current_block
    time.sleep(10)
