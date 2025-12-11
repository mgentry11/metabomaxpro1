-- Create interview_reports table for storing interview analysis reports
CREATE TABLE IF NOT EXISTS interview_reports (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Input data
    candidate_name VARCHAR(255),
    job_title VARCHAR(255),
    transcript TEXT NOT NULL,
    job_description TEXT NOT NULL,

    -- Analysis results
    fit_score INTEGER,
    strengths JSONB,
    matching_skills JSONB,
    concerns JSONB,
    notable_quotes JSONB,
    summary TEXT,

    -- Full response for future reference
    full_response JSONB,

    -- Optional: link to user if authenticated
    user_email VARCHAR(255),

    -- Metadata
    ip_address VARCHAR(45),
    user_agent TEXT
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_interview_reports_created_at ON interview_reports(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_interview_reports_user_email ON interview_reports(user_email);
CREATE INDEX IF NOT EXISTS idx_interview_reports_candidate_name ON interview_reports(candidate_name);

-- Enable RLS (Row Level Security)
ALTER TABLE interview_reports ENABLE ROW LEVEL SECURITY;

-- Policy: Allow all operations for now (public access)
-- You can restrict this later if needed
CREATE POLICY "Allow all access to interview_reports" ON interview_reports
    FOR ALL
    USING (true)
    WITH CHECK (true);
