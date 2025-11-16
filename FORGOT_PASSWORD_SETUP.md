# Forgot Password Feature - Setup Guide

The forgot password feature has been successfully added to your MetaboMax Pro application!

## Files Created/Modified

### New Files:
1. **migration_password_reset.sql** - Database migration for password reset tokens table
2. **templates/forgot_password.html** - Forgot password request page
3. **templates/reset_password.html** - Password reset confirmation page
4. **FORGOT_PASSWORD_SETUP.md** - This documentation file

### Modified Files:
1. **app.py** - Added 3 new routes:
   - `/forgot-password` (GET/POST) - Request password reset
   - `/reset-password/<token>` (GET/POST) - Reset password with token
   - `send_password_reset_email()` - Email sending function

2. **templates/login.html** - Added "Forgot Password?" link

## Setup Instructions

### Step 1: Run Database Migration

1. Log into your Supabase dashboard: https://supabase.com
2. Navigate to your project: **svuewehmvqncvrpqpouo**
3. Go to **SQL Editor**
4. Copy and paste the contents of `migration_password_reset.sql`
5. Click **Run** to execute the migration

This will create the `password_reset_tokens` table with proper security policies.

### Step 2: Configure Email Service (Optional but Recommended)

Currently, the forgot password feature works but **doesn't send emails**. In development mode, the reset link will be shown in the console and as a flash message.

To enable email sending, choose ONE of these options:

#### Option A: SendGrid (Recommended)

1. Sign up for SendGrid: https://sendgrid.com
2. Get your API key from SendGrid dashboard
3. Add to your `.env` file:
```bash
EMAIL_SERVICE=sendgrid
SENDGRID_API_KEY=your_sendgrid_api_key_here
FROM_EMAIL=noreply@metabomaxpro.com
```

4. Install SendGrid package:
```bash
pip install sendgrid
```

5. Uncomment the SendGrid code in `app.py` (lines 744-761)

#### Option B: SMTP (Gmail, Outlook, etc.)

Add to your `.env` file:
```bash
EMAIL_SERVICE=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
```

Then add this code to `send_password_reset_email()` function in app.py:

```python
elif email_service == 'smtp':
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Reset Your MetaboMaxPro Password"
    msg['From'] = from_email
    msg['To'] = to_email

    html = f"""
    <html>
      <body>
        <h2>Reset Your Password</h2>
        <p>Hi {user_name},</p>
        <p>You requested to reset your password. Click the link below to reset it:</p>
        <p><a href="{reset_url}" style="background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Reset Password</a></p>
        <p><small>Or copy this link: {reset_url}</small></p>
        <p>This link will expire in 1 hour.</p>
        <p>If you didn't request this, please ignore this email.</p>
        <p>Thanks,<br>MetaboMax Pro Team</p>
      </body>
    </html>
    """

    part = MIMEText(html, 'html')
    msg.attach(part)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
```

## How It Works

### User Flow:

1. **Request Reset:**
   - User goes to login page
   - Clicks "Forgot Password?" link
   - Enters email address
   - Receives reset link (via email or console in dev mode)

2. **Reset Password:**
   - User clicks link in email
   - Lands on reset password page
   - Enters new password twice
   - Password is updated in database
   - Token is marked as used
   - User is redirected to login

### Security Features:

✅ **Secure tokens** - Uses `secrets.token_urlsafe(32)` for cryptographically secure random tokens
✅ **Token expiration** - Tokens expire after 1 hour
✅ **Single-use tokens** - Tokens can only be used once
✅ **Password hashing** - Uses Werkzeug's secure password hashing
✅ **No email disclosure** - Doesn't reveal if email exists in database
✅ **HTTPS required** - Reset links use `_external=True` for full URLs

### Database Schema:

The `password_reset_tokens` table includes:
- `id` - Unique identifier (UUID)
- `user_id` - References profiles table
- `token` - Secure random token string
- `expires_at` - Expiration timestamp (1 hour)
- `used` - Boolean flag to prevent reuse
- `created_at` - Creation timestamp

## Testing

### Development Mode Testing:

1. Start your Flask app:
```bash
cd /Users/markgentry/Downloads/pnoe_webapp
python app.py
```

2. Navigate to: http://localhost:5000/login

3. Click "Forgot Password?"

4. Enter your email address (must exist in database)

5. Check the **console output** for the reset link (since email isn't configured)

6. Copy the reset link and paste it in your browser

7. Enter new password and confirm

8. Try logging in with new password

### Important Notes:

- In development (`FLASK_ENV=development`), reset links are shown in flash messages
- In production, you **must** configure an email service
- Tokens expire after 1 hour
- Each token can only be used once
- Old/expired tokens can be cleaned up with the `cleanup_expired_reset_tokens()` SQL function

## Production Deployment

Before deploying to production:

1. ✅ Run the database migration
2. ✅ Configure email service (SendGrid or SMTP)
3. ✅ Set `FLASK_ENV=production` in `.env`
4. ✅ Test the complete flow
5. ✅ Ensure HTTPS is enabled on your domain

## Troubleshooting

### "Email service not configured" error
- Add email configuration to `.env` file
- Choose SendGrid or SMTP option above

### Reset link not working
- Check if token has expired (1 hour limit)
- Verify database migration ran successfully
- Check browser console for errors

### Database errors
- Ensure migration was run in Supabase SQL Editor
- Check Supabase logs for RLS policy issues
- Verify API keys are correct in `.env`

## Support

For issues:
1. Check server console for detailed error messages
2. Verify all environment variables are set
3. Test database connection to Supabase
4. Check email service credentials

---

**Feature Status:** ✅ Fully Implemented
**Email Sending:** ⚠️ Requires configuration (SendGrid or SMTP)
**Database:** ⚠️ Migration pending (run `migration_password_reset.sql`)
