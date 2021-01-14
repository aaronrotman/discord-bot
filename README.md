# Discord Bot

A discord bot that provides Ethereum blockchain data in response to user prompts. Data includes the current price of Ethereum and the current gas prices for Ethereum.

## Tools used:
* Python
* Etherscan API
* Heroku

## Current Commands:
* $gas
    * Retrieves current Ethereum gas prices and posts them to discord.
* $eth
    * Retrieves the current price of Ethereum and posts it to discord.

## Example Usage: 

!["Example bot command and response"](images/command_gas.PNG "Example bot command and response")

## Data Sources:
Ethereum data provided by [Etherscan.io](https://etherscan.io/).

## Dependencies to install:
 * [Requests](https://requests.readthedocs.io/en/master/user/install/#install)
   pip install requests
 * [python-dotenv](https://pypi.org/project/python-dotenv/)
   pip install python-dotenv
 * [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)
   pip install psycopg2-binary
 * [Discord.py](https://discordpy.readthedocs.io/en/latest/)
   pip install discord.py
 
 
