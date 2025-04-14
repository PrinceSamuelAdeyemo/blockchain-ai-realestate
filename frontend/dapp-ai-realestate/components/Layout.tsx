import React, { ReactNode } from 'react';
import Navbar from './Navbar';
import Footer from './Footer';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="w-full p-0">
      <Navbar />
      <main>{children}</main>
      <Footer />
    </div>
  );
};

export default Layout;