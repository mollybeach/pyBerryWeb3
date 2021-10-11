#from eth_typing.evm import ChecksumAddress
import json
from web3 import Web3

#ALCHEMY_MAINNET_KEY="WT5LDdM3ZG2O_3Bz4KbfstNc-vXskLmF"
#ALCHEMY_URL = "https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_MAINNET_KEY}"
ETHERSCAN_API_KEY = "8DZ7FZZ3GEM1KN4SJAKDEF7KWQJHJKIA62"
TREASURE_ADDRESS = "0x07edbd02923435fe2c141f390510178c79dbbc46"
CHECKSUM_ADDRESS = Web3.toChecksumAddress(TREASURE_ADDRESS )
#make an api call in web3 using Etherscan API and return the response
#def get_etherscan_api_response(url):
#web3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

#print(web3.eth.getBalance(CHECKSUM_ADDRESS))    
#string interpolation etherscan api url web3
url = f"https://api.etherscan.io/api?module=account&action=txlist&address=0x07edbd02923435fe2c141f390510178c79dbbc46&startblock=0&endblock=99999999&sort=asc&apikey=8DZ7FZZ3GEM1KN4SJAKDEF7KWQJHJKIA62"

#make an api call to url and return the response and save to a json file ./etherscan_api_response.json
def save_etherscan_api_response(url):
    response = get_etherscan_api_response(url)
    with open('./etherscan_api_response.json', 'w') as outfile:
        json.dump(response, outfile)
        

save_etherscan_api_response(url)





