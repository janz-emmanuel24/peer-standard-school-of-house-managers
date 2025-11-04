# Docker Deployment Guide

This guide provides comprehensive step-by-step instructions for deploying the Peer Standard School Django application using Docker in a production server environment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Server Preparation](#server-preparation)
3. [Application Deployment](#application-deployment)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [SSL/HTTPS Setup](#sslhttps-setup)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

- **Server**: Linux server (Ubuntu 20.04+ or Debian 11+ recommended)
- **Resources**: Minimum 2GB RAM, 10GB disk space (20GB recommended)
- **Access**: SSH access with sudo privileges
- **Domain**: Domain name pointing to your server's IP address
- **Knowledge**: Basic familiarity with Linux command line and Docker

---

## Server Preparation

### Step 1: Update System Packages

```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git ufw software-properties-common
```

### Step 2: Install Docker

```bash
# Remove old Docker versions if any
sudo apt remove -y docker docker-engine docker.io containerd runc

# Install Docker using official repository
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (to run docker without sudo)
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installations
docker --version
docker-compose --version

# Log out and back in for group changes to take effect
# Or run: newgrp docker
```

**Verification:**
```bash
docker run hello-world
```

If you see "Hello from Docker!", Docker is installed correctly.

### Step 3: Configure Firewall

```bash
# Enable UFW firewall
sudo ufw enable

# Allow SSH (IMPORTANT: Do this first!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check firewall status
sudo ufw status
```

### Step 4: Create Application Directory

```bash
# Create directory for application
sudo mkdir -p /opt/peer-school
sudo chown $USER:$USER /opt/peer-school
cd /opt/peer-school
```

---

## Application Deployment

### Step 5: Clone the Repository

```bash
# Clone your repository
git clone <your-github-repo-url> .

# Or if repository is already cloned elsewhere:
# git clone <your-github-repo-url> /opt/peer-school

# Verify files are present
ls -la
```

**Expected files:**
- `Dockerfile`
- `docker-compose.yml`
- `requirements.txt`
- `manage.py`
- `peer_standard_school/` directory

### Step 6: Generate Secret Key

```bash
# Generate a secure Django secret key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copy the generated key** - you'll need it in the next step.

### Step 7: Configure Environment Variables

```bash
# Copy the example environment file
cp env.production.example .env

# Edit the environment file
nano .env
```

**Update the following values in `.env`:**

```bash
# Django Settings - REQUIRED
SECRET_KEY=your-generated-secret-key-here  # Paste the key from Step 6
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com  # Replace with your domain

# Database Settings - REQUIRED
DB_ENGINE=postgresql
DB_NAME=peer_school_db
DB_USER=peer_school_user
DB_PASSWORD=your-strong-password-here  # Generate a strong password (min 16 chars)
DB_HOST=db
DB_PORT=5432

# CSRF and CORS Settings - REQUIRED
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CORS_ALLOW_CREDENTIALS=True

# Security Settings - REQUIRED for production
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Port Configuration (optional, defaults shown)
WEB_PORT=8000
NGINX_PORT=80
NGINX_HTTPS_PORT=443
```

**Important Security Notes:**
- Use a **strong password** for `DB_PASSWORD` (mix of upper, lower, numbers, special chars)
- Generate a **unique SECRET_KEY** (never use the example one)
- Set `DEBUG=False` for production
- Update all domain references to your actual domain

**Save and exit** (Ctrl+X, then Y, then Enter in nano)

### Step 8: Build Docker Images

```bash
# Build all Docker images
docker-compose build

# This may take 5-10 minutes on first build
# Watch for any errors
```

**Expected output:**
```
Building web...
Step 1/20 : FROM python:3.11-slim as builder
...
Successfully built <image-id>
```

**Troubleshooting:**
- If build fails, check internet connection
- Verify Docker is running: `sudo systemctl status docker`
- Check disk space: `df -h`

### Step 9: Start Services

```bash
# Start all services in detached mode
docker-compose up -d

# Verify services are running
docker-compose ps
```

**Expected output:**
```
NAME                 STATUS          PORTS
peer_school_db       Up 30 seconds   0.0.0.0:5432->5432/tcp
peer_school_web      Up 25 seconds   0.0.0.0:8000->8000/tcp
peer_school_nginx    Up 20 seconds   0.0.0.0:80->80/tcp
```

All services should show "Up" status.

### Step 10: Check Service Logs

```bash
# View logs for all services
docker-compose logs -f

# Press Ctrl+C to exit log viewing

# Check specific service logs
docker-compose logs web
docker-compose logs db
docker-compose logs nginx
```

**Look for:**
- ✅ "PostgreSQL is ready!"
- ✅ "Running migrations..."
- ✅ "Collecting static files..."
- ✅ "Starting server..."
- ❌ Any ERROR messages

### Step 11: Run Database Migrations

```bash
# Migrations should run automatically via entrypoint script
# But verify they completed successfully:
docker-compose exec web python manage.py showmigrations

# If migrations didn't run automatically, run manually:
docker-compose exec web python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: ...
Running migrations:
  Applying accounts.0001_initial... OK
  Applying courses.0001_initial... OK
  ...
```

### Step 12: Collect Static Files

```bash
# Static files should be collected automatically
# But verify:
docker-compose exec web python manage.py collectstatic --noinput
```

### Step 13: Create Superuser Account

```bash
# Create Django admin superuser
docker-compose exec web python manage.py createsuperuser
```

**Follow the prompts:**
- Username: (choose a username)
- Email address: (your email)
- Password: (strong password - will not echo)

**Verify superuser creation:**
```bash
docker-compose exec web python manage.py shell -c "from accounts.models import User; print(User.objects.filter(is_superuser=True).count())"
```

Should output `1` or more.

### Step 14: Populate Initial Data (Optional)

```bash
# Populate course categories
docker-compose exec web python manage.py populate_categories
```

### Step 15: Verify Application is Running

```bash
# Test from server
curl http://localhost
curl http://localhost/api/

# Test from your local machine
curl http://your-server-ip
```

**Expected response:** HTML content or JSON API response

**Access the admin panel:**
- URL: `http://your-server-ip/admin/`
- Use the superuser credentials created in Step 13

---

## Post-Deployment Configuration

### Step 16: Set Up Domain Name

**If you have a domain:**

1. **Update DNS Records:**
   - Add an A record pointing your domain to the server's IP
   - Add a CNAME record for www subdomain

2. **Update .env file:**
   ```bash
   nano .env
   # Update ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS
   ```

3. **Restart services:**
   ```bash
   docker-compose restart web nginx
   ```

### Step 17: Configure Email (Optional but Recommended)

```bash
nano .env
```

Add email configuration:
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

For Gmail, you'll need an [App Password](https://support.google.com/accounts/answer/185833).

Restart web service:
```bash
docker-compose restart web
```

### Step 18: Set Up Automated Backups

Create backup script:

```bash
sudo mkdir -p /opt/peer-school/backups
nano /opt/peer-school/backup.sh
```

Add this content:

```bash
#!/bin/bash
BACKUP_DIR="/opt/peer-school/backups"
DATE=$(date +%Y%m%d_%H%M%S)
CONTAINER_NAME="peer_school_db"

# Create backup
docker-compose exec -T db pg_dump -U peer_school_user peer_school_db | gzip > "$BACKUP_DIR/backup_$DATE.sql.gz"

# Keep only last 30 days
find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup completed: backup_$DATE.sql.gz"
```

Make it executable:
```bash
chmod +x /opt/peer-school/backup.sh
```

Set up cron job for daily backups:
```bash
crontab -e
```

Add this line (runs daily at 2 AM):
```
0 2 * * * /opt/peer-school/backup.sh >> /opt/peer-school/backups/backup.log 2>&1
```

Test backup:
```bash
/opt/peer-school/backup.sh
ls -lh /opt/peer-school/backups/
```

---

## SSL/HTTPS Setup

### Step 19: Install Certbot (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Stop nginx temporarily (we'll use standalone mode)
docker-compose stop nginx
```

### Step 20: Obtain SSL Certificate

```bash
# Obtain certificate (replace with your domain)
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Follow prompts:
# - Enter email address
# - Agree to terms
# - Choose whether to share email (optional)
```

**Certificates will be saved to:**
- `/etc/letsencrypt/live/yourdomain.com/fullchain.pem`
- `/etc/letsencrypt/live/yourdomain.com/privkey.pem`

### Step 21: Update Nginx Configuration for SSL

```bash
# Copy certificates to nginx directory
sudo mkdir -p /opt/peer-school/nginx/ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/peer-school/nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/peer-school/nginx/ssl/
sudo chmod 644 /opt/peer-school/nginx/ssl/fullchain.pem
sudo chmod 600 /opt/peer-school/nginx/ssl/privkey.pem
```

Update nginx configuration:

```bash
nano /opt/peer-school/nginx/nginx.conf
```

Replace the entire file with SSL-enabled version (see SSL configuration section below).

### Step 22: Restart Services with SSL

```bash
docker-compose up -d
```

### Step 23: Set Up Auto-Renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot will auto-renew, but update nginx config after renewal
# Create renewal hook
sudo nano /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh
```

Add:
```bash
#!/bin/bash
cd /opt/peer-school
docker-compose exec nginx nginx -s reload
```

Make executable:
```bash
sudo chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh
```

---

## Monitoring and Maintenance

### Step 24: Set Up Log Rotation

```bash
# Edit docker-compose.yml to add logging configuration
nano docker-compose.yml
```

Add to each service:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

Restart services:
```bash
docker-compose up -d
```

### Step 25: Monitor Service Health

```bash
# Check service status
docker-compose ps

# Check resource usage
docker stats

# Check disk space
df -h

# Check Docker logs
docker-compose logs --tail=50
```

### Step 26: Set Up Monitoring (Optional)

Consider setting up:
- **Uptime monitoring**: UptimeRobot, Pingdom
- **Application monitoring**: Sentry, New Relic
- **Server monitoring**: Datadog, Prometheus + Grafana

---

## Common Operations

### Update Application

```bash
# 1. Pull latest code
cd /opt/peer-school
git pull origin main

# 2. Rebuild images
docker-compose build

# 3. Stop services
docker-compose down

# 4. Start services
docker-compose up -d

# 5. Run migrations
docker-compose exec web python manage.py migrate

# 6. Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# 7. Restart services
docker-compose restart
```

### Access Django Shell

```bash
docker-compose exec web python manage.py shell
```

### Run Management Commands

```bash
docker-compose exec web python manage.py <command>
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart web
docker-compose restart nginx
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (CAUTION: Deletes data!)
docker-compose down -v
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f nginx
docker-compose logs -f db

# Last 100 lines
docker-compose logs --tail=100
```

### Database Backup and Restore

**Backup:**
```bash
docker-compose exec -T db pg_dump -U peer_school_user peer_school_db > backup_$(date +%Y%m%d).sql
```

**Restore:**
```bash
docker-compose exec -T db psql -U peer_school_user peer_school_db < backup_YYYYMMDD.sql
```

---

## Troubleshooting

### Issue: Services Won't Start

**Check:**
```bash
# Check Docker status
sudo systemctl status docker

# Check logs
docker-compose logs

# Check port conflicts
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443
sudo netstat -tulpn | grep :8000
```

**Solutions:**
- Stop conflicting services
- Change ports in `.env` file
- Restart Docker: `sudo systemctl restart docker`

### Issue: Database Connection Errors

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test connection
docker-compose exec web python manage.py dbshell

# Verify environment variables
docker-compose exec web env | grep DB_
```

**Solutions:**
- Verify `.env` file has correct database credentials
- Check database container is healthy: `docker-compose ps`
- Ensure database finished initializing (check logs)

### Issue: Static Files Not Loading

```bash
# Recollect static files
docker-compose exec web python manage.py collectstatic --noinput --clear

# Check volume mounts
docker-compose exec web ls -la /app/staticfiles

# Check nginx can access files
docker-compose exec nginx ls -la /static
```

**Solutions:**
- Verify static files exist: `docker-compose exec web ls /app/staticfiles`
- Check nginx volume mount: `docker-compose config`
- Restart nginx: `docker-compose restart nginx`

### Issue: Permission Errors

```bash
# Fix file permissions
docker-compose exec web chown -R django:django /app/staticfiles /app/media

# Check file ownership
docker-compose exec web ls -la /app/
```

### Issue: Port Already in Use

```bash
# Find what's using the port
sudo lsof -i :80
sudo lsof -i :443

# Stop conflicting service or change ports in .env
nano .env
# Change NGINX_PORT=8080
docker-compose up -d
```

### Issue: SSL Certificate Errors

```bash
# Check certificate files exist
sudo ls -la /etc/letsencrypt/live/yourdomain.com/

# Verify certificate
sudo certbot certificates

# Test renewal
sudo certbot renew --dry-run
```

### Issue: Application Returns 502 Bad Gateway

```bash
# Check web service is running
docker-compose ps web

# Check web service logs
docker-compose logs web

# Test web service directly
curl http://localhost:8000

# Restart web service
docker-compose restart web
```

### Issue: Can't Access Admin Panel

**Check:**
1. Superuser exists: `docker-compose exec web python manage.py shell -c "from accounts.models import User; print(User.objects.filter(is_superuser=True).count())"`
2. URL is correct: `https://yourdomain.com/admin/`
3. Check ALLOWED_HOSTS in `.env`
4. Check nginx logs: `docker-compose logs nginx`

---

## Security Checklist

Before going live, verify:

- [ ] `DEBUG=False` in `.env`
- [ ] Strong `SECRET_KEY` (not the example one)
- [ ] Strong database password
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] SSL/HTTPS enabled
- [ ] Firewall configured (only ports 22, 80, 443 open)
- [ ] Regular backups configured
- [ ] `.env` file is not in version control (check `.gitignore`)
- [ ] Superuser password is strong
- [ ] Log rotation configured
- [ ] Services running as non-root user

---

## Performance Optimization

### Resource Limits

Edit `docker-compose.yml`:

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Gunicorn Workers

Adjust workers based on CPU cores (2 × CPU cores + 1):

```bash
# Edit docker-compose.yml
# Change: --workers 3
# To: --workers 5 (for 2 CPU cores)
```

### Database Optimization

```bash
# Connect to database
docker-compose exec db psql -U peer_school_user peer_school_db

# Create indexes (if needed)
# Analyze tables
ANALYZE;
```

---

## Support

For additional help:

1. **Check logs**: `docker-compose logs`
2. **Verify configuration**: `docker-compose config`
3. **Check service status**: `docker-compose ps`
4. **Test database**: `docker-compose exec web python manage.py dbshell`
5. **Review Docker documentation**: https://docs.docker.com/
6. **Django deployment checklist**: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

---

## Appendix: SSL Nginx Configuration

If you need the complete SSL-enabled nginx configuration:

```nginx
upstream django {
    server web:8000;
}

limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;

# HTTP - Redirect to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    client_max_body_size 100M;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files
    location /static/ {
        alias /static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    # API endpoints
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Login endpoints
    location ~ ^/(accounts/login|api/token)/ {
        limit_req zone=login_limit burst=3 nodelay;
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # All other requests
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Save this to `nginx/nginx.conf` after SSL setup.

