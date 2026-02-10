# Feature List: IPB Internship & Career Tracker

**Tech Stack:** FastAPI (Backend), PostgreSQL (SQLAlchemy), Agno/LangGraph (AI Agents), Python Pandas (Automation).

---

## 1. User Management & Authentication (IAM) -> **@Peka**

*Fondasi keamanan dan pengelolaan akses pengguna.*

### 1.1 Authentication & Security

* [ ] **Register (Sign Up):** Pendaftaran user baru dengan hashing password (bcrypt).
* *Schema Ref:* Insert ke `users`.

* [ ] **Login (Sign In):** Autentikasi email/password dan generate JWT Token.
* *Schema Ref:* Read `users`, update `last_login_at`.

* [ ] **Role-Based Access Control (RBAC):** Middleware membatasi endpoint berdasarkan role (`ADMIN`, `STUDENT`, `COMPANY`, `LECTURER`).

* [ ] **Audit Trail Login:** Mencatat timestamp login terakhir.
* *Schema Ref:* Trigger update `users.last_login_at`.

### 1.2 User Utilities

* [ ] **Password Reset:** Mekanisme reset password via email link token.
* *Schema Ref:* Update `users.password_hash`.

* [ ] **Account Activation:** Admin dapat menonaktifkan user bermasalah.
* *Schema Ref:* Update `users.is_active`.

---

## 2. Profile Management (Setup Data) -> **@Insan**

*Manajemen data profil untuk semua tipe pengguna.*

### 2.1 Master Data (Admin)

* [ ] **Manage Departments:** CRUD data Program Studi.
* *Schema Ref:* `master_departments`.

* [ ] **Manage Master Skills:** Standarisasi nama skill (mencegah duplikasi "Python" vs "python").
* *Schema Ref:* `master_skills`.

* [ ] **Manage Master Courses:** Input mata kuliah dan bobot SKS.
* *Schema Ref:* `master_courses`.

### 2.2 Student Profile (Mahasiswa)

* [ ] **Basic Setup & Academic Sync:** Input NIM, Nama, dan relasi ke Prodi.
* *Schema Ref:* `profiles_student` relasi ke `master_departments`.

* [ ] **CV & Portfolio Upload:** Upload file ke Object Storage, simpan URL.
* *Schema Ref:* Update `profiles_student.cv_url`.

* [ ] **Manage Skills:** Tagging skill yang dimiliki mahasiswa.
* *Schema Ref:* `student_skills`.

* [ ] **AI CV Parser:** Ekstrak skill otomatis dari file PDF CV mahasiswa.
* *Tech:* Agno Agent membaca PDF -> Output JSON Skills -> Insert `student_skills`.

### 2.3 Company & Lecturer Profile

* [ ] **Company Setup & Verification:** Input profil perusahaan dan status verifikasi oleh Admin.
* *Schema Ref:* `profiles_company`.

* [ ] **Lecturer Slot Management:** Mengatur kuota bimbingan maksimal.
* *Schema Ref:* `profiles_lecturer.max_mentoring_slots`.

---

## 3. Job Discovery & Engagement -> **@Peka**

*Fitur pencarian kerja dan interaksi awal (Pre-Application).*

### 3.1 Vacancy Management (Company)

* [ ] **Post Vacancy:** Posting lowongan dengan syarat skill spesifik.
* *Schema Ref:* Insert `vacancies` & `vacancy_skills`.

* [ ] **Auto-Close Scheduler:** Cron job menutup lowongan yang melewati `close_date`.
* *Schema Ref:* Update `vacancies.is_active`.

### 3.2 Student Discovery (Search & Wishlist)

* [ ] **Advanced Job Search:** Filter lowongan by Lokasi, Tipe (MBKM), Gaji.
* *Schema Ref:* Query `vacancies`.

* [ ] **Company Profile Viewing:** Melihat detail perusahaan.
* [ ] **Bookmark Company:** Follow perusahaan favorit.
* *Schema Ref:* Insert `student_bookmarks_company`.

* [ ] **Save Job (Wishlist):** Simpan lowongan dengan catatan pribadi (misal: "Deadline tgl 20").
* *Schema Ref:* Insert `student_wishlist_vacancies`.

* [ ] **🔵 AI Job Matching:** Menghitung % kecocokan profil pelamar vs lowongan.
* *Logic:* Bandingkan `student_skills` vs `vacancy_skills` + Semantik analisis deskripsi.
* *Schema Ref:* Update `applications.match_percentage` (saat apply) atau display dynamic score.

---

## 4. Application Tracking System (ATS) -> **@Insan**

*Manajemen siklus pelamaran (Applied to Accepted).*

### 4.1 Application Workflow

* [ ] **One-Click Apply:** Melamar menggunakan snapshot CV profil tanpa input ulang.
* *Schema Ref:* Insert `applications` (copy `cv_url` ke `cv_snapshot_url`).

* [ ] **Status Pipeline Management:** Update status (`SCREENING` -> `INTERVIEW` -> `OFFERED`).
* *Schema Ref:* Update `applications.status`.

* [ ] **History Logging:** Audit trail otomatis siapa yang mengubah status dan kapan.
* *Schema Ref:* Trigger insert `application_logs`.

* [ ] **Interview Scheduler:** Menambahkan catatan jadwal saat status berubah ke INTERVIEW.
* *Schema Ref:* Insert `application_logs` dengan `reason` berisi jadwal.

### 4.2 Utilities

* [ ] **Withdraw Application:** Mahasiswa membatalkan lamaran.
* *Schema Ref:* Update status `WITHDRAWN`.

---

## 5. Internship Management (The Tracker) -> **@Peka**

*Fase pelaksanaan magang (Post-Accepted).*

### 5.1 Placement Lifecycle

* [ ] **Placement Activation:** Sistem otomatis membuat record placement saat lamaran = `ACCEPTED`.
* *Schema Ref:* Trigger insert `placements` from `applications`.

* [ ] **Assign Lecturer:** Penetapan Dosen Pembimbing untuk placement tersebut.
* *Schema Ref:* Update `placements.lecturer_id`.

* [ ] **Auto-Generate Milestones:** Membuat target otomatis (Laporan Minggu 1, Laporan Akhir) saat placement aktif.
* *Schema Ref:* Bulk Insert `placement_milestones`.

### 5.2 Activity & Logbook

* [ ] **Daily Log Entry:** Input kegiatan harian, durasi, dan bukti.
* *Schema Ref:* Insert `activity_logs`.

* [ ] **Mentor Validation:** Dosen/Mentor approve atau reject logbook.
* *Schema Ref:* Update `activity_logs.status` & `mentor_comment`.

* [ ] **🔵 AI Log Enhancer:** Memperbaiki tata bahasa deskripsi kegiatan agar profesional.
* *Tech:* Agno Agent rewrite `activity_logs.description` (Draft -> Professional).

---

## 6. Academic Integration & Automation -> **@Insan**

*Integrasi dengan kebutuhan administratif kampus (MBKM).*

### 6.1 Document Automation

* [ ] **Request Surat Pengantar:** Form request surat resmi.
* *Schema Ref:* Insert `document_requests`.

* [ ] **PDF Generator Worker:** Script Python membuat PDF surat, upload storage, update URL.
* *Tech:* ReportLab/WeasyPrint.
* *Schema Ref:* Update `document_requests.generated_url`.

### 6.2 SKS Conversion & Export

* [ ] **Activity to Course Mapping:** Mahasiswa memilih mata kuliah untuk dikonversi dari magang.
* *Schema Ref:* Insert `placement_course_conversions`.

* [ ] **SKS Calculation Engine:** Agregasi jam logbook vs bobot SKS mata kuliah.
* *Schema Ref:* Validasi `sum(duration)` vs `master_courses.sks_weight`.

* [ ] **Logbook Export (CSV/Excel):** Konversi data logbook ke format Portal Kampus Merdeka.
* *Tech:* Pandas DataFrame -> Excel Stream.

---

## 7. Notification System -> **@Peka**

*Sistem komunikasi terpusat.*

### 7.1 Queue Management

* [ ] **Create Notification:** Service internal membuat notifikasi (misal: Status berubah).
* *Schema Ref:* Insert `notification_queue` (Status: `QUEUED`).

* [ ] **In-App Inbox:** API untuk list notifikasi user.
* *Schema Ref:* Query `notification_queue`.

### 7.2 Workers

* [ ] **Email Sender Worker:** Background task membaca queue -> kirim email (SMTP) -> update status `SENT`.
* [ ] **Daily Reminder:** Cron job cek deadline milestone -> buat notifikasi H-1.
* *Logic:* Query `placement_milestones` due date.
