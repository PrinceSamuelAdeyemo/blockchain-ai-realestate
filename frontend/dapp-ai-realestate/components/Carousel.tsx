"use client"

import { useState, useEffect } from 'react';
import Image from 'next/image';

const Carousel: React.FC = () => {
  const [activeSlide, setActiveSlide] = useState(0);
  
  const slides = [
    {
      image: "/icons/vu-anh-TiVPTYCG_3E-unsplash.jpg",
      alt: "Property 1"
    },
    {
      image: "/icons/federico-respini-sYffw0LNr7s-unsplash (1).jpg", 
      alt: "Property 2"
    },
    {
      image: "/images/241521806_331627732039086_4965274948243405333_n.jpg",
      alt: "Property 3"
    }
  ];

  // Auto-advance slides
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveSlide((prev) => (prev === slides.length - 1 ? 0 : prev + 1));
    }, 5000);
    return () => clearInterval(interval);
  }, [slides.length]);

  const nextSlide = () => {
    setActiveSlide((prev) => (prev === slides.length - 1 ? 0 : prev + 1));
  };

  const prevSlide = () => {
    setActiveSlide((prev) => (prev === 0 ? slides.length - 1 : prev - 1));
  };

  return (
    <div className="relative h-full w-full">
      {slides.map((slide, index) => (
        <div 
          key={index}
          className={`absolute top-0 left-0 w-full h-full transition-opacity duration-500 ease-in-out ${
            index === activeSlide ? 'opacity-100' : 'opacity-0 pointer-events-none'
          }`}
        >
          <div className="relative w-full h-full">
            <Image 
              src={slide.image} 
              alt={slide.alt} 
              className="object-cover"
              fill
              priority={index === 0}
            />
            <div className="absolute inset-0 flex flex-col items-center justify-center text-white bg-opacity-30">
              <p className="text-2xl md:text-4xl font-bold">Homes & Properties for everybody.</p>
              <p className="text-xl md:text-2xl mt-2">Get amazing offers</p>
            </div>
          </div>
        </div>
      ))}
      <button 
        onClick={prevSlide} 
        className="absolute left-2 top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-2 rounded z-10"
        aria-label="Previous slide"
      >
        ←
      </button>
      <button 
        onClick={nextSlide} 
        className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-2 rounded z-10"
        aria-label="Next slide"
      >
        →
      </button>
    </div>
  );
};

export default Carousel;