#!/bin/bash
# Step 4: Update CloudFront distribution with certificate and configuration

set -e

DISTRIBUTION_ID="E1R1OOQP5GPCDX"

echo "=========================================="
echo "Update CloudFront Distribution"
echo "=========================================="
echo ""

# Source environment variables
if [ -f /tmp/bigoil_cert_arn.sh ]; then
    source /tmp/bigoil_cert_arn.sh
    echo "Loaded certificate ARN: $BIGOIL_CERT_ARN"
    echo "Loaded OAC ID: $BIGOIL_OAC_ID"
else
    echo "ERROR: Certificate ARN not found. Run 2_create_certificate.sh first."
    exit 1
fi

# Verify certificate is issued
echo ""
echo "Verifying certificate status..."
CERT_STATUS=$(aws acm describe-certificate \
    --certificate-arn $BIGOIL_CERT_ARN \
    --region us-east-1 \
    --query 'Certificate.Status' \
    --output text)

echo "Certificate Status: $CERT_STATUS"

if [ "$CERT_STATUS" != "ISSUED" ]; then
    echo ""
    echo "ERROR: Certificate is not yet validated (Status: $CERT_STATUS)"
    echo "Please complete DNS validation first."
    echo ""
    echo "To check validation status:"
    echo "  aws acm describe-certificate --certificate-arn $BIGOIL_CERT_ARN --region us-east-1"
    exit 1
fi

echo "✅ Certificate is validated and ready"
echo ""

# Get current distribution config
echo "Fetching current CloudFront configuration..."
aws cloudfront get-distribution-config --id $DISTRIBUTION_ID > /tmp/dist_config.json
ETAG=$(cat /tmp/dist_config.json | jq -r '.ETag')

echo "Current ETag: $ETAG"
echo ""

# Extract distribution config
cat /tmp/dist_config.json | jq '.DistributionConfig' > /tmp/dist_config_only.json

# Get current origin domain to preserve it
ORIGIN_DOMAIN=$(cat /tmp/dist_config_only.json | jq -r '.Origins.Items[0].DomainName')
echo "Origin Domain: $ORIGIN_DOMAIN"
echo ""

# Update the configuration
echo "Updating CloudFront configuration..."

cat /tmp/dist_config_only.json | jq \
    --arg cert_arn "$BIGOIL_CERT_ARN" \
    --arg oac_id "$BIGOIL_OAC_ID" \
    '
    # Update SSL certificate
    .ViewerCertificate = {
        "ACMCertificateArn": $cert_arn,
        "SSLSupportMethod": "sni-only",
        "MinimumProtocolVersion": "TLSv1.2_2021",
        "Certificate": $cert_arn,
        "CertificateSource": "acm"
    } |

    # Add domain aliases
    .Aliases = {
        "Quantity": 2,
        "Items": ["bigoil.net", "www.bigoil.net"]
    } |

    # Set default root object
    .DefaultRootObject = "index.html" |

    # Configure Origin Access Control
    .Origins.Items[0].OriginAccessControlId = $oac_id |
    .Origins.Items[0].S3OriginConfig.OriginAccessIdentity = "" |

    # Ensure HTTPS redirect
    .DefaultCacheBehavior.ViewerProtocolPolicy = "redirect-to-https"
    ' > /tmp/dist_config_updated.json

echo "Configuration updated:"
cat /tmp/dist_config_updated.json | jq '{
    Aliases: .Aliases,
    DefaultRootObject: .DefaultRootObject,
    Certificate: .ViewerCertificate.ACMCertificateArn,
    OAC: .Origins.Items[0].OriginAccessControlId,
    ViewerProtocol: .DefaultCacheBehavior.ViewerProtocolPolicy
}'
echo ""

# Apply the update
echo "Applying CloudFront distribution update..."
echo "This will trigger a deployment that takes 15-30 minutes..."
echo ""

UPDATE_RESULT=$(aws cloudfront update-distribution \
    --id $DISTRIBUTION_ID \
    --distribution-config file:///tmp/dist_config_updated.json \
    --if-match $ETAG)

UPDATE_STATUS=$(echo $UPDATE_RESULT | jq -r '.Distribution.Status')
LAST_MODIFIED=$(echo $UPDATE_RESULT | jq -r '.Distribution.LastModifiedTime')

echo "✅ CloudFront distribution updated successfully!"
echo ""
echo "Distribution Status: $UPDATE_STATUS"
echo "Last Modified: $LAST_MODIFIED"
echo ""

echo "=========================================="
echo "Deployment in Progress"
echo "=========================================="
echo ""
echo "CloudFront is now deploying your changes."
echo "This typically takes 15-30 minutes."
echo ""
echo "To check deployment status, run:"
echo "  aws cloudfront get-distribution --id $DISTRIBUTION_ID --query 'Distribution.Status'"
echo ""
echo "Or run: 5_verify_website.sh (it will wait for deployment)"
echo ""
echo "Once status shows 'Deployed', your website will be live at:"
echo "  https://bigoil.net"
echo "  https://www.bigoil.net"
