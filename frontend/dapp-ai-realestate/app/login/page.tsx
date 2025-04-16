"use client"

import Image from 'next/image';
import Link from 'next/link';
import { useState } from 'react';
import Head from 'next/head';

export default function Login() {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle login logic here
    window.location.href = '/'; // Redirect to homepage after login
  };

  return (
    <>
      <Head>
        <title>Sign In | Homes & Props</title>
        <meta name="description" content="My first e-commerce website" />
        <meta name="keywords" content="ecommerce buyproducts" />
        <meta name="author" content="Samuel Adeyemo" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>

      <div className="min-h-screen flex flex-col">
        {/* Header/Navbar */}
        <header className="bg-white shadow-sm">
          <nav className="container mx-auto px-4">
            <div className="flex items-center justify-between py-3">
              <Link href="/" className="flex items-center">
                <Image src="/icons/real-estate.png" alt="Logo" width={24} height={24} className="mr-2" />
                <h4 className="font-bold text-lg">HOMES & PROPS</h4>
              </Link>

              {/* Mobile menu button */}
              <div className="md:hidden">
                <button className="flex items-center p-2">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
                  </svg>
                </button>
              </div>

              {/* Desktop menu */}
              <div className="hidden md:flex items-center space-x-4">
                <Link href="/" className="px-2 py-1 hover:text-gray-600">Home</Link>
                <Link href="/category" className="px-2 py-1 hover:text-gray-600">Category</Link>
                <Link href="/location" className="px-2 py-1 hover:text-gray-600">Location</Link>
                <Link href="/faq" className="px-2 py-1 hover:text-gray-600">FAQ</Link>
                <Link href="/signup" className="bg-blue-600 text-white px-4 py-1 rounded-md hover:bg-blue-700 transition-colors">
                  Sign up
                </Link>
              </div>
            </div>

            {/* Mobile menu (hidden by default) */}
            <div className="md:hidden hidden">
              <div className="flex flex-col space-y-2 pb-3">
                <Link href="/" className="px-2 py-1 hover:text-gray-600">Home</Link>
                <Link href="/category" className="px-2 py-1 hover:text-gray-600">Category</Link>
                <Link href="/location" className="px-2 py-1 hover:text-gray-600">Location</Link>
                <Link href="/faq" className="px-2 py-1 hover:text-gray-600">FAQ</Link>
                <Link href="/signup" className="bg-blue-600 text-white px-4 py-1 rounded-md hover:bg-blue-700 transition-colors w-full text-center">
                  Sign up
                </Link>
              </div>
            </div>
          </nav>
        </header>

        {/* Main Content */}
        <main className="flex-grow py-8 md:py-12">
          <div className="container mx-auto px-4">
            <div className="max-w-5xl mx-auto bg-white rounded-lg overflow-hidden shadow-lg">
              <div className="flex flex-col md:flex-row">
                {/* Sign In Form */}
                <div className="w-full md:w-1/2 p-8">
                  <div className="mb-8">
                    <div className="flex items-center">
                      <Image src="/icons/real-estate.png" alt="Logo" width={24} height={24} className="mr-2" />
                      <h4 className="font-bold">HOMES & PROPS</h4>
                    </div>
                  </div>

                  <form onSubmit={handleSubmit}>
                    <div className="mb-6">
                      <h2 className="text-xl font-bold">SIGN IN</h2>
                      <p className="text-gray-600">Please sign in to continue</p>
                    </div>

                    <div className="mb-4">
                      <div className="flex border-b border-gray-300">
                        <input
                          type="email"
                          id="email"
                          className="w-full py-2 focus:outline-none"
                          placeholder="Email Address"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          required
                          autoFocus
                        />
                        <div className="flex items-center px-2">
                          <Image src="/icons/email-icon1.png" alt="Email" width={20} height={20} />
                        </div>
                      </div>
                    </div>

                    <div className="mb-6">
                      <div className="flex border-b border-gray-300">
                        <input
                          type="password"
                          id="password"
                          className="w-full py-2 focus:outline-none"
                          placeholder="Password"
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                          required
                        />
                        <div className="flex items-center px-2">
                          <Image src="/icons/password lock.png" alt="Password" width={20} height={20} />
                        </div>
                      </div>
                    </div>

                    <button
                      type="submit"
                      className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition-colors"
                    >
                      Sign in
                    </button>

                    <div className="text-center mt-4">
                      <p>
                        Haven't Registered?{' '}
                        <Link href="/signup" className="text-blue-600 hover:underline">
                          Sign Up
                        </Link>
                      </p>
                    </div>
                  </form>
                </div>

                {/* Image Section */}
                <div className="w-full md:w-1/2 order-first md:order-last">
                  <div className="h-full">
                    <Image 
                      src="/icons/right sidesignin-image.png" 
                      alt="Login image" 
                      width={600} 
                      height={600} 
                      className="w-full h-full object-cover"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </>
  );
}