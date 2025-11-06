ALTER TABLE subscriptions ADD COLUMN IF NOT EXISTS ai_credits INTEGER DEFAULT 0;

UPDATE subscriptions SET reports_limit = 2 WHERE plan_name = 'free' AND status = 'active';

CREATE OR REPLACE FUNCTION public.handle_new_user() RETURNS TRIGGER AS $$ BEGIN INSERT INTO public.profiles (id, email, full_name) VALUES (NEW.id, NEW.email, COALESCE(NEW.raw_user_meta_data->>'full_name', '')); INSERT INTO public.subscriptions (user_id, plan_name, status, reports_limit, ai_credits) VALUES (NEW.id, 'free', 'active', 2, 0); RETURN NEW; END; $$ LANGUAGE plpgsql SECURITY DEFINER;
