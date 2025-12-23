#!/bin/bash
# Step 5: Verify website is working properly

set -e

DISTRIBUTION_ID="E1R1OOQP5GPCDX"

echo "=========================================="
echo "Verify bigoil.net Website"
echo "=========================================="
echo ""

# Check CloudFront deployment status
echo "Checking CloudFront deployment status..."
STATUS=$(aws cloudfront get-distribution \
    --id $DISTRIBUTION_ID \
    --query 'Distribution.Status' \
    --output text)

echo "Current Status: $STATUS"
echo ""

if [ "$STATUS" != "Deployed" ]; then
    echo "Distribution is still deploying..."
    echo "Waiting for deployment to complete (this may take 15-30 minutes)..."
    echo ""

    # Poll status every 30 seconds
    while [ "$STATUS" != "Deployed" ]; do
        echo "Status: $STATUS - Waiting 30 seconds..."
        sleep 30
        STATUS=$(aws cloudfront get-distribution \
            --id $DISTRIBUTION_ID \
            --query 'Distribution.Status' \
            --output text)
    done

    echo ""
    echo "✅ Deployment complete!"
fi

echo ""
echo "=========================================="
echo "Testing Website Access"
echo "=========================================="
echo ""

# Test HTTPS access
echo "Testing https://bigoil.net..."
RESPONSE_1=$(curl -sI https://bigoil.net)
STATUS_CODE_1=$(echo "$RESPONSE_1" | grep -i "^HTTP" | awk '{print $2}')

echo "Status Code: $STATUS_CODE_1"
echo "$RESPONSE_1" | head -10
echo ""

echo "Testing https://www.bigoil.net..."
RESPONSE_2=$(curl -sI https://www.bigoil.net)
STATUS_CODE_2=$(echo "$RESPONSE_2" | grep -i "^HTTP" | awk '{print $2}')

echo "Status Code: $STATUS_CODE_2"
echo "$RESPONSE_2" | head -10
echo ""

# Test HTTP redirect
echo "Testing HTTP to HTTPS redirect..."
REDIRECT_TEST=$(curl -sI http://bigoil.net)
REDIRECT_LOCATION=$(echo "$REDIRECT_TEST" | grep -i "^Location:" | awk '{print $2}')

echo "Redirect Location: $REDIRECT_LOCATION"
echo ""

echo "=========================================="
echo "Test Results Summary"
echo "=========================================="
echo ""

# Check results
ERRORS=0

if [ "$STATUS_CODE_1" = "200" ]; then
    echo "✅ https://bigoil.net returns 200 OK"
else
    echo "❌ https://bigoil.net returns $STATUS_CODE_1 (expected 200)"
    ERRORS=$((ERRORS + 1))
fi

if [ "$STATUS_CODE_2" = "200" ]; then
    echo "✅ https://www.bigoil.net returns 200 OK"
else
    echo "❌ https://www.bigoil.net returns $STATUS_CODE_2 (expected 200)"
    ERRORS=$((ERRORS + 1))
fi

if echo "$REDIRECT_LOCATION" | grep -q "https://"; then
    echo "✅ HTTP redirects to HTTPS"
else
    echo "⚠️  HTTP redirect may not be configured"
fi

# Check SSL certificate
echo ""
echo "Checking SSL certificate..."
CERT_INFO=$(echo | openssl s_client -servername bigoil.net -connect bigoil.net:443 2>/dev/null | openssl x509 -noout -subject -dates 2>/dev/null)

if [ -n "$CERT_INFO" ]; then
    echo "✅ SSL Certificate is valid"
    echo "$CERT_INFO"
else
    echo "❌ Could not verify SSL certificate"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "=========================================="

if [ $ERRORS -eq 0 ]; then
    echo "✅ All tests passed! Website is working correctly."
    echo ""
    echo "Your website is now live at:"
    echo "  🌐 https://bigoil.net"
    echo "  🌐 https://www.bigoil.net"
    echo ""
    echo "You can also check the distribution:"
    echo "  📊 CloudFront: https://console.aws.amazon.com/cloudfront/v3/home#/distributions/$DISTRIBUTION_ID"
else
    echo "❌ $ERRORS error(s) found. Please review the issues above."
    echo ""
    echo "Common troubleshooting steps:"
    echo "1. Wait a few more minutes for CloudFront cache to update"
    echo "2. Create a cache invalidation:"
    echo "   aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths '/*'"
    echo "3. Check S3 bucket has index.html:"
    echo "   aws s3 ls s3://\$BUCKET_NAME/index.html"
    echo "4. Verify DNS is pointing to CloudFront:"
    echo "   dig bigoil.net"
fi

echo ""
echo "=========================================="
