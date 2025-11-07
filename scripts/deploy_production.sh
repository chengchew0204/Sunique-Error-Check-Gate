#!/bin/bash

# Production Deployment Script for InFlow Error Check Gate
# Deploys to AWS Lambda using Serverless Framework

set -e  # Exit on error

echo "=================================="
echo "InFlow Error Check Gate Deployment"
echo "=================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Installing..."
    echo "Please install AWS CLI from: https://aws.amazon.com/cli/"
    exit 1
fi
echo "✅ AWS CLI found"

# Check if Serverless Framework is installed
if ! command -v serverless &> /dev/null; then
    echo "❌ Serverless Framework not found."
    echo "Installing Serverless Framework..."
    npm install -g serverless
fi
echo "✅ Serverless Framework found"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your production credentials."
    exit 1
fi
echo "✅ .env file found"

# Check AWS credentials
echo ""
echo "Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured."
    echo "Please run: aws configure"
    exit 1
fi
AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
echo "✅ AWS Account: $AWS_ACCOUNT"

# Prompt for deployment stage
echo ""
read -p "Enter deployment stage (dev/staging/prod) [prod]: " STAGE
STAGE=${STAGE:-prod}

echo ""
echo "Deploying to AWS Lambda..."
echo "Stage: $STAGE"
echo "Region: us-east-1"
echo ""

# Install serverless plugin if not exists
echo "Installing Serverless plugins..."
cd "$(dirname "$0")/.."
if [ ! -d "node_modules" ]; then
    npm init -y
fi
npm install --save-dev serverless-python-requirements

# Deploy
echo ""
echo "🚀 Deploying..."
serverless deploy --stage $STAGE --config serverless/serverless.yml

echo ""
echo "=================================="
echo "✅ Deployment Complete!"
echo "=================================="
echo ""
echo "Next Steps:"
echo "1. Copy the webhook endpoint URL from above"
echo "2. Update InFlow webhook subscription:"
echo ""
echo "   python scripts/update_webhook.py <YOUR_PRODUCTION_URL>"
echo ""
echo "3. Test the endpoint:"
echo "   curl https://YOUR_ENDPOINT_URL/"
echo ""
echo "4. Monitor logs:"
echo "   serverless logs -f webhook --stage $STAGE --tail"
echo ""
echo "=================================="

