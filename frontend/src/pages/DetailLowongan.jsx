import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate, useParams } from "react-router-dom";
import vacancyService from "../services/vacancyService";
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
	PiSpinnerGap,
	PiArrowLeft,
} from "react-icons/pi";

function DetailLowongan() {
	const navigate = useNavigate();
	const queryClient = useQueryClient();
	const { vacancyId } = useParams();

	const vacancyQuery = useQuery({
		queryKey: ["vacancy", vacancyId],
		queryFn: () => vacancyService.getVacancy(vacancyId),
		enabled: !!vacancyId,
	});

	const jobMatchQuery = useQuery({
		queryKey: ["jobmatch", vacancyId],
		queryFn: () => vacancyService.getJobMatch(vacancyId),
		enabled: !!vacancyId,
		staleTime: 1000 * 60 * 5,
	});

	const saveWishlistMutation = useMutation({
		mutationFn: () => vacancyService.addToWishlist(vacancyId),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["vacancy", vacancyId] });
			alert("Lowongan berhasil disimpan ke wishlist.");
		},
		onError: (error) => {
			alert(error.response?.data?.detail || "Gagal menyimpan ke wishlist.");
		},
	});

	const vacancy = vacancyQuery.data;
	const match = jobMatchQuery.data;

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

	if (vacancyQuery.isLoading) {
		return (
			<div className="flex min-h-[60vh] items-center justify-center">
				<div className="flex flex-col items-center gap-4 text-sky-950">
					<PiSpinnerGap size={44} className="animate-spin" />
					<p className="text-sm font-bold uppercase tracking-widest text-sky-950/60">Memuat detail lowongan...</p>
				</div>
			</div>
		);
	}

	if (vacancyQuery.isError || !vacancy) {
		return (
			<div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 text-center">
				<p className="text-lg font-bold text-sky-950">Detail lowongan tidak ditemukan.</p>
				<button onClick={() => navigate("/lowongan")} className="rounded bg-sky-950 px-4 py-2 text-white">
					Kembali ke Lowongan
				</button>
			</div>
		);
	}

	return (
		<div className="font-jakarta text-black">
			<button onClick={() => navigate("/lowongan")} className="mb-4 inline-flex items-center gap-2 text-sm font-bold text-sky-950 hover:text-sky-800">
				<PiArrowLeft size={16} />
				Kembali ke Lowongan
			</button>

			<div className="flex flex-col gap-5 lg:flex-row">
				<div className="flex-1 flex flex-col gap-5">
					<div className="flex-1 text-sm self-stretch py-10 px-10 bg-sky-950 rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex gap-4">
						<div className="size-15 bg-slate-100 flex justify-center items-center rounded text-sky-950 font-bold text-xl">
							{vacancy.company?.name?.slice(0, 1) || "V"}
						</div>
						<div className="text-white">
							<div className="text-3xl font-bold">{vacancy.title}</div>
							<div className="text-xl">{vacancy.company?.name || "Perusahaan belum tercantum"}</div>
							{match && (
								<div className="mt-3 text-sm">
									<span className="font-bold">Kecocokan: </span>
									<span className="text-white">{match.match_percentage}%</span>
								</div>
							)}
						</div>
					</div>

					<div className="flex-1 text-sm self-stretch p-10 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-6">
						<div className="flex items-center gap-3 font-bold">
							<div className="bg-sky-950 p-1 rounded h-7"></div>
							<div className="text-lg text-sky-950">Tentang Perusahaan</div>
						</div>
						<div className="text-justify text-slate-700">
							{vacancy.company?.industry || "Informasi perusahaan belum tersedia di backend."}
						</div>

						<div className="flex items-center gap-3 font-bold">
							<div className="bg-sky-950 p-1 rounded h-7"></div>
							<div className="text-lg text-sky-950">Deskripsi Pekerjaan</div>
						</div>
						<div className="text-justify text-slate-700 whitespace-pre-line">{vacancy.description}</div>

						<div className="flex items-center gap-3 font-bold">
							<div className="bg-sky-950 p-1 rounded h-7"></div>
							<div className="text-lg text-sky-950">Kualifikasi & Persyaratan</div>
						</div>
						<div className="grid grid-cols-1 md:grid-cols-2 gap-5">
							<div className="flex-1 text-sm self-stretch px-5 rounded-xl flex gap-4">
								<div className="flex gap-3">
									<PiGraduationCap className="size-8" />
									<div>
										<div className="font-bold text-sky-950">Lowongan</div>
										<div className="text-slate-700">{displayType(vacancy.type)}</div>
									</div>
								</div>
							</div>
							<div className="flex-1 text-sm self-stretch px-5 rounded-xl flex gap-4">
								<div className="flex gap-3">
									<PiCodeSimpleBold className="size-6" />
									<div>
										<div className="font-bold text-sky-950">Kompensasi</div>
										<div className="text-slate-700">{displayPayment(vacancy.payment_type)}</div>
									</div>
								</div>
							</div>
							<div className="flex-1 text-sm self-stretch px-5 rounded-xl flex gap-4">
								<div className="flex gap-3">
									<PiMagnifyingGlassBold className="size-8" />
									<div>
										<div className="font-bold text-sky-950">Lokasi</div>
										<div className="text-slate-700">{vacancy.location || "-"}</div>
									</div>
								</div>
							</div>
							<div className="flex-1 text-sm self-stretch px-5 rounded-xl flex gap-4">
								<div className="flex gap-3">
									<PiCalendarBlank className="size-8" />
									<div>
										<div className="font-bold text-sky-950">Periode</div>
										<div className="text-slate-700">{new Date(vacancy.open_date).toLocaleDateString("id-ID")} - {new Date(vacancy.close_date).toLocaleDateString("id-ID")}</div>
									</div>
								</div>
							</div>
						</div>

						<div>
							<div className="font-bold text-sky-950 mb-3">Skills yang Dibutuhkan</div>
							<div className="flex flex-wrap gap-2">
								{vacancy.skills?.length > 0 ? vacancy.skills.map((skill) => (
									<span key={skill.skill_id} className="rounded-full bg-sky-50 px-3 py-1 text-xs font-bold text-sky-700 border border-sky-100">
										{skill.skill_name}{skill.is_mandatory ? " *" : ""}
									</span>
								)) : (
									<span className="text-sm text-zinc-500">Belum ada requirement skill yang diisi.</span>
								)}
							</div>
						</div>
					</div>
				</div>

				<div>
					<div className="flex-1 flex text-sm self-stretch w-full lg:w-80 p-5 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex-col gap-4">
						<div className="text-xl font-bold text-sky-950">Informasi Lowongan</div>
						<div className="flex gap-2 items-center">
							<PiMapPinLine className="size-10 p-2 bg-indigo-100 text-sky-950 rounded-full" />
							<div>
								<div className="font-bold text-sm text-slate-700">Lokasi</div>
								<div className="font-bold text-base text-sky-950">{vacancy.location || "-"}</div>
							</div>
						</div>
						<div className="flex gap-2 items-center">
							<PiClock className="size-10 p-2 bg-indigo-100 text-sky-950 rounded-full" />
							<div>
								<div className="font-bold text-sm text-slate-700">Tipe Kerja</div>
								<div className="font-bold text-base text-sky-950">{displayType(vacancy.type)}</div>
							</div>
						</div>
						<div className="flex gap-2 items-center">
							<PiCalendarDots className="size-10 p-2 bg-indigo-100 text-sky-950 rounded-full" />
							<div>
								<div className="font-bold text-sm text-slate-700">Kompensasi</div>
								<div className="font-bold text-base text-sky-950">{displayPayment(vacancy.payment_type)}</div>
							</div>
						</div>
						<div className="flex flex-col gap-2">
							<a href={vacancy.source_url || "#"} target="_blank" rel="noreferrer" className="flex gap-2 w-full p-3 bg-sky-950 hover:bg-sky-900 text-white rounded justify-center items-center">
								<div className="text-base">Lamar Sekarang</div>
								<PiCaretCircleRightFill className="size-5 text-white" />
							</a>
							<button
								onClick={() => saveWishlistMutation.mutate()}
								disabled={saveWishlistMutation.isPending}
								className="flex gap-2 w-full p-3 hover:bg-slate-100 text-sky-950 hover:text-sky-900 border-2 border-gray-300 hover:border-sky-900 rounded justify-center items-center disabled:opacity-70"
							>
								<PiBookmarkSimple className="size-5" />
								<div className="text-base">{saveWishlistMutation.isPending ? "Menyimpan..." : "Simpan Lowongan"}</div>
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default DetailLowongan;
