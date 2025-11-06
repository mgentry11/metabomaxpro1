-- Migration: Pricing Restructure - Limited Free Basic Reports
-- Date: 2025-01-05
-- Description: Add ai_credits column and update free tier to 2 reports limit

-- Add ai_credits column to subscriptions table
ALTER TABLE subscriptions
ADD COLUMN IF NOT EXISTS ai_credits INTEGER DEFAULT 0;

-- Update existing free tier users to new limits (2 free reports)
UPDATE subscriptions
SET reports_limit = 2
WHERE plan_name = 'free' AND status = 'active';

-- Update the handle_new_user function to give new users 2 free reports
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', '')
    );

    -- Create default free subscription with 2 free reports
    INSERT INTO public.subscriptions (user_id, plan_name, status, reports_limit, ai_credits)
    VALUES (NEW.id, 'free', 'active', 2, 0);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Add comments to document the schema (using proper quoting for column names)
COMMENT ON COLUMN subscriptions.ai_credits IS 'Number of AI recommendation credits remaining (0 = no AI, 10 = AI package, 9999 = unlimited subscription)';
COMMENT ON COLUMN subscriptions."reports_limit" IS 'Maximum number of basic reports allowed (2 = free tier, 9999 = unlimited)';
COMMENT ON COLUMN subscriptions."reports_used" IS 'Number of basic reports generated so far';
