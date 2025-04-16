"use client"

import { useState } from 'react';
import Head from 'next/head';
import Image from 'next/image';
import Link from 'next/link';
import Navbar from '../../components/Navbar';

export default function SignUp() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setFormData({
      ...formData,
      [id]: value
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission here
    console.log('Form submitted:', formData);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Head>
        <title>Sign Up - HOMES & PROPS</title>
        <meta name="author" content="Samuel Adeyemo" />
        <meta name="description" content="My first e-commerce website" />
        <meta name="keywords" content="ecommerce buyproducts" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>

      <Navbar />

      <main className="flex-grow py-6 md:py-12 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="flex flex-col md:flex-row border shadow-md overflow-hidden">
            {/* Form Section */}
            <div className="w-full md:w-1/2 p-4 md:p-8 order-last md:order-first">
              <div className="mb-6">
                <div className="flex items-center mb-8">
                  <Image 
                    src="/icons/real-estate.png" 
                    alt="Logo" 
                    width={30} 
                    height={30} 
                    className="mr-2"
                  />
                  <h1 className="text-xl font-bold">HOMES & PROPS</h1>
                </div>
                
                <form onSubmit={handleSubmit}>
                  <div className="mb-4">
                    <h2 className="text-xl font-medium text-center mb-6">REGISTER</h2>
                  </div>
                  
                  <div className="mb-4">
                    <div className="flex items-center">
                      <label htmlFor="name" className="w-1/3 text-right pr-4">Name</label>
                      <div className="w-2/3">
                        <input
                          type="text"
                          id="name"
                          className="w-full border-b border-gray-300 focus:border-blue-500 outline-none px-1 py-2"
                          value={formData.name}
                          onChange={handleChange}
                          autoFocus
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <div className="flex items-center">
                      <label htmlFor="email" className="w-1/3 text-right pr-4">Email</label>
                      <div className="w-2/3">
                        <input
                          type="email"
                          id="email"
                          className="w-full border-b border-gray-300 focus:border-blue-500 outline-none px-1 py-2"
                          value={formData.email}
                          onChange={handleChange}
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <div className="flex items-center">
                      <label htmlFor="phone" className="w-1/3 text-right pr-4">Phone</label>
                      <div className="w-2/3">
                        <input
                          type="tel"
                          id="phone"
                          className="w-full border-b border-gray-300 focus:border-blue-500 outline-none px-1 py-2"
                          value={formData.phone}
                          onChange={handleChange}
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <div className="flex items-center">
                      <label htmlFor="password" className="w-1/3 text-right pr-4">Password</label>
                      <div className="w-2/3">
                        <input
                          type="password"
                          id="password"
                          className="w-full border-b border-gray-300 focus:border-blue-500 outline-none px-1 py-2"
                          value={formData.password}
                          onChange={handleChange}
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="mb-6">
                    <div className="flex items-center">
                      <label htmlFor="confirmPassword" className="w-1/3 text-right pr-4">Confirm Password</label>
                      <div className="w-2/3">
                        <input
                          type="password"
                          id="confirmPassword"
                          className="w-full border-b border-gray-300 focus:border-blue-500 outline-none px-1 py-2"
                          value={formData.confirmPassword}
                          onChange={handleChange}
                        />
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex justify-end mb-4">
                    <button
                      type="submit"
                      className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-md transition duration-200"
                    >
                      Register
                    </button>
                  </div>
                  
                  <div className="text-center">
                    <p>
                      Already have an account?{' '}
                      <Link href="/signin" className="text-blue-600 hover:text-blue-800">
                        Sign In
                      </Link>
                    </p>
                  </div>
                </form>
              </div>
            </div>
            
            {/* Image Section */}
            <div className="w-full md:w-1/2 order-first md:order-last">
              <div className="h-full">
                <Image
                  src="/icons/right side login.png"
                  alt="Registration"
                  width={600}
                  height={800}
                  className="h-full w-full object-cover"
                />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
