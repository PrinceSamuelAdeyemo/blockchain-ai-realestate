"use client"

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <div className="w-full bg-white shadow-sm">
      <nav className="w-full p-0">
        <div className="container mx-auto p-0 pr-3 bg-white flex flex-wrap items-center justify-between">
          <Link href="/" className="flex items-center ml-5">
            <h4 className="font-bold flex items-center">
              <span>
                <Image className="h-8 w-8 mr-2" src="/icons/real-estate.png" alt="Logo" width={32} height={32} />
              </span> 
              HOMES & PROPS
            </h4>
          </Link>
          
          <div className="block md:hidden">
            <button 
              className="p-2 border rounded" 
              type="button" 
              onClick={toggleMenu}
            >
              <span className="block w-6 h-1 bg-gray-600 mb-1"></span>
              <span className="block w-6 h-1 bg-gray-600 mb-1"></span>
              <span className="block w-6 h-1 bg-gray-600"></span>
            </button>
          </div>
          
          <div className={`${isMenuOpen ? 'block' : 'hidden'} md:flex md:justify-end w-full md:w-auto`}>
            <ul className="flex flex-col md:flex-row">
              <li className="px-2">
                <Link href="/" className="block py-2 px-2 text-blue-500">Home</Link>
              </li>
              <li className="px-2">
                <Link href="/category" className="block py-2 px-2 hover:text-blue-500">Category</Link>
              </li>
              <li className="px-2">
                <Link href="/location" className="block py-2 px-2 hover:text-blue-500">Location</Link>
              </li>
              <li className="px-2">
                <Link href="/faq" className="block py-2 px-2 hover:text-blue-500">FAQ</Link>
              </li>
              <li className="px-2">
                <Link href="/cart" className="block py-1">
                  <Image className="h-6 w-6" src="/icons/images - 2022-09-10T130814.085_1.jpeg" alt="Cart" width={24} height={24} />
                </Link>
              </li>
              <li className="px-2">
                <Link href="/profile" className="block py-1">
                  <Image className="h-6 w-6" src="/icons/profile_1107841.png" alt="Profile" width={24} height={24} />
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default Navbar;