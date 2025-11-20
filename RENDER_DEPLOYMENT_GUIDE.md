# Render.com Deployment Guide for MetaboMax Pro + HIT Coach Pro

This guide walks you through deploying the integrated MetaboMax Pro and HIT Coach Pro Flask application to Render.com.

## Prerequisites

- ✅ Code pushed to GitHub: https://github.com/mgentry11/metabomaxpro1
- ✅ Render.com account (free tier works)
- ✅ Supabase project with environment variables
- ✅ Stripe account with API keys
- ✅ OpenAI API key (optional, for AI features)

## Step 1: Connect GitHub Repository to Render

1. **Log in to Render.com**
   - Go to: https://dashboard.render.com/

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub account if not already connected
   - Select repository: `mgentry11/metabomaxpro1`
   - Click "Connect"

3. **Configure Web Service**
   - **Name**: `metabomaxpro1` (or your preferred name)
   - **Region**: Choose closest to your users (e.g., `Oregon (US West)`)
   - **Branch**: `main`
   - **Root Directory**: (leave blank)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --workers 1 --timeout 120 --bind 0.0.0.0:$PORT`

## Step 2: Set Environment Variables

Click "Advanced" and add these environment variables:

### Required Variables

```
FLASK_SECRET_KEY=your-secret-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
STRIPE_SECRET_KEY=sk_live_or_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_live_or_test_your_stripe_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
FLASK_ENV=production
```

### Optional Variables

```
OPENAI_API_KEY=sk-your-openai-key
```

### How to Get Each Variable

**FLASK_SECRET_KEY**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**SUPABASE_URL & SUPABASE_KEY**
- Go to: https://app.supabase.com/project/_/settings/api
- Copy "Project URL" → `SUPABASE_URL`
- Copy "anon public" key → `SUPABASE_KEY`

**STRIPE_SECRET_KEY & STRIPE_PUBLISHABLE_KEY**
- Go to: https://dashboard.stripe.com/test/apikeys (for test mode)
- Or: https://dashboard.stripe.com/apikeys (for live mode)
- Copy "Secret key" → `STRIPE_SECRET_KEY`
- Copy "Publishable key" → `STRIPE_PUBLISHABLE_KEY`

**STRIPE_WEBHOOK_SECRET**
- Go to: https://dashboard.stripe.com/test/webhooks (for test mode)
- Click "+ Add endpoint"
- Endpoint URL: `https://metabomaxpro1.onrender.com/webhook/stripe`
- Events to send: Select `checkout.session.completed`
- Copy the "Signing secret" → `STRIPE_WEBHOOK_SECRET`

**OPENAI_API_KEY** (Optional)
- Go to: https://platform.openai.com/api-keys
- Create new secret key → `OPENAI_API_KEY`

## Step 3: Deploy

1. **Choose Plan**
   - Free tier works for testing
   - Starter ($7/month) recommended for production

2. **Click "Create Web Service"**
   - Render will automatically build and deploy
   - Wait for build to complete (~3-5 minutes)

3. **Monitor Build Logs**
   - Watch for any errors in the logs
   - Should see: "Installing collected packages: Flask, gunicorn..."
   - Final message: "Your service is live 🎉"

## Step 4: Set Up Supabase Database

1. **Go to Supabase SQL Editor**
   - https://app.supabase.com/project/_/sql

2. **Run Database Setup**
   - Copy all SQL commands from `HITCOACH_DATABASE_SCHEMA.md`
   - Create tables: `workout_history`, `exercise_sets`, `user_workout_preferences`
   - Set up Row Level Security (RLS) policies

3. **Verify Tables Created**
   - Go to Table Editor
   - Confirm all tables exist with correct columns

## Step 5: Configure Stripe Webhook

1. **Set Webhook Endpoint**
   - Endpoint URL: `https://metabomaxpro1.onrender.com/webhook/stripe`
   - Or use your custom domain if configured

2. **Test Webhook**
   - Send test event from Stripe dashboard
   - Check Render logs for webhook receipt confirmation

## Step 6: Test Deployment

1. **Visit Your App**
   - URL: `https://metabomaxpro1.onrender.com`
   - Or your custom URL if configured

2. **Test HIT Coach Pro Routes**
   - Marketing page: `/hitcoachpro`
   - Web app: `/hitcoach-app`
   - Health check: `/health` (should return `{"status": "ok"}`)
   - Version check: `/version`

3. **Test Key Functionality**
   - User registration
   - Login/logout
   - HIT Coach Pro workout flow
   - Voice coaching (enable microphone permissions)
   - PWA installation (Add to Home Screen on mobile)

## Step 7: Custom Domain (Optional)

1. **Add Custom Domain in Render**
   - Go to web service settings
   - Click "Custom Domains"
   - Add: `metabomaxpro.com` or `app.metabomaxpro.com`

2. **Configure DNS**
   - Add CNAME record pointing to Render
   - Follow Render's DNS instructions

3. **SSL Certificate**
   - Render automatically provisions Let's Encrypt SSL
   - Wait ~5 minutes for SSL to activate

## Troubleshooting

### Build Fails

**Error**: `No module named 'X'`
- **Fix**: Add missing package to `requirements.txt`
- Commit and push to trigger rebuild

**Error**: `Application timeout`
- **Fix**: Increase timeout in start command
- Change to: `gunicorn app:app --timeout 300`

### Runtime Errors

**Error**: `ModuleNotFoundError` after deployment
- **Fix**: Check build logs for installation errors
- Ensure all dependencies in `requirements.txt`

**Error**: `Database connection failed`
- **Fix**: Verify `SUPABASE_URL` and `SUPABASE_KEY` are set correctly
- Check Supabase project is active

**Error**: `404 on /hitcoach-app`
- **Fix**: Verify `templates/hitcoach_app.html` exists
- Check build logs for template copy errors

### Stripe Issues

**Error**: `Invalid API Key`
- **Fix**: Regenerate Stripe keys and update env vars
- Use test keys for development, live keys for production

**Error**: `Webhook signature verification failed`
- **Fix**: Verify `STRIPE_WEBHOOK_SECRET` matches Stripe dashboard
- Check webhook endpoint URL is correct

## Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render web service created and connected
- [ ] All environment variables set
- [ ] Build completed successfully
- [ ] Supabase database tables created
- [ ] RLS policies configured
- [ ] Stripe webhook configured
- [ ] Health check endpoint returns 200
- [ ] `/hitcoach-app` route loads
- [ ] Voice coaching works (microphone permissions)
- [ ] PWA installation works
- [ ] User authentication works
- [ ] Payment flow tested (test mode)
- [ ] Custom domain configured (if applicable)

## URLs Reference

- **Production App**: https://metabomaxpro1.onrender.com
- **HIT Coach Pro**: https://metabomaxpro1.onrender.com/hitcoach-app
- **Marketing Page**: https://metabomaxpro1.onrender.com/hitcoachpro
- **API Health**: https://metabomaxpro1.onrender.com/health
- **GitHub Repo**: https://github.com/mgentry11/metabomaxpro1
- **Render Dashboard**: https://dashboard.render.com/

## Next Steps After Deployment

1. **Test all features** in production environment
2. **Set up monitoring** (Render provides basic logs)
3. **Configure auto-deploy** from main branch (already configured)
4. **Add error tracking** (e.g., Sentry)
5. **Set up database backups** (Supabase automatic backups)
6. **Create staging environment** (optional, separate Render service)
7. **Document API endpoints** for future development
8. **Set up CI/CD** (GitHub Actions, optional)

## Support & Maintenance

- **Render Logs**: View real-time logs in Render dashboard
- **Supabase Logs**: Check database query logs in Supabase
- **Stripe Events**: Monitor payments and webhooks in Stripe dashboard
- **Update Dependencies**: Regularly update `requirements.txt`
- **Security**: Keep Flask and all dependencies up to date

## Contact

For issues or questions:
- Render Support: https://render.com/docs
- Supabase Docs: https://supabase.com/docs
- Stripe Docs: https://stripe.com/docs

---

**Deployment completed!** Your integrated MetaboMax Pro + HIT Coach Pro application is now live.
