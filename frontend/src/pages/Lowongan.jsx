import data from "../data/items.json";
import { useState } from "react";
import { useMediaQuery } from "react-responsive";
import {
  PiBookmarkSimple,
  PiLeaf,
  PiBriefcase,
  PiMapPin,
  PiShapes,
  PiCaretLeft,
  PiCaretRight,
  PiMagnifyingGlass
} from "react-icons/pi";

function Lowongan() {
	// Dropdown
	const [isOpenDropdown, setIsOpenDropdown] = useState(false);
	const [sortActive, setSortActive] = useState(0);
	const sortOption = ["Terbaru", "Terlama"];

	const [currentPage, setCurrentPage] = useState(1);
	const isXl = useMediaQuery({ query: "(min-width: 1280px)" });
	const itemsPerPage = isXl ? 9 : 6;

	const lastIndex = currentPage * itemsPerPage;
	const firstIndex = lastIndex - itemsPerPage;
	const currentCards = data.slice(firstIndex, lastIndex);
	const totalPages = Math.ceil(data.length / itemsPerPage);

	const getPaginationRange = (current, total) => {
		const range = [];
		const delta = 2;
		for (let i = 1; i <= total; i++) {
			if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
				range.push(i);
			} else if (range[range.length - 1] !== "...") {
				range.push("...");
			}
		}
		return range;
	};
	const paginationRange = getPaginationRange(currentPage, totalPages);

	return (
		<div className="font-jakarta">
			{/* Banner */}
			<div className="mb-5 bg-sky-950 py-7 px-10 rounded-xl text-white flex justify-between items-center shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)]">
				<div className="flex flex-col gap-2">
					<div className="text-3xl font-bold">Eksplorasi Karirmu</div>
					<div className="text-justify  opacity-90">
						Temukan peluang magang dan karir profesional yang telah dikurasi khusus untuk mahasiswa dan alumni IPB University.
					</div>
				</div>
			</div>

			{/* Search Section */}
			<div className="bg-white p-6 rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] mb-8 flex gap-4 items-end">
				<div className="flex-1 flex flex-col gap-1.5 w-60">
					<label className="text-xs font-bold text-black uppercase">Apa yang ingin kamu cari?</label>
					<div className="relative">
						<PiBriefcase className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" size={20} />
						<input
							type="text"
							placeholder="Posisi, Kata Kunci, atau Perusahaan"
							className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none"
						/>
					</div>
				</div>
				<div className="w-full md:w-50 flex flex-col gap-1.5">
					<label className="text-xs font-bold text-black uppercase">Lokasi</label>
					<div className="relative">
						<PiMapPin className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" size={20} />
						<input
							type="text"
							placeholder="Semua Lokasi"
							className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none"
						/>
					</div>
				</div>
				<div className="w-full md:w-50 flex flex-col gap-1.5">
					<label className="text-xs font-bold text-black uppercase">Tipe</label>
					<div className="relative">
						<PiShapes className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" size={20} />
						<input
							type="text"
							placeholder="Semua Tipe"
							className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none"
						/>
					</div>
				</div>
				<button className="bg-sky-950 text-white p-2.5 rounded hover:bg-sky-900 transition-colors">
					<PiMagnifyingGlass size={20} weight="bold" />
				</button>
			</div>

			<div className="flex flex-col lg:flex-row gap-8">
				{/* Sidebar Filters */}
				<aside className="w-full lg:w-72 flex flex-col gap-5">
					<div className="p-6 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)]">
						<h3 className="font-bold text-black border-b pb-3 mb-5">Filter Detail</h3>
						
						<div className="space-y-4">
							<p className="text-xs font-bold text-zinc-500 uppercase">Bidang Industri</p>
							{['Agrikultur', 'Teknologi Informasi', 'FMCG', 'Perbankan'].map((item) => (
								<label key={item} className="flex items-center gap-3 cursor-pointer group">
									<input type="checkbox" className="w-4 h-4 rounded border-zinc-300 text-sky-950 focus:ring-sky-500" />
									<span className="text-sm font-medium text-zinc-700 group-hover:text-black">{item}</span>
								</label>
							))}
						</div>

						<button className="w-full mt-8 py-2.5 bg-sky-950 text-white font-bold rounded hover:bg-sky-900 transition-colors">
							Terapkan Filter
						</button>
					</div>
				</aside>

				{/* Listings */}
				<div className="flex-1">
					<div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
						{currentCards.map((item, idx) => (
							<div key={idx} className="p-6 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4 hover:translate-y-[-4px] transition-transform">
								<div className="flex justify-between items-start">
									<div className="bg-sky-200 px-2 py-1 rounded text-[10px] text-sky-800 font-bold uppercase">
										DIKURASI CDA
									</div>
									<PiLeaf size={20} className="text-zinc-400" />
								</div>
								<div>
									<h4 className="text-base font-bold text-black">{item.name}</h4>
									<p className="text-sm text-zinc-500">Shopee Indonesia</p>
								</div>
								<div className="flex gap-2 mt-2">
									<span className="px-2 py-0.5 bg-zinc-100 text-[10px] text-zinc-600 font-bold rounded uppercase tracking-wider">Remote</span>
									<span className="px-2 py-0.5 bg-zinc-100 text-[10px] text-zinc-600 font-bold rounded uppercase tracking-wider">Paid</span>
								</div>
							</div>
						))}
					</div>

					{/* Pagination */}
					<div className="flex justify-center mt-12 gap-2">
						<button
							disabled={currentPage === 1}
							onClick={() => setCurrentPage((p) => p - 1)}
							className="w-10 h-10 flex items-center justify-center rounded border border-zinc-200 text-zinc-600 hover:bg-zinc-100 disabled:opacity-30"
						>
							<PiCaretLeft size={20} weight="bold" />
						</button>
						<div className="flex gap-1">
							{paginationRange.map((page, index) => (
								<button
									key={index}
									onClick={() => (page !== "..." ? setCurrentPage(page) : null)}
									className={`w-10 h-10 rounded font-bold transition-all ${
										currentPage === page
											? "bg-sky-950 text-white"
											: page === "..." ? "cursor-default text-zinc-400" : "hover:bg-zinc-100 text-zinc-600 border border-zinc-200"
									}`}
								>
									{page}
								</button>
							))}
						</div>
						<button
							disabled={currentPage === totalPages}
							onClick={() => setCurrentPage((p) => p + 1)}
							className="w-10 h-10 flex items-center justify-center rounded border border-zinc-200 text-zinc-600 hover:bg-zinc-100 disabled:opacity-30"
						>
							<PiCaretRight size={20} weight="bold" />
						</button>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Lowongan;
