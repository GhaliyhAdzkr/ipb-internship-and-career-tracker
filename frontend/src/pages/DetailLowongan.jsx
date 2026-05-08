// COMPONENTS
import Sidebar from "../components/SideNav";
import Navbar from "../components/NavBar";
import data from "../data/items.json";
import TheFooter from "../components/TheFooter";
import {
	PiGraduationCap,
	PiCodeSimpleBold,
	PiCalendarBlank,
	PiMagnifyingGlassBold,
	PiMapPinLine,
	PiClock,
	PiCalendarDots,
	PiCaretCircleRightFill,
	PiBookmarkSimple,
} from "react-icons/pi";

import { useParams } from "react-router-dom";

function DetailLowongan() {
	return (
		<>
			<div className="flex-1 mx-5 flex font-jakarta text-black gap-5">
				<div className="flex flex-col gap-5">
					{/* Head Card */}
					<div className="flex-1 text-sm self-stretch  py-10 px-10 font-jakarta bg-sky-950 rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex gap-4">
						<div className="size-15 bg-slate-100 flex justify-center items-center rounded">
							<div className="size-12 bg-slate-500 rounded"></div>
						</div>
						<div className="text-white">
							<div className="text-3xl font-bold">
								Data Analyst Intern
							</div>
							<div className="text-xl">
								PT Teknologi adalah pokoknya
							</div>
						</div>
					</div>
					{/* Detail */}
					<div className="flex-1 text-sm self-stretch  p-10 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
						<div className="flex items-center gap-3 font-bold">
							<div className="bg-sky-950 p-1 rounded h-7"></div>
							<div className="text-lg text-sky-950">
								Tentang Perusahaan
							</div>
						</div>
						<div className="text-justify text-slate-700">
							PT Teknologi Nusantara adalah pionir dalam
							transformasi digital berskala nasional. Kami
							berfokus pada pengembangan ekosistem big data dan
							solusi kecerdasan buatan untuk membantu sektor
							industri di Indonesia tumbuh lebih efisien. Sebagai
							perusahaan yang didorong oleh data, kami menghargai
							ketelitian, inovasi, dan semangat kolaborasi yang
							tinggi.
						</div>
						<div className="flex items-center gap-3 font-bold">
							<div className="bg-sky-950 p-1 rounded h-7"></div>
							<div className="text-lg text-sky-950">
								Deskripsi Pekerjaan
							</div>
						</div>
						<div className="text-justify text-slate-700">
							Melakukan pembersihan data (data cleaning) dan
							validasi set data dari berbagai sumber internal.
							Melakukan pembersihan data (data cleaning) dan
							validasi set data dari berbagai sumber
							internal.Membantu tim analis senior dalam menyusun
							laporan tren pasar bulanan.Menganalisis anomali data
							untuk memastikan integritas informasi yang dikelola
							perusahaan.Membangun dashboard visualisasi data
							menggunakan alat bantu seperti Tableau atau PowerBI.
						</div>
						<div className="flex items-center gap-3 font-bold">
							<div className="bg-sky-950 p-1 rounded h-7"></div>
							<div className="text-lg text-sky-950">
								Kualifikasi & Persyaratan
							</div>
						</div>
						<div className="grid grid-cols-2 gap-5">
							<div className="flex-1 text-sm self-stretch px-5  font-jakarta  rounded-xl flex gap-4">
								<div className="flex gap-3">
									<PiGraduationCap className="size-8" />
									<div>
										<div className="font-bold text-sky-950">
											Pendidikan
										</div>
										<div className="text-slate-700">
											Mahasiswa tingkat akhir (S1) rumpun
											STEM/Ekonomi
										</div>
									</div>
								</div>
							</div>
							<div className="flex-1 text-sm self-stretch px-5  font-jakarta  rounded-xl flex gap-4">
								<div className="flex gap-3">
									<PiCodeSimpleBold className="size-6" />
									<div>
										<div className="font-bold text-sky-950">
											Techincal Skills
										</div>
										<div className="text-slate-700">
											Menguasai dasar Python dan SQL
										</div>
									</div>
								</div>
							</div>
							<div className="flex-1 text-sm self-stretch px-5  font-jakarta  rounded-xl flex gap-4">
								<div className="flex gap-3">
									<PiMagnifyingGlassBold className="size-8" />
									<div>
										<div className="font-bold text-sky-950">
											Karakter
										</div>
										<div className="text-slate-700">
											Teliti, analitis, dan memiliki
											kemauan belajar yang kuat.
										</div>
									</div>
								</div>
							</div>
							<div className="flex-1 text-sm self-stretch px-5  font-jakarta  rounded-xl flex gap-4">
								<div className="flex gap-3">
									<PiCalendarBlank className="size-8" />
									<div>
										<div className="font-bold text-sky-950">
											Komitmen
										</div>
										<div className="text-slate-700">
											Bersedia magang full-time selama
											minimal 6-bulan
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div>
					<div className="flex-1 flex text-sm self-stretch w-70 p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex-col gap-4">
						<div className="text-xl font-bold text-sky-950">
							Informasi Lowongan
						</div>
						<div className="flex gap-2 items-center">
							<PiMapPinLine className="size-10 p-2 bg-indigo-100 text-sky-950 rounded-full" />
							<div>
								<div className="font-bold text-sm text-slate-700">
									Lokasi
								</div>
								<div className="font-bold text-base text-sky-950">
									Jakarta Selatan
								</div>
							</div>
						</div>
						<div className="flex gap-2 items-center">
							<PiClock className="size-10 p-2 bg-indigo-100 text-sky-950 rounded-full" />
							<div>
								<div className="font-bold text-sm text-slate-700">
									TIpe Kerja
								</div>
								<div className="font-bold text-base text-sky-950">
									Full Time
								</div>
							</div>
						</div>
						<div className="flex gap-2 items-center">
							<PiCalendarDots className="size-10 p-2 bg-indigo-100 text-sky-950 rounded-full" />
							<div>
								<div className="font-bold text-sm text-slate-700">
									Durasi
								</div>
								<div className="font-bold text-base text-sky-950">
									6 Bulan
								</div>
							</div>
						</div>
						<div className="flex flex-col gap-2">
							<button className="flex gap-2 w-full p-3 bg-sky-950 hover:bg-sky-900 text-white rounded justify-center items-center">
								<div className="text-base">Lamar Sekarang</div>
								<PiCaretCircleRightFill className="size-5 text-white" />
							</button>
							<button className="flex gap-2 w-full p-3 hover:bg-slate-100 text-sky-950 hover:text-sky-900 border-2 border-gray-300 hover:border-sky-900 rounded justify-center items-center">
								<PiBookmarkSimple className="size-5" />
								<div className="text-base">Simpan Lowongan</div>
							</button>
						</div>
					</div>
				</div>
			</div>
		</>
	);
}

export default DetailLowongan;
