"use client";

import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import Web3 from "web3";
import propertyCrowdfundABI from "@/contracts_json/PropertyCrowdfund.json";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const PROPERTYCROWDFUND_CONTRACT_ADDRESS = process.env.PROPERTYFUNDCONTRACTADDRESS;

const mockProperty = {
  image: "/images/sample-house.jpg",
  title: "Modern Family Home",
  description: "A beautiful 4-bedroom family home in a quiet neighborhood, close to schools and parks.",
  location: "123 Main St, Springfield",
  size: "2,500 sq ft",
  bedrooms: 4,
  bathrooms: 3,
  priceWei: "1000000000000000000", // 1 ETH
  // Add all required features here (mock values)
  apartment_total_area: 120,
  apartment_living_area: 90,
  apartment_rooms: 5,
  apartment_bedrooms: 4,
  apartment_bathrooms: 3,
  building_age: 8,
  building_total_floors: 10,
  apartment_floor: 3,
  country_encoded: 1,
  price_per_sqm: 0.0083,
  // Mock price predictions for the next 5 years
  pricePredictions: [
    { year: 2025, price: 1.0 },
    { year: 2026, price: 1.1 },
    { year: 2027, price: 1.25 },
    { year: 2028, price: 1.32 },
    { year: 2029, price: 1.45 },
  ],
};

export default function PropertyBuyPage() {
  const { propertyId } = useParams();
  const [amount, setAmount] = useState("");
  const [txStatus, setTxStatus] = useState("");
  const [web3, setWeb3] = useState<Web3 | null>(null);
  const [property, setProperty] = useState<any>(null);
  const [loading, setLoading] = useState(true);


  /* useEffect(() => {
    if (typeof window !== "undefined" && typeof window.ethereum !== "undefined") {
      setWeb3(new Web3(window.ethereum));
    }
  }, []); */

  /* 
  useEffect(() => {
    if (web3) {
      const fetchProperty = async () => {
        try {
          const contract = new web3.eth.Contract(
            propertyCrowdfundABI.abi,
            PROPERTYCROWDFUND_CONTRACT_ADDRESS
          );
          const propertyData = await contract.methods.getProperty(propertyId).call();
          setProperty(propertyData);
        } catch (error) {
          console.error("Error fetching property data:", error);
        } finally {
          setLoading(false);
        }
      };
      fetchProperty();
    }
  }, [web3, propertyId]); */

  useEffect(() => {
    async function fetchProperty() {
      setLoading(true);
      try {
        const res = await fetch(`http://localhost:8000/property/api/v1/properties/1/`);
        if (!res.ok) throw new Error("Failed to fetch property");
        const data = await res.json();
        console.log(data)
        setProperty(data);
      } catch (err) {
        setProperty(null);
      }
      setLoading(false);
    }
    if (propertyId) fetchProperty();
}, [propertyId]);


  const handleInvest = async () => {
    if (!web3) {
      setTxStatus("MetaMask not found");
      return;
    }
    try {
      await window.ethereum.request({ method: "eth_requestAccounts" });
      const accounts = await web3.eth.getAccounts();
      const contract = new web3.eth.Contract(
        propertyCrowdfundABI.abi,
        PROPERTYCROWDFUND_CONTRACT_ADDRESS
      );
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
/* 
  // Prepare chart data
  const chartData = {
    labels: mockProperty.pricePredictions.map((p) => p.year),
    datasets: [
      {
        label: "Predicted Price (ETH)",
        data: mockProperty.pricePredictions.map((p) => p.price),
        fill: false,
        borderColor: "#3b82f6",
        backgroundColor: "#3b82f6",
        tension: 0.2,
      },
    ],
  };
 */

  const chartData = property && property.price_prediction ? {
  labels: property.price_prediction.map((p: any) => p.year),
  datasets: [
    {
      label: "Predicted Price (ETH)",
      data: property.price_prediction.map((p: any) => p.price),
      fill: false,
      borderColor: "#3b82f6",
      backgroundColor: "#3b82f6",
      tension: 0.2,
    },
  ],
} : { labels: [], datasets: [] };

  return (
  <div>
    <Navbar />
    <div>
      <div style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
        {loading ? (
          <p>Loading property...</p>
        ) : !property ? (
          <p>Property not found.</p>
        ) : (
          <>
            <div style={{ display: "flex", gap: 32, flexWrap: "wrap" }}>
              <img
                src={property.image}
                alt={property.title}
                style={{ width: 350, height: 250, objectFit: "cover", borderRadius: 8 }}
              />
              <div style={{ flex: 1 }}>
                <h1>{property.title}</h1>
                <p style={{ color: "#666" }}>{property.location}</p>
                <p>{property.description}</p>
                <ul style={{ padding: 0, listStyle: "none", margin: "16px 0" }}>
                  <li><strong>Apartment Total Area:</strong> {property.total_area} m²</li>
                  <li><strong>Apartment Living Area:</strong> {property.usable_area} m²</li>
                  <li><strong>Rooms:</strong> {property.rooms}</li>
                  <li><strong>Bedrooms:</strong> {property.bedrooms}</li>
                  <li><strong>Bathrooms:</strong> {property.bathrooms}</li>
                  <li><strong>Building Age:</strong> {property.building_age} years</li>
                  <li><strong>Building Total Floors:</strong> {property.total_floors}</li>
                  <li><strong>Apartment Floor:</strong> {property.floor_number}</li>
                  <li><strong>Country Encoded:</strong> {property.country_encoded}</li>
                  <li><strong>Price per sqm:</strong>$ {property.price_per_sqm}</li>
                </ul>
                <div style={{ margin: "16px 0" }}>
                  <strong>
                    Price: {web3 ? web3.utils.fromWei(property.priceWei, "ether") : property.priceWei} ETH
                  </strong>
                </div>
                <div style={{ margin: "16px 0" }}>
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
                  <button onClick={handleInvest} style={{ padding: "6px 18px" }}>
                    Buy/Crowdfund
                  </button>
                  <p>{txStatus}</p>
                </div>
              </div>
            </div>
            <div style={{ marginTop: 40 }}>
              <h2>Price Prediction (AI Insights)</h2>
              <h2>Current Price prediction: ${property.price_prediction[0]["price"]}</h2>
              <Line data={chartData} />
            </div>
          </>
        )}
      </div>
      <Footer />
    </div>
  </div>
);
}