#get wallets and total amount from each project
#query each wallet over the last day, if match total amount = paid



import requests
from datetime import datetime, timedelta
from projects_list import projects
from post_telegram import send_message_telegram
from dotenv import load_dotenv
import os

load_dotenv()



USDC_CONTRACT = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")


# Get block number closest to 24h ago
def get_block_by_timestamp(timestamp):
    url = f"https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey={ETHERSCAN_API_KEY}"
    return int(requests.get(url).json()["result"])

# Calculate start timestamp (24 hours ago)
end_time = int(datetime.utcnow().timestamp())
start_time = int((datetime.utcnow() - timedelta(days=1)).timestamp())

start_block = get_block_by_timestamp(start_time)
end_block = get_block_by_timestamp(end_time)

# Get USDC transfer events to the ETH address
def get_usdc_transfers(ETH_ADDRESS):
    url = (
        f"https://api.etherscan.io/api?module=account&action=tokentx"
        f"&contractaddress={USDC_CONTRACT}"
        f"&address={ETH_ADDRESS}"
        f"&startblock={start_block}&endblock={end_block}"
        f"&sort=asc&apikey={ETHERSCAN_API_KEY}"
    )
    return requests.get(url).json()["result"]


def check_txs(txs,addy,total_amount,name):
    for tx in txs:
        amount = int(tx["value"]) / 1e6  # Convert from raw USDC
        if amount > 1 and addy.lower() == tx['to'].lower():
            timestamp = datetime.utcfromtimestamp(int(tx["timeStamp"])).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp} | From: {tx['from']} | To: {tx['to']} | Amount: {amount} USDC")
            if tx['to'].lower() == addy.lower() and int(amount) == int(total_amount):
                print(f"{name} paid {amount}")
                send_message_telegram(f"{name} paid {amount}")


for project in projects:
    name = project["project"]
    amounts = project["amount"]
    type = project['payment_type']
    addy = project['payment_address'] 
    total_amount = sum(amounts)

    if type == "ERC20":

        txs = get_usdc_transfers(addy)
        check_txs(txs,addy,total_amount,name)


        #need to find a solana alternative


