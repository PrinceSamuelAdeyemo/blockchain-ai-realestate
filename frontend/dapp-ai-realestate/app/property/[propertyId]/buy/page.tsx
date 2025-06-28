"use client";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { apiUrl } from "@/utils/env";
import Web3 from "web3";

export default function BuyPage() {
  const { propertyId } = useParams();
  const [property, setProperty] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [txStatus, setTxStatus] = useState("");

  useEffect(() => {
    async function fetchProperty() {
      setLoading(true);
      try {
        const res = await fetch(`${apiUrl}/property/api/v1/properties/${propertyId}/`);
        if (!res.ok) throw new Error("Failed to fetch property");
        const data = await res.json();
        setProperty(data);
      } catch (err) {
        setProperty(null);
      }
      setLoading(false);
    }
    if (propertyId) fetchProperty();
  }, [propertyId]);

  const handleBuy = async () => {
    if (!window.ethereum) {
      setTxStatus("MetaMask not found");
      return;
    }
    if (!property || !property.owner_wallet_address || !property.base_value) {
      setTxStatus("Property or owner wallet not found");
      return;
    }
    try {
      setTxStatus("Connecting to MetaMask...");
      await window.ethereum.request({ method: "eth_requestAccounts" });
      const web3 = new Web3(window.ethereum);
      const accounts = await web3.eth.getAccounts();
      const from = accounts[0];
      const to = property.owner_wallet_address;
      // Convert base_value (USD) to ETH if needed, else use property.priceWei or property.base_value as ETH
      const valueEth = property.base_value/2700; // If already in ETH
      const valueWei = web3.utils.toWei(valueEth.toString(), "ether");

      setTxStatus("Sending transaction...");
      await web3.eth.sendTransaction({
        from,
        to,
        value: valueWei,
      });

      setTxStatus("Purchase successful!");
    } catch (err: any) {
      setTxStatus("Error: " + (err.message || err));
    }
  };

  return (
    <div>
      <Navbar />
      <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-lg shadow min-h-[80vh]">
        <h1 className="text-2xl font-bold mb-4">Buy Property #{propertyId}</h1>
        {loading ? (
          <p>Loading property...</p>
        ) : !property ? (
          <p>Property not found.</p>
        ) : (
          <>
            <div className="mb-4">
              <strong>Owner Wallet:</strong> {property.owner_wallet_address}
            </div>
            <div className="flex flex-col mb-4">
              <strong>Price (USD):</strong>${property.base_value}
              <strong>Price (ETH):</strong> {property.base_value/2700} ETH
            </div>
            <button
              onClick={handleBuy}
              style={{ padding: "8px 24px", fontWeight: "bold" }}
            >
              Buy Now
            </button>
            <p className="mt-4">{txStatus}</p>
          </>
        )}
      </div>
      <Footer />
    </div>
  );
}