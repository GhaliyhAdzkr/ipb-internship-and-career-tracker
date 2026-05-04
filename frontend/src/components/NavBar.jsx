import Sidebar from "../components/SideNav";
import { NavLink } from "react-router-dom";
import { MdNotificationsNone } from "react-icons/md";
import { useState } from "react";
import { RiArrowDropDownLine } from "react-icons/ri";

function Navbar() {
	const [isOpenDropdown, setIsOpenDropdown] = useState(false);
	const navOption = ["Profil", "Logout"];
	const navRoute = ["profil", ""];
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

					<div class="cursor-pointer">
						<div className="relative inline-block text-left">
							<div class="mt-1 w-10 h-10 overflow-hidden rounded-full border-2 border-transparent hover:border-blue-600 transition-all">
								<img
									src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=100&q=80"
									alt="User Profile"
									class="w-full h-full object-cover"
									onClick={() =>
										setIsOpenDropdown(!isOpenDropdown)
									}
								/>
								{isOpenDropdown && (
									<div className="absolute right-0 mt-2 w-fit bg-white border border-gray-200 rounded-md shadow-lg z-10">
										<div className="p-1 text-black flex flex-col">
											{navOption.map((tab, index) => (
												<NavLink
													to={`/${navRoute[index]}`}
													key={index}
													className=" p-1 hover:bg-gray-100 rounded"
													onClick={() => {
														setIsOpenDropdown(
															!isOpenDropdown,
														);
													}}
												>
													{tab}
												</NavLink>
											))}
										</div>
									</div>
								)}
							</div>
						</div>
					</div>
				</div>
			</nav>
		</>
	);
}

export default Navbar;
