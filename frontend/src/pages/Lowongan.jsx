import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { useMediaQuery } from "react-responsive";
import { vacancyService } from "../services/vacancyService";
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
	const navigate = useNavigate();
	const [query, setQuery] = useState("");
	const [location, setLocation] = useState("");
	const [type, setType] = useState("");
	const [paymentType, setPaymentType] = useState("");

	const [currentPage, setCurrentPage] = useState(1);
	const isXl = useMediaQuery({ query: "(min-width: 1280px)" });
	const itemsPerPage = isXl ? 9 : 6;

	useEffect(() => {
		setCurrentPage(1);
	}, [query, location, type, paymentType]);

	const vacanciesQuery = useQuery({
		queryKey: ["vacancies", currentPage, itemsPerPage, query, location, type, paymentType],
		queryFn: () => vacancyService.getVacancies({
			page: currentPage,
			perPage: itemsPerPage,
			query: query.trim() || undefined,
			location: location.trim() || undefined,
			type: type || undefined,
			paymentType: paymentType || undefined,
		}),
	});

	const currentCards = vacanciesQuery.data?.items || [];
	const totalPages = vacanciesQuery.data?.total_pages || 1;
	const totalItems = vacanciesQuery.data?.total || 0;

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

	const displayType = (value) => {
		switch (value) {
			case "INTERNSHIP_GENERAL":
				return "Magang Umum";
			case "MBKM_INTERNSHIP":
				return "MBKM Magang";
			case "MBKM_STUDY_INDEPENDENT":
				return "MBKM Studi Independen";
			case "FULL_TIME":
				return "Full Time";
			default:
				return value || "-";
		}
	};

	const displayPayment = (value) => {
		switch (value) {
			case "PAID":
				return "Paid";
			case "UNPAID":
				return "Unpaid";
			case "ALLOWANCE_ONLY":
				return "Allowance";
			default:
				return value || "-";
		}
	};

	const handleCardClick = (vacancyId) => {
		navigate(`/detail/${vacancyId}`);
	};

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
							value={query}
							onChange={(e) => setQuery(e.target.value)}
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
							value={location}
							onChange={(e) => setLocation(e.target.value)}
							className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none"
						/>
					</div>
				</div>
				<div className="w-full md:w-50 flex flex-col gap-1.5">
					<label className="text-xs font-bold text-black uppercase">Tipe</label>
					<select
						value={type}
						onChange={(e) => setType(e.target.value)}
						className="w-full py-2.5 px-3 bg-zinc-50 border border-zinc-200 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none"
					>
						<option value="">Semua Tipe</option>
						<option value="INTERNSHIP_GENERAL">Magang Umum</option>
						<option value="MBKM_INTERNSHIP">MBKM Magang</option>
						<option value="MBKM_STUDY_INDEPENDENT">MBKM Studi Independen</option>
						<option value="FULL_TIME">Full Time</option>
					</select>
				</div>
				<div className="w-full md:w-50 flex flex-col gap-1.5">
					<label className="text-xs font-bold text-black uppercase">Kompensasi</label>
					<select
						value={paymentType}
						onChange={(e) => setPaymentType(e.target.value)}
						className="w-full py-2.5 px-3 bg-zinc-50 border border-zinc-200 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none"
					>
						<option value="">Semua Kompensasi</option>
						<option value="PAID">Paid</option>
						<option value="UNPAID">Unpaid</option>
						<option value="ALLOWANCE_ONLY">Allowance</option>
					</select>
				</div>
				<button type="button" onClick={() => setCurrentPage(1)} className="bg-sky-950 text-white p-2.5 rounded hover:bg-sky-900 transition-colors">
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
					<div className="mb-4 flex items-center justify-between text-sm text-zinc-500">
						<span>{vacanciesQuery.isLoading ? "Memuat lowongan..." : `${totalItems} lowongan ditemukan`}</span>
						<span className="font-medium">Halaman {currentPage} dari {totalPages}</span>
					</div>

					{vacanciesQuery.isError && (
						<div className="mb-6 p-4 rounded-xl border border-red-100 bg-red-50 text-red-700 text-sm font-medium">
							Gagal memuat lowongan dari backend.
						</div>
					)}

					<div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
						{currentCards.map((item) => (
							<div
								key={item.id}
								onClick={() => handleCardClick(item.id)}
								className="p-6 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4 hover:-translate-y-1 transition-transform cursor-pointer"
							>
								<div className="flex justify-between items-start">
									<div className="bg-sky-200 px-2 py-1 rounded text-[10px] text-sky-800 font-bold uppercase">
										{item.is_active ? "AKTIF" : "NONAKTIF"}
									</div>
									<PiLeaf size={20} className="text-zinc-400" />
								</div>
								<div>
									<h4 className="text-base font-bold text-black">{item.title}</h4>
									<p className="text-sm text-zinc-500">{item.company?.name || "Perusahaan belum tercantum"}</p>
								</div>
								<div className="text-sm text-zinc-600 line-clamp-2">{item.location || "Lokasi belum tercantum"}</div>
								<div className="flex gap-2 mt-2">
									<span className="px-2 py-0.5 bg-zinc-100 text-[10px] text-zinc-600 font-bold rounded uppercase tracking-wider">{displayType(item.type)}</span>
									<span className="px-2 py-0.5 bg-zinc-100 text-[10px] text-zinc-600 font-bold rounded uppercase tracking-wider">{displayPayment(item.payment_type)}</span>
								</div>
								<div className="text-xs text-zinc-400 font-medium">
									{item.skills?.length || 0} skill requirement
								</div>
							</div>
						))}
						{!vacanciesQuery.isLoading && currentCards.length === 0 && (
							<div className="col-span-full p-8 rounded-xl border border-dashed border-zinc-200 text-center text-zinc-500 bg-white">
								Tidak ada lowongan yang cocok dengan filter saat ini.
							</div>
						)}
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
