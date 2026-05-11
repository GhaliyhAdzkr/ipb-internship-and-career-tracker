import React from 'react';
import Sidebar from '../components/SideNav';
import NavBar from '../components/NavBar';
import { Outlet } from 'react-router-dom';

export default function AppShell() {
  return (
    <div className="min-h-screen flex bg-[#F8FAFF]">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <NavBar />
        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
