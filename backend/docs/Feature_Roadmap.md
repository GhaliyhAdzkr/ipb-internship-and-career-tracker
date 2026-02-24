# Feature List: IPB Internship & Career Tracker (Middleman Model)

**Tech Stack:** FastAPI (Backend), PostgreSQL (SQLAlchemy), Agno/LangGraph (AI Agents), Python Pandas (Automation).

---

## 1. User Management & Authentication (IAM) -> **@Peka**

*Fondasi keamanan dan pengelolaan akses pengguna dengan arsitektur Multi-Schema.*

### 1.1 Authentication & Security (Schema: auth)

* [ ] **Register (Sign Up):** Pendaftaran user baru dengan hashing password (bcrypt).
* *Schema Ref:* Insert ke `auth.users`.
* [ ] **JWT Login (Sign In):** Autentikasi kredensial. Menghasilkan Stateless Access Token dan Stateful Refresh Token.
* *Schema Ref:* Read `auth.users`, insert `auth.user_refresh_tokens`, update `last_login_at`.
* [ ] **Token Rotation & Refresh:** Endpoint untuk memperbarui Access Token menggunakan Refresh Token.
* *Schema Ref:* Query & Update `auth.user_refresh_tokens`.
* [ ] **Role-Based Access Control (RBAC):** Middleware membatasi endpoint secara ketat hanya untuk `ADMIN` dan `STUDENT`.
* [ ] **Device Session Logout:** Mencabut (revoke) sesi perangkat spesifik atau seluruh perangkat.
* *Schema Ref:* Update `auth.user_refresh_tokens.is_revoked`.

### 1.2 User Utilities

* [ ] **Password Reset (Action Tokens):** Mekanisme reset sandi menggunakan token sekali pakai yang dikirim via email.
* *Schema Ref:* Insert/Update `auth.auth_action_tokens`.
* [ ] **Account Activation:** Admin dapat menonaktifkan pengguna bermasalah.
* *Schema Ref:* Update `auth.users.is_active`.

---

## 2. Profile Management (Setup Data) -> **@Peka**

*Manajemen data profil dan entitas referensi utama sistem.*

### 2.1 Master Data (Admin)

* [ ] **Manage Departments:** CRUD data Program Studi dan Fakultas.
* *Schema Ref:* `public.master_departments`.
* [ ] **Manage External Companies:** Katalogisasi perusahaan untuk referensi lowongan (Middleman data).
* *Schema Ref:* `public.master_external_companies`.
* [ ] **Manage Master Skills:** Standarisasi pustaka keahlian untuk *Matching Engine*.
* *Schema Ref:* `public.master_skills`.

### 2.2 Student Profile (Mahasiswa)

* [ ] **Basic Setup & Academic Sync:** Input NIM, Nama, Semester, dan relasi ke Prodi.
* *Schema Ref:* `public.profiles_student`.
* [ ] **CV Upload:** Upload dokumen ke Object Storage, simpan URL.
* *Schema Ref:* Update `public.profiles_student.cv_url`.
* [ ] **Manage Skills:** Penandaan (*tagging*) keahlian teknis/non-teknis yang dimiliki mahasiswa.
* *Schema Ref:* `public.student_skills`.
* [ ] **[AI] CV Parser:** Ekstrak keahlian otomatis dari file PDF CV mahasiswa.
* *Tech:* Agno Agent membaca PDF -> Output JSON Skills -> Insert `public.student_skills`.

### 2.3 Admin Profile (Fasilitator)

* [ ] **Admin Setup:** Input NIP, Nama Lengkap, dan Unit Kerja (contoh: CDA IPB).
* *Schema Ref:* `public.profiles_admin`.

---

## 3. Aggregated Job Board & Discovery -> **@Peka**

*Papan lowongan terpusat yang dikurasi oleh internal IPB.*

### 3.1 Vacancy Management (Admin)

* [ ] **Post External Vacancy:** Posting lowongan yang ditemukan di internet ke dalam sistem (termasuk tipe kompensasi `PAID`/`UNPAID`).
* *Schema Ref:* Insert `public.vacancies` & `public.vacancy_skills`.
* [ ] **Vacancy Scraper Worker:** Background task yang menarik metadata lowongan dari portal publik secara otomatis.
* *Schema Ref:* Insert `public.vacancies` (is_scraped = TRUE).
* [ ] **Auto-Close Scheduler:** Pekerja latar belakang menutup lowongan yang melewati `close_date`.
* *Schema Ref:* Update `public.vacancies.is_active`.

### 3.2 Student Discovery

* [ ] **Advanced Job Search:** Filter lowongan berdasarkan Lokasi, Tipe, dan Kompensasi.
* *Schema Ref:* Query `public.vacancies`.
* [ ] **Save Job (Wishlist):** Menyimpan lowongan incaran beserta catatan pengingat pribadi.
* *Schema Ref:* Insert `public.student_wishlist_vacancies`.
* [ ] **[AI] Job Matching:** Menghitung persentase kecocokan profil pelamar dengan prasyarat lowongan.
* *Logic:* Bandingkan `student_skills` vs `vacancy_skills`.

---

## 4. Self-Reported ATS -> **@Insan**

*Pelacakan status lamaran secara mandiri oleh mahasiswa.*

### 4.1 Application Initialization

* [ ] **Initialize External Apply:** Menekan tombol lamar untuk mengunci CV dan mencatat niat pelamaran sebelum dialihkan ke situs eksternal.
* *Schema Ref:* Insert `public.applications` (copy `cv_url` ke `cv_snapshot_url`).

### 4.2 Self-Reporting Pipeline

* [ ] **Status Update (Self-Report):** Mahasiswa memperbarui status mandiri (contoh: `SCREENING` -> `INTERVIEW`).
* *Schema Ref:* Update `public.applications.status`.
* [ ] **Proof Upload (LoA/Email):** Kewajiban mengunggah bukti tangkapan layar jika status diubah ke `ACCEPTED`.
* *Schema Ref:* Insert `public.application_logs` (mengisi `proof_url`).
* [ ] **History Logging:** Audit otomatis pelacakan waktu setiap perubahan status lamaran.
* *Schema Ref:* Trigger/Insert `public.application_logs`.

### 4.3 Admin Verification

* [ ] **Verify Accepted Application:** Admin meninjau bukti `proof_url` sebelum menyetujui aktivasi penempatan magang.
* *Schema Ref:* Query `public.application_logs` -> Eksekusi ke Placement.

---

## 5. Tracker & Auto-Report Automation -> **@Insan**

*Pencatatan aktivitas magang untuk otomatisasi pelaporan.*

### 5.1 Placement Management

* [ ] **Placement Activation:** Sistem otomatis (atau via verifikasi Admin) membuat rekaman penempatan saat lamaran valid disetujui.
* *Schema Ref:* Insert `public.placements`.

### 5.2 Activity Logging

* [ ] **Daily Log Entry:** Mahasiswa menginput tanggal, jam, draf mentah kegiatan, dan lampiran.
* *Schema Ref:* Insert `public.activity_logs` (mengisi `description_raw`).
* [ ] **[AI] Log Enhancer Worker:** Menyunting tata bahasa draf kegiatan menjadi struktur bahasa profesional secara asinkron.
* *Tech:* Agno Agent membaca `description_raw` -> Output -> Update `public.activity_logs.description_ai_enhanced`.

### 5.3 Auto-Report Generator

* [ ] **Generate Final Report:** Agregasi seluruh logbook yang telah disempurnakan AI menjadi satu dokumen siap cetak.
* *Tech:* Python Pandas + ReportLab (mengonversi data SQL ke PDF/Excel template kampus).
* *Schema Ref:* Caching URL di `public.placements.auto_generated_report_url`.

---

## 6. Analytics & Utilities -> **@Insan**

*Fitur pendukung administratif dan eksplorasi data.*

### 6.1 Internship Distribution

* [ ] **Alumni Distribution Dashboard:** Menampilkan perusahaan mana yang paling banyak menerima mahasiswa dari prodi terkait.
* *Schema Ref:* Query view `public.view_internship_distribution`.

### 6.2 Document Requests

* [ ] **Request Surat Pengantar:** Formulir permohonan surat rekomendasi kampus untuk keperluan pelamaran.
* *Schema Ref:* Insert `public.document_requests`.
* [ ] **PDF Surat Generator:** Script mengonversi permohonan menjadi surat resmi ber-kop, mengunggah ke penyimpanan, dan mengembalikan tautan unduh.
* *Schema Ref:* Update `public.document_requests.generated_url`.

---

## 7. Notification System -> **@Peka**

*Sistem komunikasi asinkron.*

### 7.1 Queue Management

* [ ] **Create Notification:** Menampung antrean pesan notifikasi (misal: "Laporan otomatis Anda sudah siap diunduh").
* *Schema Ref:* Insert `public.notification_queue` (Status: `QUEUED`).
* [ ] **In-App Inbox:** API membaca daftar notifikasi aktif untuk pengguna.
* *Schema Ref:* Query `public.notification_queue`.

### 7.2 Workers

* [ ] **Email Sender Worker:** Background task membaca antrean, mengirimkan email via SMTP, dan mengubah status ke `SENT`.
* [ ] **Garbage Collector Worker:** Cron job membersihkan token kedaluwarsa secara berkala.
* *Schema Ref:* Delete pada `auth.user_refresh_tokens` dan `auth.auth_action_tokens` (berdasarkan Index Parsial).