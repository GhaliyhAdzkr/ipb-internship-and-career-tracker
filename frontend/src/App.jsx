import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
// Layout component replaced by AppShell for protected routes
import Landing from "./pages/Landing";
import AppShell from "./layouts/AppShell";
import Wishlist from "./pages/Wishlist";
import Login from "./pages/Login";
import Registration from "./pages/Registrasi";
import ForgotPassword from "./pages/ForgotPassword";
import VerifyEmail from "./pages/VerifyEmail";
import Dashboard from "./pages/Dashboard";
import Lowongan from "./pages/Lowongan";
import Lamaran from "./pages/Lamaran";
import Jurnal from "./pages/Jurnal";
import Laporan from "./pages/Laporan";
import Profil from "./pages/Profil";
import DetailLowongan from "./pages/DetailLowongan";

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
  const token = localStorage.getItem('token');
  if (token) {
    return <Navigate to="/app/home" replace />;
  }
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Authentication Routes (Grouped logically) */}
        {/* Guest / Public Routes (landing + auth) */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
        <Route path="/registration" element={<PublicRoute><Registration /></PublicRoute>} />
        <Route path="/forgot-password" element={<PublicRoute><ForgotPassword /></PublicRoute>} />
        <Route path="/verify-email" element={<VerifyEmail />} />

        {/* App (protected) with nested routes */}
        <Route path="/app" element={<ProtectedRoute><AppShell /></ProtectedRoute>}>
          <Route index element={<Dashboard />} />
          <Route path="home" element={<Dashboard />} />
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
