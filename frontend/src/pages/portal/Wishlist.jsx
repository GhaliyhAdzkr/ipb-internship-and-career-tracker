import { useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { format } from "date-fns";
import { vacancyService } from "../../services/vacancyService";
import toast from "react-hot-toast";
import {
  PiTrash,
  PiBriefcase,
  PiMapPin,
  PiCalendar,
  PiArrowRightBold
} from "react-icons/pi";

export default function Wishlist() {
	const navigate = useNavigate();
	const queryClient = useQueryClient();

	const { data, isLoading, isError } = useQuery({
		queryKey: ["wishlist"],
		queryFn: () => vacancyService.getWishlist({ page: 1, perPage: 50 }),
	});

	const removeMutation = useMutation({
		mutationFn: (id) => vacancyService.deleteWishlist(id),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["wishlist"] });
			toast.success("Berhasil dihapus dari wishlist!");
		},
		onError: (err) => {
			toast.error(err.response?.data?.detail || "Gagal menghapus dari wishlist.");
		}
	});

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

	if (isLoading) {
		return (
			<div className="flex flex-col gap-6">
				<h2 className="text-2xl font-[900] text-sky-950 tracking-tight">Wishlist Saya</h2>
				<div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
					{[1, 2, 3].map((i) => (
						<div key={i} className="h-[280px] bg-white rounded-xl animate-pulse border border-slate-50" />
					))}
				</div>
			</div>
		);
	}

	if (isError) {
		return <div className="p-8 text-center text-red-600 font-bold">Gagal memuat wishlist.</div>;
	}

	const wishlistItems = data?.items || [];

	return (
		<div className="font-jakarta pb-12">
			{/* Banner */}
			<div className="mb-8 bg-sky-950 py-8 px-10 rounded-xl text-white flex justify-between items-center shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)]">
				<div className="flex flex-col gap-2">
					<div className="text-3xl font-bold tracking-tight">Wishlist Saya</div>
					<div className="text-sm opacity-80 font-medium">
						Daftar lowongan yang telah kamu simpan untuk dilamar nanti. Pastikan jangan sampai terlewat batas waktu pendaftaran!
					</div>
				</div>
			</div>

			{wishlistItems.length === 0 ? (
				<div className="p-12 text-center bg-white rounded-2xl border border-dashed border-slate-200">
					<div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4">
						<PiBriefcase size={32} className="text-slate-300" />
					</div>
					<h3 className="text-lg font-bold text-sky-950 mb-1">Belum ada wishlist</h3>
					<p className="text-sm text-slate-400 mb-6">Simpan lowongan menarik untuk menemukannya di sini.</p>
					<button 
						onClick={() => navigate("/app/lowongan")}
						className="bg-sky-950 text-white px-6 py-2.5 rounded-lg text-sm font-bold shadow-lg shadow-sky-900/10 hover:bg-sky-900 transition-all"
					>
						Eksplorasi Lowongan
					</button>
				</div>
			) : (
				<div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
					{wishlistItems.map((item) => {
						const vacancy = item.vacancy;
						return (
							<div
								key={item.id}
								className="p-6 bg-white rounded-2xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] border border-slate-50 flex flex-col gap-4 group hover:-translate-y-1 transition-all duration-300 relative"
							>
								<div className="flex justify-between items-start mb-2">
									<div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center text-sky-600 border border-slate-100 overflow-hidden p-1.5 group-hover:border-sky-100 transition-colors">
										{vacancy.company?.logo_url ? (
											<img 
												src={vacancy.company.logo_url} 
												alt={vacancy.company.name} 
												className="w-full h-auto max-h-full object-contain"
												onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex'; }}
											/>
										) : null}
										<div className={`${vacancy.company?.logo_url ? 'hidden' : 'flex'} w-full h-full bg-sky-50 items-center justify-center text-sky-600`}>
											<PiBriefcase size={24} />
										</div>
									</div>
									<button 
										onClick={() => removeMutation.mutate(item.id)}
										className="p-2 text-slate-300 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
										title="Hapus dari Wishlist"
									>
										<PiTrash size={22} />
									</button>
								</div>

								<div className="flex-1">
									<h4 className="text-[17px] font-[900] text-sky-950 line-clamp-2 leading-snug group-hover:text-sky-600 transition-colors">{vacancy.title}</h4>
									<p className="text-[14px] font-medium text-slate-400 mt-1">{vacancy.company?.name || "Perusahaan"}</p>
								</div>
								
								<div className="mt-auto pt-4 border-t border-slate-50 space-y-3">
									<div className="text-[13px] font-bold text-slate-500 flex items-center gap-1.5">
										<PiMapPin size={16} className="text-sky-600" />
										<span className="line-clamp-1">{vacancy.location || "Lokasi tidak dicantumkan"}</span>
									</div>
									<div className="flex gap-2">
										<span className="px-2 py-1 bg-slate-50 border border-slate-100 text-[10px] text-slate-600 font-bold rounded uppercase tracking-widest">{displayType(vacancy.type)}</span>
										<span className="px-2 py-1 bg-slate-50 border border-slate-100 text-[10px] text-slate-600 font-bold rounded uppercase tracking-widest">{displayPayment(vacancy.payment_type)}</span>
									</div>
									<div className="flex items-center justify-between mt-2 pt-2">
										<div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-400 tracking-tight">
											<PiCalendar size={14} className="text-sky-600" />
											<span>Ditutup: {vacancy.close_date ? format(new Date(vacancy.close_date), 'dd MMM yyyy') : 'N/A'}</span>
										</div>
										<button 
											onClick={() => navigate(`/detail/${vacancy.id}`)}
											className="flex items-center gap-1.5 text-[12px] font-[900] text-sky-950 hover:text-sky-600 transition-colors"
										>
											Detail
											<PiArrowRightBold size={14} />
										</button>
									</div>
								</div>
							</div>
						);
					})}
				</div>
			)}
		</div>
	);
}
