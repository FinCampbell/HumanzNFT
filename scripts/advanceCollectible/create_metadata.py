from json.decoder import JSONDecodeError
from brownie import AdvancedNFT, accounts, config, network
from scripts.helpful_scripts import get_version, NAMES, gen_art
from metadata import sample_metadata
from pathlib import Path

import os, requests, json, random

class Error(Exception):
    pass

class AuthenticationError(Error):
    def __init__(self, message):
        self.message = message

def main():
    print(entry())

def entry():
    print("Working on "+network.show_active())
    advanced_collectible = AdvancedNFT[len(AdvancedNFT) - 1]
    number_of_tokens = advanced_collectible.tokenCounter()
    print(number_of_tokens)
    write_metadata(number_of_tokens, advanced_collectible)
    return("Metadata Generated")

def write_metadata(number_of_tokens, nft_contract):
    try:
        with open("./metadata/uris", "r") as file:
            try:
                uris = json.load(file)
            except(JSONDecodeError):
                uris = []
    except(FileNotFoundError):
        uris = []


    for token_id in range(number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        head = get_version(nft_contract.tokenIdToHead(token_id))
        eyes = get_version(nft_contract.tokenIdToEyes(token_id))
        mouth = get_version(nft_contract.tokenIdToMouth(token_id))

        metadata_file_name = (
            "./metadata/{}/".format(network.show_active())+ str(token_id)
            + "-" + head + "-" + eyes + "-" + mouth +".json"
        )
        if Path(metadata_file_name).exists():
            print("{} already found!".format(metadata_file_name))
        else:
            print("Creating Metadata file {}".format(metadata_file_name))
            collectible_metadata["name"] = random.choice(NAMES)
            collectible_metadata["description"] = "An human. They're called {}".format(collectible_metadata["name"])
            print(collectible_metadata)
            image_to_upload = None
            if os.getenv('UPLOAD_IPFS') == "true":
                gen_art(head, eyes, mouth, token_id)
                img_path = "./metadata/rinkebyImg/"+str(token_id)+".png"
                image_to_upload = upload_to_ipfs(img_path)
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                uri = upload_to_ipfs(metadata_file_name)
                uris.append(uri)
                ipfs_hash = (uri.split("/")[4]).split("?")[0]
                print(ipfs_hash)
                pin_to_pinata(ipfs_hash, collectible_metadata["name"], token_id)
        with open("./metadata/uris", "w") as file:
            json.dump(uris, file)

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(
            ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(uri)
        return(uri)
    return None

def pin_to_pinata(hash, breed, token_id):
    try:
        pinata_authenticate()
    except(AuthenticationError):
        print(AuthenticationError)

    url = "https://api.pinata.cloud/pinning/pinByHash"

    headers = {
        "pinata_api_key" : os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key" : os.getenv("PINATA_API_SECRET")
    }

    pinName = str(token_id)+str(breed)
    print(pinName)

    body = { 
        "hashToPin": hash,
        "pinataMetadata": {
            "name": pinName
        }
    }

    response = requests.post(url, headers=headers, json=body)
    print(response.content)
    

def pinata_authenticate():
    url = "https://api.pinata.cloud/data/testAuthentication"
    headers = {
        "pinata_api_key" : os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key" : os.getenv("PINATA_API_SECRET")
    }
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code == 200:
        return "Success"
    elif response.status_code == 404:
        raise AuthenticationError("Could not Authenticate with Pinata")
