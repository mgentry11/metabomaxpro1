#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '').strip().replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
SUPABASE_REST_URL = f"{SUPABASE_URL}/rest/v1"

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}

# First, get all profiles to see what we have
print("📋 Fetching all profiles...")
response = requests.get(f"{SUPABASE_REST_URL}/profiles?select=*", headers=headers)
if response.ok:
    profiles = response.json()
    print(f"\nFound {len(profiles)} profiles:")
    for p in profiles:
        print(f"  - {p.get('email')} (ID: {p.get('id')[:8]}...)")
    print()
else:
    print(f"❌ Error fetching profiles: {response.status_code}")
    print(response.text)
    exit(1)

# Get all subscriptions
print("📋 Fetching all subscriptions...")
response = requests.get(f"{SUPABASE_REST_URL}/subscriptions?select=*", headers=headers)
if response.ok:
    subscriptions = response.json()
    print(f"Found {len(subscriptions)} subscriptions:")
    for s in subscriptions:
        print(f"  - User ID: {s.get('user_id')[:8]}..., Plan: {s.get('plan_name')}, Reports: {s.get('reports_used')}/{s.get('reports_limit')}")
    print()
else:
    print(f"❌ Error fetching subscriptions: {response.status_code}")
    print(response.text)
    exit(1)

# Ask for confirmation
print("\n⚠️  WARNING: This will DELETE ALL accounts from the database!")
print("This includes:")
print(f"  - {len(profiles)} profiles")
print(f"  - {len(subscriptions)} subscriptions")
print("  - All uploaded files and reports")
print()

confirm = input("Type 'DELETE ALL' to confirm: ")
if confirm != 'DELETE ALL':
    print("❌ Cancelled. No changes made.")
    exit(0)

# Delete all subscriptions first (to avoid foreign key issues)
print("\n🗑️  Deleting all subscriptions...")
response = requests.delete(
    f"{SUPABASE_REST_URL}/subscriptions?id=gte.0",
    headers=headers
)
if response.ok:
    print(f"✅ Deleted {len(subscriptions)} subscriptions")
else:
    print(f"❌ Error deleting subscriptions: {response.status_code}")
    print(response.text)

# Delete all profiles
print("🗑️  Deleting all profiles...")
response = requests.delete(
    f"{SUPABASE_REST_URL}/profiles?id=neq.",
    headers=headers
)
if response.ok:
    print(f"✅ Deleted {len(profiles)} profiles")
else:
    print(f"❌ Error deleting profiles: {response.status_code}")
    print(response.text)

print("\n✅ All accounts cleared! You can now start fresh.")
