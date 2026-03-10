# IPB Internship and Career Tracker - Backend

## Deskripsi

Backend API untuk aplikasi IPB Internship and Career Tracker menggunakan FastAPI dengan Vertical Slice Architecture (Domain Driven Design).

## Struktur Lengkap

```bash
backend/
├── src/
│   └── app_backend/
│       ├── conf/              # Konfigurasi aplikasi
│       ├── domain/            # Model domain dan business logic
│       ├── features/          # Fitur-fitur aplikasi (vertical slices)
│       ├── models/            # Model ORM (database)
│       ├── routers/           # Endpoint API
│       ├── schemas/           # Schema Pydantic (request/response)
│       ├── scripts/           # Script utilitas
│       ├── shared/            # Utilitas bersama dan helper
│       └── main.py            # Entry point aplikasi
└── tests/                     # Unit dan integration tests
```

## Cara Menjalankan

### Prasyarat

- Python 3.11+
- Poetry 1.2+
- Docker & Docker Compose
- PostgreSQL 15

### Variabel Lingkungan

```bash
cp .env.example .env
```

Edit `.env` sesuai kebutuhan.

### Menjalankan Aplikasi

Instal dependensi:

```bash
make install
```

Jalankan server lokal (development):

```bash
make dev
```

Jalankan formator dan linter:

```bash
make format
make lint
```

Jalankan tes:

```bash
make test
```

Jalankan tes dengan coverage:

```bash
make coverage
```

Server: <http://localhost:8000>
Dokumentasi API: <http://localhost:8000/docs>

## Database & Migrasi

- Model ORM SQLAlchemy di `src/app_backend/models` adalah sumber kebenaran tunggal untuk skema.
- Migrasi Alembic tersimpan di `backend/alembic/versions`.

Perintah umum (jalankan di `backend/`):

```bash
# buat migrasi baru dari perubahan model
poetry run alembic revision --autogenerate -m "deskripsi perubahan"

# terapkan migrasi ke DATABASE_URL yang dikonfigurasi
poetry run alembic upgrade head

# tandai database yang sudah ada sesuai head saat ini (hanya gunakan di production)
poetry run alembic stamp 0001_models_initial
```

Untuk pengembangan, kami merekomendasikan menjalankan aplikasi dengan Poetry (Docker tidak diperlukan):

```bash
poetry install
export DATABASE_URL="<url database lokal atau server Anda>"
poetry run uvicorn app_backend.main:app --reload
```

## Prinsip Desain Sistem

1. Vertical Slice Architecture [Referensi](https://www.jimmybogard.com/vertical-slice-architecture/)
2. Domain-Driven Design (Object-Oriented Domain Modeling) [Referensi](https://en.wikipedia.org/wiki/Domain-driven_design)
3. CQRS Pattern [Referensi](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)

## Dependensi

- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- passlib[bcrypt]
- python-jose[cryptography]
- email-validator
- psycopg2-binary

