import React from "react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { PiBookmarkSimple } from "react-icons/pi";

function Dashboard() {
	const { user } = useAuth();

	return (
		<div className="font-jakarta">
			{/* Welcome */}
			<div className="mb-8 bg-sky-950 py-7 px-10 rounded-xl text-white flex justify-between items-center shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)]">
				<div className="w-full flex gap-2 justify-between items-center">
					<div className="text-3xl font-bold">Selamat Datang Kembali, Budi</div>
					<button className="text-center bg-white text-sm font-bold py-2 px-4 text-sky-950 rounded">
						Tulis Jurnal
					</button>
				</div>
			</div>

			{/* Cards Progress */}
			<div className="grid grid-cols-1 md:grid-cols-3 mb-5 gap-5">
				<div className="p-5 font-bold bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-1">
					<div className="text-black text-sm">Waktu Tersisa</div>
					<div className="text-black text-2xl">45 / 60 Hari</div>
					<div className="bg-zinc-300 h-1 rounded mt-1">
						<div className="bg-blue-400 h-1 w-3/4 rounded"></div>
					</div>
				</div>
				<div className="p-5 font-bold bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-1">
					<div className="text-black text-sm">Jurnal Terisi</div>
					<div className="text-black text-2xl">10 / 15</div>
					<div className="bg-zinc-300 h-1 rounded mt-1">
						<div className="bg-blue-400 h-1 w-2/3 rounded"></div>
					</div>
				</div>
				<div className="p-5 font-bold bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-1">
					<div className="text-black text-sm">Laporan Diunggah</div>
					<div className="text-black text-2xl">3 / 3</div>
					<div className="bg-zinc-300 h-1 rounded mt-1">
						<div className="bg-blue-400 h-1 w-full rounded"></div>
					</div>
				</div>
			</div>

			{/* Lamaran & Rekomendasi */}
			<div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
				{/* Lamaran */}
				<div className="lg:col-span-1">
					<div className="flex justify-between items-center py-3 font-bold">
						<div className="text-black">Lamaran Terakhir</div>
						<NavLink to="/lamaran" className="text-sm text-sky-950 hover:text-sky-800">
							Selengkapnya
						</NavLink>
					</div>
					<div className="p-5 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-8">
						<div className="flex justify-between gap-2">
							<div className="text-black text-sm">
								<div className="font-bold">Data Analysis Intern</div>
								<div className="text-zinc-500">PT GoTo - Gojek Tokopedia</div>
							</div>
							<div className="flex items-center text-xs">
								<div className="bg-red-200 py-1 text-center px-2 w-16 rounded text-red-800 font-bold">
									Ditolak
								</div>
							</div>
						</div>
						<div className="flex justify-between">
							<div className="text-black text-sm">
								<div className="font-bold">Software Engineer</div>
								<div className="text-zinc-500">Traveloka</div>
							</div>
							<div className="flex items-center text-xs">
								<div className="bg-green-200 py-1 px-2 text-center w-16 rounded text-green-800 font-bold">
									Diterima
								</div>
							</div>
						</div>
					</div>
				</div>

				{/* Rekomendasi Magang */}
				<div className="lg:col-span-2">
					<div className="flex justify-between items-center py-3 font-bold">
						<div className="text-black">Rekomendasi Magang</div>
						<NavLink to="/lowongan" className="text-sm text-sky-950 hover:text-sky-800">
							Selengkapnya
						</NavLink>
					</div>
					<div className="grid grid-cols-1 md:grid-cols-2 gap-5">
						{[1, 2].map((i) => (
							<div key={i} className="p-5 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
								<div className="flex gap-2 justify-between">
									<div className="bg-sky-200 px-2 py-1 rounded text-xs text-black font-bold">
										DIKURASI CDA
									</div>
									<PiBookmarkSimple size={20} className="text-zinc-700" weight="bold" />
								</div>
								<div className="flex flex-col gap-1">
									<div className="text-black text-base font-bold">
										UI / UX Designer Intern
									</div>
									<div className="text-black text-sm text-zinc-500">
										Shopee Indonesia
									</div>
								</div>
								<div className="flex gap-2">
									<div className="bg-zinc-200 px-2 py-0.5 rounded text-[10px] text-black font-bold">
										Remote
									</div>
									<div className="bg-zinc-200 px-2 py-0.5 rounded text-[10px] text-black font-bold">
										Paid
									</div>
								</div>
							</div>
						))}
					</div>
				</div>
			</div>
		</div>
	);
}

export default Dashboard;
