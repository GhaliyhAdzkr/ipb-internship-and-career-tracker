import { useNavigate } from "react-router-dom";

function ForgotPassword() {
	const navigate = useNavigate();
	return (
		<>
			<section class="text-gray-600 bg-white min-h-screen body-font flex">
				<div class="container mx-auto flex px-5 items-center justify-center flex-col">
					<div className=" font-jakarta max-w-120 inline-flex flex-col justify-start items-start gap-8">
						<div className="self-stretch flex flex-col justify-start items-start gap-2">
							<div className="self-stretch flex flex-col justify-start items-center">
								<div className="text-center justify-center text-sky-950 text-3xl font-extrabold leading-9">
									LARAS IPB
								</div>
							</div>
							<div className="self-stretch flex flex-col justify-start items-center">
								<div className="text-center justify-center text-zinc-700 text-sm font-normal  leading-5">
									Direktorat Kemahasiswaan dan Pengembangan
									Karir
								</div>
							</div>
						</div>
						<div className="self-stretch px-8 pt-8 pb-12 relative bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col justify-start items-start gap-6">
							<div className="self-stretch flex flex-col justify-start items-start gap-2">
								<div className="self-stretch flex flex-col justify-start items-start">
									<div className="self-stretch justify-center text-slate-900 text-xl font-bold  leading-8">
										Lupa Password?
									</div>
								</div>
								<div className="self-stretch flex flex-col justify-start items-start">
									<div className="self-stretch text-sm justify-center text-zinc-700  font-normal  leading-6">
										Masukkan email IPB Anda
										(@apps.ipb.ac.id). Kami akan mengirimkan
										tautan untuk mengatur ulang password
										Anda.
									</div>
								</div>
							</div>
							<div className="max-w-120 h-96 left-0 top-0 absolute rounded-xl outline outline-neutral-300/20" />
							<div className="self-stretch flex flex-col justify-start items-start gap-6">
								<div className="self-stretch flex flex-col justify-start items-start gap-2">
									<div className="self-stretch flex flex-col justify-start items-start">
										<div className="self-stretch justify-center text-slate-900 text-sm font-semibold  leading-5">
											Email Mahasiswa
										</div>
									</div>
									<div className="self-stretch relative flex flex-col justify-start items-start">
										<input
											type="email"
											placeholder="nama@apps.ipb.ac.id"
											id="email"
											class="px-5 py-3.5 mt-0.5 bg-blue-100 text-zinc-800 w-full rounded border-gray-300 placeholder:text-zinc-500 sm:text-sm"
										></input>
									</div>
								</div>
								<div className="self-stretch pt-2 flex flex-col justify-start items-start gap-4">
									<button className="self-stretch px-4 py-3 bg-sky-950 hover:bg-sky-900 rounded-lg inline-flex justify-center items-center gap-2">
										<div className="text-center justify-center text-white text-base font-semibold  leading-6">
											Kirim Tautan Reset
										</div>
									</button>
									<div className="self-stretch px-4 py-3 rounded-lg inline-flex justify-center items-center">
										<div
											onClick={() => navigate("/")}
											className="cursor-default text-center justify-center text-sky-950 hover:text-sky-800 text-base font-semibold  leading-6"
										>
											Kembali ke Halaman Masuk
										</div>
									</div>
								</div>
							</div>
						</div>
						<div className="self-stretch flex flex-col justify-start items-center">
							<div className="text-center justify-center">
								<span class="text-zinc-700 text-sm font-normal  leading-5">
									Butuh bantuan?{" "}
								</span>
								<span class="text-sky-700 text-sm font-semibold  underline">
									Hubungi Helpdesk CDA IPB
								</span>
							</div>
						</div>
					</div>
				</div>
			</section>
		</>
	);
}

export default ForgotPassword;
