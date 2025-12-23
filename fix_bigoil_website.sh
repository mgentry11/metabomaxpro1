#!/bin/bash

# Script to fix bigoil.net website issues:
# 1. SSL certificate (ACM in us-east-1)
# 2. CloudFront 403 error (S3 bucket policy, OAC/OAI)
# 3. CloudFront distribution configuration

set -e

DISTRIBUTION_ID="E1R1OOQP5GPCDX"
DOMAIN="bigoil.net"
WWW_DOMAIN="www.bigoil.net"
REGION="us-east-1"  # Required for CloudFront certificates

echo "=========================================="
echo "bigoil.net Website Fix Script"
echo "=========================================="
echo ""

# Step 1: Get current CloudFront distribution configuration
echo "Step 1: Examining CloudFront distribution..."
aws cloudfront get-distribution --id $DISTRIBUTION_ID > /tmp/cloudfront_dist.json
echo "Distribution details saved to /tmp/cloudfront_dist.json"

# Extract key information
CLOUDFRONT_DOMAIN=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DomainName')
CURRENT_ALIASES=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Aliases.Items[]' 2>/dev/null || echo "None")
VIEWER_CERT=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.ViewerCertificate')
ORIGIN_DOMAIN=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Origins.Items[0].DomainName')
ORIGIN_ID=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Origins.Items[0].Id')
DEFAULT_ROOT=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.DefaultRootObject')
ETAG=$(cat /tmp/cloudfront_dist.json | jq -r '.ETag')

echo "CloudFront Domain: $CLOUDFRONT_DOMAIN"
echo "Current Aliases: $CURRENT_ALIASES"
echo "Origin Domain: $ORIGIN_DOMAIN"
echo "Default Root Object: $DEFAULT_ROOT"
echo ""

# Step 2: Find S3 bucket name from origin
BUCKET_NAME=$(echo $ORIGIN_DOMAIN | sed 's/.s3.*.amazonaws.com//')
echo "Step 2: Identified S3 bucket: $BUCKET_NAME"
echo ""

# Step 3: Check S3 bucket configuration
echo "Step 3: Checking S3 bucket configuration..."
echo "Bucket Policy:"
aws s3api get-bucket-policy --bucket $BUCKET_NAME 2>/dev/null | jq -r '.Policy' | jq . || echo "No bucket policy found"
echo ""

echo "Bucket Website Configuration:"
aws s3api get-bucket-website --bucket $BUCKET_NAME 2>/dev/null || echo "No website configuration found"
echo ""

echo "Public Access Block:"
aws s3api get-public-access-block --bucket $BUCKET_NAME 2>/dev/null || echo "No public access block configured"
echo ""

# Step 4: Check for existing ACM certificates
echo "Step 4: Checking for existing ACM certificates in us-east-1..."
EXISTING_CERT=$(aws acm list-certificates --region $REGION --query "CertificateSummaryList[?DomainName=='$DOMAIN'].CertificateArn" --output text)

if [ -z "$EXISTING_CERT" ]; then
    echo "No existing certificate found for $DOMAIN"
    echo ""
    echo "Step 5: Creating new ACM certificate..."

    # Request certificate
    CERT_ARN=$(aws acm request-certificate \
        --domain-name $DOMAIN \
        --subject-alternative-names $WWW_DOMAIN \
        --validation-method DNS \
        --region $REGION \
        --query 'CertificateArn' \
        --output text)

    echo "Certificate requested: $CERT_ARN"
    echo ""

    # Get DNS validation records
    echo "Step 6: Retrieving DNS validation records..."
    sleep 5  # Wait for AWS to process the request

    aws acm describe-certificate \
        --certificate-arn $CERT_ARN \
        --region $REGION \
        --query 'Certificate.DomainValidationOptions[*].[DomainName,ResourceRecord.Name,ResourceRecord.Type,ResourceRecord.Value]' \
        --output table

    echo ""
    echo "=========================================="
    echo "ACTION REQUIRED: Add DNS Records"
    echo "=========================================="
    echo "Please add the CNAME records shown above to your DNS provider"
    echo "for $DOMAIN to validate the certificate."
    echo ""
    echo "After adding the DNS records, run:"
    echo "aws acm describe-certificate --certificate-arn $CERT_ARN --region $REGION"
    echo "to check validation status."
    echo ""
    echo "Certificate ARN: $CERT_ARN"

else
    CERT_ARN=$EXISTING_CERT
    echo "Found existing certificate: $CERT_ARN"

    # Check certificate status
    CERT_STATUS=$(aws acm describe-certificate --certificate-arn $CERT_ARN --region $REGION --query 'Certificate.Status' --output text)
    echo "Certificate Status: $CERT_STATUS"
    echo ""

    if [ "$CERT_STATUS" != "ISSUED" ]; then
        echo "WARNING: Certificate is not in ISSUED status"
        echo "Certificate validation may still be pending."
        echo ""
        aws acm describe-certificate \
            --certificate-arn $CERT_ARN \
            --region $REGION \
            --query 'Certificate.DomainValidationOptions[*].[DomainName,ResourceRecord.Name,ResourceRecord.Type,ResourceRecord.Value,ValidationStatus]' \
            --output table
    fi
fi

echo ""
echo "=========================================="
echo "Step 7: Fixing S3 Bucket Configuration"
echo "=========================================="

# Check if bucket has OAC or OAI configured
echo "Checking CloudFront Origin Access Control..."
OAC_ID=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Origins.Items[0].OriginAccessControlId // empty')
OAI_ID=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Origins.Items[0].S3OriginConfig.OriginAccessIdentity // empty')

if [ -n "$OAC_ID" ]; then
    echo "Found Origin Access Control: $OAC_ID"
    OAC_PRINCIPAL="arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity $OAC_ID"
elif [ -n "$OAI_ID" ]; then
    echo "Found Origin Access Identity: $OAI_ID"
    # Extract OAI ID from the path
    OAI_CANONICAL=$(echo $OAI_ID | sed 's/origin-access-identity\/cloudfront\///')
    OAC_PRINCIPAL="arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity $OAI_CANONICAL"
else
    echo "WARNING: No OAC or OAI configured!"
    echo "Creating Origin Access Control..."

    OAC_NAME="bigoil-net-oac"
    OAC_RESULT=$(aws cloudfront create-origin-access-control \
        --origin-access-control-config \
        "Name=$OAC_NAME,Description=OAC for bigoil.net,SigningProtocol=sigv4,SigningBehavior=always,OriginAccessControlOriginType=s3" \
        --query 'OriginAccessControl.Id' \
        --output text)

    OAC_ID=$OAC_RESULT
    echo "Created OAC: $OAC_ID"
fi

# Create bucket policy for CloudFront access
echo ""
echo "Creating S3 bucket policy for CloudFront access..."

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)

# Create bucket policy
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
            "Resource": "arn:aws:s3:::$BUCKET_NAME/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::$ACCOUNT_ID:distribution/$DISTRIBUTION_ID"
                }
            }
        }
    ]
}
EOF

echo "Applying bucket policy..."
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file:///tmp/bucket_policy.json
echo "Bucket policy applied successfully"
echo ""

echo "=========================================="
echo "Step 8: Updating CloudFront Distribution"
echo "=========================================="

# Get current distribution config
aws cloudfront get-distribution-config --id $DISTRIBUTION_ID > /tmp/dist_config.json
CURRENT_ETAG=$(cat /tmp/dist_config.json | jq -r '.ETag')

# Update the distribution configuration
cat /tmp/dist_config.json | jq '.DistributionConfig' > /tmp/dist_config_only.json

# Update certificate if validated
if [ "$CERT_STATUS" = "ISSUED" ]; then
    echo "Updating distribution with SSL certificate..."

    cat /tmp/dist_config_only.json | jq \
        --arg cert_arn "$CERT_ARN" \
        '.ViewerCertificate.ACMCertificateArn = $cert_arn |
         .ViewerCertificate.SSLSupportMethod = "sni-only" |
         .ViewerCertificate.MinimumProtocolVersion = "TLSv1.2_2021" |
         .ViewerCertificate.Certificate = $cert_arn |
         .ViewerCertificate.CertificateSource = "acm" |
         del(.ViewerCertificate.CloudFrontDefaultCertificate)' > /tmp/dist_config_updated.json
else
    cp /tmp/dist_config_only.json /tmp/dist_config_updated.json
fi

# Update aliases if not set
cat /tmp/dist_config_updated.json | jq \
    '.Aliases.Quantity = 2 |
     .Aliases.Items = ["bigoil.net", "www.bigoil.net"]' > /tmp/dist_config_final.json

# Update default root object if not set
if [ "$DEFAULT_ROOT" = "null" ] || [ "$DEFAULT_ROOT" = "" ]; then
    echo "Setting default root object to index.html..."
    cat /tmp/dist_config_final.json | jq \
        '.DefaultRootObject = "index.html"' > /tmp/dist_config_with_root.json
    mv /tmp/dist_config_with_root.json /tmp/dist_config_final.json
fi

# Update OAC if needed
if [ -n "$OAC_ID" ]; then
    echo "Setting Origin Access Control..."
    cat /tmp/dist_config_final.json | jq \
        --arg oac_id "$OAC_ID" \
        '.Origins.Items[0].OriginAccessControlId = $oac_id |
         .Origins.Items[0].S3OriginConfig.OriginAccessIdentity = ""' > /tmp/dist_config_oac.json
    mv /tmp/dist_config_oac.json /tmp/dist_config_final.json
fi

echo "Applying CloudFront distribution updates..."
aws cloudfront update-distribution \
    --id $DISTRIBUTION_ID \
    --distribution-config file:///tmp/dist_config_final.json \
    --if-match $CURRENT_ETAG > /tmp/update_result.json

echo "CloudFront distribution updated successfully!"
echo ""

UPDATE_STATUS=$(cat /tmp/update_result.json | jq -r '.Distribution.Status')
echo "Distribution Status: $UPDATE_STATUS"
echo ""

echo "=========================================="
echo "Summary"
echo "=========================================="
echo "CloudFront Distribution ID: $DISTRIBUTION_ID"
echo "S3 Bucket: $BUCKET_NAME"
echo "Certificate ARN: $CERT_ARN"
echo "Certificate Status: $CERT_STATUS"
echo ""

if [ "$CERT_STATUS" = "ISSUED" ]; then
    echo "SUCCESS: Certificate is validated and attached to CloudFront"
    echo ""
    echo "CloudFront is now deploying the changes."
    echo "This typically takes 15-30 minutes."
    echo ""
    echo "After deployment completes, test with:"
    echo "  curl -I https://bigoil.net"
    echo "  curl -I https://www.bigoil.net"
else
    echo "PENDING: Certificate validation is still pending"
    echo "Complete the DNS validation, then re-run this script"
    echo ""
    echo "To check certificate status:"
    echo "  aws acm describe-certificate --certificate-arn $CERT_ARN --region $REGION"
fi

echo ""
echo "To check deployment status:"
echo "  aws cloudfront get-distribution --id $DISTRIBUTION_ID --query 'Distribution.Status'"
echo ""
echo "=========================================="
