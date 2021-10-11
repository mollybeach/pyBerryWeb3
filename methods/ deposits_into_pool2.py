import json
import csv
from web3 import Web3

ETHERSCAN_API_KEY = "8DZ7FZZ3GEM1KN4SJAKDEF7KWQJHJKIA62"
POOL_2_ADDRESS = "0xB0c7a3Ba49C7a6EaBa6cD4a96C55a1391070Ac9A"
MAGIC_ADDRESS = "0x8c56ca4f7eb12a7c217bbe36cc427a9dcb66f590"
CHECKSUM_ADDRESS = Web3.toChecksumAddress(POOL_2_ADDRESS )
MINTING_ADDRESS = "0x0000000000000000000000000000000000000000"
FILEPATH_JSON = "../response/json/etherscan_api_response.json"
FILEPATH_CSV = "../response/csv/etherscan_api_response.csv"
FILEPATH_JSON_FINAL = "../response/json/etherscan_api_response_final.json"
FILEPATH_CSV_FINAL = "../response/csv/etherscan_api_response_final.csv"
url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={CHECKSUM_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
#make a token api call with etherscan api key for deposit into the contract address time in time out number of liqudity provider tokens deposited by the address

def get_etherscan_api_response(url):
    import requests
    response = requests.get(url)
    return response.json()


#get reponse from api url and then save as json and remove from = MINTING_ADDRESS
def etherscan_api_response_to_json(url):
    response = get_etherscan_api_response(url)
    formatted_response = json.dumps(response, indent=4)
    with open(FILEPATH_JSON, "w") as f:
        f.write(formatted_response)
    with open(FILEPATH_JSON, "r") as f:
        json_data = json.load(f)
        results = json_data["result"]
        dictWithDepo = {
            "address": {
                "time_deposit": "",
                "time_withdrawl": "",
                }
        }       
        for tx in results:
            recipient = tx["to"]
            sender = tx["from"]
            if recipient == MAGIC_ADDRESS: #then this is a deposit to magic our contract 
                #if it exists then update the time_deposit
                if sender in dictWithDepo.keys():
                    if dictWithDepo[sender]:
                        tx["deposit_time"] = dictWithDepo[tx["from"]]["time_deposit"] #deposit time equals now 
                        tx["withdrawal_time"] = tx["timeStamp"] 
                    else:
                        #if not does not exist then add to dict
                        dictWithDepo[tx["from"]] = {
                            "time_deposit": tx["timeStamp"],
                            "time_withdrawl": tx["timeStamp"]
                        }
                        tx["deposit_time"] = tx["timeStamp"]
                        tx["withdrawal_time"] = None
            #if the receipent is something other than the magic address then it is a withdrawal
            #remvoe this transaction from th results
            elif recipient == MAGIC_ADDRESS:
                results.remove(tx)
            results.append(tx)
            data = {}
            data["results"] = results
            with open(FILEPATH_JSON_FINAL, "w") as f:
                json.dump(data, f, indent=4)
        





        
'''
def write_csv(filename):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["address", "time_deposit", "time_withdrawl", "lp_tokens_deposited"])
        with open(FILEPATH_JSON, "r") as f:
            json_data = json.load(f)
            for tx in json_data["result"]:
                writer.writerow([tx["from"], tx["timeStamp"], tx["timeStamp"], tx["value"]])

'''
etherscan_api_response_to_json(url)
#write_csv(FILEPATH_CSV)


