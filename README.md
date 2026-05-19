<div align="center">

<h1>LARAS: IPB Internship and Career Tracker Platform</h1>

LARAS (Launchpad for Apprenticeship, Readiness, And Success) is an intelligent career tracker with state-driven process management, turning fragmented application data into a unified pathway for internship success.

<img src="./LARAS_Logo.png" alt="LARAS Logo" width="300">

[![License](https://img.shields.io/badge/License-AFL--3.0-blue)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Poetry Version](https://img.shields.io/badge/Poetry-1.2+-red?logo=poetry)](https://python-poetry.org/)

</div>

---

## Tentang Aplikasi Ini

**LARAS (Lintasan Arah dan Rencana Aktualisasi Studi)** — *Launchpad for Apprenticeship, Readiness, And Success* — adalah platform pelacakan magang dan karir untuk mahasiswa IPB University. Platform ini memfasilitasi pencarian lowongan magang/kerja, pelacakan status lamaran, pencatatan aktivitas harian selama magang, dan pembuatan laporan otomatis. Sistem menggunakan arsitektur Middleman Model di mana admin CDA (Career Development and Alumni) IPB mengkurasi lowongan dari berbagai sumber eksternal.


## Fitur Utama

- **Authentication & Authorization:** Sistem login JWT dengan role-based access control (ADMIN & STUDENT)
- **Profile Management:** Pengelolaan profil mahasiswa dengan skill tagging dan upload CV
- **Job Board:** Papan lowongan terpusat dengan fitur pencarian dan filter
- **Job Matching via CV Parsing:** Pencocokan otomatis profil mahasiswa dengan requirement lowongan menggunakan parsing CV
- **Application Tracking:** Pelacakan status lamaran secara mandiri (Self-Reported ATS)
- **Wishlist:** Simpan lowongan incaran dengan catatan pribadi
- **Placement & Activity Logging:** Pencatatan aktivitas harian selama magang dengan fitur pemoles berbasis AI
- **Document Requests:** Permohonan surat pengantar dan dokumen magang lainnya (Phase 6)
- **Notification System:** Notifikasi *real-time* untuk aktivitas akun dan lamaran (baca, hapus, kelola)
- **Admin Analytics:** Dashboard visual untuk distribusi penempatan, statistik lamaran, dan kinerja lowongan
- **Responsive Portal & Admin UI:** Navigasi portal/admin tetap desktop-first, dengan bottom navigation, modal bottom-sheet, dan layout stack khusus mobile

---

## Project Structure

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
│       │   ├── application/   # Pelacakan lamaran (Self-Reported ATS)
│       │   ├── placement/     # Penempatan magang, jurnal, dan laporan
│       │   ├── document/      # Pengajuan dokumen pendukung
│       │   ├── notification/  # Inbox notifikasi user
│       │   └── analytics/     # Statistik admin dan agregasi dashboard
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
```bash
├── frontend/
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Page components
│   │   └── main.jsx           # Entry point aplikasi
│   └── public/                # Static assets
└── README.md
```

## Tech Stack

### Backend

| Technology | Version | Description |
|------------|---------|-------------|
| Python | >= 3.11 | Programming language |
| FastAPI | ^0.128.0 | Web framework |
| SQLAlchemy | ^2.0.46 | ORM database |
| PostgreSQL | >= 15 | Database |
| Pydantic | ^2.0.0 | Data validation |
| Alembic | ^1.11.1 | Database migration |
| python-jose | ^3.5.0 | JWT authentication |
| passlib | ^1.7.4 | Password hashing (bcrypt) |
| Celery | ^5.4.0 | Background task queue |
| Redis | ^5.2.0 | Message broker |
| LangChain | ^0.3.0 | AI/LLM framework |
| LangGraph | ^0.2.0 | AI agent orchestration |

### Frontend

| Technology | Version | Description |
|------------|---------|-------------|
| React | ^19.2.0 | UI library |
| Vite | ^7.3.1 | Build tool |
| Tailwind CSS | ^4.2.0 | Utility-first CSS |
| DaisyUI | ^5.5.18 | Component library |
| Axios | ^1.13.5 | HTTP client |
| Swiper | ^12.1.2 | Carousel/slider |
| React Icons | ^5.6.0 | Icon library |

## Prerequisites

Pastikan telah terinstall:

- **Python** >= 3.11 ([install guide](https://www.python.org/downloads/))
- **Poetry** >= 1.2 ([install guide](https://python-poetry.org/docs/#installation))
- **Node.js** >= 18 ([install guide](https://nodejs.org/))
- **PostgreSQL** >= 15 ([install guide](https://www.postgresql.org/download/))
- **Docker** (optional, wajib untuk production)

## Installation

Clone repository:

```bash
git clone https://github.com/raihanpka/ipb-internship-and-career-tracker.git
cd ipb-internship-and-career-tracker
```

### Backend Setup

```bash
cd backend

# Copy environment file
cp .env.example .env

# Install dependencies
poetry install

# Run database migrations
poetry run alembic upgrade head

# Start development server
poetry run uvicorn app_backend.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Configuration

### Backend Environment Variables

Edit `backend/.env.example`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/internship_career_tracker

# JWT Settings
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=32

# Environment
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
CREATE_TABLES_ON_STARTUP=false
```

## Status Integrasi Terbaru

- Lowongan publik (`/api/v1/vacancies`) dipakai oleh landing page dan halaman lowongan publik tanpa memanggil endpoint privat.
- Flow lamaran utama sudah terhubung: mahasiswa melamar, update status, upload bukti LoA, admin verifikasi, placement aktif, jurnal harian, lampiran, AI enhance, dan laporan otomatis.
- Surat pengantar dan laporan akhir sudah digenerate oleh task backend; hasilnya disimpan sebagai URL dokumen/laporan dan dikirim via notifikasi.
- Endpoint admin lowongan tersedia di `/api/v1/admin/vacancies`; scraping URL di `/api/v1/admin/vacancies/scrape` berjalan sebagai background task dan masuk sebagai pending kurasi, bukan langsung listing publik.
- Docker backend menjalankan Alembic migration saat startup; schema production tidak bergantung pada `create_all`.
- Frontend sudah diperkuat untuk session persistence, token refresh, dan layout mobile portal/admin tanpa mengubah susunan dasar desktop.

## Available Commands

### Backend

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make dev` | Run development server |
| `make test` | Run tests |
| `make coverage` | Run tests with coverage |
| `make format` | Format code with Ruff |
| `make lint` | Lint code with Ruff & Bandit |
| `make up-prod` | Run production Docker Compose (secured network, local Redis) |
| `make down-prod` | Stop production Docker Compose |
| `make up-dev` | Run development Docker Compose (app-only, external DB/Redis) |
| `make down-dev` | Stop development Docker Compose |
| `poetry run alembic upgrade head` | Apply database migrations |
| `poetry run alembic revision --autogenerate -m "desc"` | Create database migration |

### Frontend

| Command | Description |
|---------|-------------|
| `npm install` | Install dependencies |
| `npm run dev` | Run development server (http://localhost:5173) |
| `npm run build` | Build for production |
| `npm run lint` | Lint code |
| `npm run preview` | Preview production build |

## API Documentation

Setelah backend berjalan, akses dokumentasi API di:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Design Principles

1. **Vertical Slice Architecture** - Setiap fitur diorganisir dalam slice terpisah ([Referensi](https://www.jimmybogard.com/vertical-slice-architecture/))
2. **Domain-Driven Design** - Logic inti bisnis dan aturan domain dipisahkan dari detail infrastruktur ([Referensi](https://en.wikipedia.org/wiki/Domain-driven_design))
3. **Command/Handler Pattern** - Pemisahan antara definisi aksi (Command) dan pelaksana logic (Handler).
4. **Repository Pattern** - Abstraksi akses database untuk memudahkan pengujian dan pemeliharaan.
5. **Dependency Injection** - Manajemen ketergantungan antar komponen untuk kode yang lebih testable dan modular.
6. **CQRS Pattern** - Command Query Responsibility Segregation ([Referensi](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs))

---

## Credits

Project ini dikembangkan oleh **Kelompok 3 (P3)** untuk memenuhi tugas proyek mata kuliah **Analsis dan Desain Sistem (ADS)** dari **Departemen Ilmu Komputer, IPB University**.

**Anggota:**
| Nama | NIM | Role |
|------|-----|------|
| Raihan Putra Kirana | G6401231027 | Project Lead & DevOps Engineer |
| Ghaliyh Rayhan Adz Dzikra | G6401231001 | Frontend Developer & UI/UX Designer |
| Insan Anshary Rasul | G6401231132 | Backend Developer & System Analyst |

---

## License

This project is licensed under the `Academic Free License version 3.0`, see the [LICENSE](LICENSE) file for details.
