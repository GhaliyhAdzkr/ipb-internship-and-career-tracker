import React from "react";
import { NavLink } from "react-router-dom";
import { 
  PiSquaresFour, 
  PiMagnifyingGlass, 
  PiClipboardText, 
  PiNotePencil, 
  PiFileText, 
  PiUser, 
  PiSignOut 
} from "react-icons/pi";
import { useAuth } from "../hooks/useAuth";

const Sidebar = () => {
	const { logout } = useAuth();
	const activeStyle = "text-sky-700 font-bold bg-white shadow-sm";
	const inactiveStyle = "text-slate-500 hover:text-sky-700 transition-colors";

	const navItems = [
		{ to: "/home", icon: PiSquaresFour, label: "Beranda" },
		{ to: "/lowongan", icon: PiMagnifyingGlass, label: "Cari Lowongan" },
		{ to: "/lamaran", icon: PiClipboardText, label: "Lamaran Saya" },
		{ to: "/jurnal", icon: PiNotePencil, label: "Jurnal Harian" },
		{ to: "/laporan", icon: PiFileText, label: "Laporan" },
		{ to: "/profil", icon: PiUser, label: "Profil" },
	];

	return (
		<div className="sticky top-0 h-screen w-64 bg-indigo-50 border-r border-neutral-300/20 flex flex-col font-jakarta shrink-0">
			{/* Brand */}
			<div className="p-6 flex items-center gap-3 mb-4">
				<img 
					src="/logo/laras.png" 
					alt="LARAS Logo" 
					className="w-10 h-10 object-contain"
				/>
				<div className="flex flex-col">
					<div className="text-sky-950 text-xl font-bold leading-7">
						LARAS
					</div>
					<div className="text-zinc-700 text-[10px] font-bold uppercase tracking-wider">
						Career Portal
					</div>
				</div>
			</div>

			{/* Navigation */}
			<div className="flex-1 px-4 flex flex-col gap-2">
				{navItems.map((item) => (
					<NavLink
						key={item.to}
						to={item.to}
						className={({ isActive }) =>
							`${isActive ? activeStyle : inactiveStyle} flex items-center gap-3 px-4 py-3 rounded-lg text-sm`
						}
					>
						<item.icon size={20} weight="bold" />
						<span>{item.label}</span>
					</NavLink>
				))}
			</div>

			{/* Logout */}
			<div className="p-4 mt-auto">
				<button 
					onClick={logout}
					className="flex items-center gap-3 w-full px-4 py-3 text-slate-500 hover:text-red-600 transition-colors text-sm font-bold"
				>
					<PiSignOut size={20} weight="bold" />
					<span>Keluar</span>
				</button>
			</div>
		</div>
	);
};

export default Sidebar;

