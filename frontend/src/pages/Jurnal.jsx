// COMPONENTS
import Sidebar from "../components/SideNav";
import Navbar from "../components/NavBar";
import Test from "../components/Test";
import TheFooter from "../components/TheFooter";

// PACKAGE
import { useState } from "react";
import { DayPicker } from "react-day-picker";
import { parse, differenceInMinutes, format, isBefore } from "date-fns";
import { id } from "date-fns/locale";
import "react-day-picker/style.css";

// ICONS
import { PiWarning } from "react-icons/pi";
import { FaRegClock } from "react-icons/fa";
import { PiUpload } from "react-icons/pi";
import { CiTextAlignJustify } from "react-icons/ci";

function Jurnal() {
	// STATE
	const [selectedDate, setSelectedDate] = useState(new Date());
	const [startDate, setStartDate] = useState(new Date(2026, 3, 7));
	const [startTimeStr, setStartTimeStr] = useState("00:00");
	const [endTimeStr, setEndTimeStr] = useState("00:00");

	// function
	const calculateShift = (selectedDate, startTimeStr, endTimeStr) => {
		// 1. Merge selectedDate with the time strings
		// parse() takes the time, the format, and the 'base date' to apply it to
		const startDateTime = parse(startTimeStr, "HH:mm", selectedDate);
		const endDateTime = parse(endTimeStr, "HH:mm", selectedDate);

		// 2. Calculate total minutes
		let diffMinutes = differenceInMinutes(endDateTime, startDateTime);

		if (isBefore(endDateTime, startDateTime)) {
			return {
				error: "Waktu selesai tidak boleh lebih awal dari waktu mulai",
			};
		}

		// 3. Handle overnight shifts (e.g., 22:00 to 02:00)
		if (diffMinutes < 0) {
			diffMinutes += 24 * 60;
		}

		const hours = Math.floor(diffMinutes / 60);
		const minutes = diffMinutes % 60;

		return {
			hours,
			minutes,
			totalMinutes: diffMinutes,
			label: `${hours} Jam ${minutes} Menit`,
		};
	};
	const selectedDayWorkTime = calculateShift(
		selectedDate,
		startTimeStr,
		endTimeStr,
	);
	return (
		<>
			<div className="flex bg-[#F8F9FF]">
				<Sidebar></Sidebar>
				<div className=" flex-1 flex flex-col">
					<Navbar></Navbar>
					{/* Header */}
					<div className="m-5 flex flex-col font-jakarta text-black gap-5">
						<div className="flex flex-col gap-2">
							<div className="text-3xl font-bold">
								Logbook Magang
							</div>
							<div className="text-justify w-xl xl:w-full">
								Catat aktivitas harian Anda selama periode
								magang. Jurnal ini akan ditinjau oleh dosen
								pembimbing.
							</div>{" "}
						</div>
					</div>
					{/* Main */}
					<div className="flex mx-5 gap-5">
						{/* Left Side */}
						<div className="text-black flex flex-col gap-5">
							{/* Status */}
							<div className=" self-stretch  p-5 font-jakarta font-bold bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-1">
								<div className=" text-black text-sm ">
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
								<div className="bg-zinc-300 h-1 rounded">
									<div className="bg-blue-400 h-1 w-full rounded"></div>
								</div>
							</div>
							{/* Calendar */}
							<DayPicker
								locale={id}
								classNames={{
									month: "p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)]",
									button_next: "mt-10 mr-8",
									button_previous: "mt-10",
									day_button: "size-7 ",
									day: "size-5 text-xs ",
									head_cell: "size-5 font-medium text-xs",
									month_grid:
										"size-5 border-separate border-spacing-2",
									caption_label: "text-xl mt-2 font-bold",
									nav_button: "h-10 w-10",
									week_number_header: "text-xs",
									weekday: "text-sm ",
									MonthsDropdown: "bg-blue-200",
								}}
								captionLayout="label"
								mode="single"
								noonSafe
								fixedWeeks
								numberOfMonths={1}
								showOutsideDays
								timeZone="Asia/Jakarta"
								weekStartsOn={1}
								onSelect={setSelectedDate}
								selected={selectedDate}
								disabled={[
									{ dayOfWeek: [0] },
									{ before: startDate },
									{ after: new Date() },
								]}
								modifiers={{
									afterStartDate: (date) => {
										const isAfterStart = date > startDate;
										const isWeekend = date.getDay() === 0;
										const isBeforeToday = date < new Date();
										return (
											isAfterStart &&
											isBeforeToday &&
											!isWeekend
										);
									},
									beforeStartDate: {
										before: new Date(2026, 1, 1),
									},
								}}
								modifiersClassNames={{
									selected:
										"!bg-sky-500 text-white rounded-full",
									today: "font-bold !bg-sky-900 !text-white ring-3 ring-sky-900 ring-offset-1 ring-offset-white rounded-full underline",
									beforeStartDate: "text-slate-500",
									afterStartDate:
										"bg-slate-200 text-black rounded-full",
								}}
							/>
						</div>
						{/* Right Side */}
						<div className="flex-1 pb-10">
							<div className=" self-stretch p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-3">
								{/* Header Entri */}
								<div className="text-black flex justify-between items-start">
									<div>
										<div className="font-bold text-black text-xl ">
											Entri Jurnal
										</div>
										<div className="text-black">
											{selectedDate
												? selectedDate.toLocaleDateString(
														"id-ID",
														{
															weekday: "long",
															day: "numeric",
															month: "long",
															year: "numeric",
														},
													)
												: "None"}
										</div>
									</div>
									<div className="flex gap-2 font-bold items-center text-xs px-2 py-1 bg-red-200 text-red-800 rounded-full">
										<PiWarning className="size-4" />
										<div>Belum Terisi</div>
									</div>
								</div>
								{/* Jam */}
								<div>
									{/* Input */}
									<div className="grid grid-cols-2 gap-2">
										<div className="text-black">
											<span class="text-sm font-bold">
												{" "}
												Jam Mulai{" "}
											</span>
											<div class="relative ">
												{" "}
												<input
													type="time"
													id="key"
													value={startTimeStr}
													onChange={(e) =>
														setStartTimeStr(
															e.target.value,
														)
													}
													class="mt-0.5 pl-10 w-full rounded border-gray-300  shadow-sm sm:text-sm "
												/>
												<span class="absolute inset-y-0 left-0 grid w-8 place-content-center ">
													<FaRegClock className="text-black size-5 ml-2 mt-1" />
												</span>
											</div>
										</div>
										<div className="text-black">
											<span class="text-sm font-bold">
												{" "}
												Jam Selesai{" "}
											</span>
											<div class="relative ">
												<input
													type="time"
													id="key"
													value={endTimeStr}
													onChange={(e) =>
														setEndTimeStr(
															e.target.value,
														)
													}
													class="mt-0.5 pl-10 w-full rounded border-gray-300  shadow-sm sm:text-sm "
												/>

												<span class="absolute inset-y-0 left-0 grid w-8 place-content-center ">
													<FaRegClock className="text-black size-5 ml-2 mt-1" />
												</span>
											</div>
										</div>
									</div>
									{/* Output */}
									<div>
										{!selectedDayWorkTime?.error && (
											<div className="text-black flex gap-2 text-sm">
												<div>Durasi :</div>
												<div>
													{selectedDayWorkTime.label}
												</div>
											</div>
										)}

										{/* Show error if invalid */}
										{selectedDayWorkTime?.error && (
											<div className="flex gap-2 w-fit items-center text-xs px-2 py-1 bg-red-200 text-red-800 rounded-full">
												<PiWarning className="size-4" />
												{selectedDayWorkTime.error}
											</div>
										)}
									</div>
								</div>
								{/* Textarea */}
								<div className="text-black">
									<span class="text-sm font-bold">
										{" "}
										Deskripsi Aktivitas{" "}
									</span>
									<textarea
										placeholder="Jelaskan kegiatan yang dijalankan secara detail"
										className="mt-0.5 w-full h-50 rounded border-gray-300  shadow-sm sm:text-sm "
									/>
								</div>
								{/* Upload */}
								<div className="text-black">
									<span class="text-sm font-bold">
										{" "}
										Lampiran/Dokumen Pendukung{" "}
									</span>
									<label
										for="File"
										class="flex flex-col items-center rounded border border-gray-300  p-10 text-gray-900 shadow-sm"
									>
										<CiTextAlignJustify className="size-10 outline-2 rounded" />
										<div class="mt-4 font-medium text-sm text-center">
											Tekan untuk unggah atau
											<br />
											seret dokumen anda ke sini
										</div>
										<div class="font-medium text-xs text-slate-400">
											PDF, JPEG, atau PNG (Maks. 5MB)
										</div>

										<input
											multiple=""
											type="file"
											id="File"
											class="sr-only"
										/>
									</label>
								</div>
								{/* Buttons */}
								<div className="flex w-full gap-5 justify-end text-sm">
									<button className="rounded font-bold p-3 text-black">
										Batal
									</button>
									<button className="bg-sky-950 hover:bg-sky-900  rounded  p-3">
										Simpan Perubahan
									</button>
								</div>
							</div>
						</div>
					</div>
					<TheFooter></TheFooter>
				</div>
			</div>
		</>
	);
}

export default Jurnal;
