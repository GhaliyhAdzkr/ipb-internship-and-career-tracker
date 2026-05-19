# LARAS: IPB Internship and Career Tracker - Frontend

LARAS (Launchpad for Apprenticeship, Readiness, And Success) is an intelligent career tracker with state-driven process management, turning fragmented application data into a unified pathway for internship success.

Frontend aplikasi LARAS (Lintasan Arah dan Rencana Aktualisasi Studi) dikembangkan menggunakan **React 19** dan **Vite**, dikombinasikan dengan **Tailwind CSS v4** dan **DaisyUI v5** untuk performa serta estetika UI yang moderen dan premium.

## Perkembangan & Fitur Utama Saat Ini

Berikut adalah perkembangan penting dan perbaikan menyeluruh yang baru saja diterapkan pada sisi frontend untuk meningkatkan kestabilan dan pengalaman pengguna (UX):

1. **Client-Side Schema Validation (Zod & React Hook Form)**
   - Form **Login** (`Login.jsx`) dan **Registrasi** (`Registrasi.jsx`) kini divalidasi menggunakan **Zod** secara penuh pada sisi klien sebelum mengirimkan data ke API Backend.
   - Mencegah *unnecessary roundtrips* ke server dan memberikan feedback error instan yang ramah pengguna langsung di bawah input field masing-masing.
   - Menggunakan hook `useWatch` dari `react-hook-form` untuk mendeteksi ketersediaan email institusi secara real-time, kompatibel sepenuhnya dengan aturan memoization baru dari **React Compiler**.

2. **Pembersihan Logika Backend Polling & Toast**
   - Menghapus komponen polling status koneksi backend global dari `QueryProvider.jsx`.
   - Menghentikan kemunculan berkali-kali dari banner toast "Server Tersambung / Server Terputus" yang mengganggu alur pengoperasian portal oleh mahasiswa.

3. **Optimalisasi Desain Lowongan & Job Cards**
   - Menghapus tombol eksplisit "Detail Lowongan" pada card pekerjaan di halaman Landing maupun Portal.
   - Navigasi detail kini dipicu secara elegan hanya dengan melakukan interaksi hover dan mengklik **judul posisi pekerjaan** (dengan garis bawah/underline yang intuitif).
   - Memperbaiki komponen filter pencarian pada Lowongan Portal dengan kelas `pointer-events-none` pada ikon-ikon SVG, menyelesaikan masalah tidak bisa ditekan/diinput-nya kolom search bar sebelumnya.

4. **Mobile-First Responsive Design**
   - Penyempurnaan responsivitas pada halaman publik, portal mahasiswa, dan panel admin.
   - Desktop tetap menjadi susunan dasar: sidebar kiri dan TopBar kanan tidak diubah pada viewport desktop.
   - Mobile menggunakan bottom navigation, header yang lebih ringkas, modal bottom-sheet, form yang stack per kolom, dan tabel admin dengan horizontal scroll agar tetap dapat diakses.

5. **Integrasi Flow Bisnis Utama**
   - Landing page dan halaman lowongan publik mengambil data real dari endpoint public vacancies, tanpa fallback mock UUID.
   - Detail lowongan publik tidak lagi memanggil endpoint privat `/applications/my` untuk guest user.
   - Flow portal sudah terhubung dari lamaran, upload bukti LoA, perpindahan placement aktif, jurnal harian, upload lampiran, AI enhance deskripsi jurnal, hingga generate laporan.
   - Admin sudah memakai endpoint `/admin/vacancies`, `/admin/vacancies/scrape`, pending verification, verify/reject proof, placement, analytics, dan master data.
   - Kurasi lowongan admin memiliki modal Scrape URL yang mengirim daftar URL ke background task backend, lalu menampilkan hasil impor pending pada tab Hasil Scraping sebelum dipublikasi.

6. **Auth & Session Handling**
   - Token dan refresh token disimpan/dibersihkan konsisten.
   - Guard route tidak memaksa logout saat state user masih loading.
   - Interceptor mencoba refresh token untuk request terproteksi yang menerima `401`.

## Tech Stack & Dependencies

- **React:** ^19.2.0 (UI Library)
- **Vite:** ^7.3.1 (Build Tool & HMR)
- **Tailwind CSS:** ^4.2.0 (Utility CSS Engine)
- **DaisyUI:** ^5.5.18 (Tailwind Component Library)
- **TanStack React Query:** ^5.100.9 (Server State Management)
- **React Hook Form & Zod:** Penanganan validasi form & skema terintegrasi
- **React Icons (Pi):** Iconography set

## Cara Menjalankan

1. Masuk ke direktori frontend:
   ```bash
   cd frontend
   ```
2. Instal seluruh dependensi:
   ```bash
   npm install
   ```
3. Jalankan server lokal development:
   ```bash
   npm run dev
   ```
   Aplikasi akan berjalan di port `http://localhost:5173`.

4. Build untuk mode produksi:
   ```bash
   npm run build
   ```
5. Jalankan verifikasi linting kode:
   ```bash
   npm run lint
   ```
