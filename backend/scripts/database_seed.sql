-- ============================================================================
-- IPB Internship & Career Tracker - Seed Data
-- ============================================================================
-- Execute this AFTER running supabase_schema.sql
-- Run in Supabase SQL Editor
-- ============================================================================

-- Step 1: Seed Master Departments
-- ============================================================================
INSERT INTO public.master_departments (id, code, name, faculty) VALUES
  ('550e8400-e29b-41d4-a716-446655440001'::uuid, 'TI', 'Teknik Informatika', 'FMIPA'),
  ('550e8400-e29b-41d4-a716-446655440002'::uuid, 'SI', 'Sistem Informasi', 'FMIPA'),
  ('550e8400-e29b-41d4-a716-446655440003'::uuid, 'IF', 'Ilmu Komputer', 'FMIPA'),
  ('550e8400-e29b-41d4-a716-446655440004'::uuid, 'TE', 'Teknik Elektro', 'FT'),
  ('550e8400-e29b-41d4-a716-446655440005'::uuid, 'TM', 'Teknik Mesin', 'FT'),
  ('550e8400-e29b-41d4-a716-446655440006'::uuid, 'TB', 'Teknologi Bioproses', 'FTP'),
  ('550e8400-e29b-41d4-a716-446655440007'::uuid, 'AGR', 'Agronomi', 'FP'),
  ('550e8400-e29b-41d4-a716-446655440008'::uuid, 'MGT', 'Manajemen', 'FEB'),
  ('550e8400-e29b-41d4-a716-446655440009'::uuid, 'AKT', 'Akuntansi', 'FEB'),
  ('550e8400-e29b-41d4-a716-446655440010'::uuid, 'AEC', 'Ekonomi dan Studi Pembangunan', 'FEB')
ON CONFLICT DO NOTHING;

-- Step 2: Seed Master Skills
-- ============================================================================
INSERT INTO public.master_skills (id, name, category) VALUES
  ('660e8400-e29b-41d4-a716-446655440001'::uuid, 'Python', 'Programming Language'),
  ('660e8400-e29b-41d4-a716-446655440002'::uuid, 'JavaScript', 'Programming Language'),
  ('660e8400-e29b-41d4-a716-446655440003'::uuid, 'Java', 'Programming Language'),
  ('660e8400-e29b-41d4-a716-446655440004'::uuid, 'React', 'Frontend Framework'),
  ('660e8400-e29b-41d4-a716-446655440005'::uuid, 'Vue.js', 'Frontend Framework'),
  ('660e8400-e29b-41d4-a716-446655440006'::uuid, 'FastAPI', 'Backend Framework'),
  ('660e8400-e29b-41d4-a716-446655440007'::uuid, 'Node.js', 'Backend Runtime'),
  ('660e8400-e29b-41d4-a716-446655440008'::uuid, 'PostgreSQL', 'Database'),
  ('660e8400-e29b-41d4-a716-446655440009'::uuid, 'MongoDB', 'Database'),
  ('660e8400-e29b-41d4-a716-446655440010'::uuid, 'Docker', 'DevOps'),
  ('660e8400-e29b-41d4-a716-446655440011'::uuid, 'AWS', 'Cloud Platform'),
  ('660e8400-e29b-41d4-a716-446655440012'::uuid, 'GCP', 'Cloud Platform'),
  ('660e8400-e29b-41d4-a716-446655440013'::uuid, 'Git', 'Version Control'),
  ('660e8400-e29b-41d4-a716-446655440014'::uuid, 'HTML/CSS', 'Frontend'),
  ('660e8400-e29b-41d4-a716-446655440015'::uuid, 'Tailwind CSS', 'CSS Framework'),
  ('660e8400-e29b-41d4-a716-446655440016'::uuid, 'SQL', 'Database Query'),
  ('660e8400-e29b-41d4-a716-446655440017'::uuid, 'REST API Design', 'Backend'),
  ('660e8400-e29b-41d4-a716-446655440018'::uuid, 'Agile/Scrum', 'Methodology'),
  ('660e8400-e29b-41d4-a716-446655440019'::uuid, 'Problem Solving', 'Soft Skill'),
  ('660e8400-e29b-41d4-a716-446655440020'::uuid, 'Communication', 'Soft Skill')
ON CONFLICT DO NOTHING;

-- Step 3: Seed Master Companies
-- ============================================================================
INSERT INTO public.master_external_companies (id, name, industry, website_url, address) VALUES
  ('770e8400-e29b-41d4-a716-446655440001'::uuid, 'PT Telkom Indonesia', 'Telecommunications', 'https://telkom.co.id', 'Jakarta, Indonesia'),
  ('770e8400-e29b-41d4-a716-446655440002'::uuid, 'PT Bank Central Asia', 'Finance & Banking', 'https://bca.co.id', 'Jakarta, Indonesia'),
  ('770e8400-e29b-41d4-a716-446655440003'::uuid, 'Gojek', 'Technology/Transportation', 'https://gojek.com', 'Jakarta, Indonesia'),
  ('770e8400-e29b-41d4-a716-446655440004'::uuid, 'Tokopedia', 'E-commerce', 'https://tokopedia.com', 'Jakarta, Indonesia'),
  ('770e8400-e29b-41d4-a716-446655440005'::uuid, 'Bukalapak', 'E-commerce', 'https://bukalapak.com', 'Jakarta, Indonesia'),
  ('770e8400-e29b-41d4-a716-446655440006'::uuid, 'Grab', 'Technology/Transportation', 'https://grab.com', 'Singapore/Jakarta'),
  ('770e8400-e29b-41d4-a716-446655440007'::uuid, 'Google Indonesia', 'Technology', 'https://google.com', 'Jakarta, Indonesia'),
  ('770e8400-e29b-41d4-a716-446655440008'::uuid, 'Microsoft Indonesia', 'Technology', 'https://microsoft.com', 'Jakarta, Indonesia'),
  ('770e8400-e29b-41d4-a716-446655440009'::uuid, 'Accenture Indonesia', 'Consulting/IT', 'https://accenture.com', 'Jakarta, Indonesia'),
  ('770e8400-e29b-41d4-a716-446655440010'::uuid, 'Deloitte Indonesia', 'Consulting', 'https://deloitte.com', 'Jakarta, Indonesia')
ON CONFLICT DO NOTHING;

-- Step 4: Seed Users (Admin & Students)
-- ============================================================================

-- Admin User (password: admin123 - hashed with bcrypt)
INSERT INTO auth.users (id, email, password_hash, role, is_active, created_at) VALUES
  ('880e8400-e29b-41d4-a716-446655440001'::uuid, 'admin@ipb.ac.id', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUqvMona', 'ADMIN', true, NOW())
ON CONFLICT DO NOTHING;

-- Admin Profile
INSERT INTO public.profiles_admin (user_id, full_name, role_name) VALUES
  ('880e8400-e29b-41d4-a716-446655440001'::uuid, 'Admin Tracker', 'System Administrator')
ON CONFLICT DO NOTHING;

-- Student Users (password: student123 - hashed with bcrypt)
INSERT INTO auth.users (id, email, password_hash, role, is_active, created_at) VALUES
  ('880e8400-e29b-41d4-a716-446655440002'::uuid, 'budi.santoso@student.ipb.ac.id', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUqvMona', 'STUDENT', true, NOW()),
  ('880e8400-e29b-41d4-a716-446655440003'::uuid, 'siti.nur.hidayah@student.ipb.ac.id', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUqvMona', 'STUDENT', true, NOW()),
  ('880e8400-e29b-41d4-a716-446655440004'::uuid, 'ahmad.wijaya@student.ipb.ac.id', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUqvMona', 'STUDENT', true, NOW()),
  ('880e8400-e29b-41d4-a716-446655440005'::uuid, 'dewi.lestari@student.ipb.ac.id', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUqvMona', 'STUDENT', true, NOW()),
  ('880e8400-e29b-41d4-a716-446655440006'::uuid, 'reza.pratama@student.ipb.ac.id', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUqvMona', 'STUDENT', true, NOW())
ON CONFLICT DO NOTHING;

-- Student Profiles
INSERT INTO public.profiles_student (user_id, nim, full_name, semester, department_id, gpa, phone_number, is_mbkm_eligible) VALUES
  ('880e8400-e29b-41d4-a716-446655440002'::uuid, 'G64190001', 'Budi Santoso', 6, '550e8400-e29b-41d4-a716-446655440001'::uuid, 3.45, '081234567890', true),
  ('880e8400-e29b-41d4-a716-446655440003'::uuid, 'G64190002', 'Siti Nur Hidayah', 7, '550e8400-e29b-41d4-a716-446655440002'::uuid, 3.78, '081234567891', true),
  ('880e8400-e29b-41d4-a716-446655440004'::uuid, 'G64190003', 'Ahmad Wijaya', 5, '550e8400-e29b-41d4-a716-446655440004'::uuid, 3.12, '081234567892', true),
  ('880e8400-e29b-41d4-a716-446655440005'::uuid, 'G64190004', 'Dewi Lestari', 6, '550e8400-e29b-41d4-a716-446655440006'::uuid, 3.56, '081234567893', false),
  ('880e8400-e29b-41d4-a716-446655440006'::uuid, 'G64190005', 'Reza Pratama', 8, '550e8400-e29b-41d4-a716-446655440001'::uuid, 3.89, '081234567894', true)
ON CONFLICT DO NOTHING;

-- Step 5: Seed Student Skills
-- ============================================================================
INSERT INTO public.student_skills (id, student_id, skill_id, proficiency_level) VALUES
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440002'::uuid, '660e8400-e29b-41d4-a716-446655440001'::uuid, 'INTERMEDIATE'),
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440002'::uuid, '660e8400-e29b-41d4-a716-446655440002'::uuid, 'ADVANCED'),
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440002'::uuid, '660e8400-e29b-41d4-a716-446655440004'::uuid, 'ADVANCED'),
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440002'::uuid, '660e8400-e29b-41d4-a716-446655440008'::uuid, 'INTERMEDIATE'),
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440003'::uuid, '660e8400-e29b-41d4-a716-446655440001'::uuid, 'ADVANCED'),
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440003'::uuid, '660e8400-e29b-41d4-a716-446655440006'::uuid, 'INTERMEDIATE'),
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440004'::uuid, '660e8400-e29b-41d4-a716-446655440002'::uuid, 'INTERMEDIATE'),
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440004'::uuid, '660e8400-e29b-41d4-a716-446655440015'::uuid, 'ADVANCED')
ON CONFLICT DO NOTHING;

-- Step 6: Seed Vacancies
-- ============================================================================
INSERT INTO public.vacancies (
  id, company_id, title, description, type, open_date, close_date,
  created_by, location, payment_type, compensation_min, compensation_max,
  is_active, is_scraped
) VALUES
  (
    '990e8400-e29b-41d4-a716-446655440001'::uuid,
    '770e8400-e29b-41d4-a716-446655440001'::uuid,
    'Full Stack Developer - MBKM Program',
    'Kami mencari mahasiswa untuk program MBKM di divisi digital transformation kami. Tugas utama mencakup pengembangan aplikasi web dan mobile.',
    'MBKM_INTERNSHIP',
    NOW() - INTERVAL '5 days',
    NOW() + INTERVAL '30 days',
    '880e8400-e29b-41d4-a716-446655440001'::uuid,
    'Jakarta, Indonesia',
    'PAID',
    2000000,
    3000000,
    true,
    false
  ),
  (
    '990e8400-e29b-41d4-a716-446655440002'::uuid,
    '770e8400-e29b-41d4-a716-446655440002'::uuid,
    'Data Analyst Internship',
    'Bergabunglah dengan tim analytics kami untuk menganalisis data keuangan dan membuat dashboard bisnis.',
    'INTERNSHIP_GENERAL',
    NOW() - INTERVAL '10 days',
    NOW() + INTERVAL '20 days',
    '880e8400-e29b-41d4-a716-446655440001'::uuid,
    'Jakarta, Indonesia',
    'ALLOWANCE_ONLY',
    NULL,
    NULL,
    true,
    false
  ),
  (
    '990e8400-e29b-41d4-a716-446655440003'::uuid,
    '770e8400-e29b-41d4-a716-446655440003'::uuid,
    'Backend Engineer - Full Time',
    'Posisi full time untuk senior backend engineer dengan pengalaman Python dan sistem terdistribusi.',
    'FULL_TIME',
    NOW() - INTERVAL '3 days',
    NOW() + INTERVAL '45 days',
    '880e8400-e29b-41d4-a716-446655440001'::uuid,
    'Jakarta, Indonesia',
    'PAID',
    5000000,
    8000000,
    true,
    false
  ),
  (
    '990e8400-e29b-41d4-a716-446655440004'::uuid,
    '770e8400-e29b-41d4-a716-446655440004'::uuid,
    'Frontend Developer - React',
    'Tim produk kami mencari frontend developer untuk mengembangkan aplikasi e-commerce terbaru.',
    'INTERNSHIP_GENERAL',
    NOW() - INTERVAL '1 days',
    NOW() + INTERVAL '35 days',
    '880e8400-e29b-41d4-a716-446655440001'::uuid,
    'Jakarta, Indonesia',
    'PAID',
    2500000,
    3500000,
    true,
    false
  ),
  (
    '990e8400-e29b-41d4-a716-446655440005'::uuid,
    '770e8400-e29b-41d4-a716-446655440005'::uuid,
    'DevOps Engineer Trainee',
    'Pelajari infrastructure dan cloud technologies sambil berkontribusi ke sistem produksi kami.',
    'INTERNSHIP_GENERAL',
    NOW() - INTERVAL '7 days',
    NOW() + INTERVAL '25 days',
    '880e8400-e29b-41d4-a716-446655440001'::uuid,
    'Jakarta, Indonesia',
    'ALLOWANCE_ONLY',
    NULL,
    NULL,
    true,
    false
  )
ON CONFLICT DO NOTHING;

-- Step 7: Seed Vacancy Skills
-- ============================================================================
INSERT INTO public.vacancy_skills (id, vacancy_id, skill_id, proficiency_level) VALUES
  -- For Full Stack Developer
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440001'::uuid, '660e8400-e29b-41d4-a716-446655440001'::uuid, 'INTERMEDIATE'),
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440001'::uuid, '660e8400-e29b-41d4-a716-446655440002'::uuid, 'ADVANCED'),
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440001'::uuid, '660e8400-e29b-41d4-a716-446655440004'::uuid, 'INTERMEDIATE'),
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440001'::uuid, '660e8400-e29b-41d4-a716-446655440008'::uuid, 'INTERMEDIATE'),
  -- For Backend Engineer
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440003'::uuid, '660e8400-e29b-41d4-a716-446655440001'::uuid, 'ADVANCED'),
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440003'::uuid, '660e8400-e29b-41d4-a716-446655440006'::uuid, 'ADVANCED'),
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440003'::uuid, '660e8400-e29b-41d4-a716-446655440008'::uuid, 'ADVANCED'),
  -- For Frontend Developer
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440004'::uuid, '660e8400-e29b-41d4-a716-446655440002'::uuid, 'ADVANCED'),
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440004'::uuid, '660e8400-e29b-41d4-a716-446655440004'::uuid, 'ADVANCED'),
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440004'::uuid, '660e8400-e29b-41d4-a716-446655440014'::uuid, 'ADVANCED'),
  -- For DevOps Engineer
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440005'::uuid, '660e8400-e29b-41d4-a716-446655440010'::uuid, 'INTERMEDIATE'),
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440005'::uuid, '660e8400-e29b-41d4-a716-446655440011'::uuid, 'INTERMEDIATE')
ON CONFLICT DO NOTHING;

-- Step 8: Seed Applications (Some students have applied)
-- ============================================================================
INSERT INTO public.applications (id, vacancy_id, student_id, status, matched_score, applied_at) VALUES
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440001'::uuid, '880e8400-e29b-41d4-a716-446655440002'::uuid, 'REVIEWED', 82.5, NOW() - INTERVAL '2 days'),
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440001'::uuid, '880e8400-e29b-41d4-a716-446655440003'::uuid, 'SHORTLISTED', 88.0, NOW() - INTERVAL '3 days'),
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440004'::uuid, '880e8400-e29b-41d4-a716-446655440002'::uuid, 'PENDING', 75.0, NOW() - INTERVAL '1 days'),
  (gen_random_uuid(), '990e8400-e29b-41d4-a716-446655440003'::uuid, '880e8400-e29b-41d4-a716-446655440004'::uuid, 'REJECTED', 45.0, NOW() - INTERVAL '5 days')
ON CONFLICT DO NOTHING;

-- Step 9: Seed Wishlist (Students add vacancies to wishlist)
-- ============================================================================
INSERT INTO public.student_wishlist_vacancies (id, student_id, vacancy_id, added_at) VALUES
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440002'::uuid, '990e8400-e29b-41d4-a716-446655440001'::uuid, NOW() - INTERVAL '2 days'),
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440002'::uuid, '990e8400-e29b-41d4-a716-446655440003'::uuid, NOW() - INTERVAL '1 days'),
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440003'::uuid, '990e8400-e29b-41d4-a716-446655440001'::uuid, NOW() - INTERVAL '4 days'),
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440005'::uuid, '990e8400-e29b-41d4-a716-446655440004'::uuid, NOW() - INTERVAL '3 days')
ON CONFLICT DO NOTHING;

-- Step 10: Seed Notifications
-- ============================================================================
INSERT INTO public.notification_queue (id, user_id, type, title, message, is_read, created_at) VALUES
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440002'::uuid, 'APPLICATION_STATUS'::public.notification_type_enum, 'Lamaran Diulas', 'Lamaran Anda untuk posisi Full Stack Developer sedang diulas.', false, NOW() - INTERVAL '1 days'),
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440003'::uuid, 'APPLICATION_STATUS'::public.notification_type_enum, 'Anda Lolos Seleksi', 'Selamat! Anda lolos ke tahap berikutnya.', false, NOW() - INTERVAL '2 hours'),
  (gen_random_uuid(), '880e8400-e29b-41d4-a716-446655440002'::uuid, 'NEW_VACANCY'::public.notification_type_enum, 'Lowongan Baru', 'Ada lowongan baru yang sesuai dengan profil Anda dari PT Tokopedia.', true, NOW() - INTERVAL '6 hours')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- Seed data complete!
-- ============================================================================
-- Test Credentials:
-- Admin:
--   Email: admin@ipb.ac.id
--   Password: admin123
--
-- Students:
--   Email: budi.santoso@student.ipb.ac.id (Password: student123)
--   Email: siti.nur.hidayah@student.ipb.ac.id (Password: student123)
--   Email: ahmad.wijaya@student.ipb.ac.id (Password: student123)
--   Email: dewi.lestari@student.ipb.ac.id (Password: student123)
--   Email: reza.pratama@student.ipb.ac.id (Password: student123)
--
-- Backend should now be ready to accept API requests!
-- ============================================================================
