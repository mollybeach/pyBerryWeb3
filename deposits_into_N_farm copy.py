#from eth_typing.evm import ChecksumAddress
import json
import csv
from web3 import Web3

#ALCHEMY_MAINNET_KEY="WT5LDdM3ZG2O_3Bz4KbfstNc-vXskLmF"
#ALCHEMY_URL = "https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_MAINNET_KEY}"
ETHERSCAN_API_KEY = "8DZ7FZZ3GEM1KN4SJAKDEF7KWQJHJKIA62"
#TREASURE_ADDRESS = "0x07edbd02923435fe2c141f390510178c79dbbc46"
NFARM_ADDRESS = "0x08543f4c79f7e5d585A2622cA485e8201eFd9aDA"
CHECKSUM_ADDRESS = Web3.toChecksumAddress(NFARM_ADDRESS)
#make an api call in web3 using Etherscan API and return the response
#def get_etherscan_api_response(url):
#web3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

#print(web3.eth.getBalance(CHECKSUM_ADDRESS))    
#string interpolation etherscan api url web3

#url = f"https://api.etherscan.io/api?module=account&action=txlist&address=0x07edbd02923435fe2c141f390510178c79dbbc46&startblock=0&endblock=99999999&sort=asc&apikey=8DZ7FZZ3GEM1KN4SJAKDEF7KWQJHJKIA62"


#make an api call to url and return the response and save to a json file ./etherscan_api_response.json
#url = f"https://api.etherscan.io/api?module=account&action=txlist&address={CHECKSUM_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
#make a token api cakk with etherscan api key for deposit into the contract address time in time out number of liqudity provider tokens deposited by the address : https://etherscan.io/token/0xB0c7a3Ba49C7a6EaBa6cD4a96C55a1391070Ac9A?a=0x8c56ca4f7eb12a7c217bbe36cc427a9dcb66f590


url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={CHECKSUM_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"

def get_etherscan_api_response(url):
    import requests
    response = requests.get(url)
    return response.json()

#convert eth to usd using coinmarketcap api
def get_usd_value(eth_value):
    import requests
    url = f"https://api.coinmarketcap.com/v1/ticker/ethereum/?convert=USD"
    response = requests.get(url)
    return response.json()[0]["price_usd"]

# list of addresses who deposited into pool2 (address, time in, time out, # LP tokens deposited by address) - https://etherscan.io/token/0xB0c7a3Ba49C7a6EaBa6cD4a96C55a1391070Ac9A?a=0x8c56ca4f7eb12a7c217bbe36cc427a9dcb66f590



def save_etherscan_api_response(url):
    response = get_etherscan_api_response(url)
    # format json response
    formatted_response = json.dumps(response, indent=4)
    # save to a json file
    with open("./etherscan_api_response.json", "w") as f:
        f.write(formatted_response)

#write the json file to a csv file
def write_csv(filename):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["address", "time_in", "time_out", "lp_tokens_deposited"])
        with open("./etherscan_api_response.json", "r") as f:
            json_data = json.load(f)
            for tx in json_data["result"]:
                writer.writerow([tx["from"], tx["timeStamp"], tx["timeStamp"], tx["value"]])
'''
def write_etherscan_api_response_to_csv(url):
    response = get_etherscan_api_response(url)
    with open("./etherscan_api_response.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["blockNumber", "timeStamp", "hash", "nonce", "blockHash", "transactionIndex", "from", "to", "value", "gas", "gasPrice", "isError", "txreceipt_status", "input", "contractAddress", "cumulativeGasUsed", "gasUsed", "confirmations"])
        
        for tx in response["result"]:
            writer.writerow(tx.values())
            '''








save_etherscan_api_response(url)
#write_etherscan_api_response_to_csv(url)
write_csv("./etherscan_api_response.csv")
