<div className="flex justify-between items-center">
										<div>
											<div className="font-bold text-xl">
												Upload Dokumen
											</div>
											<div>
												Format yang diterima : PDF.
												Maksimal ukuran File : 10MB
											</div>
										</div>
										<AiOutlineCloudUpload className="size-8" />
									</div>
									<label
										for="File"
										class="flex flex-col items-center justify-center rounded border border-gray-300 h-70 bg-sky-50 p-4 text-gray-900 shadow-sm sm:p-6"
									>
										<CiTextAlignJustify className="size-20 outline-4 rounded" />
										<div class="mt-4 font-bold text-lg">
											Tarik dan lepas file di sini
										</div>
										<div class="font-medium text-xs">
											atau klik untuk memilih file dari
											komputer anda
										</div>

										<span class="mt-2 inline-block rounded border border-gray-200 bg-gray-50 px-3 py-1.5 text-center text-xs font-medium text-gray-700 shadow-sm hover:bg-gray-100">
											Pilih File
										</span>

										<input
											multiple=""
											type="file"
											id="File"
											class="sr-only "
										/>
									