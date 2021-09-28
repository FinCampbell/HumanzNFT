from brownie import AdvancedNFT, network
from scripts.helpful_scripts import OPENSEA_FORMAT

import requests, time

OPENSEA_API_BASE = "https://rinkeby-api.opensea.io/api/v1/asset/"

def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedNFT[len(AdvancedNFT) - 1]
    number_of_tokens = advanced_collectible.tokenCounter()
    
    for token_id in range(number_of_tokens):
        URL = OPENSEA_API_BASE+advanced_collectible.address+"/"+str(token_id)
        print(URL)

        payload = {"force_update": "true"}

        response = requests.request("GET", URL, params=payload)
        print(response)
        time.sleep(5)
