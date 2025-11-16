-- Migration: Add Password Reset Functionality
-- Run this in your Supabase SQL Editor

-- Create password_reset_tokens table
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster token lookups
CREATE INDEX IF NOT EXISTS idx_password_reset_tokens_token ON password_reset_tokens(token);
CREATE INDEX IF NOT EXISTS idx_password_reset_tokens_user_id ON password_reset_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_password_reset_tokens_expires_at ON password_reset_tokens(expires_at);

-- Enable Row Level Security
ALTER TABLE password_reset_tokens ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Service role can manage all tokens (for app backend)
CREATE POLICY "Service role can manage tokens" ON password_reset_tokens
    FOR ALL USING (true);

-- Add password_hash column to profiles if it doesn't exist
-- (This may already exist if you've run previous migrations)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'profiles' AND column_name = 'password_hash'
    ) THEN
        ALTER TABLE profiles ADD COLUMN password_hash TEXT;
    END IF;
END $$;

-- Function to clean up expired tokens (optional - run periodically)
CREATE OR REPLACE FUNCTION cleanup_expired_reset_tokens()
RETURNS void AS $$
BEGIN
    DELETE FROM password_reset_tokens
    WHERE expires_at < NOW() OR used = TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON TABLE password_reset_tokens IS 'Stores password reset tokens with expiration';
COMMENT ON FUNCTION cleanup_expired_reset_tokens IS 'Deletes expired and used password reset tokens';
