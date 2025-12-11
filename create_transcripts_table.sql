-- Create transcripts table to store reusable interview transcripts
-- Run this in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS transcripts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    candidate_name VARCHAR(255) NOT NULL DEFAULT 'Unknown Candidate',
    transcript TEXT NOT NULL,
    resume TEXT,  -- Optional resume text for more thorough analysis
    source VARCHAR(50) DEFAULT 'upload',  -- 'upload', 'paste', 'import'
    filename VARCHAR(255),
    ip_address VARCHAR(45),
    user_agent TEXT
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_transcripts_created_at ON transcripts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_transcripts_candidate_name ON transcripts(candidate_name);

-- Enable Row Level Security
ALTER TABLE transcripts ENABLE ROW LEVEL SECURITY;

-- Allow all access (for public API without auth)
CREATE POLICY "Allow all access to transcripts" ON transcripts
    FOR ALL USING (true) WITH CHECK (true);

-- Add transcript_id column to interview_reports if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'interview_reports' AND column_name = 'transcript_id'
    ) THEN
        ALTER TABLE interview_reports ADD COLUMN transcript_id UUID REFERENCES transcripts(id);
        CREATE INDEX idx_interview_reports_transcript_id ON interview_reports(transcript_id);
    END IF;
END $$;
