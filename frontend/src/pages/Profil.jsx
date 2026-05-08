import { React, useState, useEffect, useRef } from "react";
import { useAuth } from "../hooks/useAuth";
import { authService } from "../services/authService";
import {
	PiUserCircle,
	PiIdentificationCard,
	PiEnvelope,
	PiBuildings,
	PiGraduationCap,
	PiCamera,
	PiPhone,
	PiLinkedinLogo,
	PiChartLineUp,
	PiSpinnerGap,
	PiCheckCircle,
	PiCaretDown,
	PiMagnifyingGlass,
} from "react-icons/pi";

// PACKAGE

// ICONS
import { PiUpload } from "react-icons/pi";
import { AiOutlineCloudUpload } from "react-icons/ai";
import { HiOutlineDotsCircleHorizontal } from "react-icons/hi";
import { CiTextAlignJustify } from "react-icons/ci";
import { FaRegCircleCheck } from "react-icons/fa6";
import { TiMessages } from "react-icons/ti";

function Profil() {
	const { user, updateProfile, isUpdating } = useAuth();

	const [formData, setFormData] = useState({
		full_name: "",
		nim: "",
		semester: "",
		phone_number: "",
		linkedin_url: "",
		gpa: "",
		department_id: "",
		department_name: "",
	});

	const [departments, setDepartments] = useState([]);
	const [isDeptOpen, setIsDeptOpen] = useState(false);
	const [deptSearch, setDeptSearch] = useState("");
	const [showSuccess, setShowSuccess] = useState(false);
	const dropdownRef = useRef(null);

	// Fetch departments on mount
	useEffect(() => {
		const fetchDepts = async () => {
			try {
				const data = await authService.getDepartments();
				setDepartments(data);
			} catch (err) {
				console.error("Failed to fetch departments:", err);
			}
		};
		fetchDepts();
	}, []);

	// Sync state with user data
	useEffect(() => {
		if (user) {
			setFormData({
				full_name: user.full_name || "",
				nim: user.nim || "",
				semester: user.semester || "",
				phone_number: user.phone_number || "",
				linkedin_url: user.linkedin_url || "",
				gpa: user.gpa || "",
				department_id: user.department_id || "",
				department_name: user.department_name || "",
			});
		}
	}, [user]);

	// Close dropdown when clicking outside
	useEffect(() => {
		function handleClickOutside(event) {
			if (
				dropdownRef.current &&
				!dropdownRef.current.contains(event.target)
			) {
				setIsDeptOpen(false);
			}
		}
		document.addEventListener("mousedown", handleClickOutside);
		return () =>
			document.removeEventListener("mousedown", handleClickOutside);
	}, []);

	const filteredDepts = departments.filter(
		(d) =>
			d.name.toLowerCase().includes(deptSearch.toLowerCase()) ||
			d.faculty.toLowerCase().includes(deptSearch.toLowerCase()),
	);

	const handleSubmit = async (e) => {
		e.preventDefault();

		// Validasi Dasar
		const semesterInt = parseInt(formData.semester);
		const gpaFloat = parseFloat(formData.gpa);

		if (
			formData.semester &&
			(isNaN(semesterInt) || semesterInt < 1 || semesterInt > 14)
		) {
			alert("Semester harus berupa angka antara 1 - 14");
			return;
		}

		if (formData.gpa && (isNaN(gpaFloat) || gpaFloat < 0 || gpaFloat > 4)) {
			alert("IPK harus berupa angka antara 0.0 - 4.0");
			return;
		}

		try {
			await updateProfile({
				full_name: formData.full_name,
				nim: formData.nim,
				semester: semesterInt || undefined,
				phone_number: formData.phone_number,
				linkedin_url: formData.linkedin_url,
				gpa: gpaFloat || undefined,
				department_id: formData.department_id || undefined,
			});
			setShowSuccess(true);
			setTimeout(() => setShowSuccess(false), 3000);
		} catch (err) {
			console.error("Update profile failed:", err);
		}
	};

	return (
		<div className="font-jakarta pb-10">
			{/* Banner */}
			<div className="mb-8 bg-sky-950 py-7 px-10 rounded-xl text-white flex justify-between items-center shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)]">
				<div className="flex flex-col gap-2">
					<div className="text-3xl font-bold">Profil Saya</div>
					<div className="text-justify text-zinc-200">
						Kelola informasi pribadi dan akademik Anda untuk
						verifikasi internship.
					</div>
				</div>
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
				{/* Avatar Card */}
				<div className="lg:col-span-4">
					<div className="p-8 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col items-center text-center gap-6">
						<div className="relative">
							<div className="w-32 h-32 bg-zinc-100 rounded-full flex items-center justify-center border-4 border-white shadow-sm overflow-hidden">
								<PiUserCircle
									size={100}
									className="text-zinc-400"
								/>
							</div>
							<button className="absolute bottom-0 right-0 p-2 bg-sky-950 text-white rounded-full shadow-lg hover:bg-sky-900 transition-all">
								<PiCamera size={20} weight="bold" />
							</button>
						</div>
						<div>
							<h3 className="text-xl font-bold text-black">
								{user?.full_name || "User"}
							</h3>
							<p className="text-xs font-bold text-sky-700 uppercase tracking-widest mt-1">
								{user?.role || "STUDENT"}
							</p>
						</div>

						{showSuccess && (
							<div className="flex items-center gap-2 text-green-600 text-sm font-bold bg-green-50 px-4 py-2 rounded-full border border-green-100 animate-in fade-in zoom-in duration-300">
								<PiCheckCircle weight="fill" size={18} />
								<span>Berhasil Disimpan</span>
							</div>
						)}
					</div>
				</div>

				{/* Info Card */}
				<div className="lg:col-span-8">
					<form
						onSubmit={handleSubmit}
						className="p-8 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-8"
					>
						<div className="flex items-center gap-3 border-b pb-4">
							<PiIdentificationCard
								size={24}
								className="text-sky-950"
								weight="bold"
							/>
							<h3 className="text-lg font-bold text-black">
								Informasi Pribadi & Akademik
							</h3>
						</div>

						<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
							{/* Nama Lengkap */}
							<div className="flex flex-col gap-1.5">
								<label className="text-xs font-bold text-zinc-500 uppercase tracking-wider">
									Nama Lengkap
								</label>
								<div className="relative">
									<PiUserCircle
										size={20}
										className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400"
									/>
									<input
										type="text"
										value={formData.full_name}
										onChange={(e) =>
											setFormData({
												...formData,
												full_name: e.target.value,
											})
										}
										className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 text-zinc-700 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none transition-all"
									/>
								</div>
							</div>

							{/* Email (Read Only) */}
							<div className="flex flex-col gap-1.5">
								<label className="text-xs font-bold text-zinc-500 uppercase tracking-wider">
									Email Institusi
								</label>
								<div className="relative">
									<PiEnvelope
										size={20}
										className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400"
									/>
									<input
										type="email"
										disabled
										value={user?.email || ""}
										className="pl-10 w-full py-2.5 bg-zinc-100 border border-zinc-200 text-zinc-700 rounded text-sm text-zinc-500 cursor-not-allowed"
									/>
								</div>
							</div>

							{/* NIM */}
							<div className="flex flex-col gap-1.5">
								<label className="text-xs font-bold text-zinc-500 uppercase tracking-wider">
									NIM
								</label>
								<div className="relative">
									<PiIdentificationCard
										size={20}
										className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400"
									/>
									<input
										type="text"
										value={formData.nim}
										onChange={(e) =>
											setFormData({
												...formData,
												nim: e.target.value,
											})
										}
										className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 text-zinc-700 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none transition-all"
									/>
								</div>
							</div>

							{/* Semester */}
							<div className="flex flex-col gap-1.5">
								<label className="text-xs font-bold text-zinc-500 uppercase tracking-wider">
									Semester Aktif
								</label>
								<div className="relative">
									<PiGraduationCap
										size={20}
										className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400"
									/>
									<input
										type="number"
										value={formData.semester}
										onChange={(e) =>
											setFormData({
												...formData,
												semester: e.target.value,
											})
										}
										className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 text-zinc-700 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none transition-all"
									/>
								</div>
							</div>

							{/* Departemen (Searchable Dropdown) */}
							<div
								className="flex flex-col gap-1.5"
								ref={dropdownRef}
							>
								<label className="text-xs font-bold text-zinc-500 uppercase tracking-wider">
									Departemen
								</label>
								<div className="relative">
									<PiBuildings
										size={20}
										className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400"
									/>
									<div
										onClick={() =>
											setIsDeptOpen(!isDeptOpen)
										}
										className="pl-10 pr-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 text-zinc-700 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none cursor-pointer flex justify-between items-center"
									>
										<span
											className={
												formData.department_name
													? "text-black"
													: "text-zinc-400"
											}
										>
											{formData.department_name ||
												"Cari Departemen..."}
										</span>
										<PiCaretDown
											size={16}
											className={`transition-transform duration-200 ${isDeptOpen ? "rotate-180" : ""}`}
										/>
									</div>

									{isDeptOpen && (
										<div className="absolute z-50 top-full left-0 w-full mt-2 bg-white border border-zinc-200 text-zinc-700 rounded-xl shadow-2xl overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
											<div className="p-3 border-b bg-zinc-50">
												<div className="relative">
													<PiMagnifyingGlass
														size={16}
														className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400"
													/>
													<input
														autoFocus
														type="text"
														className="w-full pl-9 pr-4 py-2 bg-white border border-zinc-200 text-zinc-700 rounded-lg text-xs outline-none focus:ring-2 focus:ring-sky-500"
														placeholder="Ketik nama departemen..."
														value={deptSearch}
														onChange={(e) =>
															setDeptSearch(
																e.target.value,
															)
														}
														onClick={(e) =>
															e.stopPropagation()
														}
													/>
												</div>
											</div>
											<div className="max-h-60 overflow-y-auto">
												{filteredDepts.length > 0 ? (
													filteredDepts.map(
														(dept) => (
															<div
																key={dept.id}
																onClick={() => {
																	setFormData(
																		{
																			...formData,
																			department_id:
																				dept.id,
																			department_name:
																				dept.name,
																		},
																	);
																	setIsDeptOpen(
																		false,
																	);
																	setDeptSearch(
																		"",
																	);
																}}
																className="px-4 py-3 hover:bg-sky-50 cursor-pointer transition-colors border-b last:border-0 border-zinc-50"
															>
																<div className="text-sm font-bold text-zinc-800">
																	{dept.name}
																</div>
																<div className="text-[10px] text-sky-600 font-bold uppercase tracking-tighter">
																	{
																		dept.faculty
																	}
																</div>
															</div>
														),
													)
												) : (
													<div className="px-4 py-6 text-center text-xs text-zinc-400">
														Tidak ada hasil
													</div>
												)}
											</div>
										</div>
									)}
								</div>
							</div>

							{/* IPK / GPA */}
							<div className="flex flex-col gap-1.5">
								<label className="text-xs font-bold text-zinc-500 uppercase tracking-wider">
									IPK / GPA
								</label>
								<div className="relative">
									<PiChartLineUp
										size={20}
										className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400"
									/>
									<input
										type="number"
										step="0.01"
										value={formData.gpa}
										onChange={(e) =>
											setFormData({
												...formData,
												gpa: e.target.value,
											})
										}
										placeholder="Contoh: 3.85"
										className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 text-zinc-700 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none transition-all"
									/>
								</div>
							</div>

							{/* No. HP */}
							<div className="flex flex-col gap-1.5">
								<label className="text-xs font-bold text-zinc-500 uppercase tracking-wider">
									Nomor WhatsApp
								</label>
								<div className="relative">
									<PiPhone
										size={20}
										className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400"
									/>
									<input
										type="text"
										value={formData.phone_number}
										onChange={(e) =>
											setFormData({
												...formData,
												phone_number: e.target.value,
											})
										}
										placeholder="Contoh: 08123456789"
										className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 text-zinc-700 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none transition-all"
									/>
								</div>
							</div>

							{/* LinkedIn */}
							<div className="flex flex-col gap-1.5">
								<label className="text-xs font-bold text-zinc-500 uppercase tracking-wider">
									URL LinkedIn
								</label>
								<div className="relative">
									<PiLinkedinLogo
										size={20}
										className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400"
									/>
									<input
										type="text"
										value={formData.linkedin_url}
										onChange={(e) =>
											setFormData({
												...formData,
												linkedin_url: e.target.value,
											})
										}
										placeholder="linkedin.com/in/username"
										className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 text-zinc-700 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none transition-all"
									/>
								</div>
							</div>
						</div>

						<div className="flex justify-end mt-4 border-t pt-6">
							<button
								type="submit"
								disabled={isUpdating}
								className="px-8 py-2.5 bg-sky-950 text-white font-bold rounded hover:bg-sky-900 transition-all flex items-center gap-2 disabled:opacity-50"
							>
								{isUpdating ? (
									<PiSpinnerGap className="animate-spin" />
								) : null}
								<span>Simpan Perubahan</span>
							</button>
						</div>
					</form>
				</div>
			</div>
		</div>
	);
}

export default Profil;
