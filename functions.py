# Dependencies
import os
import requests
import json


from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment eariables
load_dotenv()

# Import Etherscan key from environment variables
etherscan_key = os.environ.get('etherscan_key')

# Database url
database_url = os.environ.get("DATABASE_URL")

# Database engine
engine = create_engine(database_url)


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
        print(e, flush=True)
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
        print(e, flush=True)
        eth_price = "Data Unavailable"
        # eth_dict = {
        #     "eth_usd": "Data Unavailable",
        #     "time": "Data Unavailable"
        # }
        return eth_price


# Function to query the database.
def query_db_chests():
    # Dictionary to store the queried chest data
    chest_dict = {}
    # Query string to return set, rarity and total supply data from the 'gu_chests' table.
    query_string = "SELECT set, rarity, total_supply FROM gu_chests;"
    
    # Connect to the database and execute query
    try:
        with engine.connect() as conn:
            query_data = conn.execute(text(query_string))
            data = query_data.fetchall()
            for chest in data:
                chest_dict[f"{chest[0]}_{chest[1]}"] = chest[2]
            return chest_dict
    
    # Handle database connection failures
    except Exception as e:
        # Print error message
        error_message = "Database query failed."
        print(f"{error_message}\n{e}", flush=True)
        # Assign
        chest_dict['genesis_rare'] = 'Error'
        chest_dict['genesis_legendary'] = 'Error'
        chest_dict['totg_rare'] = 'Error'
        chest_dict['totg_legendary'] = 'Error'
        return chest_dict

