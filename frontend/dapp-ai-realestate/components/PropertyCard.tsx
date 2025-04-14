import React from 'react';
import Image from 'next/image';
import { PropertyProps } from '../types';

const PropertyCard: React.FC<PropertyProps> = ({ image, title, price }) => {
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
        <button className="bg-blue-500 hover:bg-blue-600 text-white py-1 px-2 rounded flex items-center justify-center mx-auto transition-colors duration-300">
          <Image 
            className="w-4 h-4 mr-1 bg-white text-white" 
            src="/icons/images - 2022-09-10T130706.541_1.jpeg" 
            alt="cart" 
            width={16} 
            height={16} 
          />
          ADD TO CART
        </button>
      </div>
    </div>
  );
};

export default PropertyCard;