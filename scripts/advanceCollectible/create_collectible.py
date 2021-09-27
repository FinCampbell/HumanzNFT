from brownie import AdvancedNFT, accounts, config, network
from scripts.helpful_scripts import get_version
import time

STATIC_SEED = 123

def main():
    dev = accounts.add(config['wallets']['from_key'])
    advanced_collectible = AdvancedNFT[len(AdvancedNFT) - 1]
    transaction = advanced_collectible.createCollectible(
        STATIC_SEED, "None", {"from": dev}
    )
    transaction.wait(1)
    requestId = transaction.events['requestedCollectible']['requestId']
    token_id = advanced_collectible.requestIdToTokenId(requestId)
    time.sleep(25)
    head = get_version(advanced_collectible.tokenIdToHead(token_id))
    mouth = get_version(advanced_collectible.tokenIdToMouth(token_id))
    eyes = get_version(advanced_collectible.tokenIdToEyes(token_id))

    print("Head type of tokenId {} is {}".format(token_id, head))
    print("Head type of tokenId {} is {}".format(token_id, mouth))
    print("Head type of tokenId {} is {}".format(token_id, eyes))
