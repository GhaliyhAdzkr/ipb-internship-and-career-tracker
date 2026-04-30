import { useNavigate } from "react-router-dom";

function Registration() {
	const navigate = useNavigate();
	return (
		<>
			<div class="grid min-h-screen bg-white grid-cols-1 md:grid-cols-12">
				<div class="flex items-center justify-center col-span-1 md:col-span-5 bg-white p-6 md:p-12">
					<div class="w-full max-w-md">
						<div className="w-full font-jakarta max-w-96 inline-flex flex-col justify-start items-start gap-8">
							<div className="self-stretch flex flex-col justify-start items-start gap-2">
								<div className="self-stretch flex flex-col justify-start items-start">
									<div className="self-stretch justify-center text-sky-950 text-3xl font-extrabold font-['Plus_Jakarta_Sans'] leading-9">
										Daftar LARAS
									</div>
								</div>
								<div className="self-stretch flex flex-col justify-start items-start">
									<div className="self-stretch font-jakarta justify-center text-zinc-700 text-base font-normal  leading-6">
										Mulai langkah awal karis profesional
										Anda bersama IPB University.
									</div>
								</div>
							</div>
							<div className="self-stretch pt-2 flex flex-col justify-start items-start gap-6">
								<div className="self-stretch flex flex-col justify-start items-start gap-2">
									<div className="self-stretch flex flex-col justify-start items-start">
										<div className="self-stretch justify-center text-slate-900 text-sm font-semibold  leading-5">
											Nama Lengkap
										</div>
									</div>
									<div className="self-stretch relative flex flex-col justify-start items-start">
										<input
											type="email"
											placeholder="Contoh: Budiono Siregar"
											id="Email"
											class="px-5 py-3.5 mt-0.5 bg-blue-100 text-zinc-800 w-full rounded border-gray-300 placeholder:text-zinc-500 sm:text-sm"
										></input>
									</div>
								</div>
								<div className="self-stretch flex flex-col justify-start items-start gap-2">
									<div className="self-stretch flex flex-col justify-start items-start">
										<div className="self-stretch justify-center text-slate-900 text-sm font-semibold  leading-5">
											NIM (Nomor Induk Mahasiswa)
										</div>
									</div>
									<div className="self-stretch relative flex flex-col justify-start items-start">
										<input
											type="text"
											placeholder="G64012310XXX"
											id="nim"
											class="px-5 py-3.5 mt-0.5 bg-blue-100 text-zinc-800 w-full rounded border-gray-300 placeholder:text-zinc-500 sm:text-sm"
										></input>
									</div>
								</div>
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
								<div className="self-stretch flex flex-col justify-start items-start gap-2">
									<div className="self-stretch flex flex-col justify-start items-start">
										<div className="self-stretch justify-center text-slate-900 text-sm font-semibold  leading-5">
											Kata Sandi
										</div>
									</div>
									<div className="self-stretch relative flex flex-col justify-start items-start">
										<input
											type="password"
											placeholder="minimal 8 karakter"
											id="password"
											class="px-5 py-3.5 mt-0.5 bg-blue-100 text-zinc-800 w-full rounded border-gray-300 placeholder:text-zinc-500 sm:text-sm"
										></input>
									</div>
								</div>
								<label
									for="Option2"
									class="inline-flex items-center gap-3"
								>
									<input
										type="checkbox"
										class="size-4 rounded border-gray-300 shadow-sm"
										id="agreement"
									/>

									<span class="font-medium text-sm text-gray-700">
										{" "}
										Saya menyetujui{" "}
										<strong className="underline">
											{" "}
											Syarat &amp; Ketentuan{" "}
										</strong>
										dan{" "}
										<strong className="underline">
											Kebijakan Privasi{" "}
										</strong>
										Laras{" "}
									</span>
								</label>
								<div className="self-stretch pt-4 flex flex-col justify-start items-start">
									<button
										onClick={() => navigate("/home")}
										className="self-stretch py-4 bg-sky-950 hover:bg-sky-900 rounded-lg shadow-[0px_8px_24px_0px_rgba(0,41,87,0.12)] inline-flex justify-center items-center gap-2"
									>
										<div className="text-center justify-center text-white text-base font-bold font-['Plus_Jakarta_Sans'] leading-6">
											Daftar
										</div>
									</button>
								</div>
							</div>
							<div className="text-sky-950 text-sm cursor-default">
								Sudah punya akun?{" "}
								<strong onClick={() => navigate("/")} className="hover:text-sky-800">
									Masuk di sini
								</strong>
							</div>
						</div>
					</div>
				</div>
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
			</div>
		</>
	);
}

export default Registration;
