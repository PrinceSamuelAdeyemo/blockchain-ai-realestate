// File: pages/index.tsx
import Head from 'next/head';
import Layout from '../components/Layout';
import Carousel from '../components/Carousel';
import PropertySection from '../components/PropertySection';
import { PropertyProps } from '../types';

export default function Home() {
  const luxuryProperties: PropertyProps[] = [
    { image: "/images/the houses/download (1).jfif", title: "A brown duplex", price: "N5,700,000" },
    { image: "/images/the houses/download (2).jfif", title: "A brown duplex", price: "N5,700,000" },
    { image: "/images/the houses/download (3).jfif", title: "A brown duplex", price: "N5,700,000" },
    { image: "/images/the houses/download (4).jfif", title: "A brown duplex", price: "N5,700,000" }
  ];

  const corporateProperties: PropertyProps[] = [
    { image: "/images/the houses/images (3).jfif", title: "A brown duplex", price: "N5,700,000" },
    { image: "/images/the houses/images (1).jfif", title: "A brown duplex", price: "N5,700,000" },
    { image: "/images/the houses/images (2).jfif", title: "A brown duplex", price: "N5,700,000" },
    { image: "/images/the houses/images (4).jfif", title: "A brown duplex", price: "N5,700,000" }
  ];

  const affordableProperties: PropertyProps[] = [
    { image: "/images/the houses/download (5).jfif", title: "A brown duplex", price: "N5,700,000" },
    { image: "/images/the houses/images (5).jfif", title: "A brown duplex", price: "N5,700,000" },
    { image: "/images/the houses/images (7).jfif", title: "A brown duplex", price: "N5,700,000" },
    { image: "/images/the houses/images (6).jfif", title: "A brown duplex", price: "N5,700,000" }
  ];

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
      <div className="relative w-full h-96">
        <Carousel />
      </div>

      {/* Main Content */}
      <div className="main-section">
        <div className="p-5 md:px-5">
          <PropertySection title="LUXURY PROPERTIES" properties={luxuryProperties} />
          <PropertySection title="CORPORATE PROPERTIES" properties={corporateProperties} />
          <PropertySection title="AFFORDABLE PROPERTIES" properties={affordableProperties} />
        </div>
      </div>
    </Layout>
  );
}
