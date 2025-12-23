# bigoil.net Website Fix - Quick Start Guide

## Problem Summary
- **HTTPS SSL Error**: CloudFront distribution (E1R1OOQP5GPCDX) doesn't have a valid SSL certificate for bigoil.net
- **HTTP 403 Forbidden**: CloudFront can't access S3 origin due to missing permissions

## Solution Overview
1. Create ACM SSL certificate for bigoil.net (in us-east-1 region)
2. Configure S3 bucket policy to allow CloudFront access
3. Set up Origin Access Control (OAC) for security
4. Update CloudFront distribution with certificate and proper configuration

---

## Quick Fix - Option 1: Automated Script

Run the fully automated script that handles everything:

```bash
cd /Users/markgentry/metabomaxpro1
chmod +x *.sh
./fix_bigoil_auto.sh
```

This script will:
- Diagnose current configuration
- Create/verify ACM certificate
- Fix S3 bucket permissions
- Update CloudFront distribution
- Wait for deployment
- Verify website is working

**Note**: If certificate validation is needed, the script will pause and show you the DNS records to add. After adding them, run the script again.

---

## Step-by-Step Fix - Option 2: Manual Control

If you prefer to run each step manually:

### Step 1: Diagnose Issues
```bash
./1_diagnose_bigoil.sh
```
This will show current configuration and list all issues found.

### Step 2: Create/Verify SSL Certificate
```bash
./2_create_certificate.sh
```
- Creates ACM certificate if it doesn't exist
- Shows DNS validation records to add
- Checks if existing certificate is validated

**If DNS validation is required:**
1. Add the CNAME records shown to your DNS provider
2. Wait 5-30 minutes for validation
3. Run this script again to verify

### Step 3: Fix S3 Bucket Access
```bash
./3_fix_s3_access.sh
```
- Creates Origin Access Control (OAC)
- Updates S3 bucket policy for CloudFront access
- Verifies index.html exists

### Step 4: Update CloudFront Distribution
```bash
./4_update_cloudfront.sh
```
- Attaches SSL certificate to CloudFront
- Adds domain aliases (bigoil.net, www.bigoil.net)
- Configures OAC for S3 access
- Sets default root object to index.html
- Triggers CloudFront deployment (15-30 minutes)

### Step 5: Verify Website
```bash
./5_verify_website.sh
```
- Waits for CloudFront deployment to complete
- Tests HTTPS access
- Verifies SSL certificate
- Confirms website is working

---

## Manual Commands Reference

All detailed manual commands are documented in:
```bash
cat bigoil_fix_steps.md
```

---

## Files Created

| File | Purpose |
|------|---------|
| `fix_bigoil_auto.sh` | Fully automated fix script |
| `1_diagnose_bigoil.sh` | Diagnose current configuration |
| `2_create_certificate.sh` | Create/verify ACM certificate |
| `3_fix_s3_access.sh` | Fix S3 bucket permissions |
| `4_update_cloudfront.sh` | Update CloudFront distribution |
| `5_verify_website.sh` | Verify website is working |
| `bigoil_fix_steps.md` | Detailed manual steps |
| `fix_bigoil_website.sh` | Original comprehensive script |
| `README_BIGOIL_FIX.md` | This guide |

---

## Quick Verification Commands

After running the fix, verify with:

```bash
# Check CloudFront deployment status
aws cloudfront get-distribution --id E1R1OOQP5GPCDX \
  --query 'Distribution.Status'

# Test HTTPS access
curl -I https://bigoil.net
curl -I https://www.bigoil.net

# Check certificate status
aws acm describe-certificate \
  --certificate-arn <CERT_ARN> \
  --region us-east-1 \
  --query 'Certificate.Status'

# View in browser
open https://bigoil.net
```

---

## Troubleshooting

### Certificate Validation Pending
**Problem**: ACM certificate stuck in "PENDING_VALIDATION"

**Solution**:
1. Check DNS records are added correctly:
   ```bash
   dig _<validation-string>.<domain> CNAME
   ```
2. Wait 5-30 minutes for DNS propagation
3. Run `./2_create_certificate.sh` again to check status

### 403 Error After Fix
**Problem**: Still getting 403 errors after applying fixes

**Solution**:
1. Wait for CloudFront deployment to complete (check with step 5)
2. Clear CloudFront cache:
   ```bash
   aws cloudfront create-invalidation \
     --distribution-id E1R1OOQP5GPCDX \
     --paths "/*"
   ```
3. Verify S3 bucket has index.html:
   ```bash
   aws s3 ls s3://<bucket-name>/index.html
   ```

### SSL Certificate Error in Browser
**Problem**: Browser shows SSL certificate warning

**Possible Causes**:
- CloudFront deployment not complete (wait longer)
- Certificate not attached to distribution
- DNS not pointing to CloudFront

**Solution**:
1. Verify DNS points to CloudFront:
   ```bash
   dig bigoil.net
   ```
2. Check CloudFront status is "Deployed"
3. Verify certificate ARN is set in distribution:
   ```bash
   ./1_diagnose_bigoil.sh
   ```

### Website Returns 404
**Problem**: HTTPS works but website shows 404

**Solution**:
Upload your website files to S3:
```bash
# Upload single file
aws s3 cp /path/to/index.html s3://<bucket-name>/index.html

# Sync entire directory
aws s3 sync /path/to/website/ s3://<bucket-name>/ --delete
```

---

## AWS Resources Modified

This fix modifies the following AWS resources:

1. **ACM Certificate** (us-east-1)
   - Creates new certificate for bigoil.net and www.bigoil.net
   - Uses DNS validation

2. **CloudFront Distribution** (E1R1OOQP5GPCDX)
   - Adds ACM certificate
   - Configures domain aliases
   - Sets up Origin Access Control
   - Sets default root object

3. **S3 Bucket** (bigoil.net or similar)
   - Updates bucket policy for CloudFront access
   - No changes to bucket contents

4. **Origin Access Control**
   - Creates new OAC for secure S3 access
   - Replaces public bucket access

---

## Timeline

| Step | Estimated Time |
|------|----------------|
| 1. Diagnosis | 1 minute |
| 2. Certificate creation | 2 minutes |
| 2a. DNS validation (if needed) | 5-30 minutes |
| 3. S3 bucket policy | 1 minute |
| 4. CloudFront update | 1 minute |
| 5. CloudFront deployment | 15-30 minutes |
| 6. Verification | 2 minutes |
| **Total (if no validation needed)** | ~20-35 minutes |
| **Total (with DNS validation)** | ~30-65 minutes |

---

## Support

If issues persist after running all fixes:

1. Review CloudFront logs:
   ```bash
   aws cloudfront get-distribution --id E1R1OOQP5GPCDX
   ```

2. Check S3 bucket configuration:
   ```bash
   aws s3api get-bucket-policy --bucket <bucket-name>
   aws s3api get-public-access-block --bucket <bucket-name>
   ```

3. Verify DNS settings:
   ```bash
   dig bigoil.net
   dig www.bigoil.net
   ```

4. Check ACM certificate details:
   ```bash
   aws acm describe-certificate \
     --certificate-arn <cert-arn> \
     --region us-east-1
   ```

---

## Next Steps After Fix

Once the website is working:

1. **Enable Logging** (Optional):
   ```bash
   # Configure CloudFront to log access
   aws cloudfront update-distribution \
     --id E1R1OOQP5GPCDX \
     --logging-config Enabled=true,Bucket=<log-bucket>.s3.amazonaws.com,Prefix=bigoil-logs/
   ```

2. **Set up Monitoring** (Optional):
   - Enable CloudWatch alarms for 4xx/5xx errors
   - Set up billing alerts

3. **Performance Optimization** (Optional):
   - Configure cache behaviors
   - Enable compression
   - Add custom error pages

4. **Security Enhancements** (Optional):
   - Configure WAF rules
   - Set up geo-restrictions if needed
   - Review security headers

---

## Success Criteria

Website is considered fully fixed when:

- ✅ https://bigoil.net returns HTTP 200
- ✅ https://www.bigoil.net returns HTTP 200
- ✅ SSL certificate is valid (no browser warnings)
- ✅ HTTP redirects to HTTPS
- ✅ CloudFront distribution status is "Deployed"
- ✅ ACM certificate status is "ISSUED"
- ✅ S3 bucket policy allows CloudFront access
- ✅ Website content loads correctly

---

**Ready to fix? Run:**
```bash
cd /Users/markgentry/metabomaxpro1
chmod +x *.sh
./fix_bigoil_auto.sh
```
