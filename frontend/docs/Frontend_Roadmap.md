# IPB Internship & Career Tracker - Frontend Development Roadmap

- **Document Version**: 1.0
- **Last Updated**: May 11, 2026
- **Project**: IPB Internship & Career Tracker Frontend
- **Authors**: Ghaliyh Rayhan Adz Dzikra

---

## Table of Contents

- [API Integration Map](#api-integration-map)
- [Phase 0 Frontend Foundation dan Infrastructure](#phase-0-frontend-foundation-dan-infrastructure)
- [Phase 1 Authentication dan Session Handling](#phase-1-authentication-dan-session-handling)
- [Phase 2 Profile Management dan Master Data UI](#phase-2-profile-management-dan-master-data-ui)
- [Phase 3 Job Board dan Discovery UI](#phase-3-job-board-dan-discovery-ui)
- [Phase 4 Application Tracking UI](#phase-4-application-tracking-ui)
- [Phase 5 Placement dan Activity Tracker UI](#phase-5-placement-dan-activity-tracker-ui)
- [Phase 6 Report dan Document UI](#phase-6-report-dan-document-ui)
- [Phase 7 Analytics dan Dashboard UI](#phase-7-analytics-dan-dashboard-ui)
- [Phase 8 Notification Center UI](#phase-8-notification-center-ui)
- [Data Prefill Requirements](#data-prefill-requirements)

---

## Aturan Pengembangan

### Global Flow

- [x] Setiap card memiliki scope jelas, acceptance criteria, dan For yang ditentukan
- [x] Setiap card memiliki implementation checklist dan test checklist terpisah
- [x] Tidak ada card yang pindah ke Done tanpa bukti review kode dan QA
- [x] Tidak ada phase baru dimulai sebelum test gate phase sebelumnya green

### Prinsip Frontend

- [x] Frontend harus membaca data nyata dari backend untuk fitur yang sudah tersedia endpoint-nya
- [x] State async dikelola konsisten lewat React Query atau hook domain, bukan state lokal yang duplikatif
- [x] Komponen presentational dipisah dari layer data fetching
- [x] Semua halaman protected harus bergantung pada auth state yang benar, tanpa bypass dev di production
- [x] Semua fitur baru harus punya loading, empty, success, dan error state

### Konvensi Integrasi

- [x] Layer API dipecah per domain: auth, profile, vacancy, application, placement, notification, analytics, document
- [x] Token dan session handling dipusatkan di satu client HTTP
- [x] Endpoint yang belum siap backend boleh dipasang sebagai stub sementara, tetapi diberi penanda jelas di roadmap
- [x] Semua fitur baru harus mengikuti visual language proyek yang sudah ada, kecuali ada keputusan desain khusus per halaman

---

## API Integration Map

Bagian ini menjadi peta kerja frontend untuk menentukan halaman mana yang sudah terhubung ke backend dan mana yang masih placeholder.

### Sudah Terkoneksi

- Auth login, register, verify email, forgot password, get me, update profile, dan list departments
- Notifikasi in-app untuk list, unread count, read, dan delete
- Bootstrap auth state melalui React Query

### Perlu Difinalkan

- Halaman lowongan masih memakai data lokal dan perlu diganti ke vacancy endpoint backend
- Halaman lamaran masih statis dan perlu koneksi ke application endpoint
- Halaman jurnal dan laporan masih belum mengambil data placement/activity log nyata
- Dashboard masih menampilkan data contoh dan belum merefleksikan state user secara penuh
- Profil sudah membaca user dan departments, tetapi perlu cek payload update dan state loading/error agar solid

### Prioritas Integrasi

1. Auth dan session consistency
2. Profile dan master data lookup
3. Job board dan vacancy detail
4. Application tracking
5. Placement, journal, dan report
6. Analytics dan notification polish

---

## Phase 0 Frontend Foundation dan Infrastructure

**Objective**: Menyiapkan fondasi frontend yang rapi, konsisten, dan siap dihubungkan ke backend secara bertahap.
**For**: @Raihan, @Ghaliyh

### Setup dan Struktur

- [x] Finalisasi struktur folder `src/api/`, `src/services/`, `src/hooks/`, `src/pages/`, `src/components/`, dan `src/providers/`
- [x] Tetapkan pola pemisahan antara API client, service layer, hook layer, dan UI layer
- [x] Pastikan environment variable API terdefinisi dan fallback default aman untuk local dev
- [x] Setup query provider dan global query defaults untuk loading, retry, dan stale time
- [x] Setup routing dasar untuk public route dan protected route
- [x] Setup layout utama yang konsisten untuk halaman internal

### UX Foundation

- [x] Finalisasi global style, typography, spacing scale, dan warna utama
- [x] Definisikan loading skeleton / spinner / empty state standar
- [x] Definisikan toast atau inline alert pattern untuk success dan error API
- [x] Audit semua halaman agar tidak ada hardcode data yang terlihat seperti data produksi

### Test Gate Phase 0

- [x] Build frontend berhasil tanpa error
- [x] Semua route utama dapat dirender
- [x] Query provider aktif dan dapat dipakai di hook domain

**Exit Criteria**: Struktur frontend stabil, siap dipakai untuk integrasi backend feature-by-feature.

---

## Phase 1 Authentication dan Session Handling

**Objective**: Menyelaraskan alur login, register, verifikasi email, reset password, dan session handling frontend dengan backend.
**For**: @Raihan

### Login dan Register

- [x] Hubungkan form login ke endpoint login backend
- [x] Simpan access token dan refresh token sesuai alur yang disepakati
- [x] Tampilkan pesan error login yang berasal dari response backend
- [x] Hubungkan form registrasi mahasiswa ke endpoint register student
- [x] Tambahkan handling validasi response register yang rapih di UI

### Session dan Guard

- [x] Buat mekanisme auth state yang membaca profile user dari backend setelah login
- [x] Terapkan protected route yang tidak bergantung pada bypass localhost di build production
- [x] Redirect user yang sudah login agar tidak kembali ke halaman auth publik
- [x] Bersihkan token dan cache query ketika logout atau token dianggap invalid

### Password Reset dan Verifikasi Email

- [x] Hubungkan halaman forgot password ke endpoint reset request
- [x] Hubungkan halaman verify email ke endpoint verifikasi token
- [x] Tambahkan state success, loading, dan error yang jelas di kedua halaman

### Test Gate Phase 1

- [x] Login berhasil menyimpan token dan me-render user state
- [x] Token invalid memicu redirect ke login
- [x] Register, verify email, dan reset password menampilkan state API yang benar

**Exit Criteria**: Satu user journey auth selesai end-to-end dan siap dipakai di semua halaman protected.

---

## Phase 2 Profile Management dan Master Data UI

**Objective**: Membuat halaman profil menjadi sumber data utama user dan menghubungkan lookup master data yang diperlukan form.
**For**: @Raihan, @Ghaliyh

### Profil Mahasiswa

- [x] Ambil data profil user dari endpoint me dan tampilkan sebagai source of truth
- [x] Hubungkan update profil ke endpoint update profile backend
- [x] Pastikan field semester, NIM, phone number, LinkedIn, GPA, dan departemen tersinkronisasi benar
- [x] Tambahkan feedback sukses/gagal setelah update profil

### Master Data Lookup

- [x] Ambil daftar departemen dari backend untuk dropdown profil dan registrasi
- [x] Siapkan fallback state jika daftar departemen kosong atau gagal diambil
- [x] Pastikan pencarian departemen di UI tetap responsif untuk data yang cukup besar

### Admin Profile Readiness

- [x] Siapkan pola UI profile card yang bisa menyesuaikan role student atau admin
- [x] Pastikan komponen profile bisa menerima payload berbeda tanpa crash

### Test Gate Phase 2

- [x] Profil menampilkan data backend, bukan placeholder
- [x] Update profil mengembalikan data terbaru di UI
- [x] Dropdown departemen dapat dipakai dari data backend nyata

**Exit Criteria**: Halaman profil benar-benar bergantung pada backend dan tidak lagi terasa sebagai mock form.

---

## Phase 3 Job Board dan Discovery UI

**Objective**: Mengganti lowongan statis menjadi job board yang benar-benar terhubung ke endpoint vacancy backend.
**For**: @Raihan

### Listing Lowongan
- [x] Ganti data lokal lowongan dengan fetch ke endpoint vacancy list/search
- [x] Tambahkan pagination, search, filter lokasi, tipe, dan pembayaran sesuai dukungan backend
- [x] Pastikan card lowongan menampilkan data yang berasal dari backend, termasuk status aktif dan company

### Detail Lowongan
- [x] Hubungkan halaman detail lowongan ke endpoint detail vacancy berdasarkan ID
- [x] Tampilkan requirement, skill, company, lokasi, dan CTA yang sesuai
- [x] Sediakan empty state jika vacancy tidak ditemukan

### Wishlist dan Match
- [x] Integrasikan wishlist student ke backend
- [x] Tampilkan indikator match percentage jika endpoint match tersedia dan data student lengkap
- [x] Buat aksi simpan/hapus wishlist yang terhubung dengan perubahan optimis di UI

### Test Gate Phase 3
- [x] Job board menampilkan vacancy backend dengan pagination
- [x] Search dan filter mengubah hasil secara benar
- [x] Detail lowongan tidak lagi bergantung pada data JSON lokal

**Exit Criteria**: Halaman discovery sudah hidup dengan data backend, bukan mock item.

---

## Phase 4 Application Tracking UI

**Objective**: Menyiapkan tampilan pelacakan lamaran yang dapat membaca status, history, dan aksi yang relevan bagi mahasiswa.
**For**: @Raihan, @Ghaliyh

### Daftar Lamaran

- [ ] Sambungkan halaman lamaran ke data application nyata
- [ ] Tampilkan grouping status seperti applied, screening, interview, offered, accepted, dan rejected
- [ ] Tambahkan empty state bila user belum memiliki aplikasi sama sekali

### Detail dan History

- [ ] Tampilkan detail lamaran per item jika backend menyediakan endpoint detail
- [ ] Tampilkan riwayat status dan proof data yang diperlukan mahasiswa
- [ ] Pastikan label status konsisten dengan backend enum

### Aksi Self-Reporting

- [ ] Tambahkan form update status lamaran sesuai lifecycle yang valid
- [ ] Siapkan upload proof UI untuk status accepted jika diperlukan

### Test Gate Phase 4

- [ ] Status lamaran terbaca dari backend
- [ ] Perubahan status menampilkan response API dan history terbaru
- [ ] UI menolak state yang tidak valid secara visual sebelum request dikirim

**Exit Criteria**: Pengguna dapat memantau dan memperbarui lamaran dari frontend secara jelas.

---

## Phase 5 Placement dan Activity Tracker UI

**Objective**: Menghubungkan jurnal harian, placement, dan aktivitas internship ke data backend yang nyata.
**For**: @Ghaliyh

### Placement Overview

- [ ] Ambil placement aktif user dari backend
- [ ] Tampilkan company, tanggal mulai-selesai, supervisor, dan status penempatan
- [ ] Siapkan kondisi empty bila user belum ditempatkan

### Jurnal Harian

- [ ] Ganti input jurnal statis dengan data harian nyata per placement
- [ ] Tambahkan create/edit/delete flow jika endpoint tersedia
- [ ] Sinkronkan calendar, work time, deskripsi, dan attachment ke backend

### Test Gate Phase 5

- [ ] Halaman jurnal tidak lagi berupa form dummy
- [ ] Data placement aktif muncul di UI
- [ ] Status empty state akurat saat user belum memiliki placement

**Exit Criteria**: Aktivitas internship terlihat sebagai data nyata dan bukan simulasi UI.

---

## Phase 6 Report dan Document UI

**Objective**: Menyajikan laporan akhir dan surat pengantar sebagai pengalaman frontend yang dapat dioperasikan penuh.
**For**: @Ghaliyh

### Laporan Akhir

- [ ] Hubungkan halaman laporan ke endpoint report generation dan report status
- [ ] Tampilkan state not generated, generating, dan ready to download
- [ ] Sediakan tombol unduh file saat URL report tersedia

### Document Request

- [ ] Tambahkan UI untuk request surat pengantar dari frontend
- [ ] Tampilkan riwayat request dokumen dan status prosesnya
- [ ] Gunakan result backend untuk status sukses/gagal dan file generated

### Test Gate Phase 6

- [ ] Laporan akhir dapat dilihat dari state backend
- [ ] Document request dan history terbaca dari UI
- [ ] Link PDF valid dapat dibuka dari frontend

**Exit Criteria**: Fitur dokumen dan laporan dapat dipakai dari frontend secara end-to-end.

---

## Phase 7 Analytics dan Dashboard UI

**Objective**: Mengubah dashboard dari rangkaian card statis menjadi ringkasan data yang benar-benar informatif.
**For**: @Raihan, @Ghaliyh

### Dashboard Overview

- [ ] Ganti angka statis dashboard dengan data ringkasan yang relevan dari backend
- [ ] Tampilkan progress yang sesuai placement, jurnal, atau lamaran user
- [ ] Tambahkan fallback jika user belum punya data aktivitas

### Analytics Admin

- [ ] Siapkan komponen visual untuk data analytics bila user role admin
- [ ] Pastikan chart atau metric card dapat menerima payload backend tanpa hardcode

### Test Gate Phase 7

- [ ] Dashboard menampilkan angka yang berasal dari backend
- [ ] Role-based view bekerja untuk student dan admin
- [ ] Komponen statistik memiliki loading dan empty state

**Exit Criteria**: Dashboard menjadi pusat ringkasan yang benar-benar reflektif terhadap data sistem.

---

## Phase 8 Notification Center UI

**Objective**: Menyajikan notifikasi in-app yang sinkron dengan backend dan dapat dikonsumsi langsung oleh user.
**For**: @Raihan

### Notification Dropdown

- [ ] Sambungkan badge unread count ke backend secara konsisten
- [ ] Pastikan list notifikasi menampilkan title, message, dan timestamp nyata
- [ ] Tambahkan aksi read dan delete yang langsung ter-reflect di UI

### Notification Page / Drawer

- [ ] Siapkan tampilan notifikasi yang lebih lengkap jika dropdown dirasa terlalu sempit
- [ ] Tampilkan loading, empty state, dan error state

### Test Gate Phase 8

- [ ] Badge unread count ter-update saat notifikasi baru masuk
- [ ] Read / delete mengubah tampilan secara benar
- [ ] Notification center tidak crash saat backend kosong atau lambat

**Exit Criteria**: Notifikasi cukup matang untuk dipakai sebagai kanal operasional utama di frontend.

---

## Data Prefill Requirements

Bagian ini adalah syarat penting agar integrasi frontend bisa divalidasi secara visual dan tidak hanya lewat response JSON.

### Prinsip Prefill

- [x] Database harus punya seed data realistis, bukan hanya data minimal untuk foreign key
- [x] Data prefill harus menutupi semua role, state, dan edge case yang perlu ditampilkan di frontend
- [x] Seed data harus aman di-reset untuk development dan test environment
- [x] Semua data prefill harus konsisten antar tabel agar relasi UI tidak putus

### Data Minimum yang Harus Ada

- [x] 1 admin aktif dengan profil lengkap
- [x] Beberapa student aktif dengan profil berbeda: ada yang lengkap, sebagian kosong, dan variasi semester
- [x] Daftar departemen real yang dipakai dropdown profil dan registrasi
- [x] Beberapa company eksternal dengan nama yang familiar dan lokasi berbeda
- [x] Minimal beberapa vacancy aktif dan beberapa vacancy nonaktif untuk test state listing
- [x] Vacancy dengan variasi payment type, location, skill requirement, dan tanggal tutup
- [x] Wishlist student untuk beberapa vacancy
- [x] Application dengan berbagai status agar UI lamaran bisa terlihat hidup
- [x] Placement aktif dan placement selesai untuk membedakan state jurnal dan laporan
- [x] Activity log beberapa hari agar dashboard dan jurnal punya data nyata
- [x] Notification queue dengan unread, read, dan deleted state
- [x] Document request dan generated file contoh untuk flow laporan/dokumen

### Scenario Prefill yang Disarankan

- [x] Student A: profil lengkap, punya placement aktif, punya notifikasi unread, dan punya beberapa lamaran
- [x] Student B: belum placement, punya wishlist dan belum punya jurnal
- [x] Student C: baru registrasi, profil belum lengkap, untuk menguji empty state
- [x] Admin A: dapat melihat analytics, vacancy management, dan notifikasi sistem

### Output yang Harus Terlihat di Frontend

- [x] Dashboard menampilkan angka dan ringkasan yang berbeda untuk tiap user
- [x] Job board menampilkan kartu vacancy dengan variasi status
- [x] Profil menampilkan departemen nyata dan data yang dapat diubah
- [x] Notifikasi badge dan dropdown terlihat aktif
- [x] Jurnal dan laporan menampilkan state nyata, bukan placeholder

---

## Catatan Implementasi

- [x] Dokumen ini adalah living document dan harus di-update setiap kali scope frontend berubah
- [x] Jika backend endpoint belum tersedia, beri penanda jelas sebagai blocker, bukan diam-diam memakai mock permanen
- [x] Setelah integrasi selesai, lakukan review dari sisi UX dan data fidelity sebelum phase ditutup

---

*Dokumen ini adalah living document untuk roadmap frontend. Setiap perubahan scope, urutan phase, atau kebutuhan data prefill harus langsung di-commit ke file ini.*
