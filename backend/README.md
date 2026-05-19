# IPB Internship and Career Tracker - Backend

## Deskripsi

LARAS (Launchpad for Apprenticeship, Readiness, And Success) is an intelligent career tracker with state-driven process management, turning fragmented application data into a unified pathway for internship success.

Backend API untuk aplikasi IPB Internship and Career Tracker (LARAS) menggunakan FastAPI dengan Vertical Slice Architecture dan Domain-Driven Design.

## Struktur Folder

```bash
backend/
├── src/
│   └── app_backend/
│       ├── conf/              # Konfigurasi aplikasi (settings backend dan environment)
│       ├── domain/            # Aturan bisnis pada aplikasi
│       ├── features/          # Fitur aplikasi atau services (dengan vertical slices)
│       │   ├── auth/          # Autentikasi
│       │   ├── admin/         # Manajemen admin
│       │   ├── profile/       # Manajemen profil mahasiswa dan admin
│       │   ├── vacancy/       # Lowongan kerja dan pencocokan kerja
│       │   ├── wishlist/      # Wishlist mahasiswa
│       │   └── application/   # Pelacakan lamaran (Self-Reported ATS)
│       ├── models/            # Model database via ORM (1:1 dengan di database)
│       ├── repositories/      # Layer akses data (CRUD)
│       ├── routers/           # Endpoint router untuk request/response
│       ├── schemas/           # Pydantic schemas untuk validasi format data
│       ├── shared/            # Shared utilities (untuk security, cache, dan lainnya)
│       └── main.py            # Entry point aplikasi
├── tests/                     # Unit testing dan integration testing
├── alembic/                   # Database migrations
├── docs/                      # Dokumentasi fitur
└── scripts/                   # Utility scripts
```

## Prinsip Desain & Arsitektur

Project ini menggunakan pendekatan modern untuk menjaga skalabilitas dan maintainability:

1. **Vertical Slice Architecture**: Setiap fitur (seperti `auth`, `vacancy`, `application`) diorganisir dalam satu folder `features`. Setiap slice berisi logic spesifik untuk fitur tersebut, mengurangi ketergantungan antar modul.
2. **Command/Handler Pattern**: Logic bisnis kompleks diimplementasikan menggunakan Command (data) dan Handler (logic). Ini memisahkan *apa yang ingin dilakukan* dengan *bagaimana cara melakukannya*.
3. **Repository Pattern**: Abstraksi akses database berada di folder `repositories`. Ini memudahkan unit testing dan memungkinkan penggantian implementasi database tanpa menyentuh business logic.
4. **Dependency Injection (DI)**: Menggunakan sistem DI bawaan FastAPI. Semua Service dan Repository dikelola melalui `shared/dependencies_service.py` untuk memastikan manajemen instance yang bersih dan testable.
5. **Domain-Driven Design (DDD)**: Logic inti bisnis dan aturan domain diletakkan di folder `domain`, terpisah dari detail infrastruktur (database/API).

## Tech Stack

| Technology | Version | Description |
|------------|---------|-------------|
| Python | >= 3.11 | Programming language |
| FastAPI | ^0.128.0 | Async web framework |
| SQLAlchemy | ^2.0.46 | ORM database |
| PostgreSQL | >= 15 | Database |
| Pydantic | ^2.0.0 | Data validation & serialization |
| Alembic | ^1.11.1 | Database migration tool |
| python-jose | ^3.5.0 | JWT token handling |
| passlib | ^1.7.4 | Password hashing (bcrypt) |
| Celery | ^5.4.0 | Distributed task queue |
| Redis | ^5.2.0 | Message broker untuk Celery |
| LangChain | ^0.3.0 | LLM framework |
| LangGraph | ^0.2.0 | AI agent orchestration |

## Cara Menjalankan

### Prasyarat

- Python 3.11+
- Poetry 1.2+
- PostgreSQL 15+
- Redis (optional, untuk Celery)

### Setup Environment

```bash
# Copy environment file
cp .env.example .env

# Edit .env sesuai kebutuhan
```

### Variabel Lingkungan

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/internship_career_tracker
DATABASE_TEST_URL=postgresql://user:password@localhost:5432/internship_career_tracker_test

# JWT Settings
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=32

# Password Reset
RESET_PASSWORD_TOKEN_EXPIRE_MINUTES=15

# Celery & Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
REDIS_URL=redis://localhost:6379/2

# Environment (development, staging, production)
ENVIRONMENT=development
```

### Menjalankan Aplikasi

```bash
# Install dependencies
make install
# atau
poetry install

# Jalankan migrasi database
poetry run alembic upgrade head

# Jalankan server development
make dev
# atau
poetry run uvicorn app_backend.main:app --reload
```

Server: http://localhost:8000
Dokumentasi API: http://localhost:8000/docs

## Available Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies dengan Poetry |
| `make dev` | Jalankan development server |
| `make test` | Jalankan unit tests |
| `make coverage` | Jalankan tests dengan coverage report |
| `make format` | Format kode dengan Ruff |
| `make lint` | Lint kode dengan Ruff dan Bandit |
| `make up-prod` | Jalankan production Docker Compose (dengan Redis internal terproteksi) |
| `make down-prod` | Hentikan production Docker Compose |
| `make up-dev` | Jalankan development Docker Compose (hanya container app FastAPI) |
| `make down-dev` | Hentikan development Docker Compose |

## Database & Migrasi

Model ORM SQLAlchemy di `src/app_backend/models` adalah source of truth untuk schema database.

```bash
# Buat migrasi baru dari perubahan model
poetry run alembic revision --autogenerate -m "deskripsi perubahan"

# Terapkan migrasi
poetry run alembic upgrade head

# Rollback satu step
poetry run alembic downgrade -1

# Lihat history migrasi
poetry run alembic history
```

## API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /register/student` - Registrasi mahasiswa
- `POST /register/admin` - Registrasi admin (admin only)
- `POST /login` - Login
- `POST /refresh-token` - Refresh access token
- `POST /logout` - Logout
- `POST /password/reset-request` - Request reset password
- `POST /password/reset` - Reset password
- `GET /me` - Ambil info user yang sedang login

### Profile (`/api/v1/profile`)
- `GET /student/me` - Ambil profil mahasiswa
- `PATCH /student/me` - Update profil mahasiswa (skill, CV url, dll)

### Admin (`/api/v1/admin`)
- `PATCH /users/{id}/toggle-active` - Mengubah status aktif/nonaktif user
- CRUD `/departments` - Pengelolaan data departemen
- CRUD `/skills` - Pengelolaan data master skill
- CRUD `/companies` - Pengelolaan data mitra/perusahaan

### Vacancies (`/api/v1/vacancies`)
- `GET /vacancies` - List lowongan aktif (paginated)
- `GET /vacancies/search` - Pencarian lowongan dengan filter detail
- `GET /vacancies/{id}` - Ambil detail lowongan
- `POST /vacancies` - Tambah lowongan baru (admin only)
- `PUT /vacancies/{id}` - Update data lowongan (admin only)
- `DELETE /vacancies/{id}` - Hapus lowongan (admin only)

### Wishlist (`/api/v1/wishlist`)
- `GET /wishlist` - List wishlist mahasiswa
- `POST /wishlist` - Tambah lowongan ke wishlist
- `DELETE /wishlist/{id}` - Hapus dari wishlist

### Job Matching (`/api/v1/job-matching`)
- `GET /job-matching` - Pencocokan lowongan sesuai dengan CV & profil mahasiswa
- `GET /job-matching/{vacancy_id}` - Detail analisis kecocokan (analisis AI)

### Applications (`/api/v1/applications`)
- `POST /applications` - Inisialisasi lamaran mahasiswa
- `GET /applications/my` - Daftar seluruh riwayat lamaran mahasiswa saat ini
- `PATCH /applications/{id}/status` - Update status lamaran (self-reported)
- `POST /applications/{id}/proof` - Upload bukti screenshot Letter of Acceptance (LoA)
- `GET /applications/{id}/history` - Riwayat perubahan status lamaran

### Placements (`/api/v1/placements`)
- `GET /placements/me` - Ambil data penempatan magang aktif mahasiswa
- `GET /placements/{id}/logs` - Ambil daftar log harian (jurnal) penempatan magang
- `POST /placements/{id}/logs` - Input log harian (jurnal) baru
- `PATCH /placements/{id}/logs/{log_id}` - Update entri log harian
- `DELETE /placements/{id}/logs/{log_id}` - Hapus entri log harian
- `POST /placements/{id}/logs/{log_id}/attachment` - Unggah dokumen/gambar lampiran log harian
- `POST /placements/{id}/logs/{log_id}/enhance` - Optimasi deskripsi jurnal harian menggunakan AI
- `POST /placements/{id}/report/generate` - Ajukan pembuatan laporan magang otomatis
- `GET /placements/{id}/report` - Ambil status & link unduhan laporan magang otomatis

### Document Requests (`/api/v1/document-requests`)
- `POST /document-requests` - Ajukan permohonan dokumen baru (e.g. Surat Pengantar)
- `GET /document-requests` - List riwayat pengajuan dokumen mahasiswa
- `GET /document-requests/{id}` - Ambil rincian detail status dokumen

### Notifications (`/api/v1/notifications`)
- `GET /notifications` - Ambil semua notifikasi aktif untuk user
- `GET /notifications/unread-count` - Hitung jumlah notifikasi belum dibaca
- `PATCH /notifications/{id}/read` - Tandai satu notifikasi sudah dibaca
- `DELETE /notifications/{id}` - Hapus notifikasi dari inbox (soft-delete)

### Analytics (`/api/v1/analytics`)
- `GET /analytics/distribution` - Distribusi penempatan magang (admin)
- `GET /analytics/applications` - Analisis statistik lamaran masuk (admin)
- `GET /analytics/vacancies` - Statistik keaktifan lowongan kerja (admin)

## Testing

```bash
# Jalankan semua tests
make test

# Jalankan dengan coverage
make coverage

# Jalankan test spesifik
poetry run pytest tests/test_auth.py -v
```
