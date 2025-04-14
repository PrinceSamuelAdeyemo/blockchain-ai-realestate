import Head from 'next/head';
import Image from 'next/image';
import Link from 'next/link';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import CategoryItem from '../../components/CategoryItem';

export default function HomePage() {
  const categoryItems = [
    {
      id: 1,
      image: '/images/the houses/download (2).png',
      title: 'Spacious Duplex'
    },
    {
      id: 2,
      image: '/images/the houses/images (11).png',
      title: 'Spacious Duplex'
    },
    {
      id: 3,
      image: '/images/the houses/images (2).png',
      title: 'Spacious Duplex'
    },
    {
      id: 4,
      image: '/images/the houses/images (5).png',
      title: 'Spacious Duplex'
    },
    {
      id: 5,
      image: '/images/the houses/images (10).png',
      title: 'Spacious Duplex'
    },
    {
      id: 6,
      image: '/images/the houses/download (5).png',
      title: 'Spacious Duplex'
    }
  ];

  return (
    <div className="flex flex-col min-h-screen">
      <Head>
        <title>HOMES & PROPS - Categories</title>
        <meta name="author" content="Samuel Adeyemo" />
        <meta name="description" content="My first e-commerce website" />
        <meta name="keywords" content="ecommerce buyproducts" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>

      <Navbar />

      <main className="flex-grow bg-white py-5 px-4 md:px-20">
        <div className="max-w-7xl mx-auto">
          <div className="text-center pb-4">
            <h2 className="text-xl md:text-2xl font-bold">DIFFERENT STYLES</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5 p-2 md:p-5">
            {categoryItems.map((item) => (
              <CategoryItem 
                key={item.id}
                image={item.image}
                title={item.title}
              />
            ))}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}