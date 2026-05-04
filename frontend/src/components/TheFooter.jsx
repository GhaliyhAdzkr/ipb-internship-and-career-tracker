import { FaInstagram, FaLinkedin, FaWhatsapp, FaYoutube } from "react-icons/fa";

function TheFooter() {
	return (
		<footer class="bg-white">
			<div class="mx-auto max-w-7xl px-4 py-5 sm:px-6 lg:px-8">
				<div class="flex justify-between text-center text-sm text-gray-500 dark:text-gray-400">
					<div>© IPB University LARAS. All Rights Reserved.</div>
					<div className="flex justify-between gap-5">
						<div>Tentang</div>
						<div>Panduan</div>
						<div>Bantuan</div>
						<div>Kontak</div>
					</div>
				</div>
			</div>
		</footer>
	);
}

export default TheFooter;
