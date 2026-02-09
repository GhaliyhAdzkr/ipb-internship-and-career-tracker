# Feature Roadmap

## 1. Fitur Dasar (Foundation / MVP)

*Fitur ini wajib ada untuk menggantikan proses manual yang "rapuh" dan menyelesaikan masalah diskoneksi data dasar.*

### Portal Lowongan Terpusat & Terkurasi

- **Fungsi:** Menggantikan model "Broadcast" (satu arah) menjadi database lowongan yang dapat dicari (searchable) dan dilamar langsung.
- **Solusi untuk:** Fragmentasi informasi di mana mahasiswa harus mencari info di situs, tapi melamar lewat email terpisah.

### Status Pelacakan Real-time (Application Status Tracker)

- **Fungsi:** Mahasiswa dapat melihat status lamaran secara transparan: *Terkirim* → *Ditinjau Dosen* → *Ditinjau Mitra* → *Wawancara* → *Diterima/Ditolak*.
- **Solusi untuk:** Menghilangkan fenomena "Black Hole" dan kecemasan mahasiswa karena tidak tahu nasib lamarannya.

### Integrasi Data Akademik (Sinergi Student Portal)

- **Fungsi:** Single Sign-On (SSO) dengan akun IPB. Sistem otomatis menarik data mahasiswa (NIM, Jurusan, SKS yang sudah ditempuh) tanpa perlu input ulang manual saat melamar.
- **Solusi untuk:** Mengurangi kesalahan input data dan mempercepat proses administrasi awal.

---

## 2. Fitur Fungsional & Efisiensi (Automation)

*Fitur ini berfokus pada penghapusan "pekerjaan sibuk" (busywork) administratif yang memakan waktu 20-30 jam per semester.*

### Generator Surat Otomatis (Auto-Generate Documents)

- **Fungsi:** Sistem membuatkan Proposal Magang dan Surat Pengantar Fakultas secara otomatis dalam format PDF resmi hanya dengan satu klik "Request", menggunakan data profil yang sudah tersimpan.
- **Solusi untuk:** Memangkas waktu pembuatan surat dari 2-3 jam menjadi <5 menit dan menghilangkan antrean fisik tanda tangan.

### Manajemen Logbook Terpadu (Single-Entry Logbook)

- **Fungsi:** Formulir logbook harian digital yang hasilnya bisa diekspor (export) ke format Kampus Merdeka maupun format Laporan Akhir IPB.
- **Solusi untuk:** Menghapus beban *double-entry* (input ganda) yang selama ini dilakukan mahasiswa untuk kepatuhan administrasi yang berbeda-beda.

### Papan Kanban Visual (Drag-and-Drop Interface)

- **Fungsi:** Tampilan visual mirip Trello/Huntr di mana mahasiswa bisa memindahkan kartu lamaran dari kolom *Wishlist*, *Applied*, *Interview*, hingga *Offer*.
- **Solusi untuk:** Memberikan rasa kontrol (gamifikasi) dan mempermudah visualisasi *pipeline* karier mahasiswa agar lebih terorganisir.

---

## 3. Fitur Cerdas Pendukung Akademik (Academic Intelligence)

*Fitur ini menjembatani kesenjangan antara dunia kerja dan kurikulum (SKS).*

### Kalkulator Rekomendasi Konversi SKS (Smart Mapping)

- **Fungsi:** Saat melihat lowongan, sistem menganalisis *Job Description* dan mencocokkannya dengan Capaian Pembelajaran Lulusan (CPL) mata kuliah. Contoh: "Posisi ini memiliki kecocokan 90% dengan Mata Kuliah Manajemen Pemasaran".
- **Solusi untuk:** Membantu mahasiswa dan dosen dalam memetakan konversi SKS secara objektif, bukan sekadar kira-kira.

### Sistem Peringatan Dini (Early Warning Notification)

- **Fungsi:** Notifikasi otomatis via Email/WA. Contoh: "H+3 Wawancara: Jangan lupa kirim email Terima Kasih" atau "Batas waktu upload laporan akhir tinggal 2 hari".
- **Solusi untuk:** Meningkatkan *conversion rate* lamaran dan mencegah mahasiswa lupa tenggat waktu administratif.

---

## 4. Fitur Lanjutan & Ekosistem (Advanced Ecosystem)

*Fitur ini untuk menyaingi "Shadow IT" (aplikasi komersial) dan memberikan data strategis bagi kampus.*

### Ekstensi Peramban (IPB Web Clipper)

- **Fungsi:** *Browser extension* (Chrome/Edge) yang memungkinkan mahasiswa "menyimpan" lowongan dari LinkedIn, JobStreet, atau Kalibrr langsung ke dalam dashboard IPB Tracker mereka dengan satu klik.
- **Solusi untuk:** Menangkap data aktivitas mahasiswa di luar sistem kampus (eksternal) agar universitas tidak kehilangan jejak data (*data trail*).

### Dasbor Analitik Departemen (Business Intelligence)

- **Fungsi:** Memberikan data agregat kepada Kaprodi/Departemen. Contoh insight: "40% Mahasiswa Agribisnis gagal di tahap Tes Teknis di perusahaan FMCG".
- **Solusi untuk:** Bahan evaluasi kurikulum berbasis data nyata pasar kerja, mendeteksi kelemahan kompetensi mahasiswa secara spesifik.

### Penilaian Digital Mitra Industri

- **Fungsi:** Portal khusus bagi pembimbing lapangan (perusahaan) untuk memberi nilai dan *feedback* kinerja mahasiswa secara online tanpa kertas, mirip sistem UI.
- **Solusi untuk:** Mempercepat proses penilaian akhir dan memastikan *feedback* industri terdokumentasi dengan baik.

---

## 5. Spesifikasi Teknis API

Berikut adalah rincian spesifikasi teknis untuk pengembangan API (Application Programming Interface) aplikasi **IPB Internship & Career Tracker**. Daftar ini dipecah dari level infrastruktur paling dasar hingga fitur bisnis utama, disesuaikan dengan masalah inefisiensi dan kebutuhan integrasi data.

### Modul Sistem Inti & Keamanan (Core System & Security)

Fondasi ini penting untuk memastikan data aman dan tercatat, mengingat masalah hilangnya jejak data (*data trail*) pada sistem lama.

- **Autentikasi & Otorisasi (Auth Service)**
  - `POST /auth/login-sso`: Integrasi dengan LDAP/SSO IPB (Single Sign-On) agar mahasiswa menggunakan akun IPB atau Google misalnya.
  - `POST /auth/refresh-token`: Manajemen JWT (JSON Web Token) untuk sesi pengguna.

- **Audit Logging (Activity Tracker)**
  - `POST /logs/activity`: Mencatat setiap aksi krusial (misal: "Mahasiswa A mengunduh Surat Pengantar", "Dosen B menyetujui lamaran"). Ini solusi untuk masalah "kebutaan data" universitas.
  - `GET /logs/history`: Endpoint untuk admin melihat riwayat aktivitas jika terjadi sengketa administrasi.

### Modul Manajemen Pengguna (User Profile Service)

Fokus pada pengurangan input berulang (*redundant data entry*) yang membebani mahasiswa.

- **Profil Mahasiswa**
  - `GET /profile/me`: Mengambil data akademik (NIM, Jurusan, IPK, SKS) langsung dari database IPB agar mahasiswa tidak perlu input manual.
  - `PUT /profile/cv-data`: Update data khusus karier (Skill, Pengalaman Organisasi) untuk *CV builder*.

- **Profil Mitra/Perusahaan**
  - `GET /companies/{id}`: Detail perusahaan mitra.
  - `POST /companies/review`: (Fitur masa depan) Mahasiswa memberi ulasan anonim terhadap tempat magang.

### Modul Manajemen Magang & Lamaran (Internship Core)

Ini adalah "jantung" aplikasi yang menerapkan logika *State Design Pattern* untuk mengatasi masalah status lamaran yang tidak jelas.

- **Lowongan (Vacancy)**
  - `GET /vacancies`: List lowongan dengan filter (Prodi, Lokasi, Tipe Magang).
  - `GET /vacancies/{id}/compatibility`: Menghitung skor kecocokan otomatis antara *Job Desc* dengan *Capaian Pembelajaran* mahasiswa (Logika pemetaan >80% cocok).

- **Pelacakan Lamaran (Application Tracker)**
  - `POST /applications/apply`: Submit lamaran (menyimpan state awal: *Draft/Submitted*).
  - `PUT /applications/{id}/status`: Endpoint krusial untuk mengubah status (*State Object*).
    - Jika status berubah jadi "Accepted", trigger notifikasi ke Dosen.
    - States: `Wishlist` → `Applied` → `Interview` → `Accepted` → `Rejected`.
  - `GET /applications/kanban`: Mengambil semua lamaran mahasiswa dalam format yang dikelompokkan berdasarkan status untuk visualisasi papan Kanban.

### Modul Dokumen & Otomatisasi (Document Engine)

Dirancang untuk memangkas waktu administrasi manual yang memakan waktu 2-3 jam menjadi instan.

- **Generator Dokumen**
  - `POST /documents/generate-letter`: Input (ID Mahasiswa + ID Perusahaan) → Output (PDF Surat Pengantar resmi bertanda tangan digital).
  - `POST /documents/generate-proposal`: Membuat proposal magang dasar berdasarkan template dinamis data akademik.

- **Manajemen File (Storage)**
  - `POST /files/upload`: Upload bukti penerimaan (LoA) atau Laporan Akhir.
  - `GET /files/{id}/preview`: Preview dokumen tanpa harus download.

### Modul Notifikasi (Notification Service)

Solusi untuk masalah "Black Hole" dan keterlambatan informasi.

- **Pengiriman Pesan**
  - `POST /notifications/send`: Service internal untuk mengirim Email atau WhatsApp (via 3rd party API).
  - Trigger Otomatis:
    - "Reminder: H+3 Interview (Follow-up)".
    - "Alert: Surat Pengantar Anda sudah terbit".

- **Inbox Dalam Aplikasi**
  - `GET /notifications/inbox`: List notifikasi di dalam aplikasi web/mobile.

### Modul Akademik & MBKM (Academic Integration)

Menangani konversi nilai dan pelaporan agar tidak terjadi *double entry*.

- **Logbook Harian**
  - `POST /logbook/entry`: Input kegiatan harian.
  - `POST /logbook/export`: Mengonversi data logbook internal menjadi format laporan MBKM/Kampus Merdeka (Excel/PDF).

- **Penilaian & Konversi**
  - `POST /assessment/mentor-score`: Endpoint bagi pembimbing industri memasukkan nilai secara digital (menggantikan form kertas).
  - `GET /assessment/sks-simulation`: Simulasi konversi SKS berdasarkan aktivitas yang telah di-log.

### Arsitektur Alur Data (Contoh Penerapan State Object)

Sesuai rekomendasi OOP pada laporan, API `PUT /applications/{id}/status` harus memiliki logika transisi:

1. **Input:** Mahasiswa update status ke "Accepted".
2. **API Logic:**
     - Validasi bukti penerimaan (cek file upload).
     - Update status database.
     - *Auto-Trigger:* Panggil `POST /documents/generate-letter` (Surat Balasan).
     - *Auto-Trigger:* Panggil `POST /notifications/send` (Info ke Dosen Pembimbing).
3. **Output:** Status Kanban berubah, Dosen ternotifikasi, Surat siap unduh.
