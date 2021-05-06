#!/usr/bin/python3
import argparse, requests, jsonrpcclient, json
from jsonrpcclient import request
from jsonrpcclient.clients.http_client import HTTPClient
from jsonrpcclient.requests import Request

if __name__ =='__main__':
    jsonobject = open(file="rpccreds.json", mode='r', encoding="utf-8")
    creds = json.load(jsonobject)
    jsonobject.close()
    parser = argparse.ArgumentParser()
    parser.add_argument('txid', metavar='transaction_id', type=str,
                        help='dogecoin transaction ID')
    args = parser.parse_args()
    txid = args.txid
    client = HTTPClient("http://localhost:22555")
    client.session.auth = (creds["rpcuser"], creds["rpcpass"])
    rq = Request("gettransaction", txid=txid)
    response = None
    try:
        response = client.send(rq)
    except jsonrpcclient.exceptions.ReceivedNon2xxResponseError as res_err:
        print(res_err)
    #print(response)
    if response:
        if response["confirmations"] >= 1:
            cleaned_tx = {"txid":response["txid"],
                          "amount": response["amount"],
                          "time":response["time"],
                          "timereceived":response["timereceived"],
                          "comment": ""}
            if "comment" in response.keys():
                cleaned_tx["comment"] = response["comment"]
            requests.post("http://localhost:42069/donation", json=cleaned_tx)
    else:
        cleaned_tx = {"txid": "1337",
                      "amount": 1337,
                      "time": 0,
                      "timereceived": 1,
                      "comment": "Fake transaction - DOGE to the MOON anyways!"}
        requests.post("http://localhost:42069/donation", json=cleaned_tx)
    #print(cleaned_tx)
