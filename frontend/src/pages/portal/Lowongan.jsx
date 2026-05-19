import { useEffect, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useMediaQuery } from "react-responsive";
import { format } from "date-fns";
import { useQueryClient } from "@tanstack/react-query";
import { useVacancies, useIndustries, useWishlist, useWishlistMutations } from "../../hooks/useVacancies";
import { vacancyService } from "../../services/vacancyService";
import {
  PiBookmarkSimple,
  PiBriefcase,
  PiMapPin,
  PiCaretLeft,
  PiCaretRight,
  PiMagnifyingGlass,
  PiXCircle,
  PiCaretDown,
  PiCalendar
} from "react-icons/pi";

import { useInView } from "react-intersection-observer";
import { resolveBackendAssetUrl } from "../../utils/assetUrl";

function Lowongan() {
	const navigate = useNavigate();
	const queryClient = useQueryClient();
	const [searchParams, setSearchParams] = useSearchParams();
	const token = localStorage.getItem("token");

	// State untuk tombol tampilkan lebih banyak industri
	const [showAllIndustries, setShowAllIndustries] = useState(false);

	// Ref untuk input tidak terkontrol guna menghindari render ulang saat mengetik
	const queryRef = useRef(null);
	const locationRef = useRef(null);

	// State turunan dari URL sebagai acuan utama data
	const query = searchParams.get("query") || "";
	const location = searchParams.get("location") || "";
	const type = searchParams.get("type") || "";
	const paymentType = searchParams.get("payment_type") || "";
	const industry = searchParams.get("industry") || "";
	const currentPage = Number(searchParams.get("page")) || 1;

	const isXl = useMediaQuery({ query: "(min-width: 1280px)" });
	const itemsPerPage = isXl ? 9 : 6;

	const vacanciesQuery = useVacancies({
		page: currentPage,
		perPage: itemsPerPage,
		query: query.trim() || undefined,
		location: location.trim() || undefined,
		type: type || undefined,
		paymentType: paymentType || undefined,
		industry: industry || undefined,
	});

	const industriesQuery = useIndustries();

	const { data: wishlistData } = useWishlist(!!token);

	const wishlistMap = new Map(wishlistData?.items?.map(w => [w.vacancy.id, w.id]) || []);

	const { toggleWishlist: toggleWishlistMutate, isToggling } = useWishlistMutations(wishlistMap);

	const updateFilters = (newFilters) => {
		const nextParams = new URLSearchParams(searchParams);
		Object.entries(newFilters).forEach(([key, value]) => {
			if (value) nextParams.set(key, value);
			else nextParams.delete(key);
		});

		// Hanya atur ulang ke halaman 1 jika tidak sedang memuat halaman spesifik
		if (!("page" in newFilters)) {
			nextParams.set("page", "1");
		}
		
		setSearchParams(nextParams);
	};

	const handleSearch = () => {
		updateFilters({
			query: queryRef.current?.value,
			location: locationRef.current?.value,
		});
	};

	const handleReset = () => {
		if (queryRef.current) queryRef.current.value = "";
		if (locationRef.current) locationRef.current.value = "";
		setSearchParams({});
	};

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
			case "INTERNSHIP_GENERAL": return "Magang Umum";
			case "MBKM_INTERNSHIP": return "MBKM Magang";
			case "MBKM_STUDY_INDEPENDENT": return "MBKM Studi Independen";
			case "FULL_TIME": return "Full Time";
			default: return value || "-";
		}
	};

	const displayPayment = (value) => {
		switch (value) {
			case "PAID": return "Paid";
			case "UNPAID": return "Unpaid";
			case "ALLOWANCE_ONLY": return "Allowance";
			default: return value || "-";
		}
	};

	const handleCardClick = (vacancyId) => {
		navigate(`/detail/${vacancyId}`);
	};

	// Komponen prefetching cerdas
	const VacancyCard = ({ item }) => {
		const { ref, inView } = useInView({
			triggerOnce: true,
			rootMargin: "200px 0px", // Prefetch saat berada 200px sebelum area pandang
		});

		useEffect(() => {
			if (inView) {
				queryClient.prefetchQuery({
					queryKey: ["vacancy", item.id],
					queryFn: () => vacancyService.getVacancy(item.id),
					staleTime: 5 * 60 * 1000,
				});
			}
		}, [inView, item.id]);

		const isWishlisted = wishlistMap.has(item.id);

		return (
			<div
				ref={ref}
				className="h-full p-6 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] border border-slate-50 flex flex-col gap-4 hover:-translate-y-1 transition-transform group"
			>
				<div className="flex justify-between items-start mb-2">
					<div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center text-sky-600 border border-slate-100 overflow-hidden group-hover:border-sky-100 transition-colors p-1.5">
						{item.company?.logo_url ? (
							<img 
								src={resolveBackendAssetUrl(item.company.logo_url)} 
								alt={item.company.name} 
								className="w-full h-auto max-h-full object-contain"
								onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex'; }}
							/>
						) : null}
						<div className={`${item.company?.logo_url ? 'hidden' : 'flex'} w-full h-full bg-sky-50 items-center justify-center text-sky-600`}>
							<PiBriefcase size={24} />
						</div>
					</div>
					<button 
						onClick={(e) => {
							e.stopPropagation();
							if (!token) {
								navigate("/login");
								return;
							}
							toggleWishlistMutate({ vacancyId: item.id, isWishlisted });
						}}
						disabled={isToggling}
						className={`p-1.5 rounded-lg transition-all ${
							isWishlisted 
								? "text-amber-500 bg-amber-50 hover:bg-amber-100/80" 
								: "text-zinc-400 hover:text-sky-600 hover:bg-sky-50"
						}`}
						title={isWishlisted ? "Hapus dari Wishlist" : "Simpan ke Wishlist"}
					>
						<PiBookmarkSimple size={22} weight={isWishlisted ? "fill" : "regular"} />
					</button>
				</div>

				<div className="flex-1">
					<h4 onClick={() => handleCardClick(item.id)} className="text-[17px] cursor-pointer font-[900] text-sky-950 line-clamp-2 leading-snug hover:text-sky-600 transition-colors hover:underline">{item.title}</h4>
					<p className="text-[14px] font-medium text-slate-400 mt-1">{item.company?.name || "Perusahaan"}</p>
				</div>
				
				<div className="mt-auto pt-4 border-t border-slate-50 space-y-3">
					<div className="text-[13px] font-bold text-slate-500 flex items-center gap-1.5">
						<PiMapPin size={16} className="text-sky-600" />
						<span className="line-clamp-1">{item.location || "Lokasi tidak dicantumkan"}</span>
					</div>
					<div className="flex gap-2">
						<span className="px-2 py-1 bg-slate-50 border border-slate-100 text-[10px] text-slate-600 font-bold rounded uppercase tracking-widest">{displayType(item.type)}</span>
						<span className="px-2 py-1 bg-slate-50 border border-slate-100 text-[10px] text-slate-600 font-bold rounded uppercase tracking-widest">{displayPayment(item.payment_type)}</span>
					</div>
					<div className="flex items-center justify-between text-[11px] font-bold text-slate-400 tracking-tight">
						<div className="flex items-center gap-1.5">
							<PiCalendar size={14} className="text-sky-600" />
							<span>Ditutup: {item.close_date ? format(new Date(item.close_date), 'dd MMM yyyy') : 'N/A'}</span>
						</div>
					</div>
				</div>
			</div>
		);
	};

	return (
		<div className="font-jakarta">
			{/* Banner Utama */}
			<div className="mb-5 bg-sky-950 py-6 px-5 sm:py-7 sm:px-10 rounded-xl text-white flex flex-col sm:flex-row justify-between sm:items-center gap-4 shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)]">
				<div className="flex flex-col gap-2">
					<div className="text-2xl sm:text-3xl font-bold">Eksplorasi Karirmu</div>
					<div className="text-sm opacity-90">
						Temukan peluang magang dan karir profesional yang telah dikurasi khusus untuk mahasiswa dan alumni IPB University.
					</div>
				</div>
			</div>

			{/* Area Pencarian */}
			<div className="bg-white p-4 sm:p-6 rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] mb-8 flex flex-col sm:flex-row sm:flex-wrap gap-4 sm:items-end relative">
				<div className="flex-1 flex flex-col gap-1.5 min-w-0 sm:min-w-[200px]">
					<label className="text-[11px] font-[900] text-slate-400 uppercase tracking-widest">Pencarian</label>
					<div className="relative">
						<PiBriefcase className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400 pointer-events-none" size={20} />
						<input
							type="text"
							ref={queryRef}
							defaultValue={query}
							placeholder="Posisi, Kata Kunci, atau Perusahaan"
							onKeyDown={(e) => e.key === "Enter" && handleSearch()}
							className="pl-10 w-full py-2.5 bg-zinc-50/50 border border-zinc-100 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 outline-none font-medium placeholder:text-zinc-400"
						/>
					</div>
				</div>
				<div className="flex-1 flex flex-col gap-1.5 min-w-0 sm:min-w-[150px]">
					<label className="text-[11px] font-[900] text-slate-400 uppercase tracking-widest">Lokasi</label>
					<div className="relative">
						<PiMapPin className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400 pointer-events-none" size={20} />
						<input
							type="text"
							ref={locationRef}
							defaultValue={location}
							placeholder="Semua Lokasi"
							onKeyDown={(e) => e.key === "Enter" && handleSearch()}
							className="pl-10 w-full py-2.5 bg-zinc-50/50 border border-zinc-100 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 outline-none font-medium placeholder:text-zinc-400"
						/>
					</div>
				</div>
				<div className="w-full sm:w-48 flex flex-col gap-1.5 relative">
					<label className="text-[11px] font-[900] text-slate-400 uppercase tracking-widest">Tipe</label>
					<div className="relative">
						<select
							value={type}
							onChange={(e) => updateFilters({ type: e.target.value })}
							className="w-full py-2.5 px-3 bg-zinc-50/50 border border-zinc-100 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 outline-none font-medium appearance-none cursor-pointer"
						>
							<option value="">Semua Tipe</option>
							<option value="INTERNSHIP_GENERAL">Magang Umum</option>
							<option value="MBKM_INTERNSHIP">MBKM Magang</option>
							<option value="MBKM_STUDY_INDEPENDENT">MBKM Studi Independen</option>
							<option value="FULL_TIME">Full Time</option>
						</select>
						<PiCaretDown className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 pointer-events-none" />
					</div>
				</div>
				<div className="grid grid-cols-2 gap-3 sm:flex sm:gap-4">
				<button 
					type="button" 
					onClick={handleReset} 
					className="bg-white text-zinc-400 border border-zinc-100 p-2.5 rounded-lg hover:bg-zinc-50 transition-colors shadow-sm flex items-center justify-center"
					title="Reset Filter"
				>
					<PiXCircle size={22} weight="bold" />
				</button>
				<button 
					type="button" 
					onClick={handleSearch}
					className="bg-sky-950 text-white p-2.5 rounded-lg hover:bg-sky-900 transition-colors shadow-lg shadow-sky-900/10 flex items-center justify-center"
				>
					<PiMagnifyingGlass size={22} weight="bold" />
				</button>
				</div>
			</div>

			<div className="flex flex-col lg:flex-row gap-8">
				{/* Filter Sisi Samping */}
				<aside className="w-full lg:w-72 flex flex-col gap-5">
					<div className="p-5 sm:p-6 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] border border-slate-50 lg:sticky lg:top-24">
						<div className="flex items-center justify-between mb-8">
							<h3 className="font-[900] text-sky-950 tracking-tight uppercase text-xs tracking-[0.1em]">Filter Detail</h3>
							<button onClick={handleReset} className="text-[11px] font-bold text-sky-600 hover:underline">Reset</button>
						</div>
						
						<div className="space-y-8">
							<div>
								<p className="text-[10px] font-[1000] text-zinc-400 uppercase tracking-widest mb-4">Bidang Industri</p>
								<div className="space-y-3">
									<label className="flex items-center gap-3 cursor-pointer group">
										<input 
											type="checkbox" 
											checked={industry === ""} 
											onChange={() => updateFilters({ industry: "" })}
											className="w-5 h-5 rounded border-zinc-200 text-sky-600 focus:ring-sky-500" 
										/>
										<span className={`text-sm font-bold ${industry === "" ? "text-sky-950" : "text-zinc-500"} group-hover:text-black`}>Semua Industri</span>
									</label>
									{industriesQuery.data?.slice(0, showAllIndustries ? undefined : 5).map((item) => (
										<label key={item} className="flex items-center gap-3 cursor-pointer group">
											<input 
												type="checkbox" 
												checked={industry === item}
												onChange={() => updateFilters({ industry: item })}
												className="w-5 h-5 rounded border-zinc-200 text-sky-600 focus:ring-sky-500" 
											/>
											<span className={`text-sm font-bold ${industry === item ? "text-sky-950" : "text-zinc-500"} group-hover:text-black`}>{item}</span>
										</label>
									))}
								</div>
								{industriesQuery.data?.length > 5 && (
									<button 
										onClick={() => setShowAllIndustries(!showAllIndustries)}
										className="mt-4 text-[11px] font-bold text-sky-600 hover:text-sky-800 transition-colors uppercase tracking-wider"
									>
										{showAllIndustries ? "Lihat Sedikit" : `Lihat Selengkapnya (${industriesQuery.data.length - 5}+)`}
									</button>
								)}
							</div>

							<div>
								<p className="text-[10px] font-[1000] text-zinc-400 uppercase tracking-widest mb-4">Kompensasi</p>
								<div className="space-y-3">
									<label className="flex items-center gap-3 cursor-pointer group">
										<input 
											type="radio" 
											name="payment"
											checked={paymentType === ""}
											onChange={() => updateFilters({ payment_type: "" })}
											className="w-5 h-5 border-zinc-200 text-sky-600 focus:ring-sky-500" 
										/>
										<span className={`text-sm font-bold ${paymentType === "" ? "text-sky-950" : "text-zinc-500"} group-hover:text-black`}>Semua</span>
									</label>
									{[
										{ val: "PAID", label: "Paid" },
										{ val: "UNPAID", label: "Unpaid" },
										{ val: "ALLOWANCE_ONLY", label: "Allowance" }
									].map((item) => (
										<label key={item.val} className="flex items-center gap-3 cursor-pointer group">
											<input 
												type="radio" 
												name="payment"
												checked={paymentType === item.val}
												onChange={() => updateFilters({ payment_type: item.val })}
												className="w-5 h-5 border-zinc-200 text-sky-600 focus:ring-sky-500" 
											/>
											<span className={`text-sm font-bold ${paymentType === item.val ? "text-sky-950" : "text-zinc-500"} group-hover:text-black`}>{item.label}</span>
										</label>
									))}
								</div>
							</div>
						</div>
					</div>
				</aside>

				{/* Daftar Lowongan */}
				<div className="flex-1">
					<div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 text-sm text-zinc-500">
						<span className="font-bold text-sky-950">
							{vacanciesQuery.isLoading ? "Memuat lowongan..." : `${totalItems} lowongan ditemukan`}
						</span>
						<div className="flex items-center gap-4">
							<span className="text-[13px] font-medium text-slate-400">Halaman {currentPage} dari {totalPages}</span>
						</div>
					</div>

					{vacanciesQuery.isError && (
						<div className="mb-6 p-4 rounded-xl border border-red-100 bg-red-50 text-red-700 text-sm font-medium">
							Gagal memuat lowongan dari backend.
						</div>
					)}

					<div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
						{currentCards.map((item) => (
							<VacancyCard key={item.id} item={item} />
						))}
						{!vacanciesQuery.isLoading && currentCards.length === 0 && (
							<div className="col-span-full p-8 rounded-xl border border-dashed border-zinc-200 text-center text-zinc-500 bg-white">
								Tidak ada lowongan yang cocok dengan filter saat ini.
							</div>
						)}
					</div>

					{/* Navigasi Halaman */}
					<div className="flex justify-center mt-12 gap-2 overflow-x-auto pb-2">
						<button
							disabled={currentPage === 1}
							onClick={() => updateFilters({ page: currentPage - 1 })}
							className="w-10 h-10 flex items-center justify-center rounded border border-zinc-200 text-zinc-600 hover:bg-zinc-100 disabled:opacity-30"
						>
							<PiCaretLeft size={20} weight="bold" />
						</button>
						<div className="flex gap-1 shrink-0">
							{paginationRange.map((page, index) => (
								<button
									key={index}
									onClick={() => (page !== "..." ? updateFilters({ page }) : null)}
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
							onClick={() => updateFilters({ page: currentPage + 1 })}
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
