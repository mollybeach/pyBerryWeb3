#from eth_typing.evm import ChecksumAddress
import json
import csv
from web3 import Web3

#ALCHEMY_MAINNET_KEY="WT5LDdM3ZG2O_3Bz4KbfstNc-vXskLmF"
#ALCHEMY_URL = "https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_MAINNET_KEY}"
#TREASURE_ADDRESS = "0x07edbd02923435fe2c141f390510178c79dbbc46"
ETHERSCAN_API_KEY = "8DZ7FZZ3GEM1KN4SJAKDEF7KWQJHJKIA62"
POOL_2_ADDRESS = "0xB0c7a3Ba49C7a6EaBa6cD4a96C55a1391070Ac9A"
CHECKSUM_ADDRESS = Web3.toChecksumAddress(POOL_2_ADDRESS )
MINTING_ADDRESS = "0x0000000000000000000000000000000000000000"

#use web3 to see if it's a deposit or withdrawal


url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={CHECKSUM_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"

# convert url to hex string use web3 
url_hex = Web3.toHex(url)


def get_etherscan_api_response(url):
    #url to hexString
    web3 = Web3(Web3.HTTPProvider(url))
    response = web3.eth.getTransactionReceipt(url)
    return response

get_etherscan_api_response(url_hex)
