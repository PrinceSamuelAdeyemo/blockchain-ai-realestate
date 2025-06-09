// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract PropertyRegistry {
    struct Property {
        string title;
        address owner;
        uint256 value;
        bool isTokenized;
    }
    
    mapping(uint256 => Property) public properties;
    uint256 public propertyCount;
    
    event PropertyRegistered(uint256 indexed id, address owner);
    event OwnershipTransferred(uint256 indexed id, address newOwner);
    
    function registerProperty(string memory title, uint256 value) external {
        propertyCount++;
        properties[propertyCount] = Property(title, msg.sender, value, false);
        emit PropertyRegistered(propertyCount, msg.sender);
    }
    
    function transferOwnership(uint256 id, address newOwner) external {
        require(properties[id].owner == msg.sender, "Not owner");
        properties[id].owner = newOwner;
        emit OwnershipTransferred(id, newOwner);
    }
}