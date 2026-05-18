import Sidebar from '../components/SideNav';
import TopBar from '../components/TopBar';
import { Outlet } from 'react-router-dom';

export default function AppShell() {
  return (
    <div className="h-screen flex bg-[#F8FAFF] overflow-hidden overscroll-none">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <TopBar />
        <main className="flex-1 overflow-y-auto p-6 scroll-smooth">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
