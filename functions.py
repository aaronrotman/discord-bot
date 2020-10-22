# Dependencies
import requests
import json
import os
# --------------------------------------------------
#LOCAL DEPLOYMENT
from config import etherscan_key
# --------------------------------------------------

# --------------------------------------------------
# HEROKU DEPLOYMENT
# etherscan_key = os.environ.get('etherscan_key')
# --------------------------------------------------


# Function to return current Ethereum gas data
def get_gas_data():
    try:
        query_url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={etherscan_key}"
        gas_response = requests.get(query_url)
        gas_price = json.loads(gas_response.text)
        results = gas_price['result']
        gas_dict = {
            "last_block": results['LastBlock'],
            "safe_gas": f"{results['SafeGasPrice']} gwei",
            "propose_gas": f"{results['ProposeGasPrice']} gwei",
            "fast_gas": f"{results['FastGasPrice']} gwei"

        }
        return gas_dict

    # Handle api call failures
    except Exception as e:
        print(e)
        gas_dict = {
            "last_block": "Data Unavailable",
            "safe_gas": "Data Unavailable",
            "propose_gas": "Data Unavailable",
            "fast_gas": "Data Unavailable"

        }
        return gas_dict

# Function to return the current Ethereum price data
def get_eth_price():
    try:
        eth_price_url = f"https://api.etherscan.io/api?module=stats&action=ethprice&apikey={etherscan_key}"
        eth_response = requests.get(eth_price_url)
        eth_data = json.loads(eth_response.text)
        eth_result = eth_data['result']
        eth_price = eth_result['ethusd']
        # Convert timestamp into a string
        # epoch_time = int(eth_result['ethusd_timestamp'])
        # string_time = datetime.fromtimestamp(epoch_time).strftime('%X')

        # eth_dict = {
        #     "eth_usd": eth_result['ethusd'],
        #     "time": string_time
        # }
        return eth_price

    # Handle api call failures
    except Exception as e:
        print(e)
        eth_price = "Data Unavailable"
        # eth_dict = {
        #     "eth_usd": "Data Unavailable",
        #     "time": "Data Unavailable"
        # }
        return eth_price