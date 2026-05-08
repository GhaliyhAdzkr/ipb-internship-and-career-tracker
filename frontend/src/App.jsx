import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
// import LandingPage from "./pages/LandingPage";
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

import { useAuth } from "./hooks/useAuth";
import { PiSpinnerGap } from "react-icons/pi";

// Component to protect routes that require authentication
const ProtectedRoute = ({ children }) => {
  const { user, isLoading, isError } = useAuth();
  const token = localStorage.getItem('token');
  
  // =========================================================================
  // DEV ONLY: Bypass login check on localhost for faster frontend development
  // UNCOMMENT the block below when ready for production!
  // =========================================================================
  const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  if (isLocalhost) {
    return <Layout>{children}</Layout>;
  }

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

  return <Layout>{children}</Layout>;
};

// Component to redirect authenticated users away from public auth pages
const PublicRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  
  if (token && !isLocalhost) {
    return <Navigate to="/lowongan" replace />;
  }
  return children;
};

function App() {
  // DEV ONLY: Detect if running on local machine
  const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

  return (
    <Router>
      <Routes>
        {/* 
            DEV ONLY: Auto redirect to /lowongan if on localhost.
            Change this to simply <Login /> for production.
        */}
        <Route 
          path="/" 
          element={isLocalhost ? <Navigate to="/lowongan" replace /> : <Login />} 
        />

        {/* Authentication Routes (Grouped logically) */}
        <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
        <Route path="/registration" element={<PublicRoute><Registration /></PublicRoute>} />
        <Route path="/forgot-password" element={<PublicRoute><ForgotPassword /></PublicRoute>} />
        <Route path="/verify-email" element={<VerifyEmail />} />

        {/* Protected Application Routes (Authentication temporarily disabled) */}
        <Route path="/home" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/lowongan" element={<ProtectedRoute><Lowongan /></ProtectedRoute>} />
        <Route path="/lamaran" element={<ProtectedRoute><Lamaran /></ProtectedRoute>} />
        <Route path="/jurnal" element={<ProtectedRoute><Jurnal /></ProtectedRoute>} />
        <Route path="/laporan" element={<ProtectedRoute><Laporan /></ProtectedRoute>} />
        <Route path="/profil" element={<ProtectedRoute><Profil /></ProtectedRoute>} />
        
        {/* Fallback redirect */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
