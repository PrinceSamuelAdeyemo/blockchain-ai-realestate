export interface PropertyProps {
    image: string;
    title: string;
    price: string;
    propertyId: number;
  }
  
  export interface PropertySectionProps {
    title: string;
    properties: PropertyProps[];
  }
  