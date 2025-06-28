import React from 'react';
import PropertyCard from './PropertyCard';
import { PropertyProps, PropertySectionProps } from '../types';

const PropertySection: React.FC<PropertySectionProps> = ({ title, properties }) => {
  return (
    <div className="my-8">
      <p className="font-bold text-xl my-4">{title}</p>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2 md:gap-5">
        {properties.map((property, index) => (
          <PropertyCard 
            key={index}
            image={property.image}
            title={property.title}
            price={property.price}
            id={property.id}
            slug={property.slug}
            base_value={property.base_value}
            description={property.description}
          />
        ))}
      </div>
    </div>
  );
};

export default PropertySection;