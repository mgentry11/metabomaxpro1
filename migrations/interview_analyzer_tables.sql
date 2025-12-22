-- Interview Analyzer Tables Migration
-- Run this in Supabase SQL Editor

-- Job descriptions table
CREATE TABLE IF NOT EXISTS job_descriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  company TEXT,
  description TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Interview transcripts - linked to jobs
CREATE TABLE IF NOT EXISTS interview_transcripts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  job_id UUID REFERENCES job_descriptions(id) ON DELETE CASCADE,
  candidate_name TEXT NOT NULL,
  transcript TEXT NOT NULL,
  resume TEXT,
  source TEXT DEFAULT 'upload',
  filename TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Interview reports - linked to jobs and transcripts
CREATE TABLE IF NOT EXISTS interview_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  job_id UUID REFERENCES job_descriptions(id) ON DELETE CASCADE,
  transcript_id UUID REFERENCES interview_transcripts(id) ON DELETE SET NULL,
  candidate_name TEXT,
  job_title TEXT,
  fit_score INTEGER,
  full_response JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_job_descriptions_user ON job_descriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_transcripts_user_job ON interview_transcripts(user_id, job_id);
CREATE INDEX IF NOT EXISTS idx_reports_user_job ON interview_reports(user_id, job_id);
CREATE INDEX IF NOT EXISTS idx_reports_transcript ON interview_reports(transcript_id);

-- Row Level Security (RLS) Policies
ALTER TABLE job_descriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE interview_transcripts ENABLE ROW LEVEL SECURITY;
ALTER TABLE interview_reports ENABLE ROW LEVEL SECURITY;

-- Job descriptions policies
CREATE POLICY "Users can view own job descriptions" ON job_descriptions
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own job descriptions" ON job_descriptions
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own job descriptions" ON job_descriptions
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own job descriptions" ON job_descriptions
  FOR DELETE USING (auth.uid() = user_id);

-- Transcripts policies
CREATE POLICY "Users can view own transcripts" ON interview_transcripts
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own transcripts" ON interview_transcripts
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own transcripts" ON interview_transcripts
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own transcripts" ON interview_transcripts
  FOR DELETE USING (auth.uid() = user_id);

-- Reports policies
CREATE POLICY "Users can view own reports" ON interview_reports
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own reports" ON interview_reports
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own reports" ON interview_reports
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own reports" ON interview_reports
  FOR DELETE USING (auth.uid() = user_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
DROP TRIGGER IF EXISTS update_job_descriptions_updated_at ON job_descriptions;
CREATE TRIGGER update_job_descriptions_updated_at
    BEFORE UPDATE ON job_descriptions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_interview_reports_updated_at ON interview_reports;
CREATE TRIGGER update_interview_reports_updated_at
    BEFORE UPDATE ON interview_reports
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
