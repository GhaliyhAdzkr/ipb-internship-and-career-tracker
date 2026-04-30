import React, { useState } from "react";
import { NavLink } from "react-router-dom";

// icons
import { LuLayoutDashboard } from "react-icons/lu";
import { VscSearch } from "react-icons/vsc";
import { BsClipboardCheck } from "react-icons/bs";
import { MdEditNote } from "react-icons/md";
import { IoDocumentTextOutline } from "react-icons/io5";
import { IoPersonOutline } from "react-icons/io5";

export default function Sidebar() {
	const activeStyle = "text-sky-700 font-bold hover:text-sky-700  bg-white";
	const inactiveStyle = "text-slate-500 hover:text-sky-700";

	return (
		<>
			<div className="w-50 min-h-screen bg-indigo-50 border-r border-neutral-300/20 inline-flex flex-col justify-start items-start">
				<NavLink
					to="/home"
					className="cursor-default self-stretch pb-6 flex flex-col justify-start items-start"
				>
					<div className="self-stretch p-6 inline-flex justify-start items-center gap-3">
						<div className="w-10 h-10 py-2 bg-sky-950 rounded-full flex justify-center items-center">
							<div className="text-center justify-center text-white text-base font-bold font-jakarta leading-6">
								IPB
							</div>
						</div>
						<div className="inline-flex flex-col justify-start items-start">
							<div className="self-stretch flex flex-col justify-start items-start">
								<div className="justify-center text-sky-950 text-xl font-bold font-jakarta leading-7">
									LARAS
								</div>
							</div>
							<div className="self-stretch flex flex-col justify-start items-start">
								<div className="justify-center text-zinc-700 text-xs font-normal font-jakarta leading-4">
									Career Portal
								</div>
							</div>
						</div>
					</div>
				</NavLink>
				<div className="self-stretch flex-1 px-4 flex flex-col justify-start items-start">
					<NavLink
						to="/home"
						className={({ isActive }) =>
							`${isActive ? activeStyle : inactiveStyle} cursor-default self-stretch px-4 py-2 rounded-lg inline-flex justify-start items-center gap-3`
						}
					>
						<div className="inline-flex flex-col justify-start items-start">
							<LuLayoutDashboard className="" size={20} />
						</div>
						<div className="justify-center text-sm  font-jakarta leading-5">
							Beranda
						</div>
					</NavLink>
					<div className="self-stretch pt-2 flex flex-col justify-start items-start">
						<NavLink
							to="/lowongan"
							className={({ isActive }) =>
								`${isActive ? activeStyle : inactiveStyle} cursor-default self-stretch px-4 py-2 rounded-lg inline-flex justify-start items-center gap-3`
							}
						>
							<div className="inline-flex flex-col justify-start items-start">
								<VscSearch className="" size={20} />
							</div>
							<div className="justify-center  text-sm font-jakarta leading-5">
								Cari Lowongan
							</div>
						</NavLink>
					</div>
					<div className="self-stretch pt-2 flex flex-col justify-start items-start">
						<NavLink
							to="/lamaran"
							className={({ isActive }) =>
								`${isActive ? activeStyle : inactiveStyle} cursor-default self-stretch px-4 py-2 rounded-lg inline-flex justify-start items-center gap-3`
							}
						>
							<div className="inline-flex flex-col justify-start items-start">
								<BsClipboardCheck className="" size={20} />
							</div>
							<div className="justify-center  text-sm font-jakarta leading-5">
								Lamaran Saya
							</div>
						</NavLink>
					</div>
					<div className="self-stretch pt-2 flex flex-col justify-start items-start">
						<NavLink
							to="/jurnal"
							className={({ isActive }) =>
								`${isActive ? activeStyle : inactiveStyle} cursor-default self-stretch px-4 py-2 rounded-lg inline-flex justify-start items-center gap-3`
							}
						>
							<div className="inline-flex flex-col justify-start items-start">
								<MdEditNote className="" size={20} />
							</div>
							<div className="justify-center  text-sm font-jakarta leading-5">
								Jurnal Harian
							</div>
						</NavLink>
					</div>
					<div className="self-stretch pt-2 flex flex-col justify-start items-start">
						<NavLink
							to="/laporan"
							className={({ isActive }) =>
								`${isActive ? activeStyle : inactiveStyle} cursor-default self-stretch px-4 py-2 rounded-lg inline-flex justify-start items-center gap-3`
							}
						>
							<div className="inline-flex flex-col justify-start items-start">
								<IoDocumentTextOutline className="" size={20} />
							</div>
							<div className="justify-center  text-sm font-jakarta leading-5">
								Laporan
							</div>
						</NavLink>
					</div>
					<div className="self-stretch pt-2 flex flex-col justify-start items-start">
						<NavLink
							to="/profil"
							className={({ isActive }) =>
								`${isActive ? activeStyle : inactiveStyle} cursor-default self-stretch px-4 py-2 rounded-lg inline-flex justify-start items-center gap-3`
							}
						>
							<div className="inline-flex flex-col justify-start items-start">
								<IoPersonOutline className="" size={20} />
							</div>
							<div className="justify-center  text-sm font-jakarta leading-5">
								Profil
							</div>
						</NavLink>
					</div>
				</div>
			</div>
		</>
	);
}
