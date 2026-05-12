import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
// Layout component replaced by AppShell for protected routes
import Landing from "./pages/public/Landing";
import AppShell from "./layouts/AppShell";
import Wishlist from "./pages/portal/Wishlist";
import Login from "./pages/auth/Login";
import Registration from "./pages/auth/Registrasi";
import ForgotPassword from "./pages/auth/ForgotPassword";
import VerifyEmail from "./pages/auth/VerifyEmail";
import Dashboard from "./pages/portal/Dashboard";
import Lowongan from "./pages/portal/Lowongan";
import Lamaran from "./pages/portal/Lamaran";
import Jurnal from "./pages/portal/Jurnal";
import Laporan from "./pages/portal/Laporan";
import Profil from "./pages/portal/Profil";
import DetailLowongan from "./pages/portal/DetailLowongan";
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminVerification from "./pages/admin/AdminVerification";
import PublicLowongan from "./pages/public/PublicLowongan";

import { useAuth } from "./hooks/useAuth";
import { PiSpinnerGap } from "react-icons/pi";

// Component to protect routes that require authentication
const ProtectedRoute = ({ children }) => {
  const { user, isLoading, isError } = useAuth();
  const token = localStorage.getItem('token');

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#F8F9FF]">
        <div className="flex flex-col items-center gap-4">
          <PiSpinnerGap size={48} className="animate-spin text-sky-950" />
          <p className="text-sm font-bold text-sky-950/50 uppercase tracking-widest">Memuat Aplikasi...</p>
        </div>
      </div>
    );
  }

  if (isError) {
    // Jika ada token tapi API return error (misal expired), bersihkan token & login ulang
    localStorage.removeItem('token');
    return <Navigate to="/login" replace />;
  }

  return children;
};

// Component to redirect authenticated users away from public auth pages
const PublicRoute = ({ children }) => {
  const { user } = useAuth();
  const token = localStorage.getItem('token');
  if (token) {
    if (user?.role === 'ADMIN') {
      return <Navigate to="/app/admin/dashboard" replace />;
    }
    return <Navigate to="/app/home" replace />;
  }
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Guest / Public Routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/lowongan" element={<PublicLowongan />} />
        <Route path="/detail/:vacancyId" element={<DetailLowongan />} />
        
        {/* Authentication Routes */}
        <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
        <Route path="/registration" element={<PublicRoute><Registration /></PublicRoute>} />
        <Route path="/forgot-password" element={<PublicRoute><ForgotPassword /></PublicRoute>} />
        <Route path="/verify-email" element={<VerifyEmail />} />

        {/* App (protected) with nested routes */}
        <Route path="/app" element={<ProtectedRoute><AppShell /></ProtectedRoute>}>
          <Route index element={<Dashboard />} />
          <Route path="home" element={<Dashboard />} />
          
          {/* Admin Routes */}
          <Route path="admin/dashboard" element={<AdminDashboard />} />
          <Route path="admin/verifikasi" element={<AdminVerification />} />
          
          <Route path="lowongan" element={<Lowongan />} />
          <Route path="wishlist" element={<Wishlist />} />
          <Route path="lamaran" element={<Lamaran />} />
          <Route path="jurnal" element={<Jurnal />} />
          <Route path="laporan" element={<Laporan />} />
          <Route path="profil" element={<Profil />} />
          <Route path="detail/:vacancyId" element={<DetailLowongan />} />
        </Route>
        
        {/* Fallback redirect */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
