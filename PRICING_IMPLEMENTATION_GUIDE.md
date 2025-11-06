# Pricing Restructure Implementation Guide

## Overview
Implementing the "2 Free Basic Reports" pricing model as defined in FINAL_PRICING_STRATEGY.md

## Step 1: Database Migration ✅
**File:** `migration_pricing_restructure.sql`
**Actions:**
- Add `ai_credits` column to subscriptions table
- Update free tier users to 2 report limit
- Update handle_new_user() function for new signups

**To Execute:**
```sql
-- Run in Supabase SQL Editor
-- Copy contents of migration_pricing_restructure.sql
```

## Step 2: Update app.py Logic

### 2.1 Add Helper Functions (after line 100)
```python
def get_user_subscription(user_id):
    """Get user's subscription details"""
    try:
        response = http_session.get(
            f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
            headers=get_supabase_headers()
        )
        if response.ok and response.json():
            return response.json()[0]
        return None
    except Exception as e:
        print(f"Error getting subscription: {e}")
        return None

def can_generate_basic_report(user_id):
    """Check if user can generate a basic report"""
    subscription = get_user_subscription(user_id)
    if not subscription:
        return False, "No subscription found"

    reports_used = subscription.get('reports_used', 0)
    reports_limit = subscription.get('reports_limit', 0)

    if reports_used >= reports_limit:
        return False, f"You've used all {reports_limit} of your free reports. Please upgrade to continue."

    return True, f"Report {reports_used + 1} of {reports_limit}"

def can_use_ai_recommendations(user_id):
    """Check if user has AI credits available"""
    subscription = get_user_subscription(user_id)
    if not subscription:
        return False, "No subscription found"

    plan_name = subscription.get('plan_name', 'free')
    ai_credits = subscription.get('ai_credits', 0)

    # Subscription users get unlimited AI
    if plan_name == 'subscription':
        return True, "Unlimited AI (subscription)"

    # AI package or one-time purchases
    if ai_credits > 0:
        return True, f"{ai_credits} AI credits remaining"

    return False, "No AI credits available. Please upgrade to add AI recommendations."

def use_ai_credit(user_id):
    """Decrement user's AI credits by 1"""
    subscription = get_user_subscription(user_id)
    if not subscription:
        return False

    plan_name = subscription.get('plan_name', 'free')

    # Subscription users have unlimited, don't decrement
    if plan_name == 'subscription':
        return True

    ai_credits = subscription.get('ai_credits', 0)
    if ai_credits > 0:
        try:
            http_session.patch(
                f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
                headers=get_supabase_headers(),
                json={'ai_credits': ai_credits - 1}
            )
            return True
        except Exception as e:
            print(f"Error using AI credit: {e}")
            return False

    return False
```

### 2.2 Update `/generate` Route (line 743)
Add check at the beginning (after line 752):
```python
@app.route('/generate', methods=['POST'])
@login_required
def generate_report():
    """Generate final HTML report with custom data"""
    data = request.json
    file_id = data.get('file_id')
    test_id = data.get('test_id')

    if not file_id:
        return jsonify({'error': 'No file ID provided'}), 400

    user_id = session['user']['id']

    # CHECK REPORT LIMIT
    can_generate, message = can_generate_basic_report(user_id)
    if not can_generate:
        return jsonify({
            'error': message,
            'upgrade_required': True,
            'pricing_url': '/pricing'
        }), 403

    # Rest of function continues...
```

### 2.3 Update `/generate-ai-recommendation` Route (line 1817)
Add AI credit check at the beginning:
```python
@app.route('/generate-ai-recommendation', methods=['POST'])
@login_required
def generate_ai_recommendation():
    """Generate AI recommendations for existing report"""
    try:
        data = request.json
        file_id = data.get('file_id')
        subjects = data.get('subjects', [])

        user_id = session['user']['id']

        # CHECK AI CREDITS
        can_use_ai, message = can_use_ai_recommendations(user_id)
        if not can_use_ai:
            return jsonify({
                'error': message,
                'upgrade_required': True,
                'pricing_url': '/pricing'
            }), 403

        # ... generate AI recommendations ...

        # USE AI CREDIT (decrement counter)
        use_ai_credit(user_id)

        # Rest of function continues...
```

## Step 3: Update Stripe Products

### Current Stripe Products:
```python
STRIPE_PRICE_ONE_TIME = 'price_1SOnZGC5St4DyD5vE5EzwQBx'  # $69 Single Report
STRIPE_PRICE_SUBSCRIPTION = 'price_1SOo8NC5St4DyD5vBPXDJrzy'  # $39/month Unlimited
```

### New Stripe Products Needed:
```python
STRIPE_PRICE_UNLIMITED_BASIC = 'price_XXX'  # $69 Unlimited Basic (no AI)
STRIPE_PRICE_AI_PACKAGE = 'price_XXX'  # $99 Unlimited Basic + 10 AI credits
STRIPE_PRICE_SUBSCRIPTION = 'price_1SOo8NC5St4DyD5vBPXDJrzy'  # $39/month (keep existing)
```

### Create in Stripe Dashboard:
1. **Product: "Unlimited Basic Reports"**
   - Price: $69 one-time
   - Metadata: `plan_type=unlimited_basic`, `reports_limit=9999`, `ai_credits=0`

2. **Product: "AI-Enhanced Package"**
   - Price: $99 one-time
   - Metadata: `plan_type=ai_package`, `reports_limit=9999`, `ai_credits=10`

3. **Product: "Monthly Subscription"** (already exists)
   - Price: $39/month recurring
   - Metadata: `plan_type=subscription`, `reports_limit=9999`, `ai_credits=9999`

### Update Stripe Webhook Handler
In `/webhook/stripe` route, update to handle new products:
```python
# After successful payment
if event_type == 'checkout.session.completed':
    session = event['data']['object']
    price_id = session.get('amount_total') / 100

    if price_id == 69:
        # Check metadata to determine which $69 product
        metadata = session.get('metadata', {})
        plan_type = metadata.get('plan_type', 'unlimited_basic')

        if plan_type == 'unlimited_basic':
            reports_limit = 9999
            ai_credits = 0
            plan_name = 'unlimited_basic'
        elif plan_type == 'ai_package' and price_id == 99:
            reports_limit = 9999
            ai_credits = 10
            plan_name = 'ai_package'

    # Update subscription in database
    http_session.patch(
        f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{customer_id}",
        headers=get_supabase_headers(),
        json={
            'plan_name': plan_name,
            'reports_limit': reports_limit,
            'ai_credits': ai_credits,
            'status': 'active'
        }
    )
```

## Step 4: Update Dashboard UI

### File: `templates/dashboard.html`

Add subscription status display after line 75:
```html
<!-- Subscription Status -->
{% if subscription %}
<div class="card" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; margin-bottom: 2rem;">
    <h2 style="color: white;">📊 Your Plan</h2>

    {% if subscription.plan_name == 'free' %}
        <div style="font-size: 1.2rem; margin-bottom: 1rem;">
            <strong>Free Tier</strong> - Try 2 FREE reports ({{ subscription.reports_used }} used)
        </div>
        <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <p style="margin: 0; font-size: 1.1rem;">
                ✅ Reports remaining: <strong>{{ subscription.reports_limit - subscription.reports_used }}</strong> of {{ subscription.reports_limit }}
            </p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.95rem; opacity: 0.9;">
                Value: ${{ (subscription.reports_limit - subscription.reports_used) * 175 }}-{{ (subscription.reports_limit - subscription.reports_used) * 250 }} (what facilities charge)
            </p>
        </div>

        {% if subscription.reports_used >= subscription.reports_limit %}
        <div style="background: rgba(239, 68, 68, 0.2); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #ef4444;">
            <p style="margin: 0 0 1rem 0; font-size: 1.1rem; font-weight: 600;">
                ⚠️ You've used all your free reports
            </p>
            <a href="{{ url_for('pricing') }}" style="background: white; color: #3b82f6; padding: 0.75rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600; display: inline-block;">
                Upgrade to Continue
            </a>
        </div>
        {% endif %}

    {% elif subscription.plan_name == 'unlimited_basic' %}
        <div style="font-size: 1.2rem; margin-bottom: 1rem;">
            <strong>Unlimited Basic</strong> - $69 one-time
        </div>
        <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;">
            <p style="margin: 0;">✅ <strong>Unlimited basic reports</strong></p>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">❌ No AI recommendations (upgrade to add)</p>
        </div>

    {% elif subscription.plan_name == 'ai_package' %}
        <div style="font-size: 1.2rem; margin-bottom: 1rem;">
            <strong>AI-Enhanced Package</strong> - $99 one-time
        </div>
        <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;">
            <p style="margin: 0;">✅ <strong>Unlimited basic reports</strong></p>
            <p style="margin: 0.5rem 0 0 0;">✅ <strong>{{ subscription.ai_credits }} AI credits remaining</strong></p>
        </div>

    {% elif subscription.plan_name == 'subscription' %}
        <div style="font-size: 1.2rem; margin-bottom: 1rem;">
            <strong>Monthly Subscription</strong> - $39/month
        </div>
        <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;">
            <p style="margin: 0;">✅ <strong>Unlimited basic reports</strong></p>
            <p style="margin: 0.5rem 0 0 0;">✅ <strong>Unlimited AI recommendations</strong></p>
        </div>
    {% endif %}
</div>
{% endif %}
```

## Step 5: Update Landing Page Messaging

### File: `templates/landing.html`

Update hero section (line 318):
```html
<h1>Try 2 FREE Professional Reports<br>Facilities Charge $175-250 Each</h1>
<p class="subtitle">Get $350-500 worth of metabolic analysis - completely free. No credit card required.</p>
<div class="price-highlight">
    2 FREE Reports to Start • Then $69 for Unlimited Basic or $99 with AI
</div>
```

Add value proposition box after hero:
```html
<section style="background: white; padding: 3rem 2rem;">
    <div style="max-width: 1100px; margin: 0 auto; text-align: center;">
        <h2 style="color: #1e293b; margin-bottom: 2rem;">🎁 Start With 2 FREE Reports</h2>

        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-bottom: 2rem;">
            <div style="background: #f0fdf4; padding: 2rem; border-radius: 12px;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎁</div>
                <h3 style="color: #065f46;">FREE Tier</h3>
                <p style="font-size: 2rem; font-weight: 800; color: #10b981; margin: 0.5rem 0;">$0</p>
                <p style="color: #64748b;">2 free basic reports<br>($350-500 value)</p>
            </div>

            <div style="background: #eff6ff; padding: 2rem; border-radius: 12px; border: 3px solid #3b82f6;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⭐</div>
                <h3 style="color: #1e40af;">Unlimited Basic</h3>
                <p style="font-size: 2rem; font-weight: 800; color: #3b82f6; margin: 0.5rem 0;">$69</p>
                <p style="color: #64748b;">Unlimited reports<br>No AI</p>
                <div style="background: #dbeafe; padding: 0.5rem; border-radius: 6px; margin-top: 1rem;">
                    <small style="font-weight: 600; color: #1e40af;">MOST POPULAR</small>
                </div>
            </div>

            <div style="background: #f5f3ff; padding: 2rem; border-radius: 12px;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <h3 style="color: #6366f1;">AI-Enhanced</h3>
                <p style="font-size: 2rem; font-weight: 800; color: #6366f1; margin: 0.5rem 0;">$99</p>
                <p style="color: #64748b;">Unlimited + 10 AI credits</p>
            </div>
        </div>

        <a href="{{ url_for('register') }}" class="btn btn-primary" style="font-size: 1.2rem; padding: 1.25rem 3rem;">
            Get Your 2 FREE Reports
        </a>
    </div>
</section>
```

## Step 6: Update Pricing Page

### File: `templates/pricing.html`

Update pricing cards to show new structure (see FINAL_PRICING_STRATEGY.md lines 222-235)

## Step 7: Testing Checklist

### Database:
- [ ] Run migration_pricing_restructure.sql in Supabase
- [ ] Verify ai_credits column exists
- [ ] Verify free tier users have reports_limit=2
- [ ] Verify new signups get reports_limit=2

### App Logic:
- [ ] Test free user can generate 2 reports
- [ ] Test free user blocked after 2 reports
- [ ] Test upgrade prompt appears when limit reached
- [ ] Test AI credit checking works
- [ ] Test AI credits decrement properly

### Stripe:
- [ ] Create new products in Stripe dashboard
- [ ] Update STRIPE_PRICE_* constants in app.py
- [ ] Test $69 unlimited basic purchase
- [ ] Test $99 AI package purchase
- [ ] Test $39/month subscription
- [ ] Verify webhook updates subscription correctly

### UI:
- [ ] Dashboard shows correct plan info
- [ ] Dashboard shows reports remaining
- [ ] Dashboard shows AI credits remaining
- [ ] Landing page shows "2 FREE" messaging
- [ ] Pricing page shows new tiers
- [ ] Upgrade prompts work

## Step 8: Deployment

1. Run database migration in Supabase
2. Update app.py with new logic
3. Create new Stripe products
4. Update template files
5. Test thoroughly in development
6. Deploy to production via git push

## Rollback Plan

If issues arise:
1. Revert database: `UPDATE subscriptions SET reports_limit = 10 WHERE plan_name = 'free';`
2. Revert app.py to previous commit
3. Keep old Stripe products active
