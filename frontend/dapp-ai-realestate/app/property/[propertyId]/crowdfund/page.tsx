"use client";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { apiUrl } from "@/utils/env";

import Web3 from "web3";


export default function CrowdfundPage() {
  const { propertyId } = useParams();
  const [property, setProperty] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [amount, setAmount] = useState("");
  const [txStatus, setTxStatus] = useState("");
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    async function fetchProperty() {
      setLoading(true);
      try {
        const res = await fetch(`${apiUrl}/property/api/v1/properties/${propertyId}/`);
        if (!res.ok) throw new Error("Failed to fetch property");
        const data = await res.json();
        setProperty(data);
        if (data.amount_raised && data.crowdfund_target) {
          setProgress((data.amount_raised / data.crowdfund_target) * 100);
        }
      } catch (err) {
        setProperty(null);
      }
      setLoading(false);
    }
    if (propertyId) fetchProperty();
  }, [propertyId]);

  // --- MetaMask Crowdfund Logic ---
  const handleInvest = async () => {
    if (!window.ethereum) {
      setTxStatus("MetaMask not found");
      return;
    }
    if (!property || !property.owner_wallet_address) {
      setTxStatus("Property owner wallet not found");
      return;
    }
    try {
      setTxStatus("Connecting to MetaMask...");
      await window.ethereum.request({ method: "eth_requestAccounts" });
      const web3 = new Web3(window.ethereum);
      const accounts = await web3.eth.getAccounts();
      const from = accounts[0];
      const to = property.owner_wallet_address;
      const valueWei = web3.utils.toWei(amount, "ether");

      setTxStatus("Sending transaction...");
      await web3.eth.sendTransaction({
        from,
        to,
        value: valueWei,
      });

      setTxStatus("Investment successful!");
      // Optionally, refresh property data to update progress
    } catch (err: any) {
      setTxStatus("Error: " + (err.message || err));
    }
  };

  return (
    <div>
      <Navbar />
      <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-lg shadow min-h-[80vh]">
        <h1 className="text-2xl font-bold mb-4">Crowdfund Property #{propertyId}</h1>
        {loading ? (
          <p>Loading...</p>
        ) : !property ? (
          <p>Property not found.</p>
        ) : (
          <>
            <div className="mb-4">
              <strong>Target:</strong> {property.crowdfund_target/2700} ETH
            </div>
            <div className="mb-4">
              <strong>Raised:</strong> {property.amount_raised} ETH
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
              <div
                className="bg-green-500 h-4 rounded-full"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <div className="mb-4">
              <label>
                Amount to invest (ETH):{" "}
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  min="0"
                  step="0.01"
                  style={{ marginRight: 8 }}
                />
              </label>
              <button
                onClick={handleInvest}
                style={{ padding: "6px 18px", fontWeight: "bold", backgroundColor: "#3b82f6", color: "#fff", borderRadius: "4px" }}
              >
                Invest
              </button>
              <p>{txStatus}</p>
            </div>
          </>
        )}
      </div>
      <Footer />
    </div>
  );
}