-- ============================================================================
-- IPB Internship & Career Tracker - Supabase Schema Migration
-- ============================================================================
-- This script creates all tables and schemas for the application
-- Execute this in Supabase SQL Editor (home > SQL Editor > Create New Query)
-- ============================================================================

-- Step 1: Create Schema & Extensions
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS auth;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Step 2: Create ENUMs
-- ============================================================================

-- User Role Enum
DO $$
BEGIN
  CREATE TYPE auth.user_role_enum AS ENUM ('ADMIN', 'STUDENT');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- Vacancy Type Enum
DO $$
BEGIN
  CREATE TYPE public.vacancy_type_enum AS ENUM (
    'INTERNSHIP_GENERAL',
    'MBKM_INTERNSHIP',
    'MBKM_STUDY_INDEPENDENT',
    'FULL_TIME'
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- Payment Type Enum
DO $$
BEGIN
  CREATE TYPE public.payment_type_enum AS ENUM ('PAID', 'UNPAID', 'ALLOWANCE_ONLY');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- Application Status Enum
DO $$
BEGIN
  CREATE TYPE public.application_status_enum AS ENUM (
    'PENDING',
    'REVIEWED',
    'SHORTLISTED',
    'ACCEPTED',
    'REJECTED',
    'WITHDRAWN'
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- Notification Type Enum
DO $$
BEGIN
  CREATE TYPE public.notification_type_enum AS ENUM (
    'APPLICATION_STATUS',
    'NEW_VACANCY',
    'PLACEMENT_OFFER',
    'DOCUMENT_REQUEST',
    'SYSTEM'
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- Auth Action Enum
DO $$
BEGIN
  CREATE TYPE public.auth_action_enum AS ENUM (
    'EMAIL_VERIFICATION',
    'PASSWORD_RESET',
    'EMAIL_CHANGE',
    'ACTIVATE_ACCOUNT'
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- Step 3: Create Core Tables
-- ============================================================================

-- 3.1 Users Table
CREATE TABLE IF NOT EXISTS auth.users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role auth.user_role_enum NOT NULL,
  is_active BOOLEAN DEFAULT true,
  last_login_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3.2 User Refresh Tokens
CREATE TABLE IF NOT EXISTS public.user_refresh_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  token_hash VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
  revoked_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, token_hash)
);

-- 3.3 Auth Action Tokens
CREATE TABLE IF NOT EXISTS public.auth_action_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  action public.auth_action_enum NOT NULL,
  token_hash VARCHAR(255) NOT NULL UNIQUE,
  used_at TIMESTAMP WITH TIME ZONE,
  expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Step 4: Create Master Data Tables
-- ============================================================================

-- 4.1 Master Departments
CREATE TABLE IF NOT EXISTS public.master_departments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code VARCHAR(10) NOT NULL UNIQUE,
  name VARCHAR(150) NOT NULL,
  faculty VARCHAR(100) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4.2 Master Skills
CREATE TABLE IF NOT EXISTS public.master_skills (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL UNIQUE,
  category VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4.3 Master External Companies
CREATE TABLE IF NOT EXISTS public.master_external_companies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(150) NOT NULL UNIQUE,
  industry VARCHAR(100),
  website_url TEXT,
  address TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_master_companies_name ON public.master_external_companies(name);

-- Step 5: Create Profile Tables
-- ============================================================================

-- 5.1 Student Profiles
CREATE TABLE IF NOT EXISTS public.profiles_student (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  nim VARCHAR(20) NOT NULL UNIQUE,
  full_name VARCHAR(150) NOT NULL,
  semester INTEGER NOT NULL CHECK (semester > 0),
  department_id UUID REFERENCES public.master_departments(id) ON DELETE RESTRICT,
  gpa NUMERIC(3, 2),
  phone_number VARCHAR(20),
  linkedin_url TEXT,
  cv_url TEXT,
  is_mbkm_eligible BOOLEAN DEFAULT true,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5.2 Admin Profiles
CREATE TABLE IF NOT EXISTS public.profiles_admin (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name VARCHAR(150) NOT NULL,
  role_name VARCHAR(100),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Step 6: Create Vacancy & Matching Tables
-- ============================================================================

-- 6.1 Vacancies
CREATE TABLE IF NOT EXISTS public.vacancies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID NOT NULL REFERENCES public.master_external_companies(id) ON DELETE RESTRICT,
  title VARCHAR(200) NOT NULL,
  description TEXT NOT NULL,
  type public.vacancy_type_enum NOT NULL,
  open_date TIMESTAMP WITH TIME ZONE NOT NULL,
  close_date TIMESTAMP WITH TIME ZONE NOT NULL,
  created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  location VARCHAR(150),
  payment_type public.payment_type_enum DEFAULT 'UNPAID'::public.payment_type_enum,
  compensation_min NUMERIC(15, 2),
  compensation_max NUMERIC(15, 2),
  compensation_note TEXT,
  source_url TEXT,
  is_scraped BOOLEAN DEFAULT false,
  is_auto_close BOOLEAN DEFAULT true,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  CHECK (close_date >= open_date),
  CHECK (compensation_min >= 0::numeric),
  CHECK (compensation_max IS NULL OR compensation_max >= compensation_min)
);

CREATE INDEX IF NOT EXISTS idx_vacancies_active ON public.vacancies(open_date, close_date);
CREATE INDEX IF NOT EXISTS idx_vacancies_company_id ON public.vacancies(company_id);
CREATE INDEX IF NOT EXISTS idx_vacancies_created_by ON public.vacancies(created_by);

-- 6.2 Vacancy Skills (Matching Junction Table)
CREATE TABLE IF NOT EXISTS public.vacancy_skills (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vacancy_id UUID NOT NULL REFERENCES public.vacancies(id) ON DELETE CASCADE,
  skill_id UUID NOT NULL REFERENCES public.master_skills(id) ON DELETE CASCADE,
  proficiency_level VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(vacancy_id, skill_id)
);

-- 6.3 Student Skills (Matching Junction Table)
CREATE TABLE IF NOT EXISTS public.student_skills (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL REFERENCES public.profiles_student(user_id) ON DELETE CASCADE,
  skill_id UUID NOT NULL REFERENCES public.master_skills(id) ON DELETE CASCADE,
  proficiency_level VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(student_id, skill_id)
);

-- 6.4 Student Wishlist
CREATE TABLE IF NOT EXISTS public.student_wishlist_vacancies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL REFERENCES public.profiles_student(user_id) ON DELETE CASCADE,
  vacancy_id UUID NOT NULL REFERENCES public.vacancies(id) ON DELETE CASCADE,
  added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(student_id, vacancy_id)
);

-- Step 7: Create Application & Placement Tables
-- ============================================================================

-- 7.1 Applications
CREATE TABLE IF NOT EXISTS public.applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vacancy_id UUID NOT NULL REFERENCES public.vacancies(id) ON DELETE CASCADE,
  student_id UUID NOT NULL REFERENCES public.profiles_student(user_id) ON DELETE CASCADE,
  status public.application_status_enum DEFAULT 'PENDING'::public.application_status_enum,
  resume_url TEXT,
  cover_letter TEXT,
  matched_score NUMERIC(5, 2),
  notes TEXT,
  applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_applications_student_id ON public.applications(student_id);
CREATE INDEX IF NOT EXISTS idx_applications_vacancy_id ON public.applications(vacancy_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON public.applications(status);

-- 7.2 Placements
CREATE TABLE IF NOT EXISTS public.placements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL REFERENCES public.profiles_student(user_id) ON DELETE CASCADE,
  company_id UUID NOT NULL REFERENCES public.master_external_companies(id) ON DELETE RESTRICT,
  position VARCHAR(150),
  start_date DATE NOT NULL,
  end_date DATE,
  status VARCHAR(50),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_placements_student_id ON public.placements(student_id);

-- Step 8: Create Notification & Logging Tables
-- ============================================================================

-- 8.1 Notification Queue
CREATE TABLE IF NOT EXISTS public.notification_queue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  type public.notification_type_enum NOT NULL,
  title VARCHAR(200),
  message TEXT,
  related_entity_id UUID,
  is_read BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  read_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_notification_queue_user_id ON public.notification_queue(user_id);
CREATE INDEX IF NOT EXISTS idx_notification_queue_is_read ON public.notification_queue(is_read);

-- 8.2 Activity Logs
CREATE TABLE IF NOT EXISTS public.activity_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  action VARCHAR(100),
  resource_type VARCHAR(50),
  resource_id UUID,
  changes JSONB,
  ip_address VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_activity_logs_user_id ON public.activity_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_created_at ON public.activity_logs(created_at);

-- 8.3 Application Logs
CREATE TABLE IF NOT EXISTS public.application_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  application_id UUID REFERENCES public.applications(id) ON DELETE SET NULL,
  action VARCHAR(100),
  status VARCHAR(50),
  details JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Step 9: Create Document & Report Tables
-- ============================================================================

-- 9.1 Document Requests
CREATE TABLE IF NOT EXISTS public.document_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL REFERENCES public.profiles_student(user_id) ON DELETE CASCADE,
  vacancy_id UUID REFERENCES public.vacancies(id) ON DELETE SET NULL,
  document_type VARCHAR(100),
  purpose public.auth_action_enum,
  submission_deadline TIMESTAMP WITH TIME ZONE,
  submitted_at TIMESTAMP WITH TIME ZONE,
  status VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_document_requests_student_id ON public.document_requests(student_id);

-- Step 10: Create Indices for Performance
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_users_email ON auth.users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON auth.users(role);
CREATE INDEX IF NOT EXISTS idx_profiles_student_department_id ON public.profiles_student(department_id);
CREATE INDEX IF NOT EXISTS idx_student_skills_student_id ON public.student_skills(student_id);
CREATE INDEX IF NOT EXISTS idx_vacancy_skills_vacancy_id ON public.vacancy_skills(vacancy_id);
CREATE INDEX IF NOT EXISTS idx_wishlist_student_id ON public.student_wishlist_vacancies(student_id);

-- ============================================================================
-- Schema creation complete!
-- ============================================================================
-- Next steps:
-- 1. Run the seed data script (supabase_seed.sql)
-- 2. Test backend connection with: poetry run python -m pytest tests/test_auth.py -v
-- ============================================================================
