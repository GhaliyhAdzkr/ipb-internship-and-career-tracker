// COMPONENTS
import Sidebar from "../components/SideNav";
import Navbar from "../components/NavBar";
import Test from "../components/Test";
import TheFooter from "../components/TheFooter";

// PACKAGE
import React, { useState } from "react";

// ICONS
import { PiUpload } from "react-icons/pi";
import { AiOutlineCloudUpload } from "react-icons/ai";
import { HiOutlineDotsCircleHorizontal } from "react-icons/hi";
import { CiTextAlignJustify } from "react-icons/ci";
import { FaRegCircleCheck } from "react-icons/fa6";
import { TiMessages } from "react-icons/ti";

function Profil() {
	const [activeTab, setActiveTab] = useState(0);
	const tabs = ["Data Personal", "Data Akademik", "Dokumen"];
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
								Pengaturan Profil{" "}
							</div>
							<div className="text-justify w-xl xl:w-full">
								Kelola informasi personal, data akademik, dan
								dokumen pendukung Anda
							</div>
						</div>
						{/* Profile Cards */}
						<div className="flex gap-4 items-center text-sm self-stretch  p-10 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] ">
							<img
								src="https://res.cloudinary.com/dhsdxi218/image/upload/v1777055810/samples/man-portrait.jpg"
								className="size-25 rounded-full object-cover"
								alt=""
							/>
							<div className="flex flex-col gap-4">
								<div className="text-2xl font-bold">
									Budi Santoso
								</div>
								<div className="flex gap-5">
									<div>
										<div className="tracking-widest text-xs text-slate-600">
											NIM
										</div>
										<div>G6401231001</div>
									</div>
									<div>
										<div className="tracking-widest text-xs text-slate-600">
											PROGRAM STUDI
										</div>
										<div>Ilmu Komputer</div>
									</div>
									<div>
										<div className="tracking-widest text-xs text-slate-600">
											FAKULTAS
										</div>
										<div>SSMI</div>
									</div>
								</div>
							</div>
						</div>
						{/* Tabs */}
						<div className="flex gap-2 p-1 w-fit text-sm font-jakarta rounded ">
							{tabs.map((tab, index) => (
								<button
									key={index}
									onClick={() => setActiveTab(index)}
									className={`px-4 py-2 rounded transition-colors ${
										activeTab === index
											? "text-black bg-white font-bold shadow-sm"
											: "text-black hover:bg-gray-100"
									}`}
								>
									{tab}
								</button>
							))}
						</div>
						<div
							className={`${activeTab == 0 ? "block" : "hidden"}`}
						>
							<div className="grid grid-cols-2 gap-4 items-start text-sm self-stretch  p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] ">
								<div>
									<div>Nama Lengkap</div>
									<input
										type="text"
										placeholder="Budi Santoso"
										className="mt-2 w-full text-black rounded border-gray-300 shadow-sm"
									/>
								</div>
								<div>
									<div>Email Universitas</div>
									<input
										type="text"
										placeholder="BudiSant0s0@apps.ipb.ac.id"
										className="mt-2 w-full text-black rounded border-gray-300 shadow-sm"
									/>
								</div>
								<div>
									<div>Nomor Telepon</div>
									<input
										type="text"
										placeholder="+62 811-1704-2204"
										className="mt-2 w-full text-black rounded border-gray-300 shadow-sm"
									/>
								</div>
								<div>
									<div>Alamat Domisili</div>
									<textarea
										type="text"
										placeholder="Komplek MPR, DPR, DPD Jl. Jend. Gatot Subroto, Senayan, Jakarta Pusat 10270"
										className="mt-2 w-full h-30 text-black rounded border-gray-300 shadow-sm"
									/>
								</div>
								<div>
									<div>Tautan Linkedin</div>
									<input
										type="text"
										placeholder="linkedin.com/in/ghaliyhra/"
										className="mt-2 w-full text-black rounded border-gray-300 shadow-sm"
									/>
								</div>
								<div>
									<div>Tautan Portofolio / GitHub</div>
									<input
										type="text"
										placeholder="github.com/GhaliyhAdzkr"
										className="mt-2 w-full text-black rounded border-gray-300 shadow-sm"
									/>
								</div>
								<div></div>
								<div className="flex gap-4 justify-end">
									<button className=" py-3 px-6 rounded font-bold">
										Batal
									</button>
									<button className="bg-sky-950 text-white py-3 px-6 rounded font-bold">
										Simpan Perubahan
									</button>
								</div>
							</div>
						</div>
						<div
							className={`${activeTab == 1 ? "block" : "hidden"}`}
						>
							<div className="grid grid-cols-2 gap-4 items-center text-sm self-stretch  p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] ">
								<div>
									<div>NIM</div>
									<input
										type="text"
										placeholder="G6401231001"
										className="mt-2 w-full text-black rounded border-gray-300 shadow-sm"
									/>
								</div>
								<div>
									<div>IPK</div>
									<input
										type="text"
										placeholder="3.99"
										className="mt-2 w-full text-black rounded border-gray-300 shadow-sm"
									/>
								</div>
								<div>
									<div>Program Studi</div>
									<input
										type="text"
										placeholder="Ilmu Komputer"
										className="mt-2 w-full text-black rounded border-gray-300 shadow-sm"
									/>
								</div>
								<div>
									<div>Fakultas</div>
									<input
										type="text"
										placeholder="SSMI"
										className="mt-2 w-full text-black rounded border-gray-300 shadow-sm"
									/>
								</div>
								<div>
									<div>Tahun Masuk</div>
									<input
										type="text"
										placeholder="2023"
										className="mt-2 w-full text-black rounded border-gray-300 shadow-sm"
									/>
								</div>
								<div>
									<div>Status</div>
									<input
										type="text"
										placeholder="Mahasiswa Aktif"
										className="mt-2 w-full text-black rounded border-gray-300 shadow-sm"
									/>
								</div>
								<div></div>
								<div className="flex gap-4 justify-end">
									<button className=" py-3 px-6 rounded font-bold">
										Batal
									</button>
									<button className="bg-sky-950 text-white py-3 px-6 rounded font-bold">
										Simpan Perubahan
									</button>
								</div>
							</div>
						</div>
						<div
							className={`${activeTab == 2 ? "block" : "hidden"}`}
						>
							<div className="flex-1 text-sm self-stretch  p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
								<div className="flex justify-between items-center">
									<div>
										<div className="font-bold text-xl">
											Upload Dokumen
										</div>
										<div>
											Format yang diterima : PDF. Maksimal
											ukuran File : 10MB
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
						</div>
					</div>
					{/* Main */}
					<TheFooter></TheFooter>
				</div>
			</div>
		</>
	);
}

export default Profil;
