#!/bin/bash
# Step 3: Fix S3 bucket policy to allow CloudFront access

set -e

DISTRIBUTION_ID="E1R1OOQP5GPCDX"

echo "=========================================="
echo "Fix S3 Bucket Access for CloudFront"
echo "=========================================="
echo ""

# Load saved diagnosis
if [ ! -f /tmp/bigoil_diagnosis.txt ]; then
    echo "Running diagnosis first..."
    ./1_diagnose_bigoil.sh
fi

source /tmp/bigoil_diagnosis.txt 2>/dev/null || true

# Get bucket name
echo "Getting S3 bucket name..."
aws cloudfront get-distribution --id $DISTRIBUTION_ID > /tmp/cloudfront_dist.json
ORIGIN_DOMAIN=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Origins.Items[0].DomainName')
BUCKET_NAME=$(echo $ORIGIN_DOMAIN | sed 's/.s3.*.amazonaws.com//' | sed 's/.s3-website.*.amazonaws.com//')

echo "S3 Bucket: $BUCKET_NAME"
echo ""

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
echo "AWS Account ID: $ACCOUNT_ID"
echo ""

# Check if OAC exists
OAC_ID=$(cat /tmp/cloudfront_dist.json | jq -r '.Distribution.DistributionConfig.Origins.Items[0].OriginAccessControlId // empty')

if [ -z "$OAC_ID" ]; then
    echo "No Origin Access Control found. Creating one..."

    OAC_ID=$(aws cloudfront create-origin-access-control \
        --origin-access-control-config \
        'Name=bigoil-net-oac,Description=Origin Access Control for bigoil.net,SigningProtocol=sigv4,SigningBehavior=always,OriginAccessControlOriginType=s3' \
        --query 'OriginAccessControl.Id' \
        --output text)

    echo "Created OAC: $OAC_ID"
    echo "export BIGOIL_OAC_ID=$OAC_ID" >> /tmp/bigoil_cert_arn.sh
else
    echo "Found existing OAC: $OAC_ID"
    echo "export BIGOIL_OAC_ID=$OAC_ID" >> /tmp/bigoil_cert_arn.sh
fi

echo ""
echo "Creating S3 bucket policy..."

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

echo "Bucket policy:"
cat /tmp/bucket_policy.json | jq .
echo ""

# Apply bucket policy
echo "Applying bucket policy to $BUCKET_NAME..."
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file:///tmp/bucket_policy.json

echo "✅ Bucket policy applied successfully!"
echo ""

# Check if bucket has index.html
echo "Checking for index.html in bucket..."
if aws s3 ls s3://$BUCKET_NAME/index.html 2>/dev/null; then
    echo "✅ index.html found in bucket"
else
    echo "⚠️  WARNING: index.html not found in bucket"
    echo "   You may need to upload your website files:"
    echo "   aws s3 cp /path/to/index.html s3://$BUCKET_NAME/index.html"
    echo "   aws s3 sync /path/to/website/ s3://$BUCKET_NAME/"
fi

echo ""
echo "✅ S3 bucket access configured successfully!"
echo ""
echo "Next step: Run 4_update_cloudfront.sh to update CloudFront distribution"
