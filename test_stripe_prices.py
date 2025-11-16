#!/usr/bin/env python3
"""
Test script to verify Stripe price IDs are valid
"""
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Price IDs from app.py
PRICE_IDS = {
    'unlimited_basic': 'price_1SQKHOC5St4DyD5v1QFSrM0j',  # $69
    'ai_package': 'price_1SQKPBC5St4DyD5vnRp1NXK2',      # $99
    'subscription': 'price_1SOo8NC5St4DyD5vBPXDJrzy'     # $39/month
}

print("=" * 60)
print("🔍 Checking Stripe Price IDs...")
print("=" * 60)

for plan_name, price_id in PRICE_IDS.items():
    try:
        price = stripe.Price.retrieve(price_id)
        amount = price.unit_amount / 100  # Convert cents to dollars
        currency = price.currency.upper()

        if price.recurring:
            interval = price.recurring.interval
            print(f"✅ {plan_name}: {currency} ${amount}/{interval}")
        else:
            print(f"✅ {plan_name}: {currency} ${amount} (one-time)")

        print(f"   Price ID: {price_id}")
        print(f"   Active: {price.active}")
        print(f"   Product: {price.product}")
        print()

    except stripe.error.InvalidRequestError as e:
        print(f"❌ {plan_name}: INVALID PRICE ID")
        print(f"   Price ID: {price_id}")
        print(f"   Error: {e}")
        print()
    except Exception as e:
        print(f"❌ {plan_name}: ERROR")
        print(f"   Error: {e}")
        print()

print("=" * 60)
print("📋 Next Steps:")
print("=" * 60)
print("If any price IDs are invalid, you need to:")
print("1. Go to https://dashboard.stripe.com/test/products")
print("2. Create products with the correct prices:")
print("   - Unlimited Basic: $69 one-time payment")
print("   - AI Package: $99 one-time payment")
print("   - Monthly Subscription: $39/month recurring")
print("3. Copy the price IDs (starts with 'price_') from Stripe")
print("4. Update them in app.py (lines 51-53)")
