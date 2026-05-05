import React from "react";
import { useAuth } from "../hooks/useAuth";
import { PiUserCircle, PiIdentificationCard, PiEnvelope, PiBuildings, PiGraduationCap, PiCamera } from "react-icons/pi";

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
	const { user } = useAuth();

	return (
		<div className="font-jakarta">
			{/* Banner */}
			<div className="mb-8 bg-sky-950 p-10 rounded-xl text-white flex justify-between items-center shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)]">
				<div className="flex flex-col gap-2">
					<div className="text-3xl font-bold">Profil Saya</div>
					<div className="text-justify max-w-xl">
						Kelola informasi pribadi dan akademik Anda untuk verifikasi internship.
					</div>
				</div>
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
				{/* Avatar Card */}
				<div className="lg:col-span-4">
					<div className="p-8 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col items-center text-center gap-6">
						<div className="relative">
							<div className="w-32 h-32 bg-zinc-100 rounded-full flex items-center justify-center border-4 border-white shadow-sm overflow-hidden">
								<PiUserCircle size={100} className="text-zinc-400" />
							</div>
							<button className="absolute bottom-0 right-0 p-2 bg-sky-950 text-white rounded-full shadow-lg hover:bg-sky-900 transition-all">
								<PiCamera size={20} weight="bold" />
							</button>
						</div>
						<div>
							<h3 className="text-xl font-bold text-black">{user?.email?.split('@')[0] || 'User'}</h3>
							<p className="text-xs font-bold text-sky-700 uppercase tracking-widest mt-1">{user?.role || 'STUDENT'}</p>
						</div>
					</div>
				</div>

				{/* Info Card */}
				<div className="lg:col-span-8">
					<div className="p-8 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-8">
						<div className="flex items-center gap-3 border-b pb-4">
							<PiIdentificationCard size={24} className="text-sky-950" weight="bold" />
							<h3 className="text-lg font-bold text-black">Informasi Pribadi</h3>
						</div>

						<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
							<div className="flex flex-col gap-1.5">
								<label className="text-xs font-bold text-zinc-500 uppercase">Nama Lengkap</label>
								<div className="relative">
									<PiUserCircle size={20} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400" />
									<input
										type="text"
										defaultValue={user?.email?.split('@')[0]}
										className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none"
									/>
								</div>
							</div>
							<div className="flex flex-col gap-1.5">
								<label className="text-xs font-bold text-zinc-500 uppercase">Email</label>
								<div className="relative">
									<PiEnvelope size={20} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400" />
									<input
										type="email"
										disabled
										value={user?.email}
										className="pl-10 w-full py-2.5 bg-zinc-200 border border-zinc-200 rounded text-sm text-zinc-500 cursor-not-allowed"
									/>
								</div>
							</div>
							<div className="flex flex-col gap-1.5">
								<label className="text-xs font-bold text-zinc-500 uppercase">Departemen</label>
								<div className="relative">
									<PiBuildings size={20} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400" />
									<input
										type="text"
										defaultValue="Ilmu Komputer"
										className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none"
									/>
								</div>
							</div>
							<div className="flex flex-col gap-1.5">
								<label className="text-xs font-bold text-zinc-500 uppercase">Angkatan</label>
								<div className="relative">
									<PiGraduationCap size={20} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400" />
									<input
										type="text"
										defaultValue="Batch 59"
										className="pl-10 w-full py-2.5 bg-zinc-50 border border-zinc-200 rounded text-sm focus:ring-2 focus:ring-sky-500 outline-none"
									/>
								</div>
							</div>
						</div>

						<div className="flex justify-end mt-4">
							<button className="px-8 py-2.5 bg-sky-950 text-white font-bold rounded hover:bg-sky-900 transition-colors">
								Simpan Perubahan
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Profil;

