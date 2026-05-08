import { useState } from "react";
import { DayPicker } from "react-day-picker";
import { format } from "date-fns";
import { id } from "date-fns/locale";
import "react-day-picker/style.css";
import { PiWarning, PiClock, PiUpload } from "react-icons/pi";

function Jurnal() {
	const [selectedDate, setSelectedDate] = useState(new Date());
	const [startTimeStr, setStartTimeStr] = useState("08:00");
	const [endTimeStr, setEndTimeStr] = useState("16:00");

	const journalStartDate = new Date(2026, 1, 1);

	const calculateWorkTime = (start, end) => {
		if (!start || !end) return { label: "0 Jam", error: null };
		const [sH, sM] = start.split(":").map(Number);
		const [eH, eM] = end.split(":").map(Number);
		const sTotal = sH * 60 + sM;
		const eTotal = eH * 60 + eM;
		const diff = eTotal - sTotal;
		if (diff <= 0)
			return { label: "-", error: "Jam selesai harus setelah jam mulai" };
		const hours = Math.floor(diff / 60);
		const minutes = diff % 60;
		return { label: `${hours} Jam ${minutes} Menit`, error: null };
	};

	const selectedDayWorkTime = calculateWorkTime(startTimeStr, endTimeStr);

	return (
		<div className="font-jakarta">
			{/* Banner */}
			<div className="mb-5 bg-sky-950 py-7 px-10 rounded-xl text-white flex justify-between items-center shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)]">
				<div className="flex flex-col gap-2">
					<div className="text-3xl font-bold">Jurnal Harian</div>
					<div className="text-justify opacity-90">
						Catat aktivitas internship harian Anda secara rutin
						untuk mempermudah penyusunan laporan akhir.
					</div>
				</div>
			</div>

			{/* Main */}
			<div className="flex flex-col lg:flex-row gap-5">
				{/* Left Side */}
				<div className="w-full lg:w-80 flex flex-col gap-5">
					{/* Status */}
					<div className="p-5 font-bold bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-1">
						<div className="text-black text-sm">
							Status Pengisian
						</div>
						<div className="text-black text-2xl flex justify-between items-center">
							<div>
								19{" "}
								<strong className="text-sm text-zinc-500">
									/ 19 Hari
								</strong>
							</div>
							<div className="text-xs px-2 py-1 bg-sky-200 text-sky-800 rounded-full">
								100% Selesai
							</div>
						</div>
						<div className="bg-zinc-300 h-1 rounded mt-1">
							<div className="bg-blue-400 h-1 w-full rounded"></div>
						</div>
					</div>

					{/* Calendar */}
					<div className="bg-white text-black rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] overflow-hidden">
						<DayPicker
							locale={id}
							mode="single"
							selected={selectedDate}
							onSelect={setSelectedDate}
							disabled={[
								{ dayOfWeek: [0] },
								{ before: journalStartDate },
								{ after: new Date() },
							]}
							classNames={{
								selected:
									"outline-3 outline-sky-700 rounded-full",
								month: "p-4",
								// selected: " focus:bg-blue-200",
								// 2. Change the color of the navigation arrows
								// nav_button: "text-red-500 hover:text-red-700",
								// 3. Change the text color of "today" (if it's blue)
								today: "text-sky-500 font-bold",
								nav: "absolute right-2 top-5",
								chevron: "fill-sky-700", // Change the color of the chevron
							}}
						/>
					</div>
				</div>

				{/* Right Side */}
				<div className="flex-1 pb-10">
					<div className="p-5 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-5">
						{/* Header Entri */}
						<div className="text-black flex justify-between items-start border-b pb-4">
							<div>
								<div className="font-bold text-black text-xl">
									Entri Jurnal
								</div>
								<div className="text-zinc-500 text-sm">
									{selectedDate
										? format(
												selectedDate,
												"EEEE, d MMMM yyyy",
												{ locale: id },
											)
										: "Pilih Tanggal"}
								</div>
							</div>
							<div className="flex gap-2 items-center text-xs px-3 py-1 bg-red-100 text-red-700 rounded-full font-bold">
								<PiWarning size={16} />
								<div>Belum Terisi</div>
							</div>
						</div>

						{/* Jam */}
						<div className="space-y-4">
							<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
								<div className="flex flex-col gap-1.5">
									<label className="text-sm font-bold text-black">
										Jam Mulai
									</label>
									<div className="relative">
										<PiClock
											className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-700"
											size={18}
										/>
										<input
											type="time"
											value={startTimeStr}
											onChange={(e) =>
												setStartTimeStr(e.target.value)
											}
											className="pl-10 w-full py-2.5  text-zinc-700 bg-zinc-50 border border-zinc-200 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none"
										/>
									</div>
								</div>
								<div className="flex flex-col gap-1.5">
									<label className="text-sm font-bold text-black">
										Jam Selesai
									</label>
									<div className="relative">
										<PiClock
											className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-700"
											size={18}
										/>
										<input
											type="time"
											value={endTimeStr}
											onChange={(e) =>
												setEndTimeStr(e.target.value)
											}
											className="pl-10 w-full py-2.5 text-zinc-700 bg-zinc-50 border border-zinc-200 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none"
										/>
									</div>
								</div>
							</div>

							{!selectedDayWorkTime.error ? (
								<div className="text-sky-700 bg-sky-50 px-3 py-2 rounded text-sm font-medium border border-sky-100 w-fit">
									Durasi Kerja: {selectedDayWorkTime.label}
								</div>
							) : (
								<div className="text-red-700 bg-red-50 px-3 py-2 rounded text-sm font-medium border border-red-100 w-fit flex items-center gap-2">
									<PiWarning size={16} />
									{selectedDayWorkTime.error}
								</div>
							)}
						</div>

						{/* Textarea */}
						<div className="flex flex-col gap-1.5">
							<label className="text-sm font-bold text-black">
								Deskripsi Aktivitas
							</label>
							<textarea
								placeholder="Jelaskan kegiatan yang dijalankan secara detail"
								className="w-full h-40 p-3 text-zinc-700 bg-zinc-50 border border-zinc-200 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none resize-none"
							/>
						</div>

						{/* Upload */}
						<div className="flex flex-col gap-1.5">
							<label className="text-sm font-bold text-black">
								Lampiran/Dokumen Pendukung
							</label>
							<label className="flex flex-col items-center justify-center p-8 border-2 border-dashed border-zinc-200 bg-zinc-50 rounded-xl cursor-pointer hover:bg-zinc-100 transition-colors group">
								<PiUpload
									className="text-zinc-400 group-hover:text-sky-600 transition-colors"
									size={40}
								/>
								<span className="mt-4 font-bold text-zinc-700">
									Klik untuk upload file
								</span>
								<span className="text-xs text-zinc-500 mt-1">
									PDF, JPG, PNG (Max 5MB)
								</span>
								<input type="file" className="hidden" />
							</label>
						</div>

						{/* Buttons */}
						<div className="flex gap-4 justify-end mt-4 pt-4 border-t">
							<button className="px-5 py-2.5 font-bold text-zinc-600 hover:bg-zinc-100 rounded transition-colors">
								Batal
							</button>
							<button className="px-6 py-2.5 bg-sky-950 text-white font-bold rounded shadow-lg hover:bg-sky-900 transition-colors">
								Simpan Perubahan
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Jurnal;
