"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import Web3 from 'web3';
import { connectWallet, signMessage, verifySignature } from '@/lib/web3/auth';
import { apiUrl } from '@/utils/env';

interface Web3AuthContextType {
  web3: Web3 | null;
  account: string | null;
  chainId: bigint | null;
  connect: () => Promise<void>;
  disconnect: () => void;
  isAuthenticated: boolean;
  authToken: string | null;
}

const Web3AuthContext = createContext<Web3AuthContextType | undefined>(undefined);

export const Web3AuthProvider = ({ children }: { children: ReactNode }) => {
  const [web3, setWeb3] = useState<Web3 | null>(null);
  const [account, setAccount] = useState<string | null>(null);
  const [chainId, setChainId] = useState<bigint | null>(null);
  const [authToken, setAuthToken] = useState<string | null>(null);

  const connect = async () => {
    console.log("apiUrl triggered", apiUrl)
    try {
      const { web3, account, chainId } = await connectWallet();
      setWeb3(web3);
      setAccount(account);
      setChainId(chainId);

      // Generate a signature for backend verification
      // Step 1: Request a nonce from the backend
      console.log("account", account)
      console.log("apiUrl", apiUrl)
      console.log("web3", web3)
      const nonceResponse = await fetch(`${apiUrl}/core/api/auth/nonce`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address: account }),
      });

      if (!nonceResponse.ok) {
        throw new Error('Failed to fetch nonce');
      }

      const { nonce } = await nonceResponse.json();

      const message = `Sign this message to verify your wallet: ${nonce}`;
      const signature = await signMessage(web3, account, nonce);

      /* // In a real app, you would send this to your backend for verification
      const isValid = await verifySignature(web3, message, signature, account);
      if (isValid) {
        setAuthToken(signature); // In production, use a proper JWT from your backend
      } */
     // Step 3: Verify the signature with the backend
      const verifyResponse = await fetch(`${apiUrl}/core/api/auth/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          address: account, 
          signature: signature, 
          message: nonce
        }),
      });

      console.log("Message", message);
      console.log("Signature", signature);
      console.log("Account", account);
      if (!verifyResponse.ok) {
        throw new Error('Signature verification failed');
      }

      const { success, token } = await verifyResponse.json();

      if (success) {
        setAuthToken(token); // Use the token provided by the backend
      }


      // Listen for account changes
      if (window.ethereum) {
        window.ethereum.on('accountsChanged', (accounts: string[]) => {
          if (accounts.length > 0) {
            setAccount(accounts[0]);
          } else {
            disconnect();
          }
        });

        window.ethereum.on('chainChanged', () => {
          window.location.reload();
        });
      }
    } catch (error) {
      console.error('Error connecting wallet:', error);
      throw error;
    }
  };

  const disconnect = () => {
    setWeb3(null);
    setAccount(null);
    setChainId(null);
    setAuthToken(null);
  };

  useEffect(() => {
    // Check if wallet is already connected when component mounts
    const checkConnectedWallet = async () => {
      if (window.ethereum && window.ethereum.selectedAddress) {
        try {
          await connect();
        } catch (error) {
          console.error('Error reconnecting wallet:', error);
        }
      }
    };

    checkConnectedWallet();

    return () => {
      if (window.ethereum) {
        window.ethereum.removeAllListeners();
      }
    };
  }, []);

  return (
    <Web3AuthContext.Provider
      value={{
        web3,
        account,
        chainId,
        connect,
        disconnect,
        isAuthenticated: !!authToken,
        authToken,
      }}
    >
      {children}
    </Web3AuthContext.Provider>
  );
};

export const useWeb3Auth = () => {
  const context = useContext(Web3AuthContext);
  if (context === undefined) {
    throw new Error('useWeb3Auth must be used within a Web3AuthProvider');
  }
  return context;
};