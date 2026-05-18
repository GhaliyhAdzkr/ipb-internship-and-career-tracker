import Sidebar from './SideNav';
import TopBar from './TopBar';
import TheFooter from './TheFooter';

const Layout = ({ children }) => {
  return (
    <div className="flex h-screen bg-[#F8F9FF] overflow-hidden overscroll-none">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <TopBar />
        <main className="flex-1 overflow-y-auto p-6 scroll-smooth">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
        <TheFooter />
      </div>
    </div>
  );
};

export default Layout;
