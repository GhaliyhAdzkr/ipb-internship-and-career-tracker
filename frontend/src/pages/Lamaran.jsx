import React from "react";
import { PiLeaf } from "react-icons/pi";

function Lamaran() {
	return (
		<div className="font-jakarta">
			{/* Banner */}
			<div className="mb-5 bg-sky-950 p-10 rounded-xl text-white flex justify-between items-center shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)]">
				<div className="flex flex-col gap-2">
					<div className="text-3xl font-bold">Lacak Lamaranmu</div>
					<div className="text-justify max-w-xl">
						Pantau status lamaran magang dan karir profesional Anda secara real-time.
					</div>
				</div>
			</div>

			<div className="grid grid-cols-1 md:grid-cols-3 gap-5">
				{/* Dikirim */}
				<div className="bg-indigo-50 p-4 rounded-xl flex flex-col gap-4 min-h-[600px]">
					<div className="font-bold text-black px-1">Dikirim</div>
					{[1, 2].map((i) => (
						<div key={i} className="p-5 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4 hover:translate-y-[-2px] transition-transform cursor-pointer">
							<div className="flex gap-2 justify-between items-center">
								<PiLeaf className="size-7 text-zinc-700 bg-indigo-50 rounded p-1" />
								<div className="bg-sky-200 px-2 py-0.5 rounded text-[10px] text-sky-800 font-bold uppercase">
									DIKURASI CDA
								</div>
							</div>
							<div className="flex flex-col gap-1">
								<div className="text-black text-sm font-bold">
									Software Engineering
								</div>
								<div className="text-zinc-500 text-xs">
									Shopee Indonesia
								</div>
							</div>
							<div className="flex gap-2 mt-2">
								<div className="bg-zinc-100 px-2 py-0.5 rounded text-[10px] text-zinc-600 font-bold uppercase">
									Remote
								</div>
								<div className="bg-zinc-100 px-2 py-0.5 rounded text-[10px] text-zinc-600 font-bold uppercase">
									Paid
								</div>
							</div>
						</div>
					))}
				</div>

				{/* Seleksi */}
				<div className="bg-indigo-50 p-4 rounded-xl flex flex-col gap-4 min-h-[600px]">
					<div className="font-bold text-black px-1">Proses Seleksi</div>
					{[1, 2].map((i) => (
						<div key={i} className="p-5 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4 hover:translate-y-[-2px] transition-transform cursor-pointer">
							<div className="flex gap-2 justify-between items-center">
								<PiLeaf className="size-7 text-zinc-700 bg-indigo-50 rounded p-1" />
								<div className="bg-sky-200 px-2 py-0.5 rounded text-[10px] text-sky-800 font-bold uppercase">
									DIKURASI CDA
								</div>
							</div>
							<div className="flex flex-col gap-1">
								<div className="text-black text-sm font-bold">
									UI / UX Designer
								</div>
								<div className="text-zinc-500 text-xs">
									Gojek Tokopedia
								</div>
							</div>
							<div className="flex gap-2 mt-2">
								<div className="bg-zinc-100 px-2 py-0.5 rounded text-[10px] text-zinc-600 font-bold uppercase">
									Remote
								</div>
								<div className="bg-zinc-100 px-2 py-0.5 rounded text-[10px] text-zinc-600 font-bold uppercase">
									Paid
								</div>
							</div>
						</div>
					))}
				</div>

				{/* Selesai */}
				<div className="bg-indigo-50 p-4 rounded-xl flex flex-col gap-4 min-h-[600px]">
					<div className="font-bold text-black px-1">Selesai</div>
					<div className="p-5 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4 hover:translate-y-[-2px] transition-transform cursor-pointer">
						<div className="flex gap-2 justify-between items-center">
							<PiLeaf className="size-7 text-zinc-700 bg-indigo-50 rounded p-1" />
							<div className="bg-sky-200 px-2 py-0.5 rounded text-[10px] text-sky-800 font-bold uppercase">
								DIKURASI CDA
							</div>
						</div>
						<div className="flex flex-col gap-1">
							<div className="text-black text-sm font-bold">
								Data Analyst
							</div>
							<div className="text-zinc-500 text-xs">
								Traveloka
							</div>
						</div>
						<div className="flex gap-2 mt-2">
							<div className="bg-zinc-100 px-2 py-0.5 rounded text-[10px] text-zinc-600 font-bold uppercase">
								Remote
							</div>
							<div className="bg-zinc-100 px-2 py-0.5 rounded text-[10px] text-zinc-600 font-bold uppercase">
								Paid
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Lamaran;
