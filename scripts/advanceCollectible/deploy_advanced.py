from brownie import AdvancedNFT, accounts, network, config
from scripts.helpful_scripts import fund_advanced_collectible

def main():
    dev = accounts.add(config['wallets']['from_key'])
    public_source = True
    advancednft = AdvancedNFT.deploy(
        config['networks'][network.show_active()]['vrf_coordinator'],
        config['networks'][network.show_active()]['link_token'],
        config['networks'][network.show_active()]['keyhash'],
        {'from' : dev},
        publish_source = public_source
    )
    fund_advanced_collectible(advancednft)
    return advancednft
    