# Social Media API - AWS Elastic Beanstalk Deployment Guide

## Complete Step-by-Step Guide for AWS Deployment

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [AWS Setup](#aws-setup)
3. [Database Setup (RDS PostgreSQL)](#database-setup)
4. [S3 Bucket Setup (Optional)](#s3-bucket-setup)
5. [Application Configuration](#application-configuration)
6. [Elastic Beanstalk Deployment](#elastic-beanstalk-deployment)
7. [Environment Variables](#environment-variables)
8. [SSL Configuration](#ssl-configuration)
9. [Monitoring and Logs](#monitoring-and-logs)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1. Install AWS CLI

**Windows:**
```powershell
# Download and install from:
# https://awscli.amazonaws.com/AWSCLIV2.msi
```

**macOS:**
```bash
brew install awscli
```

**Linux:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**Verify Installation:**
```bash
aws --version
```

### 2. Install EB CLI

```bash
pip install awsebcli
```

**Verify Installation:**
```bash
eb --version
```

### 3. AWS Account
- Active AWS account
- IAM user with appropriate permissions
- Access key ID and Secret access key

---

## AWS Setup

### 1. Configure AWS Credentials

```bash
aws configure
```

Enter:
- AWS Access Key ID: `[Your Access Key]`
- AWS Secret Access Key: `[Your Secret Key]`
- Default region name: `us-east-1` (or your preferred region)
- Default output format: `json`

### 2. Verify Configuration

```bash
aws sts get-caller-identity
```

Should show your AWS account details.

---

## Database Setup (RDS PostgreSQL)

### Option A: Using AWS Console

1. **Go to AWS RDS Console**
   - Navigate to https://console.aws.amazon.com/rds/

2. **Create Database**
   - Click "Create database"
   - Choose "Standard create"
   - Engine: PostgreSQL (version 15 or later)
   - Templates: Free tier (for testing) or Production

3. **Settings**
   - DB instance identifier: `social-media-db`
   - Master username: `dbadmin`
   - Master password: `[Your Secure Password]`
   - Confirm password

4. **Instance Configuration**
   - DB instance class: `db.t3.micro` (free tier eligible)
   - Storage: 20 GB GP2

5. **Connectivity**
   - VPC: Default VPC
   - Publicly accessible: Yes (for initial setup)
   - VPC security group: Create new
     - Name: `social-media-db-sg`
     - Rules: PostgreSQL (5432) from your IP

6. **Additional Configuration**
   - Initial database name: `social_media_db`
   - Backup retention: 7 days
   - Enable auto minor version upgrade

7. **Create Database**
   - Click "Create database"
   - Wait 5-10 minutes for creation

8. **Get Endpoint**
   - Once available, copy the endpoint
   - Format: `social-media-db.xxxxx.us-east-1.rds.amazonaws.com`

### Option B: Using AWS CLI

```bash
aws rds create-db-instance \
    --db-instance-identifier social-media-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username dbadmin \
    --master-user-password YourSecurePassword123 \
    --allocated-storage 20 \
    --db-name social_media_db \
    --backup-retention-period 7 \
    --no-multi-az \
    --publicly-accessible
```

### 3. Update Security Group

```bash
# Get security group ID
aws rds describe-db-instances \
    --db-instance-identifier social-media-db \
    --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' \
    --output text

# Allow access from anywhere (change for production)
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 5432 \
    --cidr 0.0.0.0/0
```

---

## S3 Bucket Setup (Optional - for Static/Media Files)

### 1. Create S3 Bucket

```bash
aws s3 mb s3://social-media-api-static --region us-east-1
```

### 2. Configure Bucket Policy

Create `bucket-policy.json`:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::social-media-api-static/*"
    }
  ]
}
```

Apply policy:
```bash
aws s3api put-bucket-policy \
    --bucket social-media-api-static \
    --policy file://bucket-policy.json
```

### 3. Enable CORS

Create `cors-config.json`:
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "HEAD"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

Apply CORS:
```bash
aws s3api put-bucket-cors \
    --bucket social-media-api-static \
    --cors-configuration file://cors-config.json
```

---

## Application Configuration

### 1. Update Project Files

**Ensure these files exist:**
- `requirements.txt` ✓
- `.ebextensions/01_django.config` ✓
- `.ebextensions/02_python.config` ✓
- `.ebextensions/03_packages.config` ✓
- `.ebignore` ✓
- `social_media_api/settings_production.py` ✓

### 2. Generate Secret Key

```python
# Run in Python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Save this for environment variables.

### 3. Update ALLOWED_HOSTS

In `settings_production.py`, ensure:
```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
```

---

## Elastic Beanstalk Deployment

### 1. Initialize EB Application

Navigate to project directory:
```bash
cd C:\Users\foste\Alx_DjangoLearnLab\social_media_api
```

Initialize:
```bash
eb init
```

**Follow prompts:**
```
1. Select a default region: 1 (us-east-1)
2. Application name: social-media-api
3. Platform: Python
4. Platform version: Python 3.11 (or latest)
5. SSH access: Yes
6. Keypair: Create new or use existing
```

This creates `.elasticbeanstalk/config.yml`

### 2. Create Environment

```bash
eb create social-media-prod
```

**Options during creation:**
- Environment name: social-media-prod
- DNS CNAME: social-media-api (will be social-media-api.elasticbeanstalk.com)
- Load balancer: Application Load Balancer
- Instance type: t3.small (recommended) or t2.micro (free tier)

**Wait 5-10 minutes for environment creation.**

### 3. Verify Deployment

```bash
eb status
```

Should show:
```
Environment details for: social-media-prod
  Application name: social-media-api
  Region: us-east-1
  Status: Ready
  Health: Green
```

---

## Environment Variables

### Set Environment Variables

```bash
# Django Settings
eb setenv DEBUG=False

eb setenv SECRET_KEY="your-generated-secret-key-here"

eb setenv ALLOWED_HOSTS="social-media-prod.elasticbeanstalk.com,yourdomain.com"

# Database (RDS)
eb setenv DB_NAME=social_media_db
eb setenv DB_USER=dbadmin
eb setenv DB_PASSWORD="YourSecurePassword123"
eb setenv DB_HOST="social-media-db.xxxxx.us-east-1.rds.amazonaws.com"
eb setenv DB_PORT=5432

# Superuser (Optional - for automatic creation)
eb setenv DJANGO_SUPERUSER_USERNAME=admin
eb setenv DJANGO_SUPERUSER_EMAIL=admin@example.com
eb setenv DJANGO_SUPERUSER_PASSWORD="AdminPassword123"

# AWS S3 (Optional)
eb setenv USE_S3=False  # Set to True if using S3
eb setenv AWS_STORAGE_BUCKET_NAME=social-media-api-static
eb setenv AWS_S3_REGION_NAME=us-east-1
```

### Verify Environment Variables

```bash
eb printenv
```

### Apply Changes

```bash
eb deploy
```

---

## Post-Deployment Configuration

### 1. Run Migrations (if not auto-run)

```bash
eb ssh

# Inside EC2 instance
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py migrate
python manage.py collectstatic --noinput
exit
```

### 2. Create Superuser

If not created automatically:
```bash
eb ssh
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py createsuperuser
exit
```

### 3. Access Application

```bash
eb open
```

Or visit: `http://social-media-prod.elasticbeanstalk.com`

### 4. Test API Endpoints

```bash
# Health check
curl http://social-media-prod.elasticbeanstalk.com/api/posts/

# Admin panel
# http://social-media-prod.elasticbeanstalk.com/admin/
```

---

## SSL Configuration

### Option A: Using AWS Certificate Manager (ACM)

1. **Request Certificate**
   ```bash
   aws acm request-certificate \
       --domain-name yourdomain.com \
       --validation-method DNS \
       --subject-alternative-names www.yourdomain.com
   ```

2. **Validate Certificate**
   - Add DNS CNAME records as shown in ACM console
   - Wait for validation (5-30 minutes)

3. **Configure Load Balancer**
   - Go to EC2 > Load Balancers
   - Select your EB load balancer
   - Add HTTPS listener (port 443)
   - Select ACM certificate
   - Forward to target group

4. **Update Environment**
   ```bash
   eb setenv SECURE_SSL_REDIRECT=True
   eb deploy
   ```

### Option B: Using Elastic Beanstalk Console

1. Go to EB Console
2. Select your environment
3. Configuration > Load Balancer
4. Add listener: HTTPS:443
5. Select SSL certificate
6. Apply changes

---

## Custom Domain Setup

### 1. Configure Route 53 (or your DNS provider)

**Using Route 53:**
```bash
# Create hosted zone
aws route53 create-hosted-zone \
    --name yourdomain.com \
    --caller-reference $(date +%s)

# Get load balancer DNS
eb status | grep CNAME

# Create A record (alias)
# Point yourdomain.com to EB load balancer
```

### 2. Update ALLOWED_HOSTS

```bash
eb setenv ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com,social-media-prod.elasticbeanstalk.com"
eb deploy
```

---

## Monitoring and Logs

### 1. View Logs

**Recent logs:**
```bash
eb logs
```

**Tail logs in real-time:**
```bash
eb logs --stream
```

**Download all logs:**
```bash
eb logs --all
```

### 2. Health Monitoring

```bash
eb health
```

### 3. CloudWatch Integration

**View metrics in AWS Console:**
- EC2 > Load Balancers > Monitoring
- CloudWatch > Dashboards

**Set up alarms:**
```bash
aws cloudwatch put-metric-alarm \
    --alarm-name social-media-cpu-high \
    --alarm-description "Alert when CPU exceeds 80%" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2
```

---

## Scaling Configuration

### 1. Auto Scaling

```bash
eb config
```

Update configuration:
```yaml
aws:autoscaling:asg:
  MaxSize: '4'
  MinSize: '1'
aws:autoscaling:trigger:
  MeasureName: CPUUtilization
  Unit: Percent
  UpperThreshold: '80'
  LowerThreshold: '20'
```

### 2. Instance Type

```bash
eb scale 2  # Scale to 2 instances
```

---

## Database Backup

### 1. Enable Automated Backups

Already enabled in RDS with 7-day retention.

### 2. Manual Snapshot

```bash
aws rds create-db-snapshot \
    --db-instance-identifier social-media-db \
    --db-snapshot-identifier social-media-db-snapshot-$(date +%Y%m%d)
```

### 3. Restore from Snapshot

```bash
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier social-media-db-restored \
    --db-snapshot-identifier social-media-db-snapshot-20241214
```

---

## Troubleshooting

### Common Issues

#### 1. Health Check Failing

**Check:**
```bash
eb logs
eb health --refresh
```

**Fix:**
- Ensure application starts without errors
- Check database connectivity
- Verify environment variables

#### 2. Database Connection Error

**Fix:**
```bash
# Verify security group allows connections
aws ec2 describe-security-groups \
    --group-ids sg-xxxxxxxxx

# Test connection from EC2
eb ssh
psql -h DB_HOST -U DB_USER -d DB_NAME
```

#### 3. Static Files Not Loading

**Fix:**
```bash
eb ssh
cd /var/app/current
source /var/app/venv/*/bin/activate
python manage.py collectstatic --noinput
```

#### 4. 502 Bad Gateway

**Check application logs:**
```bash
eb logs
cat /var/log/web.stdout.log
cat /var/log/eb-engine.log
```

**Common causes:**
- Application crash
- Timeout during startup
- Missing dependencies

#### 5. Migration Errors

**Manually run migrations:**
```bash
eb ssh
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py migrate --noinput
python manage.py showmigrations
```

---

## Updating the Application

### 1. Make Changes Locally

```bash
# Make your code changes
git add .
git commit -m "Update feature X"
```

### 2. Deploy to EB

```bash
eb deploy
```

### 3. Verify Deployment

```bash
eb status
eb logs
```

---

## Cost Optimization

### 1. Use Reserved Instances

For production, consider reserved instances (up to 75% savings).

### 2. Right-Size Instances

Start with t3.small, monitor usage, adjust as needed.

### 3. Database Optimization

- Use appropriate instance size
- Consider Aurora Serverless for variable workloads

### 4. S3 Lifecycle Policies

```bash
aws s3api put-bucket-lifecycle-configuration \
    --bucket social-media-api-static \
    --lifecycle-configuration file://lifecycle.json
```

---

## Security Best Practices

### 1. Rotate Credentials

```bash
# Generate new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Update in EB
eb setenv SECRET_KEY="new-secret-key"
```

### 2. Restrict Database Access

Update RDS security group to allow only EB security group.

### 3. Enable WAF (Web Application Firewall)

Protect against common attacks:
- SQL injection
- XSS
- DDoS

### 4. Enable CloudTrail

Monitor API calls and changes.

---

## Complete Deployment Checklist

- [ ] AWS CLI installed and configured
- [ ] EB CLI installed
- [ ] RDS PostgreSQL database created
- [ ] S3 bucket created (optional)
- [ ] Secret key generated
- [ ] EB application initialized
- [ ] EB environment created
- [ ] Environment variables set
- [ ] Application deployed
- [ ] Migrations run successfully
- [ ] Static files collected
- [ ] Superuser created
- [ ] SSL certificate configured
- [ ] Custom domain configured
- [ ] Health checks passing
- [ ] Logs reviewed
- [ ] Auto-scaling configured
- [ ] Backups enabled
- [ ] Monitoring set up
- [ ] Security groups configured

---

## Quick Command Reference

```bash
# Initialize
eb init

# Create environment
eb create environment-name

# Deploy
eb deploy

# Set environment variables
eb setenv KEY=value

# View status
eb status

# View health
eb health

# View logs
eb logs

# SSH into instance
eb ssh

# Open in browser
eb open

# Terminate environment
eb terminate environment-name
```

---

## Support Resources

- **AWS Documentation**: https://docs.aws.amazon.com/elasticbeanstalk/
- **EB CLI Guide**: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html
- **Django on EB**: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html
- **RDS Documentation**: https://docs.aws.amazon.com/rds/
- **AWS Support**: https://console.aws.amazon.com/support/

---

## Estimated Costs (Monthly)

**Free Tier:**
- EC2 t2.micro: Free (750 hours/month for 12 months)
- RDS db.t3.micro: Free (750 hours/month for 12 months)
- ELB: ~$16/month
- Total: ~$16/month

**Production (Minimum):**
- EC2 t3.small (2 instances): ~$30/month
- RDS db.t3.small: ~$30/month
- ELB: ~$16/month
- Data transfer: ~$10/month
- Total: ~$86/month

**Note**: Prices vary by region and usage.

---

**Deployment Complete!** 🚀

Your Social Media API is now running on AWS Elastic Beanstalk with:
- ✅ Scalable infrastructure
- ✅ Managed database (RDS)
- ✅ Load balancing
- ✅ Auto-scaling
- ✅ Health monitoring
- ✅ SSL/HTTPS (optional)
- ✅ Custom domain (optional)

For questions or issues, refer to the troubleshooting section or AWS documentation.
