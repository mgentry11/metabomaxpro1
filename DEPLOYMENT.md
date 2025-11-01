# Deployment Guide - Render.com

This guide will walk you through deploying MetaboMax Pro to Render.com and connecting your custom domain.

## Prerequisites

- ✅ Git repository initialized (done!)
- ✅ Code committed to Git (done!)
- ✅ Supabase account and database set up
- ⏳ Stripe account (optional for testing, required for payments)
- ⏳ GitHub account (for connecting to Render)

## Part 1: Push to GitHub

### Step 1: Create a GitHub Repository

1. Go to [https://github.com](https://github.com)
2. Click the **"+"** icon in the top right → **"New repository"**
3. Repository settings:
   - **Name**: `metabomaxpro` (or any name you prefer)
   - **Description**: "MetaboMax Pro - Metabolic Report Generation SaaS"
   - **Visibility**: Private (recommended) or Public
   - **DO NOT** initialize with README (you already have one)
4. Click **"Create repository"**

### Step 2: Push Your Code to GitHub

GitHub will show you commands. Run these in your terminal:

```bash
# Add GitHub as remote origin
git remote add origin https://github.com/YOUR_USERNAME/metabomaxpro.git

# Push your code
git push -u origin main
```

**Replace `YOUR_USERNAME`** with your actual GitHub username.

**If you get authentication errors:**
- You may need to create a Personal Access Token (PAT)
- Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate new token with `repo` permissions
- Use the token as your password when pushing

## Part 2: Deploy to Render.com

### Step 1: Create Render Account

1. Go to [https://render.com](https://render.com)
2. Click **"Get Started"** or **"Sign Up"**
3. **Sign up with GitHub** (recommended - easier integration)
4. Authorize Render to access your GitHub repositories

### Step 2: Create New Web Service

1. From Render Dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository:
   - Click **"Connect account"** if not already connected
   - Find and select your `metabomaxpro` repository
   - Click **"Connect"**

### Step 3: Configure Web Service

Render will auto-detect your `render.yaml` configuration, but verify these settings:

**Basic Settings:**
- **Name**: `metabomaxpro` (or your preferred name)
- **Region**: Oregon (US West) - or closest to your users
- **Branch**: `main`
- **Runtime**: Python 3

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt` (auto-detected)
- **Start Command**: `gunicorn app:app` (auto-detected)

**Instance Type:**
- **Free** (for testing) - ⚠️ Spins down after 15 min of inactivity
- **Starter** ($7/month) - For production, always running
- Choose **Free** for now, upgrade later

### Step 4: Add Environment Variables

Click **"Environment"** tab and add these variables:

**Required Variables:**

```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
FLASK_SECRET_KEY=(Render auto-generates this)
FLASK_ENV=production
```

**Stripe Variables** (add when ready):

```
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
```

**To add each variable:**
1. Click **"Add Environment Variable"**
2. Enter **Key** and **Value**
3. Click **"Save Changes"**

**Where to find these values:**
- **Supabase**: Dashboard → Project Settings → API
- **Stripe**: Dashboard → Developers → API keys

### Step 5: Deploy!

1. Click **"Create Web Service"**
2. Render will start building your app
3. Watch the deployment logs in real-time
4. First deployment takes 5-10 minutes

**Success Indicators:**
- Logs show: `Starting gunicorn`
- Status changes to **"Live"** (green)
- You get a URL like: `https://metabomaxpro.onrender.com`

### Step 6: Test Your Deployment

1. Click on your Render URL
2. You should see your landing page
3. Test key features:
   - Registration
   - Login
   - Pricing page
   - Report generation

**Troubleshooting:**
- If deployment fails, check logs for errors
- Common issues:
  - Missing environment variables
  - Database connection errors
  - Import errors

## Part 3: Connect Custom Domain (metabomaxpro.com)

### Step 1: Add Custom Domain in Render

1. In Render Dashboard, go to your web service
2. Click **"Settings"** tab
3. Scroll to **"Custom Domain"**
4. Click **"Add Custom Domain"**
5. Enter: `metabomaxpro.com`
6. Click **"Save"**

Render will show you DNS records to add.

### Step 2: Configure DNS in GoDaddy

1. Log in to [GoDaddy.com](https://godaddy.com)
2. Go to **"My Products"** → **"Domains"**
3. Click **"DNS"** next to `metabomaxpro.com`

**Add these DNS records from Render:**

Render will provide specific values, but typically:

**For Root Domain (metabomaxpro.com):**
- **Type**: A Record
- **Name**: @ (or leave blank)
- **Value**: The IP address Render provides
- **TTL**: 600 (or default)

**For WWW subdomain (www.metabomaxpro.com):**
- **Type**: CNAME
- **Name**: www
- **Value**: `metabomaxpro.onrender.com` (or the value Render provides)
- **TTL**: 600 (or default)

### Step 3: Wait for DNS Propagation

- DNS changes take 15 minutes to 48 hours to propagate
- Usually works within 1-2 hours
- Check status at: [https://www.whatsmydns.net](https://www.whatsmydns.net)

### Step 4: Enable SSL/HTTPS

1. In Render, once DNS is verified:
2. Render automatically provisions SSL certificate (Let's Encrypt)
3. Your site will be accessible via HTTPS
4. HTTP automatically redirects to HTTPS

## Part 4: Update Stripe Webhooks (When Ready)

Once your domain is live, update Stripe webhook endpoint:

1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. **Developers** → **Webhooks**
3. Click your existing webhook or **"Add endpoint"**
4. Update endpoint URL to: `https://metabomaxpro.com/stripe-webhook`
5. Select events:
   - `checkout.session.completed`
   - `customer.subscription.deleted`
   - `customer.subscription.updated`
6. Copy the **Signing Secret** and update `STRIPE_WEBHOOK_SECRET` in Render

## Post-Deployment Checklist

✅ Site loads at Render URL
✅ Custom domain works
✅ HTTPS/SSL enabled
✅ User registration works
✅ Login works
✅ Report generation works
✅ Stripe payments work (test mode)
✅ Database stores data correctly

## Monitoring & Maintenance

### Check Application Logs

In Render Dashboard:
- Click **"Logs"** tab
- View real-time application logs
- Look for errors or issues

### Monitor Performance

- **Metrics** tab shows:
  - CPU usage
  - Memory usage
  - Request count
  - Response times

### Upgrade to Paid Plan When Ready

**Free Tier Limitations:**
- Spins down after 15 minutes of inactivity
- 750 hours/month (enough for testing)
- Slower cold starts

**Starter Plan ($7/month):**
- Always running
- Faster performance
- Better for production

**To upgrade:**
1. Go to **"Settings"** → **"Instance Type"**
2. Select **"Starter"**
3. Click **"Save Changes"**

## Continuous Deployment

Your app is now set up for continuous deployment:

1. Make changes to your code locally
2. Commit changes: `git commit -m "Your message"`
3. Push to GitHub: `git push`
4. Render automatically detects and deploys changes
5. New version goes live in 2-5 minutes

**Example workflow:**
```bash
# Make changes to your code
# Test locally

# Commit changes
git add .
git commit -m "Add new feature"

# Push to GitHub
git push

# Render automatically deploys!
```

## Troubleshooting Common Issues

### "Application Error" on Render

**Check logs for:**
- Missing environment variables
- Database connection failures
- Import errors

**Solutions:**
- Verify all environment variables are set
- Check Supabase connection string
- Review requirements.txt for missing packages

### Site is Slow

**Free tier spins down:**
- First request after inactivity takes 30-60 seconds
- Subsequent requests are fast
- Upgrade to Starter ($7/month) for always-on

### Custom Domain Not Working

**DNS not propagated yet:**
- Wait 1-2 hours
- Check [whatsmydns.net](https://whatsmydns.net)

**Wrong DNS settings:**
- Verify A record and CNAME
- Use exact values from Render

### Stripe Webhooks Failing

**Wrong endpoint URL:**
- Update to: `https://metabomaxpro.com/stripe-webhook`

**Wrong signing secret:**
- Copy from Stripe webhook settings
- Update `STRIPE_WEBHOOK_SECRET` in Render

## Support

- **Render Documentation**: [https://render.com/docs](https://render.com/docs)
- **Render Support**: Dashboard → Help → Contact Support
- **Community**: [Render Community Forum](https://community.render.com)

## Next Steps

After successful deployment:

1. ✅ Test all functionality thoroughly
2. ✅ Set up Stripe live mode (see STRIPE_SETUP.md)
3. ✅ Monitor error logs
4. ✅ Set up custom email domain
5. ✅ Create backup strategy
6. ✅ Plan your launch!

---

## Summary

**Your deployment flow:**
```
Local Development
      ↓
Git Commit
      ↓
Push to GitHub
      ↓
Render Auto-Deploys
      ↓
Live at metabomaxpro.onrender.com
      ↓
Configure DNS
      ↓
Live at metabomaxpro.com
      ↓
Launch! 🚀
```

Congratulations on deploying MetaboMax Pro!
