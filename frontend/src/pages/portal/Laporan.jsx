import React from "react";
import { PiFileText, PiCloudArrowUp, PiCheckCircle } from "react-icons/pi";

// ICONS
import { PiUpload } from "react-icons/pi";
import { AiOutlineCloudUpload } from "react-icons/ai";
import { HiOutlineDotsCircleHorizontal } from "react-icons/hi";
import { CiTextAlignJustify } from "react-icons/ci";
import { FaRegCircleCheck } from "react-icons/fa6";
import { TiMessages } from "react-icons/ti";
function Laporan() {
	return (
		<div className="font-jakarta">
			{/* Banner */}
			<div className="mb-8 bg-sky-950 py-7 px-10 rounded-xl text-white flex justify-between items-center shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)]">
				<div className="flex flex-col gap-2">
					<div className="text-3xl font-bold">Laporan Akhir</div>
					<div className="text-justify  opacity-90">
						Unggah laporan akhir magang Anda untuk proses penilaian dan verifikasi sertifikat.
					</div>
				</div>
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
				{/* Left: Requirements */}
				<div className="lg:col-span-1">
					<div className="p-6 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-6">
						<h3 className="font-bold text-black border-b pb-3">Persyaratan</h3>
						<ul className="space-y-4">
							{[
								"Format file PDF (Maks. 10MB)",
								"Sudah disetujui pembimbing lapang",
								"Menggunakan template resmi IPB",
								"Melampirkan form penilaian"
							].map((text, i) => (
								<li key={i} className="flex items-start gap-3">
									<PiCheckCircle size={20} className="text-emerald-500 mt-0.5" weight="bold" />
									<span className="text-sm font-medium text-zinc-600">{text}</span>
								</li>
							))}
						</ul>
						<button className="w-full py-2.5 border-2 border-sky-950 text-sky-950 font-bold rounded hover:bg-sky-50 transition-colors text-sm">
							Unduh Template
						</button>
					</div>
				</div>

				{/* Right: Upload Area */}
				<div className="lg:col-span-2">
					<div className="p-8 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-8">
						<div className="flex items-center gap-3 border-b pb-4">
							<PiFileText size={24} className="text-sky-950" weight="bold" />
							<h3 className="text-lg font-bold text-black">Unggah Dokumen</h3>
						</div>

						<div className="flex flex-col gap-6">
							<div className="p-12 border-2 border-dashed border-zinc-200 rounded-xl bg-zinc-50 flex flex-col items-center justify-center gap-4 hover:bg-zinc-100 transition-colors cursor-pointer group">
								<PiCloudArrowUp size={48} className="text-zinc-400 group-hover:text-sky-700 transition-colors" />
								<div className="text-center">
									<p className="text-base font-bold text-black">Klik atau seret file PDF Anda ke sini</p>
									<p className="text-xs text-zinc-500 mt-1">Pastikan file sudah ditandatangani dan discan dengan jelas.</p>
								</div>
								<input type="file" className="hidden" />
							</div>

							<div className="flex items-center gap-4 p-4 bg-amber-50 text-amber-800 rounded-lg border border-amber-200">
								<PiFileText size={24} weight="bold" />
								<div className="text-xs">
									<p className="font-bold">Status: Belum Ada File</p>
									<p className="mt-0.5 opacity-80">Anda belum mengunggah laporan untuk periode ini.</p>
								</div>
							</div>

							<div className="flex justify-end pt-4">
								<button disabled className="px-10 py-2.5 bg-zinc-200 text-zinc-400 font-bold rounded cursor-not-allowed">
									Kirim Laporan
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Laporan;
