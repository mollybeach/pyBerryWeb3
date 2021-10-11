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
        json_data = json_data["result"]      
        for tx in json_data:
            recipient = tx["to"]
            sender = tx["from"]
            if recipient != MAGIC_ADDRESS: #then this is a deposit to magic our contract 
                #if it exists then update the time_deposit
                if sender in dictWithDepo.keys():
                    tx["deposit_time"] = dictWithDepo[sender]["time_deposit"] #deposit time is the time of the last deposit
                    tx["withdrawal_time"] = tx["timeStamp"] 
                else:
                    #if not does not exist then add to dict
                    dictWithDepo[sender] = {
                        "time_deposit": tx["timeStamp"],
                        "time_withdrawl": None
                    }
                    tx["deposit_time"] = tx["timeStamp"]
                    tx["withdrawal_time"] = None
            #if the receipent is something other than the magic address then it is a withdrawal
            #remvoe this transaction from the results
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
        with open(FILEPATH_JSON_FINAL, "r") as f:
            json_data = json.load(f)
            for tx in json_data["result"]:
                writer.writerow([tx["from"], tx["timeStamp"], tx["timeStamp"], tx["value"]])

'''
#etherscan_api_response_to_json(url)
#write_csv(FILEPATH_CSV)

def saveascsv():
    import json
    import csv
    
    with open(FILEPATH_JSON) as json_file:
        jsondata = json.load(json_file)
        jsondata = jsondata["result"]
    
    data_file = open("../response/json/etherscan_as_csv.csv", 'w', newline='')
    csv_writer = csv.writer(data_file)
    
    count = 0
    for data in jsondata:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    
    data_file.close()

import pandas as pd

def change_data():
    file = pd.read_csv("../response/json/etherscan_as_csv.csv")
    file = file[file["to"] == MAGIC_ADDRESS]
    df = file
    df.sort_values(by=['from'], inplace=True)
    for sender in df.groupby('from'):
        if len(df[df['from']==sender]) > 1:
            prev = df[df['from']==sender].head(1)
            #df.loc(df['from']==sender, "desposit_time") = prev["time_deposit"]
            #df.loc(df['from']==sender, "withdrawal_time") = df.loc([df['from']==sender], "timeStamp")
            same_sender = df.loc[df['from'] == sender, :]
            same_sender.loc[:, "deposit_time"] = prev["timeStamp"]
            same_sender.loc[:, "withdrawal_time"] = same_sender["timeStamp"]
            df.loc[df['from'] == sender, :] = same_sender
        else:
            df.loc[:, "deposit_time"] = df["timeStamp"]
            df.loc[:, "withdrawal_time"] = None
    df.to_csv("../response/json/etherscan_as_csv_EDITED.csv")



    



change_data()