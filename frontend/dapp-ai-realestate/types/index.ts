export interface PropertyProps {
    id: number;
    slug: string;
    image: string;
    title: string;
    price: string;
    base_value: number | string;
    description?: string;
    is_featured?: boolean;
    category?: string | null;
    location?: string;
    bedrooms?: number;
    bathrooms?: number;
    area?: string;
    created_at?: string;
    updated_at?: string;
    
  }
  
  export interface PropertySectionProps {
    title: string;
    properties: PropertyProps[];
  }
  