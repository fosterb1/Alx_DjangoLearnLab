# Social Media API - AWS Deployment Script (PowerShell)
# This script automates the deployment to AWS Elastic Beanstalk

$ErrorActionPreference = "Stop"

Write-Host "==================================" -ForegroundColor Green
Write-Host "Social Media API - AWS Deployment" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""

# Check if AWS CLI is installed
try {
    aws --version | Out-Null
    Write-Host "✓ AWS CLI found" -ForegroundColor Green
} catch {
    Write-Host "✗ AWS CLI is not installed. Please install it first." -ForegroundColor Red
    Write-Host "Download from: https://awscli.amazonaws.com/AWSCLIV2.msi" -ForegroundColor Yellow
    exit 1
}

# Check if EB CLI is installed
try {
    eb --version | Out-Null
    Write-Host "✓ EB CLI found" -ForegroundColor Green
} catch {
    Write-Host "✗ EB CLI not found. Installing..." -ForegroundColor Yellow
    pip install awsebcli
}

Write-Host ""

# Prompt for configuration
$AWS_REGION = Read-Host "Enter your AWS region (default: us-east-1)"
if ([string]::IsNullOrWhiteSpace($AWS_REGION)) { $AWS_REGION = "us-east-1" }

$APP_NAME = Read-Host "Enter application name (default: social-media-api)"
if ([string]::IsNullOrWhiteSpace($APP_NAME)) { $APP_NAME = "social-media-api" }

$ENV_NAME = Read-Host "Enter environment name (default: social-media-prod)"
if ([string]::IsNullOrWhiteSpace($ENV_NAME)) { $ENV_NAME = "social-media-prod" }

Write-Host ""
Write-Host "Deployment Configuration:" -ForegroundColor Yellow
Write-Host "  Region: $AWS_REGION"
Write-Host "  Application: $APP_NAME"
Write-Host "  Environment: $ENV_NAME"
Write-Host ""

$CONTINUE = Read-Host "Continue with deployment? (y/n)"
if ($CONTINUE -ne "y") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

# Step 1: Initialize EB application
Write-Host ""
Write-Host "Step 1: Initializing EB application..." -ForegroundColor Yellow
if (-not (Test-Path ".elasticbeanstalk")) {
    eb init $APP_NAME --platform python-3.11 --region $AWS_REGION
    Write-Host "✓ EB application initialized" -ForegroundColor Green
} else {
    Write-Host "✓ EB application already initialized" -ForegroundColor Green
}

# Step 2: Create environment
Write-Host ""
Write-Host "Step 2: Creating EB environment..." -ForegroundColor Yellow
$envList = eb list 2>&1 | Out-String
if ($envList -notmatch $ENV_NAME) {
    eb create $ENV_NAME --instance-type t3.small
    Write-Host "✓ Environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Environment already exists" -ForegroundColor Green
}

# Step 3: Set environment variables
Write-Host ""
Write-Host "Step 3: Setting environment variables..." -ForegroundColor Yellow

$SECRET_KEY = Read-Host "Enter SECRET_KEY (or press Enter to generate)"
if ([string]::IsNullOrWhiteSpace($SECRET_KEY)) {
    $SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    Write-Host "Generated SECRET_KEY: $SECRET_KEY" -ForegroundColor Cyan
}

$DB_HOST = Read-Host "Enter RDS database endpoint"

$DB_NAME = Read-Host "Enter database name (default: social_media_db)"
if ([string]::IsNullOrWhiteSpace($DB_NAME)) { $DB_NAME = "social_media_db" }

$DB_USER = Read-Host "Enter database user (default: dbadmin)"
if ([string]::IsNullOrWhiteSpace($DB_USER)) { $DB_USER = "dbadmin" }

$DB_PASSWORD = Read-Host "Enter database password" -AsSecureString
$DB_PASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($DB_PASSWORD))

# Set environment variables
Write-Host "Setting environment variables..." -ForegroundColor Cyan
eb setenv DEBUG=False
eb setenv SECRET_KEY="$SECRET_KEY"
eb setenv ALLOWED_HOSTS="$ENV_NAME.elasticbeanstalk.com"
eb setenv DB_NAME=$DB_NAME
eb setenv DB_USER=$DB_USER
eb setenv DB_PASSWORD="$DB_PASSWORD"
eb setenv DB_HOST=$DB_HOST
eb setenv DB_PORT=5432

Write-Host "✓ Environment variables set" -ForegroundColor Green

# Step 4: Deploy application
Write-Host ""
Write-Host "Step 4: Deploying application..." -ForegroundColor Yellow
eb deploy

Write-Host "✓ Application deployed" -ForegroundColor Green

# Step 5: Check status
Write-Host ""
Write-Host "Step 5: Checking deployment status..." -ForegroundColor Yellow
eb status

# Final message
Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "Deployment Complete! 🚀" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your application is now running at:"
eb status | Select-String "CNAME"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Run migrations: eb ssh, then run 'python manage.py migrate'"
Write-Host "2. Create superuser: python manage.py createsuperuser"
Write-Host "3. Configure SSL certificate"
Write-Host "4. Set up custom domain"
Write-Host ""
Write-Host "For detailed instructions, see AWS_DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan
