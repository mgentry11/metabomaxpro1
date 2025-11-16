#!/usr/bin/env python3
"""
Test creating a Stripe checkout session
"""
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Price IDs from app.py
STRIPE_PRICE_UNLIMITED_BASIC = 'price_1SQKHOC5St4DyD5v1QFSrM0j'  # $69
STRIPE_PRICE_AI_PACKAGE = 'price_1SQKPBC5St4DyD5vnRp1NXK2'      # $99
STRIPE_PRICE_SUBSCRIPTION = 'price_1SOo8NC5St4DyD5vBPXDJrzy'    # $39/month

print("=" * 60)
print("🧪 Testing Checkout Session Creation...")
print("=" * 60)

# Test each plan type
plans = {
    'Unlimited Basic ($69)': {
        'price': STRIPE_PRICE_UNLIMITED_BASIC,
        'mode': 'payment'
    },
    'AI Package ($99)': {
        'price': STRIPE_PRICE_AI_PACKAGE,
        'mode': 'payment'
    },
    'Subscription ($39/mo)': {
        'price': STRIPE_PRICE_SUBSCRIPTION,
        'mode': 'subscription'
    }
}

for plan_name, config in plans.items():
    print(f"\n📦 Testing {plan_name}...")
    try:
        # Create a test customer
        customer = stripe.Customer.create(
            email="test@example.com",
            metadata={'user_id': 'test_user_123'}
        )

        # Create checkout session
        checkout_session = stripe.checkout.Session.create(
            customer=customer.id,
            payment_method_types=['card'],
            line_items=[{'price': config['price'], 'quantity': 1}],
            mode=config['mode'],
            success_url='http://localhost:5000/payment-success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:5000/payment-cancel',
            metadata={'user_id': 'test_user_123'}
        )

        print(f"   ✅ Checkout session created successfully!")
        print(f"   Session ID: {checkout_session.id}")
        print(f"   URL: {checkout_session.url[:50]}...")

        # Clean up test customer
        stripe.Customer.delete(customer.id)

    except stripe.error.InvalidRequestError as e:
        print(f"   ❌ Invalid request: {e}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ All checkout sessions can be created successfully!")
print("=" * 60)
print("\nIf you're seeing errors when clicking 'Buy Now', check:")
print("1. Browser console for JavaScript errors")
print("2. Flask server logs for Python errors")
print("3. Make sure you're logged in before clicking 'Buy Now'")
