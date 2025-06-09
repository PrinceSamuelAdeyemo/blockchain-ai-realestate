// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract RealEstateToken is ERC20, Ownable {
    address public propertyContract;
    uint256 public tokenPrice;

    constructor(
        string memory name,
        string memory symbol,
        address _propertyContract,
        uint256 initialPrice
    ) ERC20(name, symbol) Ownable(msg.sender) { // Pass msg.sender as initial owner
        propertyContract = _propertyContract;
        tokenPrice = initialPrice;
    }

    function mintTokens(address investor, uint256 amount) external onlyOwner {
        _mint(investor, amount);
    }

    function setTokenPrice(uint256 newPrice) external onlyOwner {
        tokenPrice = newPrice;
    }
}