import React from "react";
import { useNavigate } from "react-router-dom";
import { PiEnvelopeSimple, PiArrowRight } from "react-icons/pi";

function ForgotPassword() {
	const navigate = useNavigate();

	return (
		<div className="h-screen w-full bg-gradient-to-br from-[#F8FAFF] via-[#F0F5FF] to-[#E8F1FF] flex flex-col items-center justify-center p-6 font-jakarta overflow-hidden relative">
			{/* Decorative glows */}
			<div className="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-blue-200/20 rounded-full blur-[120px]" />
			<div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-sky-200/20 rounded-full blur-[120px]" />

			<div className="relative z-10 w-full max-w-lg flex flex-col items-center">
				{/* Brand Header */}
				<div className="mb-10 text-center space-y-4">
					<img 
						src="/logo/laras.png" 
						alt="LARAS Logo" 
						className="h-16 w-auto mx-auto"
					/>
					<div className="space-y-1">
						<h1 className="text-[32px] font-extrabold text-[#002957] tracking-tight">LARAS IPB</h1>
						<p className="text-sm font-medium text-zinc-500">
							Direktorat Kemahasiswaan dan Pengembangan Karir
						</p>
					</div>
				</div>

				{/* Card */}
				<div className="w-full bg-white rounded-[2.5rem] shadow-[0_20px_50px_rgba(0,41,87,0.06)] border border-white/50 p-12 space-y-10">
					<div className="space-y-4">
						<h2 className="text-3xl font-extrabold text-[#002957]">Lupa Password?</h2>
						<p className="text-zinc-500 font-medium leading-relaxed">
							Masukkan email IPB Anda (@apps.ipb.ac.id). Kami akan mengirimkan tautan untuk mengatur ulang password Anda.
						</p>
					</div>

					<form className="space-y-8">
						<div className="space-y-2.5">
							<label className="text-sm font-bold text-[#002957] ml-1">Email IPB</label>
							<div className="relative group">
								<PiEnvelopeSimple className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400 group-focus-within:text-sky-600 transition-colors" size={22} />
								<input
									type="email"
									placeholder="NIM@apps.ipb.ac.id"
									className="w-full pl-12 pr-4 py-4.5 bg-[#E8F1FF] border-none rounded-xl focus:ring-2 focus:ring-sky-500 outline-none transition-all font-medium text-zinc-800"
								/>
							</div>
						</div>

						<button
							type="button"
							className="w-full py-4.5 bg-[#002957] hover:bg-[#001f42] text-white rounded-xl shadow-lg shadow-sky-950/20 font-bold text-base transition-all flex items-center justify-center gap-2 active:scale-[0.98]"
						>
							<span>Kirim Tautan Reset</span>
							<PiArrowRight size={20} weight="bold" />
						</button>
					</form>

					<div className="text-center pt-2">
						<button 
							onClick={() => navigate("/login")}
							className="text-[#002957] font-bold text-base hover:underline"
						>
							Kembali ke Halaman Masuk
						</button>
					</div>
				</div>

				{/* Footer Help */}
				<div className="mt-12 text-center">
					<p className="text-sm font-medium text-zinc-500">
						Butuh bantuan? <a href="#" className="text-sky-600 font-bold hover:underline">Hubungi Helpdesk CDA IPB</a>
					</p>
				</div>
			</div>
		</div>
	);
}

export default ForgotPassword;
