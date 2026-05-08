import React from "react";
import { PiLeaf } from "react-icons/pi";

function Lamaran() {
	return (
		<div className="font-jakarta">
			{/* Banner */}
			<div className="mb-5 bg-sky-950 py-7 px-10 rounded-xl text-white flex justify-between items-center shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)]">
				<div className="flex flex-col gap-2">
					<div className="text-3xl font-bold">Lacak Lamaranmu</div>
					<div className="text-justify text-sm max-w-xl">
						Pantau status lamaran magang dan karir profesional Anda
						secara real-time.
					</div>
				</div>
			</div>

			<div className="grid grid-cols-1 md:grid-cols-3 gap-5">
				{/* Dikirim */}
				<div className="p-5 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4 transition-transform cursor-pointer">
					<div className="font-bold text-black px-1">Dikirim</div>
					{[1, 2].map((i) => (
						<div
							key={i}
							className="p-5 bg-white rounded-xl border border-gray-300 flex flex-col gap-4 hover:-translate-y-0.5 transition-transform cursor-pointer"
						>
							<div className="flex justify-between items-start">
								<div className="bg-sky-200 px-2 py-1 rounded text-[10px] text-sky-800 font-bold uppercase">
									DIKURASI CDA
								</div>
								<PiLeaf size={20} className="text-zinc-400" />
							</div>
							<div>
								<h4 className="text-base font-bold text-black">
									Software Engineer
								</h4>
								<p className="text-sm text-zinc-500">
									Shopee Indonesia
								</p>
							</div>
							<div className="flex gap-2 mt-2">
								<span className="px-2 py-0.5 bg-zinc-100 text-[10px] text-zinc-600 font-bold rounded uppercase tracking-wider">
									Remote
								</span>
								<span className="px-2 py-0.5 bg-zinc-100 text-[10px] text-zinc-600 font-bold rounded uppercase tracking-wider">
									Paid
								</span>
							</div>
						</div>
					))}
				</div>

				{/* Seleksi */}
				<div className="p-5 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4 transition-transform cursor-pointer">
					<div className="font-bold text-black px-1">
						Proses Seleksi
					</div>
					{[1, 2].map((i) => (
						<div
							key={i}
							className="p-5 bg-white rounded-xl border border-gray-300 flex flex-col gap-4 hover:-translate-y-0.5 transition-transform cursor-pointer"
						>
							<div className="flex justify-between items-start">
								<div className="bg-sky-200 px-2 py-1 rounded text-[10px] text-sky-800 font-bold uppercase">
									DIKURASI CDA
								</div>
								<PiLeaf size={20} className="text-zinc-400" />
							</div>
							<div>
								<h4 className="text-base font-bold text-black">
									Software Engineer
								</h4>
								<p className="text-sm text-zinc-500">
									Shopee Indonesia
								</p>
							</div>
							<div className="flex gap-2 mt-2">
								<span className="px-2 py-0.5 bg-zinc-100 text-[10px] text-zinc-600 font-bold rounded uppercase tracking-wider">
									Remote
								</span>
								<span className="px-2 py-0.5 bg-zinc-100 text-[10px] text-zinc-600 font-bold rounded uppercase tracking-wider">
									Paid
								</span>
							</div>
						</div>
					))}
				</div>

				{/* Selesai */}
				<div className="p-5 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4 transition-transform cursor-pointer">
					<div className="font-bold text-black px-1">Selesai</div>
					<div className="p-5 bg-white rounded-xl border border-gray-300 flex flex-col gap-4 hover:-translate-y-0.5 transition-transform cursor-pointer">
						<div className="flex justify-between items-start">
								<div className="bg-sky-200 px-2 py-1 rounded text-[10px] text-sky-800 font-bold uppercase">
									DIKURASI CDA
								</div>
								<PiLeaf size={20} className="text-zinc-400" />
							</div>
							<div>
								<h4 className="text-base font-bold text-black">
									Software Engineer
								</h4>
								<p className="text-sm text-zinc-500">
									Shopee Indonesia
								</p>
							</div>
							<div className="flex gap-2 mt-2">
								<span className="px-2 py-0.5 bg-zinc-100 text-[10px] text-zinc-600 font-bold rounded uppercase tracking-wider">
									Remote
								</span>
								<span className="px-2 py-0.5 bg-zinc-100 text-[10px] text-zinc-600 font-bold rounded uppercase tracking-wider">
									Paid
								</span>
							</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Lamaran;
