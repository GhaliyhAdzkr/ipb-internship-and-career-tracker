import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
// import LandingPage from "./pages/LandingPage";
import Login from "./pages/login";
import Registration from "./pages/Registrasi";
import ForgotPassword from "./pages/ForgotPassword";
import Dashboard from "./pages/Dashboard";
import Lowongan from "./pages/Lowongan";
import Lamaran from "./pages/Lamaran";
import Jurnal from "./pages/Jurnal";
import Laporan from "./pages/Laporan";
import Profil from "./pages/Profil";

// Component to protect routes that require authentication
const ProtectedRoute = ({ children }) => {
  /*
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  */
  return <Layout>{children}</Layout>;
};

// Component to redirect authenticated users away from public auth pages
const PublicRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  if (token) {
    // Redirect to dashboard if already authenticated
    return <Navigate to="/home" replace />;
  }
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Landing Page */}
        <Route path="/" element={<Login />} />

        {/* Authentication Routes (Grouped logically) */}
        <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
        <Route path="/registration" element={<PublicRoute><Registration /></PublicRoute>} />
        <Route path="/forgot-password" element={<PublicRoute><ForgotPassword /></PublicRoute>} />

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
