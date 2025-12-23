#!/bin/bash
# Step 1: Diagnose current state of bigoil.net infrastructure

set -e

DISTRIBUTION_ID="E1R1OOQP5GPCDX"

echo "=========================================="
echo "bigoil.net Infrastructure Diagnosis"
echo "=========================================="
echo ""

# Get CloudFront distribution
echo "Fetching CloudFront distribution configuration..."
aws cloudfront get-distribution --id $DISTRIBUTION_ID > /tmp/cloudfront_dist.json

# Extract key information
CLOUDFRONT_DOMAIN=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DomainName')
DISTRIBUTION_STATUS=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.Status')
ALIASES=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Aliases.Items[]' 2>/dev/null || echo "None")
ORIGIN_DOMAIN=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Origins.Items[0].DomainName')
DEFAULT_ROOT=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.DefaultRootObject')
OAC_ID=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Origins.Items[0].OriginAccessControlId // "None"')
OAI_PATH=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Origins.Items[0].S3OriginConfig.OriginAccessIdentity // "None"')

# Certificate info
CERT_ARN=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.ViewerCertificate.ACMCertificateArn // "None"')
CERT_SOURCE=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.ViewerCertificate.CertificateSource // "None"')

echo "CloudFront Distribution:"
echo "  ID: $DISTRIBUTION_ID"
echo "  Domain: $CLOUDFRONT_DOMAIN"
echo "  Status: $DISTRIBUTION_STATUS"
echo "  Aliases: $ALIASES"
echo ""

echo "SSL Certificate:"
echo "  ARN: $CERT_ARN"
echo "  Source: $CERT_SOURCE"
echo ""

echo "Origin Configuration:"
echo "  Domain: $ORIGIN_DOMAIN"
echo "  Default Root Object: $DEFAULT_ROOT"
echo "  Origin Access Control: $OAC_ID"
echo "  Origin Access Identity: $OAI_PATH"
echo ""

# Extract bucket name
BUCKET_NAME=$(echo $ORIGIN_DOMAIN | sed 's/.s3.*.amazonaws.com//')
echo "S3 Bucket: $BUCKET_NAME"
echo ""

# Check bucket
echo "Checking S3 bucket..."
echo "Bucket exists:"
aws s3 ls s3://$BUCKET_NAME/ | head -5

echo ""
echo "Bucket policy:"
aws s3api get-bucket-policy --bucket $BUCKET_NAME 2>&1 || echo "No bucket policy"

echo ""
echo "Bucket website configuration:"
aws s3api get-bucket-website --bucket $BUCKET_NAME 2>&1 || echo "No website configuration"

echo ""
echo "Check for index.html:"
aws s3 ls s3://$BUCKET_NAME/index.html 2>&1 || echo "index.html not found"

echo ""
echo "=========================================="
echo "ACM Certificates (us-east-1):"
echo "=========================================="
aws acm list-certificates --region us-east-1 --query 'CertificateSummaryList[*].[DomainName,CertificateArn,Status]' --output table

echo ""
echo "=========================================="
echo "Issues Found:"
echo "=========================================="

# Check issues
ISSUES=0

if [ "$CERT_ARN" = "None" ] || [ "$CERT_SOURCE" != "acm" ]; then
    echo "❌ No ACM certificate attached to CloudFront distribution"
    ISSUES=$((ISSUES + 1))
fi

if [ "$DEFAULT_ROOT" = "null" ] || [ -z "$DEFAULT_ROOT" ]; then
    echo "❌ No default root object set (should be index.html)"
    ISSUES=$((ISSUES + 1))
fi

if [ "$OAC_ID" = "None" ] && [ "$OAI_PATH" = "None" ]; then
    echo "❌ No Origin Access Control or Origin Access Identity configured"
    ISSUES=$((ISSUES + 1))
fi

if [ "$ALIASES" = "None" ]; then
    echo "❌ No aliases configured (should include bigoil.net and www.bigoil.net)"
    ISSUES=$((ISSUES + 1))
fi

# Check if bucket policy allows CloudFront
POLICY_CHECK=$(aws s3api get-bucket-policy --bucket $BUCKET_NAME 2>&1 | grep -c "cloudfront" || echo "0")
if [ "$POLICY_CHECK" = "0" ]; then
    echo "❌ Bucket policy doesn't grant CloudFront access"
    ISSUES=$((ISSUES + 1))
fi

echo ""
echo "Total issues found: $ISSUES"
echo ""

# Save diagnosis results
cat > /tmp/bigoil_diagnosis.txt <<EOF
CloudFront ID: $DISTRIBUTION_ID
CloudFront Domain: $CLOUDFRONT_DOMAIN
S3 Bucket: $BUCKET_NAME
Certificate ARN: $CERT_ARN
OAC ID: $OAC_ID
OAI Path: $OAI_PATH
Default Root: $DEFAULT_ROOT
Aliases: $ALIASES
Issues Found: $ISSUES
EOF

echo "Diagnosis complete. Results saved to /tmp/bigoil_diagnosis.txt"
echo ""
echo "Next step: Run 2_create_certificate.sh to create/verify ACM certificate"
