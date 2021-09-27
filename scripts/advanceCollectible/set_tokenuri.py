from brownie import AdvancedNFT, network, accounts, config
from scripts.helpful_scripts import OPENSEA_FORMAT, get_version

import json

def main():
    with open("./metadata/uris", "r") as file:
        uris = json.load(file)
    print(uris)
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedNFT[len(AdvancedNFT) - 1]
    number_of_tokens = advanced_collectible.tokenCounter()
    print("You've deployed: "+ str(number_of_tokens))
    for token_id in range(number_of_tokens):
        #if advanced_collectible.tokenURI(token_id).startswith("None"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, advanced_collectible, uris[token_id])
            

def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config['wallets']['from_key'])
    nft_contract.setTokenURI(token_id, tokenURI, {"from" : dev})
    print(
        "Awesome, now you can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print("Please wait up to 20 minutes, and hit the 'refesh metadata' button")