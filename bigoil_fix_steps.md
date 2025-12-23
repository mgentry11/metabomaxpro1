# bigoil.net Website Fix - Step by Step Guide

## Current Issues
1. **HTTPS SSL Error** - CloudFront distribution (E1R1OOQP5GPCDX) doesn't have a valid SSL certificate
2. **HTTP 403 Forbidden** - CloudFront can't access S3 origin

## Step-by-Step Fix Process

### Step 1: Examine Current Configuration

```bash
# Get CloudFront distribution details
aws cloudfront get-distribution --id E1R1OOQP5GPCDX > cloudfront_config.json

# View key details
cat cloudfront_config.json | jq '{
  DomainName: .Distribution.DomainName,
  Status: .Distribution.Status,
  Aliases: .Distribution.DistributionConfig.Aliases,
  Certificate: .Distribution.DistributionConfig.ViewerCertificate,
  Origin: .Distribution.DistributionConfig.Origins.Items[0],
  DefaultRoot: .Distribution.DistributionConfig.DefaultRootObject
}'
```

### Step 2: Identify S3 Bucket

```bash
# Extract S3 bucket name from origin
ORIGIN_DOMAIN=$(cat cloudfront_config.json | jq -r '.Distribution.DistributionConfig.Origins.Items[0].DomainName')
BUCKET_NAME=$(echo $ORIGIN_DOMAIN | sed 's/.s3.*.amazonaws.com//')
echo "S3 Bucket: $BUCKET_NAME"

# Check bucket policy
aws s3api get-bucket-policy --bucket $BUCKET_NAME
```

### Step 3: Check for Existing ACM Certificate

```bash
# List certificates in us-east-1 (required for CloudFront)
aws acm list-certificates --region us-east-1

# Check if bigoil.net certificate exists
aws acm list-certificates --region us-east-1 \
  --query "CertificateSummaryList[?DomainName=='bigoil.net']"
```

### Step 4: Create ACM Certificate (if doesn't exist)

```bash
# Request new certificate with DNS validation
CERT_ARN=$(aws acm request-certificate \
  --domain-name bigoil.net \
  --subject-alternative-names www.bigoil.net \
  --validation-method DNS \
  --region us-east-1 \
  --query 'CertificateArn' \
  --output text)

echo "Certificate ARN: $CERT_ARN"

# Get DNS validation records
sleep 5
aws acm describe-certificate \
  --certificate-arn $CERT_ARN \
  --region us-east-1 \
  --query 'Certificate.DomainValidationOptions[*].[DomainName,ResourceRecord.Name,ResourceRecord.Type,ResourceRecord.Value]' \
  --output table
```

**ACTION REQUIRED:** Add the CNAME records shown above to your DNS provider (wherever bigoil.net DNS is hosted)

### Step 5: Wait for Certificate Validation

```bash
# Check certificate status (repeat until ISSUED)
aws acm describe-certificate \
  --certificate-arn $CERT_ARN \
  --region us-east-1 \
  --query 'Certificate.{Status:Status,ValidationStatus:DomainValidationOptions[0].ValidationStatus}'
```

### Step 6: Create Origin Access Control (OAC)

```bash
# Check if OAC already exists
cat cloudfront_config.json | jq '.Distribution.DistributionConfig.Origins.Items[0].OriginAccessControlId'

# If empty, create new OAC
OAC_ID=$(aws cloudfront create-origin-access-control \
  --origin-access-control-config \
  'Name=bigoil-net-oac,Description=OAC for bigoil.net,SigningProtocol=sigv4,SigningBehavior=always,OriginAccessControlOriginType=s3' \
  --query 'OriginAccessControl.Id' \
  --output text)

echo "OAC ID: $OAC_ID"
```

### Step 7: Fix S3 Bucket Policy

```bash
# Get your AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)

# Create bucket policy allowing CloudFront access
cat > bucket_policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$BUCKET_NAME/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::$ACCOUNT_ID:distribution/E1R1OOQP5GPCDX"
                }
            }
        }
    ]
}
EOF

# Apply bucket policy
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://bucket_policy.json
```

### Step 8: Update CloudFront Distribution

```bash
# Get current distribution config
aws cloudfront get-distribution-config --id E1R1OOQP5GPCDX > dist_config.json
ETAG=$(cat dist_config.json | jq -r '.ETag')

# Extract just the DistributionConfig
cat dist_config.json | jq '.DistributionConfig' > dist_config_only.json

# Update the configuration with certificate, OAC, and aliases
cat dist_config_only.json | jq \
  --arg cert_arn "$CERT_ARN" \
  --arg oac_id "$OAC_ID" \
  '.ViewerCertificate = {
    "ACMCertificateArn": $cert_arn,
    "SSLSupportMethod": "sni-only",
    "MinimumProtocolVersion": "TLSv1.2_2021",
    "Certificate": $cert_arn,
    "CertificateSource": "acm"
  } |
  .Aliases = {
    "Quantity": 2,
    "Items": ["bigoil.net", "www.bigoil.net"]
  } |
  .DefaultRootObject = "index.html" |
  .Origins.Items[0].OriginAccessControlId = $oac_id |
  .Origins.Items[0].S3OriginConfig.OriginAccessIdentity = ""' > dist_config_updated.json

# Apply the updated configuration
aws cloudfront update-distribution \
  --id E1R1OOQP5GPCDX \
  --distribution-config file://dist_config_updated.json \
  --if-match $ETAG
```

### Step 9: Wait for CloudFront Deployment

```bash
# Check deployment status (repeat until "Deployed")
aws cloudfront get-distribution \
  --id E1R1OOQP5GPCDX \
  --query 'Distribution.{Status:Status,LastModified:LastModifiedTime}'
```

This typically takes 15-30 minutes.

### Step 10: Verify Website is Working

```bash
# Test HTTPS access
curl -I https://bigoil.net
curl -I https://www.bigoil.net

# Should return 200 OK

# Test in browser
open https://bigoil.net
```

## Quick Reference Commands

```bash
# Check certificate status
aws acm describe-certificate --certificate-arn $CERT_ARN --region us-east-1

# Check CloudFront deployment status
aws cloudfront get-distribution --id E1R1OOQP5GPCDX --query 'Distribution.Status'

# List S3 bucket contents
aws s3 ls s3://$BUCKET_NAME/

# Check if index.html exists
aws s3 ls s3://$BUCKET_NAME/index.html

# Invalidate CloudFront cache (if needed)
aws cloudfront create-invalidation --distribution-id E1R1OOQP5GPCDX --paths "/*"
```

## Common Issues and Solutions

### Issue: Certificate validation pending
- **Solution:** Ensure CNAME records are added to DNS exactly as shown in Step 4
- **Check:** Run `dig` or `nslookup` on the validation domain

### Issue: 403 error persists after fixing bucket policy
- **Solution:** Wait for CloudFront deployment to complete (15-30 min)
- **Alternative:** Create invalidation to clear cache

### Issue: Website shows CloudFront default certificate warning
- **Solution:** Ensure certificate is ISSUED before updating distribution
- **Check:** Certificate ARN must be in us-east-1 region

### Issue: No index.html found
- **Solution:** Upload website files to S3 bucket
```bash
aws s3 cp /path/to/index.html s3://$BUCKET_NAME/index.html
aws s3 sync /path/to/website/ s3://$BUCKET_NAME/ --delete
```

## Environment Variables Used

```bash
export DISTRIBUTION_ID="E1R1OOQP5GPCDX"
export BUCKET_NAME="bigoil.net"  # or whatever the actual bucket name is
export CERT_ARN="arn:aws:acm:us-east-1:ACCOUNT:certificate/CERT-ID"
export OAC_ID="OAC-ID-HERE"
export ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
```
