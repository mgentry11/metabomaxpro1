# MetaboMax Pro Website

A professional website showcasing MetaboMax Pro's health and fitness solutions for adults over 50, featuring HIT Coach Pro and future metabolic health products.

## Overview

This website serves as the main hub for MetaboMax Pro offerings, with a dedicated focus on science-based solutions for mature adults.

## Structure

### Main Pages

1. **index.html** - Main landing page showcasing all products
   - About MetaboMax Pro
   - Product offerings (HIT Coach Pro & MetaboMax Pro)
   - Science and research foundation
   - Target audience
   - Contact/CTA

2. **hitcoachpro.html** - Dedicated HIT Coach Pro product page
   - Complete app details
   - Dr. Darden's research
   - Workout protocols (A & B)
   - Features and how it works
   - Download CTA

3. **styles.css** - Unified stylesheet for entire site

## Products Featured

### HIT Coach Pro (Available Now)
- iOS app for voice-guided High-Intensity Training
- Based on Dr. Ellington Darden's research
- 15-20 minute workouts, 2-3x per week
- Perfect for adults over 50

### MetaboMax Pro (Coming Soon)
- Metabolic health optimization program
- Nutrition protocols
- Supplement recommendations
- Biomarker tracking

## Color Scheme

The site uses a dark theme with emerald and neon green accents to match the HIT Coach Pro app branding:

- **Primary**: Emerald (#10b981) and Neon Green (#22c55e)
- **Backgrounds**: Black (#0a0a0a) and Dark Gray (#1a1a1a)
- **Text**: White and Gray

## Key Features

- **Unified Branding** - Consistent design across all products
- **Responsive Design** - Works on all devices
- **Science-Focused** - Research-backed content
- **Age-Specific** - Tailored for 50+ demographic
- **Clean Navigation** - Easy movement between products

## Local Testing

### Quick Preview
```bash
cd /Users/markgentry/Sites/metabomaxpro.com
python3 -m http.server 8000
```
Then open: http://localhost:8000

### Test Links
- Main page: http://localhost:8000/index.html
- HIT Coach Pro: http://localhost:8000/hitcoachpro.html

## Customization

### Update App Store Links

Replace all `#` placeholders with actual App Store URL:
```html
<a href="#" class="btn btn-primary">Download on App Store</a>
```

### Add Images

1. Dr. Ellington Darden photo: `placeholder-darden.jpg` (150x150px recommended)
2. Optional: App screenshots, before/after photos, product images

### Update Contact Info

Update email in footer:
```html
<p class="cta-note">Questions? Email us at info@metabomaxpro.com</p>
```

## Deployment Options

### Recommended: Static Hosting

**Netlify (Easiest)**
1. Go to https://app.netlify.com/drop
2. Drag and drop the entire folder
3. Get instant URL

**Vercel**
1. Go to https://vercel.com/new
2. Import from Git or upload
3. Deploy

**GitHub Pages**
1. Create GitHub repo
2. Push files
3. Enable Pages in settings

### Traditional Hosting

Upload these files via FTP:
- index.html
- hitcoachpro.html
- styles.css
- Any images

### Domain Setup

For metabomaxpro.com domain:
1. Purchase domain (Namecheap, GoDaddy, etc.)
2. Point DNS to hosting provider
3. Configure SSL certificate (usually automatic with modern hosts)

## SEO Optimization

Add to `<head>` section of both pages:

```html
<!-- SEO -->
<meta name="description" content="MetaboMax Pro - Science-based health and fitness solutions for adults over 50. Featuring HIT Coach Pro strength training app.">
<meta name="keywords" content="strength training over 50, HIT training, metabolic health, Dr. Ellington Darden">

<!-- Open Graph -->
<meta property="og:title" content="MetaboMax Pro - Health Solutions for Over 50">
<meta property="og:description" content="Science-backed strength training and metabolic health programs">
<meta property="og:image" content="https://metabomaxpro.com/og-image.jpg">
<meta property="og:url" content="https://metabomaxpro.com">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="MetaboMax Pro">
<meta name="twitter:description" content="Science-based solutions for thriving over 50">
```

## Analytics

Add Google Analytics before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## Future Enhancements

- [ ] Add MetaboMax Pro product page when ready
- [ ] Blog section for health/fitness articles
- [ ] Customer testimonials with photos
- [ ] Video demonstrations
- [ ] FAQ section
- [ ] Email newsletter signup
- [ ] App screenshots gallery
- [ ] Research papers library
- [ ] User success stories

## File Structure

```
metabomaxpro.com/
├── index.html           # Main landing page
├── hitcoachpro.html     # HIT Coach Pro product page
├── styles.css           # Unified stylesheet
├── README.md            # This file
└── images/              # Images folder (create as needed)
    └── placeholder-darden.jpg
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome)

## License

© 2024 MetaboMax Pro. All rights reserved.

## Credits

- **Design**: Based on HIT Coach Pro app branding
- **Research**: Dr. Ellington Darden's HIT methodology
- **Content**: 40+ years of exercise science and metabolic health research
