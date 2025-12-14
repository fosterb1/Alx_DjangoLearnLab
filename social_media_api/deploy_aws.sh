#!/bin/bash

# Social Media API - AWS Deployment Script
# This script automates the deployment to AWS Elastic Beanstalk

set -e  # Exit on error

echo "=================================="
echo "Social Media API - AWS Deployment"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo -e "${RED}EB CLI is not installed. Installing...${NC}"
    pip install awsebcli
fi

echo -e "${GREEN}✓ Prerequisites checked${NC}"
echo ""

# Prompt for configuration
read -p "Enter your AWS region (default: us-east-1): " AWS_REGION
AWS_REGION=${AWS_REGION:-us-east-1}

read -p "Enter application name (default: social-media-api): " APP_NAME
APP_NAME=${APP_NAME:-social-media-api}

read -p "Enter environment name (default: social-media-prod): " ENV_NAME
ENV_NAME=${ENV_NAME:-social-media-prod}

echo ""
echo -e "${YELLOW}Deployment Configuration:${NC}"
echo "  Region: $AWS_REGION"
echo "  Application: $APP_NAME"
echo "  Environment: $ENV_NAME"
echo ""

read -p "Continue with deployment? (y/n): " CONTINUE
if [ "$CONTINUE" != "y" ]; then
    echo "Deployment cancelled."
    exit 0
fi

# Step 1: Initialize EB application (if not already done)
echo ""
echo -e "${YELLOW}Step 1: Initializing EB application...${NC}"
if [ ! -d ".elasticbeanstalk" ]; then
    eb init $APP_NAME --platform python-3.11 --region $AWS_REGION
    echo -e "${GREEN}✓ EB application initialized${NC}"
else
    echo -e "${GREEN}✓ EB application already initialized${NC}"
fi

# Step 2: Create environment (if not exists)
echo ""
echo -e "${YELLOW}Step 2: Creating EB environment...${NC}"
if ! eb list | grep -q $ENV_NAME; then
    eb create $ENV_NAME --instance-type t3.small
    echo -e "${GREEN}✓ Environment created${NC}"
else
    echo -e "${GREEN}✓ Environment already exists${NC}"
fi

# Step 3: Set environment variables
echo ""
echo -e "${YELLOW}Step 3: Setting environment variables...${NC}"
read -p "Enter SECRET_KEY (or press Enter to generate): " SECRET_KEY
if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    echo "Generated SECRET_KEY: $SECRET_KEY"
fi

read -p "Enter RDS database endpoint: " DB_HOST
read -p "Enter database name (default: social_media_db): " DB_NAME
DB_NAME=${DB_NAME:-social_media_db}
read -p "Enter database user (default: dbadmin): " DB_USER
DB_USER=${DB_USER:-dbadmin}
read -sp "Enter database password: " DB_PASSWORD
echo ""

# Set environment variables
eb setenv \
    DEBUG=False \
    SECRET_KEY="$SECRET_KEY" \
    ALLOWED_HOSTS="$ENV_NAME.elasticbeanstalk.com" \
    DB_NAME=$DB_NAME \
    DB_USER=$DB_USER \
    DB_PASSWORD="$DB_PASSWORD" \
    DB_HOST=$DB_HOST \
    DB_PORT=5432

echo -e "${GREEN}✓ Environment variables set${NC}"

# Step 4: Deploy application
echo ""
echo -e "${YELLOW}Step 4: Deploying application...${NC}"
eb deploy

echo -e "${GREEN}✓ Application deployed${NC}"

# Step 5: Check status
echo ""
echo -e "${YELLOW}Step 5: Checking deployment status...${NC}"
eb status

# Final message
echo ""
echo -e "${GREEN}=================================="
echo "Deployment Complete! 🚀"
echo "==================================${NC}"
echo ""
echo "Your application is now running at:"
eb status | grep "CNAME"
echo ""
echo "Next steps:"
echo "1. Run migrations: eb ssh, then run 'python manage.py migrate'"
echo "2. Create superuser: python manage.py createsuperuser"
echo "3. Configure SSL certificate"
echo "4. Set up custom domain"
echo ""
echo "For detailed instructions, see AWS_DEPLOYMENT_GUIDE.md"
