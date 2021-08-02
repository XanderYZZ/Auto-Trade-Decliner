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
        else:
            print("Could not retrieve Rolimons item data")

    # Init / Main
    def main(self):
        while True:
            self.setItems()

            time.sleep(60*30)

    def __init__(self):
        # Preventing the race condition by collecting it once before making a new thread
        self.setItems()

        threading.Thread(target = self.main).start()
