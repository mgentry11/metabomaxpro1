#!/usr/bin/env python3
"""
Create admin account with unlimited access for mark.gentry@gmail.com
"""
import os
import uuid
import requests
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '').strip().replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
SUPABASE_REST_URL = f"{SUPABASE_URL}/rest/v1"

def get_supabase_headers():
    return {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }

# Admin account details
ADMIN_EMAIL = 'mark.gentry@gmail.com'
ADMIN_PASSWORD = 'AdminPass123!'  # You can change this
ADMIN_NAME = 'Mark Gentry'

print("=" * 60)
print("🔧 Creating Admin Account")
print("=" * 60)
print(f"Email: {ADMIN_EMAIL}")
print(f"Password: {ADMIN_PASSWORD}")
print()

# Check if user already exists
print("1️⃣ Checking if account already exists...")
response = requests.get(
    f"{SUPABASE_REST_URL}/profiles?email=eq.{ADMIN_EMAIL}&select=id,email",
    headers=get_supabase_headers()
)

if response.ok and response.json():
    existing_user = response.json()[0]
    user_id = existing_user['id']
    print(f"   ⚠️ Account already exists with ID: {user_id}")
    print(f"   Updating to unlimited access...")
else:
    # Create new user
    print("   ✅ No existing account found. Creating new account...")
    user_id = str(uuid.uuid4())
    password_hash = generate_password_hash(ADMIN_PASSWORD)

    profile_data = {
        'id': user_id,
        'email': ADMIN_EMAIL,
        'full_name': ADMIN_NAME,
        'password_hash': password_hash,
        'company_name': 'MetaboMax Pro Admin'
    }

    profile_response = requests.post(
        f"{SUPABASE_REST_URL}/profiles",
        headers=get_supabase_headers(),
        json=profile_data
    )

    if not profile_response.ok:
        print(f"   ❌ Failed to create profile: {profile_response.text}")
        exit(1)

    print(f"   ✅ Profile created with ID: {user_id}")

# Create or update subscription with unlimited access
print("\n2️⃣ Setting up unlimited access...")

# Check if subscription exists
sub_check = requests.get(
    f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
    headers=get_supabase_headers()
)

subscription_data = {
    'plan_name': 'admin_unlimited',
    'status': 'active',
    'reports_limit': 999999,  # Unlimited reports
    'reports_used': 0,
    'ai_credits': 999999  # Unlimited AI credits
}

if sub_check.ok and sub_check.json():
    # Update existing subscription
    print("   Updating existing subscription...")
    sub_response = requests.patch(
        f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}",
        headers=get_supabase_headers(),
        json=subscription_data
    )
else:
    # Create new subscription
    print("   Creating new subscription...")
    subscription_data['user_id'] = user_id
    sub_response = requests.post(
        f"{SUPABASE_REST_URL}/subscriptions",
        headers=get_supabase_headers(),
        json=subscription_data
    )

if not sub_response.ok:
    print(f"   ❌ Failed to update subscription: {sub_response.text}")
    exit(1)

print("   ✅ Subscription set to unlimited access")

# Verify the setup
print("\n3️⃣ Verifying account setup...")
verify_response = requests.get(
    f"{SUPABASE_REST_URL}/subscriptions?user_id=eq.{user_id}&select=*",
    headers=get_supabase_headers()
)

if verify_response.ok and verify_response.json():
    sub_data = verify_response.json()[0]
    print(f"   ✅ Verified!")
    print(f"   Plan: {sub_data.get('plan_name')}")
    print(f"   Status: {sub_data.get('status')}")
    print(f"   Reports Limit: {sub_data.get('reports_limit')}")
    print(f"   AI Credits: {sub_data.get('ai_credits')}")

print("\n" + "=" * 60)
print("✅ ADMIN ACCOUNT CREATED SUCCESSFULLY!")
print("=" * 60)
print(f"\n📧 Email: {ADMIN_EMAIL}")
print(f"🔑 Password: {ADMIN_PASSWORD}")
print(f"\n🎯 Access Level: UNLIMITED")
print(f"   - Unlimited basic reports")
print(f"   - Unlimited AI-enhanced reports")
print(f"   - All report types available")
print("\n💡 You can now log in at: http://localhost:5000/login")
print()
