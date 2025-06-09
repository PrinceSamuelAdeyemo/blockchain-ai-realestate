require("@nomicfoundation/hardhat-toolbox");
//require("dotenv").config();

/* /** @type import('hardhat/config').HardhatUserConfig *
module.exports = {
  solidity: "0.8.28",
};
 */
task("accounts", "Prints the list of accounts", async (taskArgs, hre) => {
  const accounts = await hre.ethers.getSigners();

  for (const account of accounts) {
    console.log(account.address);
  }
});


module.exports = {
  solidity: "0.8.28",
  networks: {
    ganache: {
      url: "http://127.0.0.1:8545",
      accounts: process.env.GANACHE_PRIVATE_KEY,
    }
  }
};
