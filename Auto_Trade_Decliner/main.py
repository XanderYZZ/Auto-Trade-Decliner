# Imports
import requests
import json
import time
import threading

# Files
import Rolimons
import Webhook

# Retrieving the config file
config = json.load(open('./config.json',))
cookie = config["Cookie"]
minimumValuePercent = config["MinimumValuePercent"]

# Setting up the session
rblx_session = requests.Session()
rblx_session.cookies[".ROBLOSECURITY"] = cookie

# Creating the Rolimons class
Rolimon = Rolimons.Rolimons()

# Creating the cached trades list
cachedTrades = []

def removeFromCachedTrades(id):
    cachedTrades.remove(id)

def http_request(send_method, url, **args):
    request = rblx_session.request(send_method, url, **args)

    if "X-CSRF-TOKEN" in request.headers:
        if "errors" in request.json():
            if request.json()["errors"][0]["message"] == "Token Validation Failed":
                rblx_session.headers["X-CSRF-TOKEN"] = request.headers["X-CSRF-TOKEN"]
                request = rblx_session.request(send_method, url, **args)    

    return request

# Main Loop
while True:
    Inbound_Trades = http_request("get", "https://trades.roblox.com/v1/trades/Inbound?sortOrder=Asc&limit=100")
    Inbound_Trades = Inbound_Trades.json()["data"]

    for inbound in Inbound_Trades:
        #print(inbound)

        opposingUser = inbound['user']
        opposingUserID = opposingUser['id']
        opposingUsername = opposingUser['name']
        opposingDisplayName = opposingUser['displayName']

        id = inbound["id"]

        if id in cachedTrades:
            continue

        Receiving, Giving = 0, 0

        Details = http_request("get", f"https://trades.roblox.com/v1/trades/{id}")
        Details = Details.json()["offers"]

        receivingList = Details[1]["userAssets"]
        givingList = Details[0]["userAssets"]

        for itemReceiving in receivingList:
            #print(itemReceiving)
            Receiving += Rolimon.getItem(itemReceiving["assetId"])[4]

        for itemGiving in givingList:
            #print(itemGiving)
            Giving += Rolimon.getItem(itemGiving["assetId"])[4]

        ValueRatio = Receiving / Giving

        print(f"Trade ID: {id} | Value Ratio: {ValueRatio}")

        # Bad Trade
        if ValueRatio <= minimumValuePercent:
            http_request("post", f"https://trades.roblox.com/v1/trades/{id}/decline")

            givingListText = ""
            receivingListText = ""

            for itemGiving in givingList:
                givingListText = givingListText + itemGiving['name'] + ", "

            for itemReceiving in receivingList:
                receivingListText = receivingListText + itemReceiving['name'] + ", "

            print(f"declined trade id: {id}")

            description = "Giving: " + givingListText + " | Receiving: " + receivingListText

            Webhook.sendWebhook(
                "Trade with {opposingUserName}, AKA: {opposingDisplayName}, UserID: {opposingUserID}", 
                description,
                opposingUsername
            )
        else:
            cachedTrades.append(id)

            threading.Timer(60*15, removeFromCachedTrades, [id]).start()

    time.sleep(20)