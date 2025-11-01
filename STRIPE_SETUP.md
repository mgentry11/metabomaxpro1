# Stripe Setup Guide for MetaboMax Pro

This guide will walk you through setting up Stripe payment integration for your MetaboMax Pro application.

## Step 1: Create a Stripe Account

1. Go to [https://stripe.com](https://stripe.com)
2. Click "Sign up" or "Start now"
3. Complete the registration process with your business information
4. Verify your email address

## Step 2: Get Your API Keys

### For Development (Test Mode):

1. Log in to your Stripe Dashboard
2. Make sure you're in **Test mode** (toggle in the top right corner)
3. Navigate to **Developers > API keys**
4. You'll see two keys:
   - **Publishable key** (starts with `pk_test_`)
   - **Secret key** (starts with `sk_test_`) - Click "Reveal test key"

### For Production (Live Mode):

1. In the Stripe Dashboard, toggle to **Live mode**
2. Navigate to **Developers > API keys**
3. You'll see:
   - **Publishable key** (starts with `pk_live_`)
   - **Secret key** (starts with `sk_live_`) - Click "Reveal live key"

**⚠️ Important:** Never share your secret key publicly or commit it to version control!

## Step 3: Add Keys to Your .env File

Open your `.env` file and add your Stripe keys:

```bash
# Stripe Configuration (Use test keys for development)
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

## Step 4: Set Up Webhooks

Webhooks allow Stripe to notify your application about important events (successful payments, subscription cancellations, etc.).

### For Development (Local Testing):

1. Install Stripe CLI: https://stripe.com/docs/stripe-cli
2. Run `stripe login` to connect to your account
3. Forward webhook events to your local server:
   ```bash
   stripe listen --forward-to localhost:8080/stripe-webhook
   ```
4. Copy the webhook signing secret (starts with `whsec_`) and add it to your `.env` file

### For Production:

1. Go to **Developers > Webhooks** in Stripe Dashboard
2. Click **+ Add endpoint**
3. Enter your endpoint URL: `https://yourdomain.com/stripe-webhook`
4. Select events to listen to:
   - `checkout.session.completed`
   - `customer.subscription.deleted`
   - `customer.subscription.updated`
5. Click **Add endpoint**
6. Copy the **Signing secret** (starts with `whsec_`) and add it to your production `.env` file

## Step 5: Test Your Integration

### Test Cards:

Stripe provides test card numbers for testing payments:

- **Success:** `4242 4242 4242 4242`
- **Declined:** `4000 0000 0000 0002`
- **Requires authentication:** `4000 0025 0000 3155`

Use any future expiration date, any 3-digit CVC, and any 5-digit ZIP code.

### Testing the Flow:

1. Start your Flask app
2. Register a new account
3. Go to the pricing page
4. Click "Get Started" or "Start Free Trial"
5. You should be redirected to Stripe Checkout
6. Use a test card to complete payment
7. You should be redirected to the success page
8. Check your Stripe Dashboard to see the test payment

## Step 6: Configure Pricing (Optional)

By default, the app uses inline pricing:
- One-time: $69
- Monthly subscription: $39/month

To use Stripe Price IDs instead:

1. Go to **Products** in Stripe Dashboard
2. Create products for your plans
3. Copy the Price IDs (start with `price_`)
4. Update `app.py` to use these Price IDs in the checkout session creation

## Step 7: Go Live

When you're ready to accept real payments:

1. Complete your Stripe account activation:
   - Business details
   - Bank account information
   - Tax information
2. Switch to **Live mode** in Stripe Dashboard
3. Get your live API keys
4. Update your production `.env` file with live keys:
   ```bash
   STRIPE_SECRET_KEY=sk_live_your_live_secret_key
   STRIPE_PUBLISHABLE_KEY=pk_live_your_live_publishable_key
   STRIPE_WEBHOOK_SECRET=whsec_your_live_webhook_secret
   ```
5. Set up production webhook endpoint (see Step 4)
6. Test with real cards before announcing

## Pricing Structure

Your app currently supports:

### One-Time Payment ($69)
- Single comprehensive metabolic report
- Biological age analysis
- PDF export
- Instant delivery

### Monthly Subscription ($39/month)
- **Unlimited** metabolic reports
- Cloud storage for all reports
- Progress tracking over time
- Cancel anytime

### Teams & Gyms (Custom)
- Contact sales for pricing
- Multiple user accounts
- White-label reports
- API access

## Troubleshooting

### "No API key provided"
- Make sure your `.env` file has the STRIPE_SECRET_KEY set
- Restart your Flask server after updating `.env`

### "Invalid API Key"
- Check that you're using the correct key for your mode (test vs live)
- Make sure there are no extra spaces in the key

### Webhook signature verification failed
- Ensure your STRIPE_WEBHOOK_SECRET matches the webhook endpoint
- For local testing, make sure Stripe CLI is running

### Payment succeeds but subscription not updated
- Check webhook events in Stripe Dashboard
- Look for errors in your Flask application logs
- Verify the webhook endpoint is publicly accessible (for production)

## Security Best Practices

1. **Never commit API keys to version control**
   - Use `.env` files (already in `.gitignore`)

2. **Use different keys for development and production**
   - Test mode for development
   - Live mode for production

3. **Verify webhook signatures**
   - Always validate webhook events (already implemented)

4. **Use HTTPS in production**
   - Required for live mode
   - Stripe CLI handles this for local testing

5. **Monitor your Stripe Dashboard**
   - Check for suspicious activity
   - Review failed payments
   - Monitor subscription churn

## Support

- Stripe Documentation: https://stripe.com/docs
- Stripe Support: https://support.stripe.com
- Test your integration: https://stripe.com/docs/testing

## Next Steps

After setting up Stripe:
1. Deploy your application to production (see DEPLOYMENT.md)
2. Connect your custom domain (metabomaxpro.com)
3. Start accepting payments!
