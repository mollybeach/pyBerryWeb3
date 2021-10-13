import json
import csv
import pandas as pd
from web3 import Web3
ETHERSCAN_API_KEY = "8DZ7FZZ3GEM1KN4SJAKDEF7KWQJHJKIA62"
POOL_2_ADDRESS = "0x07edbd02923435fe2c141f390510178c79dbbc46"
MAGIC_ADDRESS = "0x8c56ca4f7eb12a7c217bbe36cc427a9dcb66f590"
CHECKSUM_ADDRESS = Web3.toChecksumAddress(POOL_2_ADDRESS )
MINTING_ADDRESS = "0x0000000000000000000000000000000000000000"
FILEPATH_JSON = "../response/json/new_response.json"
FILEPATH_CSV = "../response/csv/new_reponse.csv"
FILEPATH_JSON_FINAL = "../response/json/final_reponse.json"
FILEPATH_CSV_FINAL = "../response/csv/final_response.csv"
url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={CHECKSUM_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
#make a token api call with etherscan api key for deposit into the contract address time in time out number of liqudity provider tokens deposited by the address
# write url to a file FILEPATH_JSON

#get the json response from the url and save to FILEPATH_JSON

def get_etherscan_api_response(url):
    import requests
    response = requests.get(url)
    return response.json()

#convert eth to usd using coinmarketcap api



def save_etherscan_api_response(url):
    response = get_etherscan_api_response(url)
    # format json response
    formatted_response = json.dumps(response, indent=4)
    # save to a json file
    with open(FILEPATH_JSON, "w") as f:
        f.write(formatted_response)

save_etherscan_api_response(url)