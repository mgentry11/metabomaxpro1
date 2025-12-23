#!/bin/bash
# Automated fix for bigoil.net website
# This script will diagnose and fix all issues automatically

set -e

DISTRIBUTION_ID="E1R1OOQP5GPCDX"
DOMAIN="bigoil.net"
WWW_DOMAIN="www.bigoil.net"
REGION="us-east-1"

echo "=========================================="
echo "bigoil.net Automated Fix Script"
echo "=========================================="
echo ""
echo "This script will:"
echo "1. Diagnose current configuration"
echo "2. Create/verify ACM certificate"
echo "3. Fix S3 bucket permissions"
echo "4. Update CloudFront distribution"
echo "5. Verify website is working"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."
echo ""

# ====================
# STEP 1: DIAGNOSE
# ====================
echo "=========================================="
echo "STEP 1: Diagnosing Current State"
echo "=========================================="
echo ""

aws cloudfront get-distribution --id $DISTRIBUTION_ID > /tmp/cloudfront_dist.json

ORIGIN_DOMAIN=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Origins.Items[0].DomainName')
BUCKET_NAME=$(echo $ORIGIN_DOMAIN | sed 's/.s3.*.amazonaws.com//' | sed 's/.s3-website.*.amazonaws.com//')
ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)

echo "CloudFront Distribution: $DISTRIBUTION_ID"
echo "S3 Bucket: $BUCKET_NAME"
echo "AWS Account: $ACCOUNT_ID"
echo ""

# ====================
# STEP 2: CERTIFICATE
# ====================
echo "=========================================="
echo "STEP 2: ACM Certificate Setup"
echo "=========================================="
echo ""

EXISTING_CERT=$(aws acm list-certificates --region $REGION \
    --query "CertificateSummaryList[?DomainName=='$DOMAIN'].CertificateArn" \
    --output text)

if [ -n "$EXISTING_CERT" ]; then
    echo "Found existing certificate: $EXISTING_CERT"
    CERT_ARN=$EXISTING_CERT

    CERT_STATUS=$(aws acm describe-certificate \
        --certificate-arn $CERT_ARN \
        --region $REGION \
        --query 'Certificate.Status' \
        --output text)

    echo "Certificate Status: $CERT_STATUS"

    if [ "$CERT_STATUS" != "ISSUED" ]; then
        echo ""
        echo "❌ Certificate validation is still pending!"
        echo ""
        aws acm describe-certificate \
            --certificate-arn $CERT_ARN \
            --region $REGION \
            --query 'Certificate.DomainValidationOptions[*].[DomainName,ResourceRecord.Name,ResourceRecord.Type,ResourceRecord.Value,ValidationStatus]' \
            --output table

        echo ""
        echo "Please add the DNS validation records shown above and wait for validation."
        echo "Then run this script again."
        exit 1
    fi

    echo "✅ Certificate is validated"
else
    echo "Creating new ACM certificate..."

    CERT_ARN=$(aws acm request-certificate \
        --domain-name $DOMAIN \
        --subject-alternative-names $WWW_DOMAIN \
        --validation-method DNS \
        --region $REGION \
        --query 'CertificateArn' \
        --output text)

    echo "Certificate ARN: $CERT_ARN"
    echo ""

    sleep 5

    echo ""
    echo "❌ DNS Validation Required!"
    echo ""
    aws acm describe-certificate \
        --certificate-arn $CERT_ARN \
        --region $REGION \
        --query 'Certificate.DomainValidationOptions[*].[DomainName,ResourceRecord.Name,ResourceRecord.Type,ResourceRecord.Value]' \
        --output table

    echo ""
    echo "Add the above CNAME records to your DNS, then run this script again."
    exit 1
fi

echo ""

# ====================
# STEP 3: OAC SETUP
# ====================
echo "=========================================="
echo "STEP 3: Origin Access Control Setup"
echo "=========================================="
echo ""

OAC_ID=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Origins.Items[0].OriginAccessControlId // empty')

if [ -z "$OAC_ID" ]; then
    echo "Creating Origin Access Control..."

    OAC_ID=$(aws cloudfront create-origin-access-control \
        --origin-access-control-config \
        'Name=bigoil-net-oac,Description=OAC for bigoil.net,SigningProtocol=sigv4,SigningBehavior=always,OriginAccessControlOriginType=s3' \
        --query 'OriginAccessControl.Id' \
        --output text)

    echo "Created OAC: $OAC_ID"
else
    echo "Using existing OAC: $OAC_ID"
fi

echo ""

# ====================
# STEP 4: S3 BUCKET POLICY
# ====================
echo "=========================================="
echo "STEP 4: Fixing S3 Bucket Policy"
echo "=========================================="
echo ""

cat > /tmp/bucket_policy.json <<EOF
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
            "Resource": "arn:aws:s3:::${BUCKET_NAME}/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::${ACCOUNT_ID}:distribution/${DISTRIBUTION_ID}"
                }
            }
        }
    ]
}
EOF

echo "Applying bucket policy to $BUCKET_NAME..."
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file:///tmp/bucket_policy.json

echo "✅ Bucket policy updated"
echo ""

# Check for index.html
if aws s3 ls s3://$BUCKET_NAME/index.html >/dev/null 2>&1; then
    echo "✅ index.html found in bucket"
else
    echo "⚠️  WARNING: index.html not found in bucket"
    echo "   Upload your website files before testing"
fi

echo ""

# ====================
# STEP 5: UPDATE CLOUDFRONT
# ====================
echo "=========================================="
echo "STEP 5: Updating CloudFront Distribution"
echo "=========================================="
echo ""

aws cloudfront get-distribution-config --id $DISTRIBUTION_ID > /tmp/dist_config.json
ETAG=$(cat /tmp/dist_config.json | jq -r '.ETag')

cat /tmp/dist_config.json | jq '.DistributionConfig' | jq \
    --arg cert_arn "$CERT_ARN" \
    --arg oac_id "$OAC_ID" \
    '
    .ViewerCertificate = {
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
    .Origins.Items[0].S3OriginConfig.OriginAccessIdentity = "" |
    .DefaultCacheBehavior.ViewerProtocolPolicy = "redirect-to-https"
    ' > /tmp/dist_config_updated.json

echo "Applying CloudFront updates..."
aws cloudfront update-distribution \
    --id $DISTRIBUTION_ID \
    --distribution-config file:///tmp/dist_config_updated.json \
    --if-match $ETAG > /tmp/update_result.json

echo "✅ CloudFront distribution updated"
echo ""

UPDATE_STATUS=$(cat /tmp/update_result.json | jq -r '.Distribution.Status')
echo "Deployment Status: $UPDATE_STATUS"
echo ""

# ====================
# STEP 6: WAIT FOR DEPLOYMENT
# ====================
echo "=========================================="
echo "STEP 6: Waiting for Deployment"
echo "=========================================="
echo ""

echo "CloudFront is deploying changes (typically 15-30 minutes)..."
echo ""

STATUS="InProgress"
COUNTER=0

while [ "$STATUS" != "Deployed" ]; do
    sleep 30
    COUNTER=$((COUNTER + 1))
    STATUS=$(aws cloudfront get-distribution --id $DISTRIBUTION_ID --query 'Distribution.Status' --output text)
    echo "[$COUNTER] Status: $STATUS (checked at $(date '+%H:%M:%S'))"
done

echo ""
echo "✅ Deployment complete!"
echo ""

# ====================
# STEP 7: VERIFY
# ====================
echo "=========================================="
echo "STEP 7: Verifying Website"
echo "=========================================="
echo ""

sleep 10  # Give it a moment

echo "Testing https://bigoil.net..."
RESPONSE=$(curl -sI https://bigoil.net 2>&1 || echo "FAILED")
STATUS_CODE=$(echo "$RESPONSE" | grep -i "^HTTP" | awk '{print $2}' | head -1)

if [ "$STATUS_CODE" = "200" ]; then
    echo "✅ https://bigoil.net returns 200 OK"
else
    echo "Status: $STATUS_CODE"
    echo "$RESPONSE" | head -20
fi

echo ""
echo "Testing https://www.bigoil.net..."
RESPONSE=$(curl -sI https://www.bigoil.net 2>&1 || echo "FAILED")
STATUS_CODE=$(echo "$RESPONSE" | grep -i "^HTTP" | awk '{print $2}' | head -1)

if [ "$STATUS_CODE" = "200" ]; then
    echo "✅ https://www.bigoil.net returns 200 OK"
else
    echo "Status: $STATUS_CODE"
    echo "$RESPONSE" | head -20
fi

echo ""
echo "=========================================="
echo "✅ FIX COMPLETE!"
echo "=========================================="
echo ""
echo "Your website should now be live at:"
echo "  🌐 https://bigoil.net"
echo "  🌐 https://www.bigoil.net"
echo ""
echo "Summary of changes:"
echo "  - ACM Certificate: $CERT_ARN"
echo "  - Origin Access Control: $OAC_ID"
echo "  - S3 Bucket Policy: Updated for CloudFront access"
echo "  - CloudFront Distribution: Updated with SSL and proper configuration"
echo ""
echo "If you see any errors, you may need to:"
echo "1. Wait a few more minutes for DNS propagation"
echo "2. Create a cache invalidation:"
echo "   aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths '/*'"
echo ""
