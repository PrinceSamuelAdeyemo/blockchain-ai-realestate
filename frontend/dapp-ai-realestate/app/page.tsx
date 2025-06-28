"use client";
// File: pages/index.tsx
import Head from 'next/head';
import Layout from '../components/Layout';
import Carousel from '../components/Carousel';
import PropertySection from '../components/PropertySection';
import { PropertyProps } from '../types';

import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { apiUrl } from "@/utils/env";

export default function Home() {
  const [properties, setProperties] = useState<PropertyProps[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const userDetails = localStorage.getItem("userDetails")
  console.log(userDetails)

  useEffect(() => {
    async function fetchProperties() {
      setLoading(true);
      try {
        const res = await fetch(`${apiUrl}/property/api/v1/properties/`);
        if (!res.ok) throw new Error("Failed to fetch properties");
        const data = await res.json();
        const allProps: PropertyProps[] = (data.results || data).map((p: any) => ({
          id: p.id,
          slug: p.slug,
          image: p.image,
          title: p.title,
          price: p.price,
          base_value: p.base_value,
          description: p.description,
          is_featured: p.is_featured,
          category: p.category,
          location: p.location,
          bedrooms: p.bedrooms,
          bathrooms: p.bathrooms,
          area: p.area,
          created_at: p.created_at,
          updated_at: p.updated_at,
        }));
        setProperties(allProps);
      } catch (err: any) {
        console.error(err);
        setError(err.message || 'Error fetching data');
      } finally {
        setLoading(false);
      }
    }
    fetchProperties();
  }, []);

  // Filter into categories
  const luxuryProperties = properties.filter(p => p.category === 'luxury');
  const corporateProperties = properties.filter(p => p.category === 'corporate');
  const affordableProperties = properties.filter(p => p.is_featured === true);

  return (
    <Layout>
      <Head>
        <meta charSet="UTF-8" />
        <meta name="author" content="Samuel Adeyemo" />
        <meta name="description" content="My first e-commerce website" />
        <meta name="keywords" content="ecommerce buyproducts" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Homes & Props</title>
      </Head>


      {/* Hero Carousel */}
      <div className="relative w-full h-[50vh] md:h-[60vh]">
        <Carousel />
      </div>

      {/* Main Content */}
      <div className="main-section">
        <div className="p-5 md:px-5">
          {loading && <p>Loading properties...</p>}
          {error && <p className="text-red-500">{error}</p>}
          {!loading && !error && (
            <>
              {/* <PropertySection title="LUXURY PROPERTIES" properties={luxuryProperties} />
              <PropertySection title="CORPORATE PROPERTIES" properties={corporateProperties} /> */}
              <PropertySection title="AFFORDABLE PROPERTIES" properties={affordableProperties} />
            </>
          )}
        </div>
      </div>

      <Footer />
    </Layout>
  );
}
