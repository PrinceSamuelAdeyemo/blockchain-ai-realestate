"use client";

import { useParams } from "next/navigation";
import { useState } from "react";
import Web3 from "web3";
import propertyCrowdfundABI from "P:/decentralized_ai_realestate/blockchain/artifacts/contracts/PropertyCrowdfund.sol/PropertyCrowdfund.json"; // Adjust path as needed


const PROPERTYCROWDFUND_CONTRACT_ADDRESS = process.env.PROPERTYFUNDCONTRACTADDRESS
const REALESTATETOKEN_CONTRACT_ADDRESS = process.env.REALESTATETOKENCONTRACTADDRESS

export default function PropertyBuyPage() {
  const { propertyId } = useParams();
  const [amount, setAmount] = useState("");
  const [txStatus, setTxStatus] = useState("");

  const handleInvest = async () => {
    if (typeof window.ethereum === "undefined") {
      setTxStatus("MetaMask not found");
      return;
    }
    try {
      await window.ethereum.request({ method: "eth_requestAccounts" });
      const web3 = new Web3(window.ethereum);
      const accounts = await web3.eth.getAccounts();
      const contract = new web3.eth.Contract(propertyCrowdfundABI.abi, PROPERTYCROWDFUND_CONTRACT_ADDRESS);

      const valueWei = web3.utils.toWei(amount, "ether");
      setTxStatus("Sending transaction...");
      await contract.methods.invest(propertyId).send({
        from: accounts[0],
        value: valueWei,
      });
      setTxStatus("Investment successful!");
    } catch (err: any) {
      setTxStatus("Error: " + (err.message || err));
    }
  };

  return (
    <div>
      <h1>Property #{propertyId}</h1>
      <label>
        Amount to invest (ETH):{" "}
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          min="0"
          step="0.01"
        />
      </label>
      <button onClick={handleInvest}>Buy/Crowdfund</button>
      <p>{txStatus}</p>
    </div>
  );
}