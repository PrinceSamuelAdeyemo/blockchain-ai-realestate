const hre = require("hardhat");
const fs = require("fs");
const path = require("path");
const { parseEther } = require("ethers"); // <-- Import parseEther from ethers v6

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // 1. Deploy PropertyCrowdfund
  const PropertyCrowdfund = await hre.ethers.getContractFactory("PropertyCrowdfund");
  const propertyCrowdfund = await PropertyCrowdfund.deploy();
  await propertyCrowdfund.waitForDeployment();
  const crowdfundAddress = await propertyCrowdfund.getAddress();
  console.log("PropertyCrowdfund deployed to:", crowdfundAddress);

  // 2. Deploy RealEstateToken with the crowdfund address
  const RealEstateToken = await hre.ethers.getContractFactory("RealEstateToken");
  const token = await RealEstateToken.deploy(
    "PropertyToken",                // Token name
    "PROP",                         // Token symbol
    crowdfundAddress,               // Link to the deployed PropertyCrowdfund contract
    parseEther("0.01")              // Initial token price
  );
  await token.waitForDeployment();
  const tokenAddress = await token.getAddress();
  console.log("RealEstateToken deployed to:", tokenAddress);

  // Save deployed addresses to JSON file
  const deployments = {
    PropertyCrowdfund: crowdfundAddress,
    RealEstateToken: tokenAddress
  };

  const outputPath = path.join(__dirname, "..", "deployedAddresses.json");
  fs.writeFileSync(outputPath, JSON.stringify(deployments, null, 2));
  console.log("Deployed addresses saved to deployedAddresses.json");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});



/* 
// scripts/deploy.js
const hre = require("hardhat");
const fs = require("fs");
const path = require("path");
//const { ethers } = hre;

async function main() {
    const [deployer] = await hre.ethers.getSigners();
  //const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // 1. Deploy PropertyCrowdfund
  const PropertyCrowdfund = await ethers.getContractFactory("PropertyCrowdfund");
  const propertyCrowdfund = await PropertyCrowdfund.deploy();
  await propertyCrowdfund.waitForDeployment();
  console.log("PropertyCrowdfund deployed to:", await propertyCrowdfund.getAddress());
  //await propertyCrowdfund.deployed();
  //console.log("PropertyCrowdfund deployed to:", propertyCrowdfund.address);

  // 2. Deploy RealEstateToken with the crowdfund address
  const RealEstateToken = await ethers.getContractFactory("RealEstateToken");
  const token = await RealEstateToken.deploy(
    "PropertyToken",                // Token name
    "PROP",                         // Token symbol
    propertyCrowdfund.address,      // Link to the deployed PropertyCrowdfund contract
    hre.ethers.utils.parseEther("0.01") // Initial token price
  );
  await token.deployed();
  console.log("RealEstateToken deployed to:", token.address);

  // Save deployed addresses to JSON file
  const deployments = {
    PropertyCrowdfund: propertyCrowdfund.address,
    RealEstateToken: token.address
  };

  const outputPath = path.join(__dirname, "..", "deployedAddresses.json");
  fs.writeFileSync(outputPath, JSON.stringify(deployments, null, 2));
  console.log("Deployed addresses saved to deployedAddresses.json");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
 */

/* 
const hre = require("hardhat");
const { ethers } = hre; // Explicit import for clarity

async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  async function main() {
  const PropertyCrowdfund = await ethers.getContractFactory("PropertyCrowdfund");
  const propertyCrowdfund = await PropertyCrowdfund.deploy();
  await propertyCrowdfund.deployed();
  console.log("PropertyCrowdfund deployed to:", propertyCrowdfund.address);

  // const RealEstateToken = await ethers.getContractFactory("RealEstateToken");

  /* const token = await RealEstateToken.deploy(
    "PropertyToken",                // Token name
    "PROP",                         // Token symbol
    deployer.address,              // Property contract address placeholder
    ethers.utils.parseEther("0.01") // Initial token price
  ); *

  //await token.deployed();

  //console.log("RealEstateToken deployed to:", token.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

} */
/* 
async function main() {
  const PropertyCrowdfund = await ethers.getContractFactory("PropertyCrowdfund");
  const propertyCrowdfund = await PropertyCrowdfund.deploy();
  await propertyCrowdfund.deployed();
  console.log("PropertyCrowdfund deployed to:", propertyCrowdfund.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
 */



/* 
// scripts/deploy-token.js
const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // 1. Deploy RealEstateCrowdfund
  const Crowdfund = await hre.ethers.getContractFactory("PropertyCrowdfund");
  const crowdfund = await Crowdfund.deploy();
  await crowdfund.deployed();
  console.log("PropertyCrowdfund deployed to:", crowdfund.target);

  // 2. Deploy RealEstateToken (pass crowdfund address)
  const RealEstateToken = await hre.ethers.getContractFactory("RealEstateToken");
  const token = await RealEstateToken.deploy(
    "RealEstateToken",
    "PROP",
    crowdfund.target,
    hre.ethers.parseEther("0.01")
  );
  await token.deployed();
  console.log("RealEstateToken deployed to:", token.target);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
 */




/* async function main() {
  const PropertyCrowdfund = await ethers.getContractFactory("PropertyCrowdfund");
  const propertyCrowdfund = await PropertyCrowdfund.deploy();
  await propertyCrowdfund.deployed();
  console.log("PropertyCrowdfund deployed to:", propertyCrowdfund.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
}); */