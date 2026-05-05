import React from 'react';
import Sidebar from './SideNav';
import NavBar from './NavBar';
import TheFooter from './TheFooter';

const Layout = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-[#F8F9FF]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <NavBar />
        <main className="flex-1 p-6 overflow-y-auto">
          <div>
            {children}
          </div>
        </main>
        <TheFooter />
      </div>
    </div>
  );
};

export default Layout;
