// COMPONENTS
import Sidebar from "../components/SideNav";
import Navbar from "../components/NavBar";
import TheFooter from "../components/TheFooter";

// PACKAGE
import { useState } from "react";

// ICONS
import { FaRegBookmark } from "react-icons/fa6";
import { LuLeaf } from "react-icons/lu";
import { BsSuitcaseLg } from "react-icons/bs";
import { MdOutlineLocationOn } from "react-icons/md";
import { RiShapesLine } from "react-icons/ri";

function Lowongan() {
	return (
		<>
			<div className="flex bg-[#F8F9FF]">
				<Sidebar></Sidebar>
				<div className=" flex-1 flex flex-col justify-between">
					<div>
						<Navbar></Navbar>
						<div className="flex-1 m-5 flex flex-col font-jakarta text-black gap-5">
							{/* Header */}
							<div className="flex justify-between items-end">
								<div className="flex flex-col gap-2">
									<div className="text-3xl font-bold">
										Status Lamaran
									</div>
									<div className="text-justify w-xl xl:w-full">
										Pantau perkembangan aplikasi magang dan
										karir Anda. Proses seleksi diurutkan
										berdasarkan tahap terbaru.
									</div>
								</div>
							</div>
							{/* Main */}
							<div className="flex gap-5">
								<section className="flex-1">
									<div className="flex-1 grid grid-cols-3 content-start gap-5">
										{/* Terkirim */}
										<div>
											<div className="bg-indigo-50 h-106 p-4 rounded-xl flex flex-col gap-4">
												<div className="font-jakarta font-bold">
													Terkirim
												</div>
												<div className=" text-sm self-stretch  p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
													<div className="flex gap-2 justify-between items-center">
														<LuLeaf className="size-7 text-zinc-700 bg-indigo-50 rounded p-1" />
														<div className="bg-sky-200 px-2 py-1 h-fit rounded text-[0.6rem] text-black">
															DIKURASI CDA
														</div>
													</div>
													<div className="flex flex-col gap-1">
														<div className=" text-black text-base font-bold">
															Software Engineering
														</div>
														<div className="text-zinc-500 text-sm">
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
										{/* Seleksi */}
										<div>
											<div className="bg-indigo-50 p-4 h-106 rounded-xl flex flex-col gap-4">
												<div className="font-jakarta font-bold">
													Proses Seleksi
												</div>
												<div className=" text-sm self-stretch  p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
													<div className="flex gap-2 justify-between items-center">
														<LuLeaf className="size-7 text-zinc-700 bg-indigo-50 rounded p-1" />
														<div className="bg-sky-200 px-2 py-1 h-fit rounded text-[0.6rem] text-black">
															DIKURASI CDA
														</div>
													</div>
													<div className="flex flex-col gap-1">
														<div className=" text-black text-base font-bold">
															Software Engineering
														</div>
														<div className="text-zinc-500 text-sm">
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
												<div className="text-sm  p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
													<div className="flex gap-2 justify-between items-center">
														<LuLeaf className="size-7 text-zinc-700 bg-indigo-50 rounded p-1" />
														<div className="bg-sky-200 px-2 py-1 h-fit rounded text-[0.6rem] text-black">
															DIKURASI CDA
														</div>
													</div>
													<div className="flex flex-col gap-1">
														<div className=" text-black text-base font-bold">
															Software Engineering
														</div>
														<div className="text-zinc-500 text-sm">
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
										{/* Selesai */}
										<div>
											<div className="bg-indigo-50 p-4 h-106 rounded-xl flex flex-col gap-4">
												<div className="font-jakarta font-bold">
													Selesai
												</div>
												<div className=" text-sm self-stretch  p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
													<div className="flex gap-2 justify-between items-center">
														<LuLeaf className="size-7 text-zinc-700 bg-indigo-50 rounded p-1" />
														<div className="bg-sky-200 px-2 py-1 h-fit rounded text-[0.6rem] text-black">
															DIKURASI CDA
														</div>
													</div>
													<div className="flex flex-col gap-1">
														<div className=" text-black text-base font-bold">
															Software Engineering
														</div>
														<div className="text-zinc-500 text-sm">
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

										<div></div>
									</div>
								</section>
							</div>
						</div>
					</div>
					<TheFooter></TheFooter>
				</div>
				
			</div>
		</>
	);
}

export default Lowongan;
