# Metabolic Report Generator SaaS

A Flask-based web application for generating professional metabolic test reports with user authentication and database storage.

## Features

- 🔐 User authentication (register, login, logout)
- 📊 Beautiful HTML metabolic reports
- 💾 Cloud database storage (Supabase)
- 📈 Report history and tracking
- 🎨 White-label capable
- 🖼️ Images from Optimal Vitality Health

## Setup Instructions

### 1. Create a Supabase Project

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Go to Project Settings > API
4. Copy your `Project URL` and `anon/public` key

### 2. Set Up Database Schema

1. In your Supabase dashboard, go to SQL Editor
2. Copy the contents of `schema.sql`
3. Run the SQL to create tables and security policies

### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`
```bash
cp .env.example .env
```

2. Edit `.env` and add your Supabase credentials:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here
FLASK_SECRET_KEY=generate_a_random_secret_key
```

### 4. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python app.py
```

Visit http://localhost:8080

## Project Structure

```
pnoe_webapp/
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html        # Upload/generate page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── dashboard.html    # User dashboard
├── static/
│   ├── css/
│   │   └── style.css     # Styles
│   └── js/
│       └── app.js        # Frontend JavaScript
├── utils/
│   ├── beautiful_report.py
│   └── ultimate_report_template.py
├── uploads/              # Temporary PDF uploads
├── reports/              # Generated reports
├── requirements.txt      # Python dependencies
├── schema.sql           # Database schema
└── .env                 # Environment variables (not in git)
```

## Database Schema

- **profiles** - User profile information
- **metabolic_tests** - Uploaded test data
- **reports** - Generated reports
- **subscriptions** - User subscription status (for future use)

## Future Enhancements

- [ ] Stripe payment integration
- [ ] Subscription tiers ($49, $149, $399/month)
- [ ] API for programmatic access
- [ ] White-label mobile app
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

## License

Proprietary - All Rights Reserved
