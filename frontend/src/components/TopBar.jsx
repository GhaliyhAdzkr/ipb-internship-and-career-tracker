import React, { useState } from "react";
import { PiBell, PiUserCircle } from "react-icons/pi";
import { useNotifications } from "../hooks/useNotifications";
import { useAuth } from "../hooks/useAuth";
import { NavLink } from "react-router-dom";

const TopBar = () => {
	const { unreadCount, notifications } = useNotifications();
	const { user } = useAuth();
	const [showNotifications, setShowNotifications] = useState(false);

	return (
		<nav className="flex items-center justify-end w-full h-16 px-6 bg-white border-b border-gray-100 font-jakarta">
			<div className="flex items-center gap-5">
				{/* Notifikasi */}
				<div className="relative group">
					<button 
						onClick={() => setShowNotifications(!showNotifications)}
						className="relative flex items-center justify-center p-1 text-zinc-500 hover:text-sky-700 transition-colors"
					>
						<PiBell size={26} />
						{unreadCount > 0 && (
							<span className="absolute top-0 right-0 w-2.5 h-2.5 bg-red-500 border-2 border-white rounded-full"></span>
						)}
					</button>

					{/* Dropdown Notifikasi */}
					{showNotifications && (
						<div className="absolute right-0 mt-3 w-80 bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.12)] border border-slate-100 overflow-hidden z-20">
							<div className="p-4 border-b border-slate-100 flex justify-between items-center">
								<span className="font-bold text-sky-950">Notifikasi</span>
								<span className="text-xs text-sky-700 font-semibold cursor-pointer hover:underline">Tandai semua dibaca</span>
							</div>
							<div className="max-h-96 overflow-y-auto">
								{notifications.length > 0 ? (
									notifications.map((notif) => (
										<div key={notif.id} className="p-4 border-b border-slate-50 hover:bg-slate-50 transition-colors cursor-pointer">
											<p className="text-sm font-bold text-zinc-800">{notif.title}</p>
											<p className="text-xs text-zinc-500 mt-1 line-clamp-2">{notif.message}</p>
											<span className="text-[10px] text-zinc-400 mt-2 block">{new Date(notif.scheduled_at).toLocaleString()}</span>
										</div>
									))
								) : (
									<div className="p-8 text-center text-zinc-400">
										<p className="text-sm">Tidak ada notifikasi baru</p>
									</div>
								)}
							</div>
						</div>
					)}
				</div>

				{/* Profil */}
				<NavLink to="/app/profil" className="cursor-pointer">
					<div className="w-10 h-10 overflow-hidden rounded-full border-2 border-transparent hover:border-sky-700 transition-all bg-slate-100 flex items-center justify-center">
						{user?.avatar_url ? (
							<img 
								src={user.avatar_url} 
								alt="Profile" 
								className="w-full h-full object-cover"
								referrerPolicy="no-referrer"
							/>
						) : (
							<PiUserCircle size={32} className="text-zinc-600" />
						)}
					</div>
				</NavLink>

			</div>
		</nav>
	);
};

export default TopBar;
