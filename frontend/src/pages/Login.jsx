import { useNavigate } from "react-router-dom";

function Login() {
	const navigate = useNavigate();
	return (
		<>
			<div class="grid min-h-screen bg-white grid-cols-1 md:grid-cols-12">
				<div
					class="hidden md:flex md:col-span-7 bg-cover bg-center items-center justify-center  bg-slate-100"
					// style="background-image: url('src\pics\kabas.png')"
				>
					<img
						src="https://res.cloudinary.com/dhsdxi218/image/upload/v1777055801/samples/landscapes/nature-mountains.jpg"
						alt="Welcome"
						class="h-full w-auto object-cover"
					/>
				</div>

				<div class="flex items-center justify-center col-span-1 md:col-span-5 bg-white p-6 md:p-12">
					<div class="w-full max-w-md">
						<div className="w-full font-jakarta max-w-96 inline-flex flex-col justify-start items-start gap-8">
							<div className="self-stretch flex flex-col justify-start items-start gap-2">
								<div className="self-stretch flex flex-col justify-start items-start">
									<div className="self-stretch justify-center text-sky-950 text-3xl font-extrabold font-['Plus_Jakarta_Sans'] leading-9">
										Selamat Datang Kembali
									</div>
								</div>
								<div className="self-stretch flex flex-col justify-start items-start">
									<div className="self-stretch font-jakarta justify-center text-zinc-700 text-base font-normal  leading-6">
										Silakan masuk menggunakan akun akademik
										Anda.
									</div>
								</div>
							</div>
							<div className="self-stretch pt-2 flex flex-col justify-start items-start gap-6">
								<div className="self-stretch flex flex-col justify-start items-start gap-2">
									<div className="self-stretch flex flex-col justify-start items-start">
										<div className="self-stretch justify-center text-slate-900 text-sm font-semibold  leading-5">
											Email Akademik
										</div>
									</div>
									<div className="self-stretch relative flex flex-col justify-start items-start">
										<input
											type="email"
											placeholder="Email"
											id="Email"
											class="px-5 py-3.5 mt-0.5 bg-blue-100 text-zinc-800 w-full rounded border-gray-300 placeholder:text-zinc-500 sm:text-sm"
										></input>
									</div>
								</div>
								<div className="self-stretch flex flex-col justify-start items-start gap-2">
									<div className="self-stretch inline-flex justify-between items-center">
										<div className="inline-flex flex-col justify-start items-start">
											<div className="justify-center font text-slate-900 text-sm font-semibold  leading-5">
												Kata Sandi
											</div>
										</div>
										<div className="inline-flex flex-col justify-start items-start">
											<a onClick={() => navigate("/forgot-password")} className="cursor-default justify-center text-sky-700 text-sm font-medium  leading-5">
												Lupa kata sandi?
											</a>
										</div>
									</div>
									<div className="self-stretch relative flex flex-col justify-start items-start">
										<input
											type="password"
											placeholder="Password"
											id="Password"
											class="px-5 py-3.5 mt-0.5 bg-blue-100 text-zinc-800 w-full rounded border-gray-300 placeholder:text-zinc-500 sm:text-sm"
										></input>
									</div>
								</div>
								<div className="self-stretch pt-4 flex flex-col justify-start items-start">
									<button onClick={() => navigate("/home")} className="self-stretch py-4 bg-sky-950 hover:bg-sky-900 rounded-lg shadow-[0px_8px_24px_0px_rgba(0,41,87,0.12)] inline-flex justify-center items-center gap-2">
										<div  className="text-center justify-center text-white text-base font-bold font-['Plus_Jakarta_Sans'] leading-6">
											Masuk
										</div>
									</button>
								</div>
							</div>
							<div className="self-stretch pt-2 inline-flex justify-start items-center">
								<div className="flex-1 h-px border-t border-zinc-500" />
								<div className="px-4 inline-flex flex-col justify-start items-start">
									<div className="justify-center text-zinc-500 text-xs font-normal  uppercase leading-4 tracking-wide">
										ATAU
									</div>
								</div>
								<div className="flex-1 h-px border-t border-zinc-500" />
							</div>
							<div className="self-stretch p-6 bg-indigo-50 rounded-xl flex flex-col justify-start items-center gap-2">
								<div className="self-stretch flex flex-col justify-start items-center">
									<div className="text-center justify-center text-zinc-700 text-sm font-normal  leading-5">
										Belum memiliki akun LARAS?
									</div>
								</div>
								<div className="inline-flex justify-center items-start">
									<a onClick={() => navigate("/regist")} className="cursor-default text-center justify-center text-sky-950 hover:text-sky-800 text-base font-bold font-['Plus_Jakarta_Sans'] leading-6">
										Daftar sebagai Mahasiswa/Alumni
									</a>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</>
	);
}

export default Login;
