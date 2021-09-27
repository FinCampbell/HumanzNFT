pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedNFT is ERC721, VRFConsumerBase {

    bytes32 internal keyhash;
    uint256 public fee;
    uint256 public tokenCounter;

    enum Eyes{ONE, TWO}
    enum Head{ONE, TWO}
    enum Mouth{ONE, TWO}

    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;

    mapping(uint256 => Eyes) public tokenIdToEyes;
    mapping(uint256 => Head) public tokenIdToHead;
    mapping(uint256 => Mouth) public tokenIdToMouth;

    mapping(bytes32 => uint256) public requestIdToTokenId;
    event requestedCollectible(bytes32 indexed requestId);

    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyHash) public 
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("Humanz", "HUM")
    {
        keyhash = _keyHash;
        fee = 0.1*10**18; // 0.1 ETH
        tokenCounter = 0;
    }

    function expand(uint256 randomValue, uint256 n) public pure returns (uint256[] memory expandedValues) {
    expandedValues = new uint256[](n);
        for (uint256 i = 0; i < n; i++) {
            expandedValues[i] = uint256(keccak256(abi.encode(randomValue, i)));
        }
    return expandedValues;
    }

    function createCollectible(uint256 userProvidedSeed, string memory tokenURI) 
    public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;
        emit requestedCollectible(requestId);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        uint256[] memory expanded = expand(randomNumber, 3);
        address dogOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter;
        _safeMint(dogOwner, newItemId);
        _setTokenURI(newItemId, tokenURI);
        Eyes eyeType = Eyes(expanded[0] % 2);
        Mouth mouthType = Mouth(expanded[1] % 2);
        Head headType = Head(expanded[2] % 2);
        tokenIdToEyes[newItemId] = eyeType;
        tokenIdToHead[newItemId] = headType;
        tokenIdToMouth[newItemId] = mouthType;
        requestIdToTokenId[requestId] = newItemId;
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: Transfer Caller is not owner or approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
