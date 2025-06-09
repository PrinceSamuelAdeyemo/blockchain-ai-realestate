import Web3 from 'web3';
import { getWeb3Instance, getConnectedAccounts } from './utils';

export const connectWallet = async () => {
  const web3 = await getWeb3Instance();
  if (!web3) throw new Error('Web3 not initialized');
  
  const accounts = await getConnectedAccounts(web3);
  if (accounts.length === 0) throw new Error('No accounts found');
  
  return {
    web3,
    account: accounts[0],
    chainId: await web3.eth.getChainId()
  };
};

export const signMessage = async (web3: Web3, account: string, message: string) => {
  return await web3.eth.personal.sign(message, account, '');
};

export const verifySignature = async (web3: Web3, message: string, signature: string, address: string) => {
  const recoveredAddress = await web3.eth.personal.ecRecover(message, signature);
  return recoveredAddress.toLowerCase() === address.toLowerCase();
};