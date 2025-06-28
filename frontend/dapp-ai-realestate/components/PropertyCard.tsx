"use client"

import React from 'react';
import Image from 'next/image';
import { PropertyProps } from '../types';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

const PropertyCard: React.FC<PropertyProps> = ({ image, title, price, id, slug, base_value }) => {
  const router = useRouter();

  const openPropertyDetails = (propertyId: number) => {
    router.push(`/property/${id}`);
  }
  const addToCart = () => {
    // Logic to add the property to the cart
    console.log(`Property ${id} added to cart`);
  };


  console.log(id)


  return (
    <div className="text-center">
      <div className=" bg-gray-100 p-2 hover:shadow-md transition-shadow duration-300">
        <div className="relative h-48 w-full">
          <Image 
            src={image} 
            alt={title} 
            className="object-cover"
            fill
          />
        </div>
        <p className="font-bold mt-2">{title}</p>
        <p className="font-bold">{price}</p>
        <div className="flex justify-center items-center mt-2">
          <button className="bg-blue-500 hover:bg-blue-600 text-white py-3 px-2 rounded flex items-center justify-center mx-auto transition-colors duration-300">
            <Image 
              className="w-4 h-4 mr-1 bg-white text-white" 
              src="/icons/images - 2022-09-10T130706.541_1.jpeg" 
              alt="cart" 
              width={16} 
              height={16} 
            />
            ADD TO CART
          </button>
          <button onClick={() => openPropertyDetails(id)} className="bg-blue-500 hover:bg-blue-600 text-white py-3 px-2 rounded flex items-center justify-center mx-auto transition-colors duration-300">
            <Image 
              className="w-4 h-4 mr-1 bg-white text-white" 
              src="/icons/images - 2022-09-10T130706.541_1.jpeg" 
              alt="cart" 
              width={16} 
              height={16} 
            />
            VIEW  DETAILS
          </button>
        </div>
      </div>
    </div>
  );
};

export default PropertyCard;