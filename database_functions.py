# Dependencies
import os
import json
import math

import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Function to return the remaining supply of Gods Unchained genesis chests
def update_db_chests():

    print("Updating database...")

    # Etherscan key
    etherscan_key = os.environ.get("etherscan_key")
    # Database url
    database_url = os.environ.get("DATABASE_URL")
    
    # Contract addresses for Gods Unchained chests
    # Values are tuples where the elements are: (id, contract_address, number of decimals used by contract)
    contract_addresses = {
        "gen_rare": (1, "0xEE85966b4974d3C6F71A2779cC3B6F53aFbc2B68", 0),
        "gen_leg": (2, "0x20D4Cec36528e1C4563c1BFbE3De06aBa70b22B4", 0),
        "totg_rare": (3, "0x69C3AA99e387D03d132B9AFef6C3FAeB98b930b1", 18),
        "totg_leg": (4, "0x1183e505Ad80fb1b648eFe2ef44f8429AFa8Cea9", 18)
    }

    # Dictionary to store the chest supply data from the API calls
    chest_supply_dict = {}

    # Connect to the database
    conn = psycopg2.connect(database_url, sslmode='require')
    cur = conn.cursor()

    # Iterate through each contract address and make API call to get the current token supply for that address
    for key, value in contract_addresses.items():
        
        # Make API call
        try:
            chest_supply_url = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={value[1]}&apikey={etherscan_key}"
            chest_response = requests.get(chest_supply_url)
            chest_data = json.loads(chest_response.text)
            # Math to handle different levels of decimal precision between contracts
            chest_supply_dict[key] = (value[0], int(chest_data["result"])/(10**value[2]))

        # Handle API call failures
        except Exception as e:
            print(f"Error:\n{e}")

    for supply in chest_supply_dict.values():

        # Update the database
        cur.execute(f"""
            UPDATE gu_chests
            SET total_supply = {supply[1]}
            WHERE id = {int(supply[0])}
            """)

    # Commit the changes
    conn.commit()

    # Close connections with the database
    cur.close()
    conn.close()

    message = "Update complete."
    print(message)

    return message

# Call the function to update the gu chest supply data in the database
update_db_chests()

