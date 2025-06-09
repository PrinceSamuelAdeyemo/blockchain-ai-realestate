import Web3 from 'web3';

declare global {
  interface Window {
    ethereum?: any;
    web3?: any;
  }
}

export const getWeb3Instance = async () => {
  if (typeof window !== 'undefined') {
    // Modern dapp browsers
    if (window.ethereum) {
      try {
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        return new Web3(window.ethereum);
      } catch (error) {
        console.error('User denied account access', error);
        throw error;
      }
    }
    // Legacy dapp browsers
    else if (window.web3) {
      return new Web3(window.web3.currentProvider);
    }
  }
  // Non-dapp browsers or no wallet installed
  console.log('Non-Ethereum browser detected. Consider installing MetaMask!');
  return null;
};

export const getConnectedAccounts = async (web3: Web3) => {
  return await web3.eth.getAccounts();
};


export const shortenAddress = (address: string, chars = 4) => {
    return `${address.substring(0, chars + 2)}...${address.substring(
      address.length - chars
    )}`;
  };
  
  export const switchNetwork = async (web3: Web3, chainId: number) => {
    if (!window.ethereum) throw new Error('MetaMask not installed');
    
    try {
      await window.ethereum.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: web3.utils.toHex(chainId) }],
      });
    } catch (error: any) {
      // This error code indicates that the chain has not been added to MetaMask
      if (error.code === 4902) {
        throw new Error('Network not added to MetaMask');
      }
      throw error;
    }
  };