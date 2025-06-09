// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PropertyCrowdfund {
    enum OwnershipType { SINGLE, CROWDFUND, ANY }

    struct Property {
        uint id;
        OwnershipType ownershipType;
        address currentOwner;
        uint totalShares; // e.g. 10000 means 100%
    }

    uint public nextPropertyId;
    mapping(uint => Property) public properties;
    mapping(uint => mapping(address => uint)) public shares; // propertyId => investor => %
    event PropertyListed(uint indexed propertyId, address indexed owner);
    event OwnershipTransferred(uint indexed propertyId, address indexed from, address indexed to);
    event PropertyFractionalized(uint indexed propertyId, address[] investors, uint[] shares);
    event PropertyBoughtOut(uint indexed propertyId, address indexed buyer);
    event SharesRedistributed(uint indexed propertyId, address[] newInvestors, uint[] newAmounts);

    
    address public admin;

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin");
        _;
    }

    function listProperty(uint price) external returns (uint) {
        uint propertyId = nextPropertyId++;
        properties[propertyId] = Property({
            id: propertyId,
            ownershipType: OwnershipType.SINGLE,
            currentOwner: msg.sender,
            totalShares: 10000
        });

        shares[propertyId][msg.sender] = 10000;
        emit PropertyListed(propertyId, msg.sender);
        return propertyId;
    }

    // SINGLE ➝ SINGLE
    function transferToSingleBuyer(uint propertyId, address newOwner) external {
        require(properties[propertyId].ownershipType == OwnershipType.SINGLE, "Not single-owned");
        require(shares[propertyId][msg.sender] == 10000, "Only full owner can transfer");

        shares[propertyId][msg.sender] = 0;
        shares[propertyId][newOwner] = 10000;
        properties[propertyId].currentOwner = newOwner;
        emit OwnershipTransferred(propertyId, msg.sender, newOwner);
    }

    // SINGLE ➝ MULTIPLE (crowdfund)
    function fractionalize(uint propertyId, address[] memory investors, uint[] memory amounts) external {
        require(properties[propertyId].ownershipType == OwnershipType.SINGLE, "Not single-owned");
        require(shares[propertyId][msg.sender] == 10000, "Only full owner can fractionalize");

        // Reset ownership
        shares[propertyId][msg.sender] = 0;

        uint total = 0;
        for (uint i = 0; i < investors.length; i++) {
            shares[propertyId][investors[i]] = amounts[i];
            total += amounts[i];
        }

        require(total == 10000, "Total shares must equal 10000");

        properties[propertyId].ownershipType = OwnershipType.CROWDFUND;
        properties[propertyId].currentOwner = address(0); // no single owner
        emit PropertyFractionalized(propertyId, investors, amounts);
    }

    // MULTIPLE ➝ SINGLE
    function buyFromMultiple(uint propertyId, address[] memory fromOwners) external payable {
        require(properties[propertyId].ownershipType == OwnershipType.CROWDFUND, "Not crowdfunded");

        for (uint i = 0; i < fromOwners.length; i++) {
            require(shares[propertyId][fromOwners[i]] > 0, "Not an owner");
            shares[propertyId][fromOwners[i]] = 0;
        }

        shares[propertyId][msg.sender] = 10000;
        properties[propertyId].ownershipType = OwnershipType.SINGLE;
        properties[propertyId].currentOwner = msg.sender;
        emit PropertyBoughtOut(propertyId, msg.sender);
    }

    // MULTIPLE ➝ MULTIPLE
    function redistributeShares(uint propertyId, address[] memory newInvestors, uint[] memory newAmounts) external onlyAdmin {
        require(properties[propertyId].ownershipType == OwnershipType.CROWDFUND, "Not crowdfunded");

        // Clear old shares
        // NOTE: Add proper clearing loop or store investors in array
        // For simplicity we’re assuming all are reset manually

        uint total = 0;
        for (uint i = 0; i < newInvestors.length; i++) {
            shares[propertyId][newInvestors[i]] = newAmounts[i];
            total += newAmounts[i];
        }

        require(total == 10000, "Total must be 100%");
        emit SharesRedistributed(propertyId, newInvestors, newAmounts);
    }

    function getShare(address investor, uint propertyId) external view returns (uint) {
        return shares[propertyId][investor];
    }
}
