-- HIPAA Audit Logs Table
-- Tracks all access to Protected Health Information (PHI)

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    user_id TEXT,
    action TEXT NOT NULL,  -- VIEW, CREATE, UPDATE, DELETE, DOWNLOAD, EXPORT, LOGIN, LOGOUT
    resource_type TEXT,    -- report, test, profile, session
    resource_id TEXT,
    ip_address TEXT,
    user_agent TEXT,
    details JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for efficient querying by user and time
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_time ON audit_logs(user_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);

-- HIPAA requires 6 years retention - this table should NOT have auto-delete policies

-- Grant insert access (no delete/update for audit integrity)
-- Note: In production, consider using a service role for audit logging
