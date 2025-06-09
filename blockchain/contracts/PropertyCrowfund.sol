// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PropertyCrowfund {
    struct Property {
        uint256 id;
        address owner;
        uint256 price;
        uint256 totalInvested;
        bool isFunded;
        mapping(address => uint256) investors;
        address[] investorList;
    }

    struct Proposal {
        string description;
        uint256 votesFor;
        uint256 votesAgainst;
        mapping(address => bool) voted;
        bool executed;
    }

    uint256 public propertyCount;
    mapping(uint256 => Property) public properties;
    mapping(uint256 => Proposal[]) public propertyProposals;

    event PropertyListed(uint256 propertyId, address owner, uint256 price);
    event Invested(uint256 propertyId, address investor, uint256 amount);
    event ProposalCreated(uint256 propertyId, uint256 proposalId, string description);
    event Voted(uint256 propertyId, uint256 proposalId, address voter, bool support);
    event ProposalExecuted(uint256 propertyId, uint256 proposalId);

    // List a property for crowdfunding
    function listProperty(uint256 price) external {
        propertyCount++;
        Property storage prop = properties[propertyCount];
        prop.id = propertyCount;
        prop.owner = msg.sender;
        prop.price = price;
        emit PropertyListed(propertyCount, msg.sender, price);
    }

    // Invest in a property
    function invest(uint256 propertyId) external payable {
        Property storage prop = properties[propertyId];
        require(!prop.isFunded, "Already funded");
        require(msg.value > 0, "No ETH sent");
        if (prop.investors[msg.sender] == 0) {
            prop.investorList.push(msg.sender);
        }
        prop.investors[msg.sender] += msg.value;
        prop.totalInvested += msg.value;
        emit Invested(propertyId, msg.sender, msg.value);

        if (prop.totalInvested >= prop.price) {
            prop.isFunded = true;
        }
    }

    // Create a governance proposal (only investors)
    function createProposal(uint256 propertyId, string memory description) external {
        Property storage prop = properties[propertyId];
        require(prop.investors[msg.sender] > 0, "Not an investor");
        Proposal storage proposal = propertyProposals[propertyId].push();
        proposal.description = description;
        emit ProposalCreated(propertyId, propertyProposals[propertyId].length - 1, description);
    }

    // Vote on a proposal (only investors, one vote per proposal)
    function vote(uint256 propertyId, uint256 proposalId, bool support) external {
        Property storage prop = properties[propertyId];
        require(prop.investors[msg.sender] > 0, "Not an investor");
        Proposal storage proposal = propertyProposals[propertyId][proposalId];
        require(!proposal.voted[msg.sender], "Already voted");
        proposal.voted[msg.sender] = true;
        if (support) {
            proposal.votesFor += prop.investors[msg.sender];
        } else {
            proposal.votesAgainst += prop.investors[msg.sender];
        }
        emit Voted(propertyId, proposalId, msg.sender, support);
    }

    // Execute proposal (simple majority, only once)
    function executeProposal(uint256 propertyId, uint256 proposalId) external {
        Proposal storage proposal = propertyProposals[propertyId][proposalId];
        require(!proposal.executed, "Already executed");
        proposal.executed = true;
        emit ProposalExecuted(propertyId, proposalId);
        // Add your logic for executing the proposal here
    }

    // Helper: Get investors for a property
    function getInvestors(uint256 propertyId) external view returns (address[] memory) {
        return properties[propertyId].investorList;
    }
}