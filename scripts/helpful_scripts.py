from brownie import AdvancedNFT, accounts, config, interface, network
from PIL import Image

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

def fund_advanced_collectible(nft_contract):
    dev = accounts.add(config['wallets']['from_key'])
    link_token = interface.LinkTokenInterface(
        config['networks'][network.show_active()]['link_token']
    )
    link_token.transfer(nft_contract, 1000000000000000000, {"from": dev})

def get_version(num):
    switch = {0: '1', 1:'2'}
    return switch[num]

def gen_art(head, eyes, mouth, tokenId):
    head = Image.open("./img/heads/"+str(head)+".png")
    eyes = Image.open("./img/eyes/"+str(eyes)+".png")
    mouth = Image.open("./img/mouth/"+str(mouth)+".png")

    head.paste(eyes, (0,0), eyes)
    head.paste(mouth, (0,0), mouth)

    resized_img = head.resize((300,300), resample=Image.NEAREST)
    resized_img.save("./metadata/rinkebyImg/"+str(tokenId)+".png", "PNG")

NAMES = [
    "JOHN",
    "MARK",
    "STEVE",
    "MARY",
    "SUE",
    "EMILY"
]

uris = []