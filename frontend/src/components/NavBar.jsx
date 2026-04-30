import Sidebar from "../components/SideNav";
import { NavLink } from "react-router-dom";
import { MdNotificationsNone } from "react-icons/md";

function Navbar() {
	return (
		<>
			<nav class="flex items-center justify-end w-full h-16 px-6 bg-white border-b border-gray-100">
				<div class="flex items-center gap-5">
					<div class="relative cursor-pointer group">
						<MdNotificationsNone
							size={26}
							class="text-gray-500 transition-colors group-hover:text-blue-600"
						/>
						<span class="absolute top-0 right-0 w-2.5 h-2.5 bg-red-500 border-2 border-white rounded-full"></span>
					</div>

					<NavLink to="/profil" class="cursor-pointer">
						<div class="w-10 h-10 overflow-hidden rounded-full border-2 border-transparent hover:border-blue-600 transition-all">
							<img
								src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=100&q=80"
								alt="User Profile"
								class="w-full h-full object-cover"
							/>
						</div>
					</NavLink>
				</div>
			</nav>
		</>
	);
}

export default Navbar;
