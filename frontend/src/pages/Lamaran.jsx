import { useState } from "react";
import Sidebar from "../components/SideNav";
import Navbar from "../components/NavBar";

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
				<div className=" flex-1 flex flex-col">
					<Navbar></Navbar>
					<div className="flex-1 m-5 flex flex-col font-jakarta text-black gap-5">
						<div className="flex flex-col gap-2">
							<div className="text-3xl font-bold">
								Eksplorasi Karirmu
							</div>
							<div className="text-justify w-xl xl:w-full">
								Temukan peluang magang dan karir profesional
								yang telah dikurasi khusus untuk mahasiswa dan
								alumni IPB University.
							</div>
						</div>
						<div className="flex gap-5">
							{/* CARD LOWONGAN SECTION */}
							<section className="flex-1">
								<div className="flex-1 grid grid-cols-3 content-start gap-5">
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
									<div>
										<div className="bg-indigo-50 p-4 h-106 rounded-xl flex flex-col gap-4">
											<div className="font-jakarta font-bold">
												Seleksi Berkas
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
									<div>
										<div className="bg-indigo-50 p-4 h-106 rounded-xl flex flex-col gap-4">
											<div className="font-jakarta font-bold">
												Wawancara
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
			</div>
		</>
	);
}

export default Lowongan;
