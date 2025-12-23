#!/bin/bash
# Step 2: Create or verify ACM certificate for bigoil.net

set -e

DOMAIN="bigoil.net"
WWW_DOMAIN="www.bigoil.net"
REGION="us-east-1"

echo "=========================================="
echo "ACM Certificate Setup for bigoil.net"
echo "=========================================="
echo ""

# Check for existing certificate
echo "Checking for existing certificate..."
EXISTING_CERT=$(aws acm list-certificates --region $REGION \
  --query "CertificateSummaryList[?DomainName=='$DOMAIN'].CertificateArn" \
  --output text)

if [ -n "$EXISTING_CERT" ]; then
    echo "Found existing certificate: $EXISTING_CERT"
    CERT_ARN=$EXISTING_CERT

    # Check status
    CERT_INFO=$(aws acm describe-certificate --certificate-arn $CERT_ARN --region $REGION)
    CERT_STATUS=$(echo $CERT_INFO | jq -r '.Certificate.Status')

    echo "Certificate Status: $CERT_STATUS"
    echo ""

    if [ "$CERT_STATUS" = "ISSUED" ]; then
        echo "✅ Certificate is already validated and ready to use!"
        echo ""
        echo "Certificate ARN: $CERT_ARN"
        echo ""
        echo "Next step: Run 3_fix_s3_access.sh to fix S3 bucket permissions"
        exit 0
    else
        echo "Certificate validation is pending..."
        echo ""
        echo "DNS Validation Records:"
        echo $CERT_INFO | jq -r '.Certificate.DomainValidationOptions[] |
          "Domain: " + .DomainName + "\n" +
          "  Name: " + .ResourceRecord.Name + "\n" +
          "  Type: " + .ResourceRecord.Type + "\n" +
          "  Value: " + .ResourceRecord.Value + "\n" +
          "  Status: " + .ValidationStatus'

        echo ""
        echo "Please add the above CNAME records to your DNS provider."
        echo ""
        echo "To check validation status, run:"
        echo "  aws acm describe-certificate --certificate-arn $CERT_ARN --region $REGION"
        exit 0
    fi
else
    echo "No existing certificate found. Creating new certificate..."
    echo ""

    # Request new certificate
    CERT_ARN=$(aws acm request-certificate \
        --domain-name $DOMAIN \
        --subject-alternative-names $WWW_DOMAIN \
        --validation-method DNS \
        --region $REGION \
        --query 'CertificateArn' \
        --output text)

    echo "Certificate requested successfully!"
    echo "Certificate ARN: $CERT_ARN"
    echo ""

    # Wait a moment for AWS to process
    echo "Retrieving DNS validation records..."
    sleep 5

    # Get validation records
    CERT_INFO=$(aws acm describe-certificate --certificate-arn $CERT_ARN --region $REGION)

    echo ""
    echo "=========================================="
    echo "ACTION REQUIRED: Add DNS Records"
    echo "=========================================="
    echo ""

    echo $CERT_INFO | jq -r '.Certificate.DomainValidationOptions[] |
      "Domain: " + .DomainName + "\n" +
      "  Record Name: " + .ResourceRecord.Name + "\n" +
      "  Record Type: " + .ResourceRecord.Type + "\n" +
      "  Record Value: " + .ResourceRecord.Value + "\n"'

    echo ""
    echo "Add these CNAME records to your DNS provider for bigoil.net"
    echo ""
    echo "After adding DNS records, validation typically takes 5-30 minutes."
    echo ""
    echo "To check validation status, run:"
    echo "  aws acm describe-certificate --certificate-arn $CERT_ARN --region $REGION"
    echo ""
    echo "Or wait and run this script again."
    echo ""

    # Save cert ARN for later use
    echo "export BIGOIL_CERT_ARN=$CERT_ARN" > /tmp/bigoil_cert_arn.sh
    echo "Certificate ARN saved to /tmp/bigoil_cert_arn.sh"
fi

echo ""
echo "Once certificate is ISSUED, run: 3_fix_s3_access.sh"
