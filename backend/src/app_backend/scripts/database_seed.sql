
-- IPB Internship & Career Tracker (Seed Data)

-- Step 1: Seed Master Departments (IPB University)
INSERT INTO public.master_departments (id, code, name, faculty) VALUES
  -- Fakultas Pertanian
  (gen_random_uuid(), 'MSL', 'Manajemen Sumberdaya Lahan', 'Fakultas Pertanian'),
  (gen_random_uuid(), 'AGH', 'Agronomi dan Hortikultura', 'Fakultas Pertanian'),
  (gen_random_uuid(), 'PTN', 'Proteksi Tanaman', 'Fakultas Pertanian'),
  (gen_random_uuid(), 'ARL', 'Arsitektur Lanskap', 'Fakultas Pertanian'),
  (gen_random_uuid(), 'SAG', 'Smart Agriculture', 'Fakultas Pertanian'),

  -- Fakultas Perikanan dan Ilmu Kelautan
  (gen_random_uuid(), 'IKL', 'Ilmu dan Teknologi Kelautan', 'Fakultas Perikanan dan Ilmu Kelautan'),
  (gen_random_uuid(), 'THP', 'Teknologi Hasil Perairan', 'Fakultas Perikanan dan Ilmu Kelautan'),
  (gen_random_uuid(), 'MSP', 'Manajemen Sumberdaya Perairan', 'Fakultas Perikanan dan Ilmu Kelautan'),
  (gen_random_uuid(), 'TBP', 'Teknologi dan Manajemen Perikanan Budidaya', 'Fakultas Perikanan dan Ilmu Kelautan'),
  (gen_random_uuid(), 'MPT', 'Teknologi dan Manajemen Perikanan Tangkap', 'Fakultas Perikanan dan Ilmu Kelautan'),

  -- Fakultas Peternakan
  (gen_random_uuid(), 'TPT', 'Teknologi Produksi Ternak', 'Fakultas Peternakan'),
  (gen_random_uuid(), 'NTP', 'Nutrisi dan Teknologi Pakan', 'Fakultas Peternakan'),
  (gen_random_uuid(), 'THT', 'Teknologi Hasil Ternak', 'Fakultas Peternakan'),

  -- Fakultas Kehutanan dan Lingkungan
  (gen_random_uuid(), 'MNH', 'Manajemen Hutan', 'Fakultas Kehutanan dan Lingkungan'),
  (gen_random_uuid(), 'THH', 'Teknologi Hasil Hutan', 'Fakultas Kehutanan dan Lingkungan'),
  (gen_random_uuid(), 'KSHE', 'Konservasi Sumberdaya Hutan & Ekowisata', 'Fakultas Kehutanan dan Lingkungan'),
  (gen_random_uuid(), 'SILV', 'Silvikultur', 'Fakultas Kehutanan dan Lingkungan'),

  -- Fakultas Teknik dan Teknologi
  (gen_random_uuid(), 'TPB', 'Teknik Pertanian dan Biosistem', 'Fakultas Teknik dan Teknologi'),
  (gen_random_uuid(), 'TIN', 'Teknik Industri Pertanian', 'Fakultas Teknik dan Teknologi'),
  (gen_random_uuid(), 'FAT', 'Teknologi Pangan', 'Fakultas Teknik dan Teknologi'),
  (gen_random_uuid(), 'SIL', 'Teknik Sipil dan Lingkungan', 'Fakultas Teknik dan Teknologi'),
  (gen_random_uuid(), 'TMES', 'Teknik Mesin', 'Fakultas Teknik dan Teknologi'),
  (gen_random_uuid(), 'TKIM', 'Teknik Kimia', 'Fakultas Teknik dan Teknologi'),

  -- FMIPA (Beberapa masih di bawah FMIPA atau Sekolah baru, disesuaikan)
  (gen_random_uuid(), 'MET', 'Meteorologi Terapan', 'Fakultas Matematika dan Ilmu Pengetahuan Alam'),
  (gen_random_uuid(), 'BIO', 'Biologi', 'Fakultas Matematika dan Ilmu Pengetahuan Alam'),
  (gen_random_uuid(), 'KIM', 'Kimia', 'Fakultas Matematika dan Ilmu Pengetahuan Alam'),
  (gen_random_uuid(), 'FIS', 'Fisika', 'Fakultas Matematika dan Ilmu Pengetahuan Alam'),
  (gen_random_uuid(), 'BIK', 'Biokimia', 'Fakultas Matematika dan Ilmu Pengetahuan Alam'),
  (gen_random_uuid(), 'BIF', 'Bioinformatika', 'Fakultas Matematika dan Ilmu Pengetahuan Alam'),

  -- Sekolah Sains Data, Matematika, dan Informatika
  (gen_random_uuid(), 'STK', 'Statistika dan Sains Data', 'Sekolah Sains Data, Matematika, dan Informatika'),
  (gen_random_uuid(), 'KOM', 'Ilmu Komputer', 'Sekolah Sains Data, Matematika, dan Informatika'),
  (gen_random_uuid(), 'MAT', 'Matematika', 'Sekolah Sains Data, Matematika, dan Informatika'),
  (gen_random_uuid(), 'AKT', 'Aktuaria', 'Sekolah Sains Data, Matematika, dan Informatika'),
  (gen_random_uuid(), 'AI', 'Kecerdasan Buatan', 'Sekolah Sains Data, Matematika, dan Informatika'),

  -- Fakultas Ekonomi dan Manajemen
  (gen_random_uuid(), 'EKP', 'Ekonomi Pembangunan', 'Fakultas Ekonomi dan Manajemen'),
  (gen_random_uuid(), 'MAN', 'Manajemen', 'Fakultas Ekonomi dan Manajemen'),
  (gen_random_uuid(), 'AGB', 'Agribisnis', 'Fakultas Ekonomi dan Manajemen'),
  (gen_random_uuid(), 'ESL', 'Ekonomi Sumberdaya dan Lingkungan', 'Fakultas Ekonomi dan Manajemen'),
  (gen_random_uuid(), 'EKS', 'Ilmu Ekonomi Syariah', 'Fakultas Ekonomi dan Manajemen'),

  -- Fakultas Ekologi Manusia
  (gen_random_uuid(), 'IKK', 'Ilmu Keluarga dan Konsumen', 'Fakultas Ekologi Manusia'),
  (gen_random_uuid(), 'KPM', 'Komunikasi dan Pengembangan Masyarakat', 'Fakultas Ekologi Manusia'),

  -- Fakultas Kedokteran dan Gizi
  (gen_random_uuid(), 'KED', 'Kedokteran', 'Fakultas Kedokteran dan Gizi'),
  (gen_random_uuid(), 'GIZ', 'Ilmu Gizi', 'Fakultas Kedokteran dan Gizi'),

  -- Sekolah Bisnis
  (gen_random_uuid(), 'BIS', 'Bisnis', 'Sekolah Bisnis'),

  -- Sekolah Kedokteran Hewan dan Biomedis
  (gen_random_uuid(), 'KH', 'Kedokteran Hewan', 'Sekolah Kedokteran Hewan dan Biomedis'),
  (gen_random_uuid(), 'BMD', 'Sains Biomedis', 'Sekolah Kedokteran Hewan dan Biomedis')
ON CONFLICT DO NOTHING;

-- Step 2: Seed Master Companies
INSERT INTO public.master_external_companies (id, name, industry, website_url, address) VALUES
  ('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c61'::uuid, 'Bank Central Asia (BCA)', 'Banking', 'https://karir.bca.co.id', 'Menara BCA, Grand Indonesia, Jakarta'),
  ('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c62'::uuid, 'Bank Mandiri Taspen', 'Banking', 'https://www.bankmandiritaspen.co.id', 'Jakarta Pusat'),
  ('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c63'::uuid, 'Shopee Indonesia', 'E-commerce', 'https://careers.shopee.co.id', 'Pacific Century Place, Jakarta'),
  ('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c64'::uuid, 'Traveloka', 'Technology/Travel', 'https://careers.traveloka.com', 'Wisma 77, Slipi, Jakarta'),
  ('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c65'::uuid, 'FIFGROUP (Astra Financial)', 'Finance', 'https://www.fifgroup.co.id', 'Menara FIF, Jakarta Selatan'),
  ('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c66'::uuid, 'Kompas Gramedia', 'Media', 'https://www.kompasgramedia.com', 'Palmerah Selatan, Jakarta'),
  ('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c67'::uuid, 'BFI Finance', 'Finance', 'https://www.bfi.co.id', 'Tangerang Selatan'),
  ('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c68'::uuid, 'Astro Tech', 'Quick Commerce', 'https://www.astronauts.id', 'Jakarta'),
  ('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c69'::uuid, 'Gojek (GoTo Group)', 'Technology', 'https://career.goto-group.com', 'Pasaraya Blok M, Jakarta')
ON CONFLICT DO NOTHING;

-- Step 3: Seed Vacancies
INSERT INTO public.vacancies (
  id, company_id, title, description, type, open_date, close_date,
  location, payment_type, compensation_min, compensation_max, is_active
) VALUES
  (
    gen_random_uuid(),
    'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c61'::uuid,
    'Magang Bakti Customer Service',
    'Melayani kebutuhan pembukaan rekening nasabah secara online dan memberikan informasi produk perbankan dasar.',
    'INTERNSHIP_GENERAL',
    NOW(),
    NOW() + INTERVAL '60 days',
    'Jakarta (Nasional)',
    'PAID',
    3500000,
    4500000,
    true
  ),
  (
    gen_random_uuid(),
    'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c62'::uuid,
    'HR Recruitment Intern',
    'Membantu tim HR dalam proses screening kandidat, penjadwalan interview, dan administrasi rekrutmen.',
    'INTERNSHIP_GENERAL',
    NOW(),
    NOW() + INTERVAL '30 days',
    'Jakarta Pusat',
    'PAID',
    2000000,
    3000000,
    true
  ),
  (
    gen_random_uuid(),
    'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c63'::uuid,
    'Business Development Intern',
    'Menganalisis tren pasar dan membantu kategori bisnis dalam meningkatkan performa penjualan seller di platform.',
    'INTERNSHIP_GENERAL',
    NOW(),
    NOW() + INTERVAL '45 days',
    'Jakarta Selatan',
    'PAID',
    3000000,
    4000000,
    true
  ),
  (
    gen_random_uuid(),
    'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c64'::uuid,
    'Product Management Intern',
    'Membantu Product Manager dalam melakukan riset user, penyusunan dokumentasi produk, dan koordinasi dengan tim engineering.',
    'MBKM_INTERNSHIP',
    NOW(),
    NOW() + INTERVAL '90 days',
    'Jakarta / Hybrid',
    'PAID',
    4000000,
    5500000,
    true
  ),
  (
    gen_random_uuid(),
    'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c66'::uuid,
    'Digital Content & Campaign Intern',
    'Mengembangkan konten kreatif untuk media sosial dan mengelola kampanye digital di jaringan berita Tribun.',
    'INTERNSHIP_GENERAL',
    NOW(),
    NOW() + INTERVAL '30 days',
    'Jakarta Barat',
    'PAID',
    1500000,
    2500000,
    true
  ),
  (
    gen_random_uuid(),
    'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c67'::uuid,
    'Graphic Designer Internship',
    'Membuat aset visual dan desain kreatif untuk kebutuhan promosi branding perusahaan di berbagai kanal.',
    'INTERNSHIP_GENERAL',
    NOW(),
    NOW() + INTERVAL '60 days',
    'Tangerang',
    'PAID',
    2000000,
    3000000,
    true
  ),
  (
    gen_random_uuid(),
    'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c68'::uuid,
    'Supply & Operation Planning Intern',
    'Mendukung tim operasional dalam merencanakan stok barang dan optimalisasi rantai pasok untuk layanan quick-commerce.',
    'INTERNSHIP_GENERAL',
    NOW(),
    NOW() + INTERVAL '45 days',
    'Jakarta Barat',
    'PAID',
    2500000,
    3500000,
    true
  ),
  (
    gen_random_uuid(),
    'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c69'::uuid,
    'Software Engineer (Backend) - GoPay',
    'Membangun sistem pembayaran yang scalable dan reliable menggunakan Golang/Java untuk jutaan pengguna.',
    'FULL_TIME',
    NOW(),
    NOW() + INTERVAL '120 days',
    'Jakarta Selatan',
    'PAID',
    15000000,
    25000000,
    true
  ),
  (
    gen_random_uuid(),
    'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c63'::uuid,
    'Data Scientist',
    'Mengembangkan model Machine Learning untuk optimasi logistik dan rekomendasi produk.',
    'FULL_TIME',
    NOW(),
    NOW() + INTERVAL '90 days',
    'Jakarta',
    'PAID',
    12000000,
    20000000,
    true
  ),
  (
    gen_random_uuid(),
    'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c61'::uuid,
    'Management Trainee (IT)',
    'Program percepatan karir bagi lulusan baru untuk menjadi leader di divisi IT perbankan.',
    'FULL_TIME',
    NOW(),
    NOW() + INTERVAL '30 days',
    'Jakarta',
    'PAID',
    10000000,
    14000000,
    true
  )
ON CONFLICT DO NOTHING;
