import { NavLink } from "react-router-dom";
import { 
	PiSquaresFour, 
	PiMagnifyingGlass, 
	PiClipboardText, 
	PiNotePencil, 
	PiFileText, 
	PiUser, 
	PiSignOut,
	PiBookmarkSimple,
	PiBriefcaseThin,
	PiBuildingsThin,
	PiUsersThin,
	PiFileTextThin
} from "react-icons/pi";
import { useAuth } from "../hooks/useAuth";

const Sidebar = () => {
	const { logout, user } = useAuth();
	const activeStyle = "text-sky-700 font-bold bg-white shadow-sm";
	const inactiveStyle = "text-slate-500 hover:text-sky-700 transition-colors";

	const isAdmin = user?.role === "ADMIN";

	const navItems = isAdmin ? [
		{ to: "/app/admin/dashboard", icon: PiSquaresFour, label: "Dashboard" },
		{ to: "/app/admin/lowongan", icon: PiBriefcaseThin, label: "Kelola Lowongan" },
		{ to: "/app/admin/verifikasi", icon: PiClipboardText, label: "Verifikasi" },
		{ to: "/app/admin/perusahaan", icon: PiBuildingsThin, label: "Kelola Perusahaan" },
		{ to: "/app/admin/mahasiswa", icon: PiUsersThin, label: "Kelola Mahasiswa" },
		{ to: "/app/admin/master-data", icon: PiFileTextThin, label: "Data Master" },
		{ to: "/app/admin/penempatan", icon: PiBriefcaseThin, label: "Penempatan" },
	] : [
		{ to: "/app/home", icon: PiSquaresFour, label: "Beranda" },
		{ to: "/app/lowongan", icon: PiMagnifyingGlass, label: "Cari Lowongan" },
		{ to: "/app/wishlist", icon: PiBookmarkSimple, label: "Wishlist" },
		{ to: "/app/lamaran", icon: PiClipboardText, label: "Lamaran Saya" },
		{ to: "/app/jurnal", icon: PiNotePencil, label: "Jurnal Harian" },
		{ to: "/app/laporan", icon: PiFileText, label: "Laporan" },
		{ to: "/app/profil", icon: PiUser, label: "Profil" },
	];

	return (
		<div className="fixed inset-x-0 bottom-0 z-40 h-20 bg-indigo-50 border-t border-neutral-300/20 flex font-jakarta lg:sticky lg:top-0 lg:h-screen lg:w-64 lg:border-t-0 lg:border-r lg:flex-col lg:shrink-0">
			{/* Logo Aplikasi */}
			<div className="hidden p-6 lg:flex items-center gap-3 mb-4">
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

			{/* Navigasi */}
			<div className="flex-1 px-2 py-2 flex items-center gap-1 overflow-x-auto lg:items-stretch lg:px-4 lg:py-0 lg:flex-col lg:gap-2">
				{navItems.map((item) => (
					<NavLink
						key={item.to}
						to={item.to}
						className={({ isActive }) =>
							`${isActive ? activeStyle : inactiveStyle} flex min-w-[76px] flex-col items-center justify-center gap-1 px-2 py-2 rounded-lg text-[10px] leading-tight lg:min-w-0 lg:flex-row lg:justify-start lg:gap-3 lg:px-4 lg:py-3 lg:text-sm`
						}
					>
						<item.icon size={20} weight="bold" />
						<span className="max-w-[70px] truncate lg:max-w-none">{item.label}</span>
					</NavLink>
				))}
			</div>

			{/* Keluar */}
			<div className="hidden p-4 mt-auto lg:block">
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
