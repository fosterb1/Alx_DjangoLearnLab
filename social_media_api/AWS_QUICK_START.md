# AWS Deployment - Quick Start Guide

## 🚀 Deploy in 15 Minutes

This guide will get your Social Media API running on AWS Elastic Beanstalk quickly.

---

## Prerequisites (5 minutes)

1. **AWS Account**
   - Sign up at https://aws.amazon.com/
   - Free tier available for 12 months

2. **Install AWS CLI**
   ```powershell
   # Windows: Download and install
   # https://awscli.amazonaws.com/AWSCLIV2.msi
   
   # Verify
   aws --version
   ```

3. **Install EB CLI**
   ```bash
   pip install awsebcli
   
   # Verify
   eb --version
   ```

4. **Configure AWS**
   ```bash
   aws configure
   # Enter:
   # - AWS Access Key ID
   # - AWS Secret Access Key
   # - Region: us-east-1
   # - Output: json
   ```

---

## Option 1: Automated Deployment (Recommended)

### Windows (PowerShell)
```powershell
cd C:\Users\foste\Alx_DjangoLearnLab\social_media_api
.\deploy_aws.ps1
```

### Linux/Mac
```bash
cd social_media_api
chmod +x deploy_aws.sh
./deploy_aws.sh
```

**Follow the prompts!**

---

## Option 2: Manual Deployment (Step-by-Step)

### Step 1: Create RDS Database (Optional)

**Using AWS Console:**
1. Go to RDS Console
2. Create database
3. Choose PostgreSQL
4. Free tier template
5. DB identifier: `social-media-db`
6. Master username: `dbadmin`
7. Master password: [Your choice]
8. Create database
9. Copy endpoint when ready

**OR use SQLite for testing** (skip RDS setup)

### Step 2: Initialize Elastic Beanstalk

```bash
cd C:\Users\foste\Alx_DjangoLearnLab\social_media_api

# Initialize
eb init

# Select:
# - Region: 1 (us-east-1)
# - Application name: social-media-api
# - Platform: Python 3.11
# - SSH: Yes
```

### Step 3: Create Environment

```bash
# Create production environment
eb create social-media-prod --instance-type t3.small

# Wait 5-10 minutes for creation
```

### Step 4: Set Environment Variables

```bash
# Generate secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set variables
eb setenv DEBUG=False
eb setenv SECRET_KEY="your-generated-key"
eb setenv ALLOWED_HOSTS="social-media-prod.elasticbeanstalk.com"

# If using RDS:
eb setenv DB_NAME=social_media_db
eb setenv DB_USER=dbadmin
eb setenv DB_PASSWORD="your-db-password"
eb setenv DB_HOST="your-rds-endpoint.rds.amazonaws.com"
eb setenv DB_PORT=5432
```

### Step 5: Deploy

```bash
eb deploy
```

### Step 6: Verify

```bash
# Check status
eb status

# Open in browser
eb open
```

---

## Post-Deployment Setup

### 1. Run Migrations

```bash
# SSH into instance
eb ssh

# Activate virtual environment
source /var/app/venv/*/bin/activate
cd /var/app/current

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Exit
exit
```

### 2. Test API

Visit: `http://your-app.elasticbeanstalk.com/api/posts/`

Admin: `http://your-app.elasticbeanstalk.com/admin/`

---

## Common Commands

```bash
# Deploy changes
eb deploy

# View logs
eb logs

# Check health
eb health

# SSH into instance
eb ssh

# View status
eb status

# Open in browser
eb open

# Set environment variable
eb setenv KEY=value

# View environment variables
eb printenv

# Terminate environment
eb terminate environment-name
```

---

## Troubleshooting

### Application Not Starting

```bash
# Check logs
eb logs

# Look for errors in:
# - /var/log/web.stdout.log
# - /var/log/eb-engine.log
```

### Database Connection Error

```bash
# Verify environment variables
eb printenv

# Check RDS security group allows EB access
# Go to: RDS Console > Security Groups
```

### Static Files Not Loading

```bash
eb ssh
cd /var/app/current
source /var/app/venv/*/bin/activate
python manage.py collectstatic --noinput
```

---

## What's Included

### Files Created for AWS Deployment

1. **`.ebextensions/01_django.config`**
   - Django/WSGI configuration
   - Automatic migrations
   - Static files collection

2. **`.ebextensions/02_python.config`**
   - Python process configuration
   - Timeout settings

3. **`.ebextensions/03_packages.config`**
   - System package dependencies

4. **`requirements.txt`**
   - Python dependencies

5. **`settings_production.py`**
   - Production Django settings
   - Database configuration
   - Security settings

6. **`.ebignore`**
   - Files to exclude from deployment

7. **`accounts/management/commands/createsu.py`**
   - Auto-create superuser command

---

## Estimated Costs

### Free Tier (First 12 Months)
- EC2 t2.micro: Free (750 hours/month)
- RDS db.t3.micro: Free (750 hours/month)
- Load Balancer: ~$16/month
- **Total: ~$16/month**

### After Free Tier
- EC2 t3.small: ~$15/month
- RDS db.t3.small: ~$30/month
- Load Balancer: ~$16/month
- Data transfer: ~$10/month
- **Total: ~$71/month**

**Tip:** Use Reserved Instances for 40-60% savings!

---

## Security Checklist

- [ ] SECRET_KEY is randomly generated
- [ ] DEBUG is set to False
- [ ] Database password is strong
- [ ] RDS security group is restricted
- [ ] ALLOWED_HOSTS is properly set
- [ ] SSL certificate configured (optional)
- [ ] Regular backups enabled

---

## Next Steps

### Production Readiness

1. **Configure SSL/HTTPS**
   - Use AWS Certificate Manager
   - Add HTTPS listener to load balancer
   - Enable `SECURE_SSL_REDIRECT`

2. **Custom Domain**
   - Configure Route 53
   - Point domain to EB endpoint
   - Update ALLOWED_HOSTS

3. **Monitoring**
   - Set up CloudWatch alarms
   - Configure log retention
   - Enable detailed monitoring

4. **Auto-Scaling**
   - Configure min/max instances
   - Set scaling triggers
   - Test scaling behavior

5. **Backups**
   - Configure RDS automated backups
   - Create manual snapshots
   - Test restore procedure

---

## Support

- **Full Documentation**: See `AWS_DEPLOYMENT_GUIDE.md`
- **AWS Documentation**: https://docs.aws.amazon.com/elasticbeanstalk/
- **Troubleshooting**: See `AWS_DEPLOYMENT_GUIDE.md` > Troubleshooting section

---

## Deployment Checklist

- [ ] AWS CLI installed and configured
- [ ] EB CLI installed
- [ ] RDS database created (or using SQLite)
- [ ] EB application initialized
- [ ] EB environment created
- [ ] Environment variables set
- [ ] Application deployed successfully
- [ ] Migrations run
- [ ] Superuser created
- [ ] API endpoints tested
- [ ] Admin panel accessible
- [ ] Logs reviewed

---

**Congratulations!** 🎉

Your Social Media API is now live on AWS!

**Access your API:**
- API: `http://your-app.elasticbeanstalk.com/api/`
- Admin: `http://your-app.elasticbeanstalk.com/admin/`
- Feed: `http://your-app.elasticbeanstalk.com/api/feed/`

For detailed configuration and advanced features, see **AWS_DEPLOYMENT_GUIDE.md**
