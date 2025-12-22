#!/bin/bash
# MetaboMax Pro AWS Deployment Script
# Usage: ./deploy.sh

set -e

echo "=========================================="
echo "MetaboMax Pro AWS Deployment"
echo "=========================================="

# Configuration
AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO="metabomax-app-production"
ECS_CLUSTER="metabomax-cluster-production"
ECS_SERVICE="metabomax-app-production"
IMAGE_TAG=$(git rev-parse --short HEAD 2>/dev/null || echo "latest")

echo "AWS Account: $AWS_ACCOUNT_ID"
echo "Region: $AWS_REGION"
echo "Image Tag: $IMAGE_TAG"

# Step 1: Login to ECR
echo ""
echo "Step 1: Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Step 2: Build Docker image
echo ""
echo "Step 2: Building Docker image..."
docker build -t $ECR_REPO:$IMAGE_TAG .
docker tag $ECR_REPO:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
docker tag $ECR_REPO:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest

# Step 3: Push to ECR
echo ""
echo "Step 3: Pushing to ECR..."
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest

# Step 4: Update ECS Service
echo ""
echo "Step 4: Updating ECS Service..."
aws ecs update-service \
    --cluster $ECS_CLUSTER \
    --service $ECS_SERVICE \
    --force-new-deployment \
    --region $AWS_REGION

# Step 5: Wait for deployment
echo ""
echo "Step 5: Waiting for deployment to stabilize..."
aws ecs wait services-stable \
    --cluster $ECS_CLUSTER \
    --services $ECS_SERVICE \
    --region $AWS_REGION

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "To check status:"
echo "  aws ecs describe-services --cluster $ECS_CLUSTER --services $ECS_SERVICE --region $AWS_REGION"
echo ""
echo "To view logs:"
echo "  aws logs tail /aws/ecs/metabomax-app-production --follow --region $AWS_REGION"
