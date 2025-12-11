-- Create job_descriptions table for storing reusable job descriptions
CREATE TABLE IF NOT EXISTS job_descriptions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    company VARCHAR(255),
    department VARCHAR(255)
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_job_descriptions_created_at ON job_descriptions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_job_descriptions_title ON job_descriptions(title);

-- Enable RLS
ALTER TABLE job_descriptions ENABLE ROW LEVEL SECURITY;

-- Policy: Allow all access
CREATE POLICY "Allow all access to job_descriptions" ON job_descriptions
    FOR ALL
    USING (true)
    WITH CHECK (true);
