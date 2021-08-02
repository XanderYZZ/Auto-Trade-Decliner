import threading
import requests
import time

class Rolimons:
    cachedItems = {}

    # Get Methods
    def getItem(self, itemID):
        return self.cachedItems[str(itemID)]

    # Set Methods
    def setItems(self):
        response = requests.get("https://www.rolimons.com/itemapi/itemdetails")

        if response.ok:
            self.cachedItems = response.json()["items"]

    # Init / Main
    def main(self):
        while True:
            self.setItems()

            time.sleep(60*30)

    def __init__(self):
        threading.Thread(target = self.main).start()