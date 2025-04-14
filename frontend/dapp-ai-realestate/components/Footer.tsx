import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white h-full">
      <div className="container mx-auto px-5 py-3">
        <div className="flex flex-wrap">
          <div className="w-full md:w-1/2">
            <div className="w-full">
              <p className="text-xl font-bold">ABOUT US</p>
              <p>Home and properties for everyone, we help to provide excellent and affordable house and housing facilities for everyone.</p>
              <h6 className="p-0 m-0">A TRIAL WILL CONVINCE YOU.</h6>
            </div>
            <div className="w-full pt-4">
              <p className="text-xl font-bold text-white">CONTACT</p>
              {/* Contact details would go here */}
            </div>
          </div>

          <div className="w-full md:w-1/2 mt-4 md:mt-0">
            <div className="w-full">
              <p className="text-xl font-bold text-white">POLICY</p>
              <div className="flex flex-wrap">
                <div className="w-1/2">
                  <p>Delivery</p>
                </div>
                <div className="w-1/2">
                  <p>Payment</p>
                </div>
                <div className="w-1/2">
                  <p>One section</p>
                </div>
                <div className="w-1/2">
                  <p>Another section</p>
                </div>
              </div>
            </div>
            <div className="w-full pt-4">
              <p className="text-xl font-bold text-white">SOCIALS</p>
              {/* Social media links would go here */}
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer