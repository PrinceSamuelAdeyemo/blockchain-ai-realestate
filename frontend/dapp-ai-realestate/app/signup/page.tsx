"use client"

import { useState } from 'react';
import Head from 'next/head';
import Image from 'next/image';
import Link from 'next/link';
import Navbar from '../../components/Navbar';
import GoogleLoginButton from '@/components/auth/GoogleLoginButton';

//import { Web3ConnectButton } from '../../components/auth/Web3ConnectButton';
//import { useWeb3Auth } from '@/providers/Web3AuthProvider';
import { Button } from '@/components/ui/Button';

import { apiUrl } from '@/utils/env';


export default function SignUp() {
  // const { account, authToken, isAuthenticated } = useWeb3Auth();
  const [formData, setFormData] = useState({
    firstName: '',
    middleName: '',
    lastName: '',
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    /* if (!account || !authToken) {
      alert('Please connect your wallet before registering.');
      return;
    } */
  
    const fullData = {
      ...formData,
      //wallet_address: account,
      // auth_token: authToken,
    };

    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    const isValidEmail = (email: string) => {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    };

    if (!isValidEmail(formData.email)) {
      alert('Please enter a valid email address!');
      return;
    }

    const isValidPhone = (phone: string) => {
      const re = /^\d{10}$/; // Adjust regex based on your phone number format
      return re.test(phone);
    };

    if (!isValidPhone(formData.phone)) {
      alert('Please enter a valid phone number!');
      return;
    }

    /* const isValidPassword = (password: string) => {
      const re = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/; // At least 8 characters, at least one letter and one number 
      return re.test(password);
    };

    if (!isValidPassword(formData.password)) {
      //alert('Password must be at least 8 characters long and contain at least one letter and one number!');
      return;
    } */

    const signupResponse = await fetch(`${apiUrl}/core/api/v1/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(fullData),
    });

    console.log("Sent")
    if (!signupResponse.ok) {
      const errorData = await signupResponse.json();
      alert(`Error: ${errorData.message || 'Failed to register'}`);
      return;
    }

    const responseData = await signupResponse.json();
    console.log(responseData)

    if (signupResponse.status == 201) {
      alert('Registration successful! Please check your email for verification.');
      // Redirect to login page or perform any other action
    } else {
      alert(`Error: ${responseData || 'Failed to register'}`);
    }

  
    console.log('Form submitted:', fullData);
  
    // TODO: Send fullData to backend
  };

  //const handle_google = async () => {
    //const googleResponse = await fetch(`${apiUrl}/core/api/v1/users/google/`, {
      

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
                      <label htmlFor="firstName" className="w-1/3 text-right pr-4">First Name</label>
                      <div className="w-2/3">
                        <input
                          type="text"
                          id="firstName"
                          className="w-full border-b border-gray-300 focus:border-blue-500 outline-none px-1 py-2"
                          value={formData.firstName}
                          onChange={handleChange}
                          autoFocus
                        />
                      </div>
                    </div>
                  </div>

                  <div className="mb-4">
                    <div className="flex items-center">
                      <label htmlFor="middleName" className="w-1/3 text-right pr-4">Middle Name</label>
                      <div className="w-2/3">
                        <input
                          type="text"
                          id="middleName"
                          className="w-full border-b border-gray-300 focus:border-blue-500 outline-none px-1 py-2"
                          value={formData.middleName}
                          onChange={handleChange}
                          autoFocus
                        />
                      </div>
                    </div>
                  </div>

                  <div className="mb-4">
                    <div className="flex items-center">
                      <label htmlFor="lastName" className="w-1/3 text-right pr-4">Last Name</label>
                      <div className="w-2/3">
                        <input
                          type="text"
                          id="lastName"
                          className="w-full border-b border-gray-300 focus:border-blue-500 outline-none px-1 py-2"
                          value={formData.lastName}
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

                  

                  {/* <div className="mb-6">
                    <h2 className="text-lg font-medium mb-3">Connect Wallet</h2>
                    <Web3ConnectButton />
                    {isAuthenticated && (
                      <p className="mt-2 text-sm text-green-600">
                        Wallet connected successfully! Please complete your profile.
                      </p>
                    )}
                  </div> */}
                  
                  <div className="flex justify-end mb-4">
                    <button
                      type="submit"
                      className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-md transition duration-200"
                    >
                      Register
                    </button>
                  </div>

                  <div className="mb-6">
                    <GoogleLoginButton />
                  </div>
                  
                  <div className="text-center">
                    <p>
                      Already have an account?{' '}
                      <Link href="/login" className="text-blue-600 hover:text-blue-800">
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
