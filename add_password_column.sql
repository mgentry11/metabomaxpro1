-- Add password_hash and company_name columns to profiles table
ALTER TABLE profiles
ADD COLUMN IF NOT EXISTS password_hash TEXT,
ADD COLUMN IF NOT EXISTS company_name TEXT;
