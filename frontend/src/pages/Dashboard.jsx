// COMPONENTS
import Sidebar from "../components/SideNav";
import Navbar from "../components/NavBar";
import TheFooter from "../components/TheFooter";

// PACKAGE
import { NavLink } from "react-router-dom";

// ICONS
import { FaRegBookmark } from "react-icons/fa6";
import { MdNotificationsNone } from "react-icons/md";

function Dashboard() {
	return (
		<>
			<div className="flex bg-[#F8F9FF]">
				<Sidebar></Sidebar>
				<div className=" flex-1 flex flex-col justify-between">
					<div>
						<Navbar></Navbar>
						{/* Welcome */}
						<div className="m-5 self-stretch  p-8  bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex justify-between items-center gap-6">
							<h2 className="text-2xl text-black font-jakarta font-bold">
								Selamat Datang Kembali, Budi!
							</h2>
							<NavLink
								to="/jurnal"
								className="px-3 py-2 bg-sky-950 hover:bg-sky-900 text-white rounded"
							>
								Tulis Laporan
							</NavLink>
						</div>
						{/* Cards Progress */}
						<div className="grid grid-cols-3 m-5 gap-5">
							<div className=" self-stretch  p-5 font-jakarta font-bold bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-1">
								<div className=" text-black text-sm ">
									Waktu Tersisa
								</div>
								<div className="text-black text-2xl">
									45 / 60 Hari
								</div>
								<div className="bg-zinc-300 h-1 rounded">
									<div className="bg-blue-400 h-1 w-3/4 rounded"></div>
								</div>
							</div>
							<div className=" self-stretch  p-5 font-jakarta font-bold bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-1">
								<div className=" text-black text-sm ">
									Jurnal Terisi
								</div>
								<div className="text-black text-2xl">
									10 / 15
								</div>
								<div className="bg-zinc-300 h-1 rounded">
									<div className="bg-blue-400 h-1 w-2/3 rounded"></div>
								</div>
							</div>
							<div className=" self-stretch  p-5 font-jakarta font-bold bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-1">
								<div className=" text-black text-sm ">
									Laporan Diunggah
								</div>
								<div className="text-black text-2xl">3 / 3</div>
								<div className="bg-zinc-300 h-1 rounded">
									<div className="bg-blue-400 h-1 w-full rounded"></div>
								</div>
							</div>
						</div>
						{/* Lamaran & Rekomendasi */}
						<div className="grid grid-cols-3  m-5 gap-5">
							{/* Lamaran */}
							<div>
								<div className="flex justify-between items-center py-3 font-jakarta font-bold">
									<div className="text-black ">
										Lamaran Terakhir
									</div>
									<NavLink
										to="/lamaran"
										className="cursor-default text-sm text-sky-950 hover:text-sky-800"
									>
										Selengkapnya
									</NavLink>
								</div>
								<div className=" self-stretch  p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-8">
									<div className="flex justify-between gap-2">
										<div className="text-black text-sm">
											<div className="font-bold">
												Data Analysis Intern
											</div>
											<div>PT GoTo - Gojek Tokopedia</div>
										</div>
										<div className="flex items-center text-xs">
											<div className="bg-red-200 py-1 text-center px-2 w-16 rounded text-red-800 font-bold font-jakarta">
												Ditolak
											</div>
										</div>
									</div>
									<div className="flex justify-between">
										<div className="text-black text-sm">
											<div className="font-bold">
												Software Engineer
											</div>
											<div>Traveloka</div>
										</div>
										<div className="flex items-center text-xs">
											<div className="bg-green-200 py-1 px-2 text-center w-16 rounded text-green-800 font-bold font-jakarta">
												Diterima
											</div>
										</div>
									</div>
								</div>
							</div>
							{/* Rekomendasi Magang*/}
							<div className="col-span-2">
								<div className="flex justify-between items-center py-3 font-jakarta font-bold">
									<div className="text-black ">
										Rekomendasi Magang
									</div>
									<NavLink
										to="/lowongan"
										className="cursor-default text-sm text-sky-950 hover:text-sky-800"
									>
										Selengkapnya
									</NavLink>
								</div>
								<div className="grid grid-cols-2 gap-5">
									<div className="self-stretch  p-5 font-jakarta  bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
										<div className="flex gap-2 justify-between">
											<div className="bg-sky-200 px-2 py-1 rounded text-xs text-black">
												DIKURASI CDA
											</div>
											<FaRegBookmark className="text-zinc-700" />
										</div>
										<div className="flex flex-col gap-1">
											<div className=" text-black text-base font-bold">
												UI / UX Designer Intern
											</div>
											<div className="text-black text-sm">
												Shopee Indonesia
											</div>
										</div>
										<div className="flex gap-2">
											<div className="bg-zinc-200 px-1 py-0.5 rounded text-xs text-black">
												Remote
											</div>
											<div className="bg-zinc-200 px-1 py-0.5 rounded text-xs text-black">
												Paid
											</div>
										</div>
									</div>
									<div className="self-stretch  p-5 font-jakarta  bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
										<div className="flex gap-2 justify-between">
											<div className="bg-sky-200 px-2 py-1 rounded text-xs text-black">
												DIKURASI CDA
											</div>
											<FaRegBookmark className="text-zinc-700" />
										</div>
										<div className="flex flex-col gap-1">
											<div className=" text-black text-base font-bold">
												UI / UX Designer Intern
											</div>
											<div className="text-black text-sm">
												Shopee Indonesia
											</div>
										</div>
										<div className="flex gap-2">
											<div className="bg-zinc-200 px-1 py-0.5 rounded text-xs text-black">
												Remote
											</div>
											<div className="bg-zinc-200 px-1 py-0.5 rounded text-xs text-black">
												Paid
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

export default Dashboard;
