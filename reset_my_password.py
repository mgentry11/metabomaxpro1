#!/usr/bin/env python3
"""
Quick script to reset password for mark.gentry@gmail.com
Run this to set a new password directly in the database
"""

import os
import requests
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '').strip()
SUPABASE_REST_URL = f"{SUPABASE_URL}/rest/v1"

def get_supabase_headers():
    return {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }

def reset_password(email, new_password):
    """Reset password for a user"""

    # Hash the new password
    password_hash = generate_password_hash(new_password)

    # Update password in database
    response = requests.patch(
        f"{SUPABASE_REST_URL}/profiles?email=eq.{email}",
        headers=get_supabase_headers(),
        json={'password_hash': password_hash}
    )

    if response.ok:
        print(f"✅ Password successfully reset for {email}")
        print(f"New password: {new_password}")
        print("\nYou can now log in at: https://metabomaxpro.com/login")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    EMAIL = "mark.gentry@gmail.com"
    NEW_PASSWORD = input(f"Enter new password for {EMAIL}: ")

    if len(NEW_PASSWORD) < 8:
        print("❌ Password must be at least 8 characters long!")
    else:
        confirm = input(f"\nReset password for {EMAIL}? (yes/no): ")
        if confirm.lower() == 'yes':
            reset_password(EMAIL, NEW_PASSWORD)
        else:
            print("Cancelled.")
