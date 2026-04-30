import { useState } from "react";
import Sidebar from "../components/SideNav";
import Navbar from "../components/NavBar";
import data from "../data/items.json";
import { useMediaQuery } from 'react-responsive';

// ICONS
import { FaRegBookmark } from "react-icons/fa6";
import { LuLeaf } from "react-icons/lu";
import { BsSuitcaseLg } from "react-icons/bs";
import { MdOutlineLocationOn } from "react-icons/md";
import { RiShapesLine } from "react-icons/ri";

function Lowongan() {
	const [currentPage, setCurrentPage] = useState(1);
	const isXl = useMediaQuery({ query: '(min-width: 1280px)' });
	const itemsPerPage = isXl ? 9 : 6;

	// 1. Calculate Pagination Indices
	const lastIndex = currentPage * itemsPerPage;
	const firstIndex = lastIndex - itemsPerPage;

	// 2. Slice the JSON array
	const currentCards = data.slice(firstIndex, lastIndex);
	const totalPages = Math.ceil(data.length / itemsPerPage);

	const getPaginationRange = (current, total) => {
		const range = [];
		const delta = 2; // How many pages to show around the current page

		for (let i = 1; i <= total; i++) {
			// Always include first page, last page, and pages around current
			if (
				i === 1 ||
				i === total ||
				(i >= current - delta && i <= current + delta)
			) {
				range.push(i);
			} else if (range[range.length - 1] !== "...") {
				// Add ellipsis if we haven't already
				range.push("...");
			}
		}
		return range;
	};
	const paginationRange = getPaginationRange(currentPage, totalPages);
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
							<div className="text-sm h-fit p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
								<div className="grid grid-cols-4 gap-2">
									<div class="relative col-span-2">
										<input
											type="text"
											id="key"
											placeholder="Posisi, Kata Kunci, atau Perusahaan"
											class="mt-0.5 pl-10 w-full rounded border-gray-300 bg-zinc-50 shadow-sm sm:text-sm "
										/>

										<span class="absolute inset-y-0 left-0 grid w-8 place-content-center text-gray-700 dark:text-gray-200">
											<BsSuitcaseLg className="text-black size-5 ml-2 mt-1" />
										</span>
									</div>
									<div class="relative">
										<input
											type="text"
											id="location"
											placeholder="Semua Lokasi"
											class="mt-0.5 pl-10 w-full rounded border-gray-300 bg-zinc-50 shadow-sm sm:text-sm "
										/>

										<span class="absolute inset-y-0 left-0 grid w-8 place-content-center text-gray-700 dark:text-gray-200">
											<MdOutlineLocationOn className="text-black size-5 ml-2 mt-1" />
										</span>
									</div>
									<div class="relative">
										<input
											type="text"
											id="type"
											placeholder="Semua Tipe"
											class="mt-0.5 pl-10 w-full rounded border-gray-300 bg-zinc-50 shadow-sm sm:text-sm "
										/>

										<span class="absolute inset-y-0 left-0 grid w-8 place-content-center text-gray-700 dark:text-gray-200">
											<RiShapesLine className="text-black size-5 ml-2 mt-1" />
										</span>
									</div>
								</div>
								<div>
									<div>Pencarian Populer</div>
								</div>
							</div>
						</div>
						<div className="flex gap-5">
							{/* FILTER SECTION */}
							<section className="w-70 max-w-70 text-sm h-fit p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
								<div className="font-bold">Filter Detail</div>
								<div className="flex flex-col gap-2">
									<div className="font-bold">
										Bidang Industri
									</div>
									<label class="inline-flex items-center gap-2">
										<input
											type="checkbox"
											class="size-4 rounded border-gray-300"
											id="agreement"
										/>

										<span class="font-medium text-sm text-gray-700">
											Agrikultur dan kehutanan
										</span>
									</label>
									<label class="inline-flex items-center gap-2">
										<input
											type="checkbox"
											class="size-4 rounded border-gray-300"
											id="agreement"
										/>

										<span class="font-medium text-sm text-gray-700">
											Teknologi Informasi
										</span>
									</label>
									<label class="inline-flex items-center gap-2">
										<input
											type="checkbox"
											class="size-4 rounded border-gray-300"
											id="agreement"
										/>

										<span class="font-medium text-sm text-gray-700">
											FMCG & Manufaktur
										</span>
									</label>
									<label class="inline-flex items-center gap-2">
										<input
											type="checkbox"
											class="size-4 rounded border-gray-300"
											id="agreement"
										/>

										<span class="font-medium text-sm text-gray-700">
											Perbankan & Finansial
										</span>
									</label>
								</div>
								<div className="flex flex-col gap-2">
									<div className="font-bold">
										Kualifikasi Akademik
									</div>
									<label class="inline-flex items-center gap-2">
										<input
											type="radio"
											class="size-4 rounded-full border-gray-300"
											id="agreement"
											name="stage"
										/>

										<span class="font-medium text-sm text-gray-700">
											Semua Tingkat
										</span>
									</label>
									<label class="inline-flex items-center gap-2">
										<input
											type="radio"
											class="size-4 rounded-full border-gray-300"
											id="agreement"
											name="stage"
										/>

										<span class="font-medium text-sm text-gray-700">
											Mahasiswa Aktif
										</span>
									</label>
									<label class="inline-flex items-center gap-2">
										<input
											type="radio"
											class="size-4 rounded-full border-gray-300"
											id="agreement"
											name="stage"
										/>

										<span class="font-medium text-sm text-gray-700">
											Fresh Graduate
										</span>
									</label>
								</div>
								<div className="bg-indigo-100 text-center p-2 rounded">
									Terapkan Filter
								</div>
							</section>

							{/* CARD LOWONGAN SECTION */}
							<section className="flex-1">
								<div className="flex-1 grid grid-cols-2 xl:grid-cols-3 content-start gap-5">
									{currentCards.map((item) => (
										<div>
											<div className="flex-1 text-sm self-stretch  p-5 font-jakarta bg-white rounded-xl shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] flex flex-col gap-4">
												<div className="flex gap-2 justify-between items-center">
													<LuLeaf className="size-7 text-zinc-700 bg-indigo-100 rounded p-1" />
													<div className="bg-sky-200 px-2 py-1 h-fit rounded text-[0.6rem] text-black">
														DIKURASI CDA
													</div>
												</div>
												<div className="flex flex-col gap-1">
													<div className=" text-black text-base font-bold">
														{item.name}
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
									))}
								</div>

								{/* PAGINATION */}
								<div className="flex justify-center">
									<div className="mt-10 w-110 flex justify-between items-center gap-2">
										{/* Previous Button */}
										<button
											disabled={currentPage === 1}
											onClick={() =>
												setCurrentPage((p) => p - 1)
											}
											className="px-3 py-1 font-bold disabled:opacity-30"
										>
											&lt;
										</button>
										<div>
											{/* Dynamic Page Numbers */}
											{paginationRange.map(
												(page, index) => {
													if (page === "...") {
														return (
															<span
																key={index}
																className="px-2 text-gray-400"
															>
																...
															</span>
														);
													}

													return (
														<button
															key={index}
															onClick={() =>
																setCurrentPage(
																	page,
																)
															}
															className={`w-10 h-10 rounded transition-all ${
																currentPage ===
																page
																	? "bg-sky-950 text-white font-bold"
																	: "hover:bg-gray-100 text-gray-600"
															}`}
														>
															{page}
														</button>
													);
												},
											)}
										</div>
										{/* Next Button */}
										<button
											disabled={
												currentPage === totalPages
											}
											onClick={() =>
												setCurrentPage((p) => p + 1)
											}
											className="px-3 py-1 disabled:opacity-30"
										>
											&gt;
										</button>
									</div>
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
