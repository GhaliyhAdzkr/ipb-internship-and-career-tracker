import "./App.css";
// Login
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/login";
import Registration from "./pages/Registrasi";
import ForgotPassword from "./pages/ForgotPassword";

// Dashboard
import Dashboard from "./pages/Dashboard";
import Lowongan from "./pages/Lowongan";
import Lamaran from "./pages/Lamaran";
import Jurnal from "./pages/Jurnal";
import Laporan from "./pages/Laporan";
import Profil from "./pages/Profil";

function App() {
	return (
		<>
			<Router>
				<Routes>
					<Route path="/" element={<Login />}></Route>
					<Route path="/regist" element={<Registration/>}></Route>
					<Route path="/forgot-password" element={<ForgotPassword />}></Route>
					<Route path="/home" element={<Dashboard />}></Route>
					<Route path="/lowongan" element={<Lowongan />}></Route>
					<Route path="/lamaran" element={<Lamaran />}></Route>
					<Route path="/jurnal" element={<Jurnal />}></Route>
					<Route path="/laporan" element={<Laporan />}></Route>
					<Route path="/profil" element={<Profil />}></Route>
				</Routes>
			</Router>
		</>
	);
}

export default App;
