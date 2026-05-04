// COMPONENTS
import Sidebar from "../components/SideNav";
import Navbar from "../components/NavBar";
import Test from "../components/Test";
import TheFooter from "../components/TheFooter";

// ICONS
import { PiUpload } from "react-icons/pi";
import { AiOutlineCloudUpload } from "react-icons/ai";
import { HiOutlineDotsCircleHorizontal } from "react-icons/hi";
import { CiTextAlignJustify } from "react-icons/ci";
import { FaRegCircleCheck } from "react-icons/fa6";
import { TiMessages } from "react-icons/ti";
function Laporan() {
	return (
		<>
			<div className="flex bg-[#F8F9FF]">
				<Sidebar></Sidebar>
				<div className=" flex-1 flex flex-col">
					<Navbar></Navbar>
					<div className="flex-1 m-5 flex flex-col font-jakarta text-black gap-5">
						{/* Header */}
						<div className="flex flex-col gap-2">
							{/* Teks */}
							<div className="text-3xl font-bold">
								Laporan Akhir Magang
							</div>
							<div className="text-justify w-xl xl:w-full">
								Unggah dan pantau status laporan akhir kegiatan
								magang Anda.
							</div>
						</div>
						{/* Main */}
						<div className="flex gap-5">
							{/* Left Side */}
							<div className="flex-1 flex flex-col gap-5">
								{/* Upload */}
								<div className="flex-1 text-sm self-stretch  p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
									<div className="flex justify-between items-center">
										<div>
											<div className="font-bold text-xl">
												Upload Dokumen
											</div>
											<div>
												Format yang diterima : PDF.
												Maksimal ukuran File : 10MB
											</div>
										</div>
										<AiOutlineCloudUpload className="size-8" />
									</div>
									<label
										for="File"
										class="flex flex-col items-center justify-center rounded border border-gray-300 h-70  p-4 text-gray-900 shadow-sm sm:p-6"
									>
										<CiTextAlignJustify className="size-20 outline-4 rounded" />
										<div class="mt-4 font-bold text-lg">
											Tarik dan lepas file di sini
										</div>
										<div class="font-medium text-xs">
											atau klik untuk memilih file dari
											komputer anda
										</div>

										<span class="mt-2 inline-block rounded border border-gray-200 bg-gray-50 px-3 py-1.5 text-center text-xs font-medium text-gray-700 shadow-sm hover:bg-gray-100">
											Pilih File
										</span>

										<input
											multiple=""
											type="file"
											id="File"
											class="sr-only "
										/>
									</label>
								</div>
								{/* Feedback */}
								<div className="flex-1 text-sm self-stretch  p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
									<div className="flex gap-3 items-center">
										<div className="bg-indigo-50 rounded-full">
											<TiMessages className="size-10 p-2" />
										</div>
										<div className="font-bold text-xl">
											Feedbacks
										</div>
									</div>
									<div className="flex gap-3">
										<img
											src="https://res.cloudinary.com/dhsdxi218/image/upload/v1777055810/samples/man-portrait.jpg"
											className="size-10 rounded-full object-cover"
											alt=""
										/>
										<div className="flex-1 flex flex-col gap-2 p-4 rounded-lg bg-indigo-50">
											<div className="flex justify-between items-center">
												<div>
													<div className="font-bold">
														Dr. Ir. Budi Santoso,
														M.Sc
													</div>
													<div className="text-xs">
														Dosen Pembimbing
													</div>
												</div>
												<div className="text-xs text-slate-500">
													12 Nov 2026, 15:00
												</div>
											</div>
											<div className="text-justify">
												Bab 3 perlu diperjelas pada
												bagian metodologi. Tambahkan
												sitasi jurnal terbaru untuk
												mendukung argumen pemilihan alat
												ukur. Secara keseluruhan sudah
												cukup baik, mohon segera
												direvisi.
											</div>
										</div>
									</div>
								</div>
							</div>
							{/* Right Side */}
							<div className="w-70 max-w-70">
								<div className="text-sm h-fit p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
									<div className="font-bold">
										Status Penilaian
									</div>
									<div className="flex gap-3 items-center py-3 px-5 rounded-lg bg-indigo-50">
										<HiOutlineDotsCircleHorizontal className="size-7 bg-yellow-200 text-yellow-800 rounded-full p-1" />
										<div>
											<div className="font-bold">
												Dosen Pembimbing
											</div>
											<div className="text-xs">
												Menunggu Revisi
											</div>
										</div>
									</div>
									<div className="flex gap-3 items-center py-3 px-5 rounded-lg bg-indigo-50">
										<FaRegCircleCheck className="size-7 bg-green-200 text-green-800 rounded-full p-1" />
										<div>
											<div className="font-bold">
												Dosen Pembimbing
											</div>
											<div className="text-xs">
												Menunggu Revisi
											</div>
										</div>
									</div>
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

export default Laporan;
