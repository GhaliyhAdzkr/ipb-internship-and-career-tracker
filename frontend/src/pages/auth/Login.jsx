import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { useSearchParams } from "react-router-dom";
import { 
  PiEnvelopeSimple, 
  PiLockKey, 
  PiArrowRight, 
  PiSpinnerGap, 
  PiEye, 
  PiEyeSlash, 
  PiGraduationCap,
  PiCheckCircle
} from "react-icons/pi";

function Login() {
	const navigate = useNavigate();
	const { login, isLoggingIn, loginError } = useAuth();
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [showPassword, setShowPassword] = useState(false);

	const [searchParams] = useSearchParams();
	const isVerified = searchParams.get("verified") === "true";
	const isRegistered = searchParams.get("registered") === "true";

	const handleSubmit = async (e) => {
		e.preventDefault();
		login({ email, password });
	};

	return (
		<div className="grid h-screen bg-white grid-cols-1 md:grid-cols-2 font-jakarta overflow-hidden">
			{/* Left Side: Hero Artwork Section (RESTORED) */}
			<div className="hidden md:flex relative flex-col justify-end p-16 overflow-hidden">
				<img
					src="/assets/ipb-ahn.png"
					alt="Welcome"
					className="absolute inset-0 h-full w-full object-cover opacity-80 blur-[1px]"
				/>
				<div className="absolute inset-0 bg-slate-900/20" />
				
				<div className="relative z-10 space-y-6">
					<div className="w-16 h-16 bg-white/10 backdrop-blur-md rounded-2xl flex items-center justify-center border border-white/20 shadow-lg">
						<PiGraduationCap size={36} className="text-white" />
					</div>
					<div className="space-y-4">
						<h1 className="text-6xl font-extrabold text-white leading-[1.1] tracking-tight">
							Membangun Masa <br /> Depan Karirmu.
						</h1>
						<p className="text-lg font-medium text-white/90 leading-relaxed max-w-lg">
							Portal karir resmi IPB University. Temukan peluang magang, lowongan pekerjaan, dan kembangkan potensi profesional Anda bersama LARAS.
						</p>
					</div>
				</div>
			</div>

			{/* Right Side: Login Form (Larger Sizing Maintained) */}
			<div className="flex items-center justify-center bg-white p-8 md:p-20 overflow-y-auto">
				<div className="w-full max-w-md space-y-10">
					{isVerified && (
						<div className="p-4 bg-green-50 border border-green-100 rounded-2xl flex items-center gap-3 animate-in fade-in slide-in-from-top-4 duration-500">
							<div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white shrink-0">
								<PiCheckCircle size={24} weight="fill" />
							</div>
							<div>
								<h4 className="text-sm font-bold text-green-800">Email Terverifikasi!</h4>
								<p className="text-xs text-green-600 font-medium">Akun Anda sudah aktif, silakan masuk.</p>
							</div>
						</div>
					)}
					{isRegistered && (
						<div className="p-4 bg-sky-50 border border-sky-100 rounded-2xl flex items-center gap-3 animate-in fade-in slide-in-from-top-4 duration-500">
							<div className="w-10 h-10 bg-sky-500 rounded-full flex items-center justify-center text-white shrink-0">
								<PiCheckCircle size={24} weight="fill" />
							</div>
							<div>
								<h4 className="text-sm font-bold text-sky-800">Registrasi Berhasil!</h4>
								<p className="text-xs text-sky-600 font-medium">Silakan periksa kotak masuk email apps.ipb.ac.id Anda untuk verifikasi.</p>
							</div>
						</div>
					)}
					<div className="space-y-4">
						<div className="space-y-3">
							<h2 className="text-4xl font-extrabold text-[#002957] tracking-tight">
								Selamat Datang Kembali
							</h2>
							<p className="text-zinc-500 font-medium text-base">
								Silakan masuk menggunakan akun akademik Anda.
							</p>
						</div>
					</div>

					<form onSubmit={handleSubmit} className="space-y-6">
						<div className="space-y-5">
							{/* Email Input */}
							<div className="space-y-2">
								<label className="text-sm font-bold text-[#002957] ml-1 uppercase tracking-wider">Email atau Username</label>
								<div className="relative group">
									<PiEnvelopeSimple className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400 group-focus-within:text-sky-600 transition-colors" size={20} />
									<input
										type="text"
										required
										value={email}
										onChange={(e) => setEmail(e.target.value)}
										placeholder="username@apps.ipb.ac.id atau username"
										className="w-full pl-12 pr-4 py-3.5 bg-[#E8F1FF] border-none rounded-xl focus:ring-2 focus:ring-sky-500 outline-none transition-all font-medium text-sm text-zinc-800"
									/>
								</div>
							</div>

							{/* Password Input */}
							<div className="space-y-2">
								<div className="flex justify-between items-center px-1">
									<label className="text-sm font-bold text-[#002957] uppercase tracking-wider">Kata Sandi</label>
									<button 
										type="button"
										onClick={() => navigate("/forgot-password")}
										className="text-sm font-bold text-sky-600 hover:underline"
									>
										Lupa kata sandi?
									</button>
								</div>
								<div className="relative group">
									<PiLockKey className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400 group-focus-within:text-sky-600 transition-colors" size={20} />
									<input
										type={showPassword ? "text" : "password"}
										required
										value={password}
										onChange={(e) => setPassword(e.target.value)}
										placeholder="••••••••"
										className="w-full pl-12 pr-12 py-3.5 bg-[#E8F1FF] border-none rounded-xl focus:ring-2 focus:ring-sky-500 outline-none transition-all font-medium text-sm text-zinc-800"
									/>
									<button 
										type="button"
										onClick={() => setShowPassword(!showPassword)}
										className="absolute right-4 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-[#002957] transition-colors"
									>
										{showPassword ? <PiEyeSlash size={20} /> : <PiEye size={20} />}
									</button>
								</div>
							</div>
						</div>

						{loginError && (
							<div className="p-3 bg-red-50 border border-red-100 rounded-lg text-red-600 text-xs font-bold">
								{typeof loginError.response?.data?.detail === 'string' 
									? loginError.response.data.detail 
									: "Email atau kata sandi yang Anda masukkan salah."}
							</div>
						)}

						<button
							type="submit"
							disabled={isLoggingIn}
							className="w-full py-4 bg-[#002957] hover:bg-[#001f42] text-white rounded-xl shadow-lg shadow-sky-950/20 font-bold text-base transition-all flex items-center justify-center gap-2 active:scale-[0.98] disabled:opacity-70"
						>
							{isLoggingIn ? (
								<PiSpinnerGap size={24} className="animate-spin" />
							) : (
								<>
									<span>Masuk ke Dashboard</span>
									<PiArrowRight size={20} weight="bold" />
								</>
							)}
						</button>
					</form>

					<div className="relative py-2">
						<div className="absolute inset-0 flex items-center">
							<div className="w-full border-t border-zinc-100"></div>
						</div>
						<div className="relative flex justify-center text-[10px] uppercase font-bold tracking-[0.2em] text-zinc-300">
							<span className="bg-white px-4">ATAU</span>
						</div>
					</div>

					<div className="p-8 bg-[#F0F5FF] rounded-xl flex flex-col items-center gap-2">
						<p className="text-sm text-zinc-500 font-medium">Belum memiliki akun LARAS?</p>
						<button
							onClick={() => navigate("/registration")}
							className="text-[#0052CC] font-bold text-lg hover:underline"
						>
							Daftar Sekarang
						</button>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Login;
