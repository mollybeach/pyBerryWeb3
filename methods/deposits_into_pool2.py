import json
import csv
import pandas as pd
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



def change_data():
    file = pd.read_csv("./response/json/etherscan_edited_all.csv")
    file = file[file["to"] == MAGIC_ADDRESS]
    df = file
    df.sort_values(by=['from'], inplace=True)
    filter = df.drop_duplicates(subset = ["from"])
    for sender in filter['from']:
        if len(df.loc[df['from']==sender, :]) > 1:
            prev = df[df['from']==sender].head(1)
            same_sender = df.loc[df['from'] == sender, :]
            prev_timestamp = prev["timeStamp"]
            same_sender.loc[:, "deposit_time"] = prev_timestamp.item()
            same_sender.loc[:, "withdrawal_time"] = same_sender.loc[:, "timeStamp"]
            same_sender['withdrawal_time'] = pd.to_datetime(same_sender['withdrawal_time'], unit='s')
            df.loc[df['from'] == sender, :] = same_sender
        else:
            copy = df.loc[df['from']==sender, :]
            copy.loc[:, "deposit_time"] = copy.loc[:, "timeStamp"]
            copy.loc[:, "withdrawal_time"] = None
            df.loc[df['from']==sender, :] = copy
    
    df = df[["from","deposit_time","withdrawal_time", "value"]]
    df['withdrawal_time'] = df['withdrawal_time'].astype(str).replace('\.0', '', regex=True)
    #convert deposit time to unix timestamp
    df['deposit_time'] = pd.to_datetime(df['deposit_time'], unit='s')
    #convert withdrawal time to unix timestamp
    # df['withdrawal_time'] = pd.to_datetime(df['withdrawal_time'], unit='s')

    df.to_csv("./response/json/etherscan_cols_removed.csv", index=False)
    


change_data()