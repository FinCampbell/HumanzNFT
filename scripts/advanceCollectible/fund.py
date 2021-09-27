from brownie import AdvancedNFT
from scripts.helpful_scripts import fund_advanced_collectible

def main():
    advanced_nft = AdvancedNFT[len(AdvancedNFT) - 1]
    fund_advanced_collectible(advanced_nft)