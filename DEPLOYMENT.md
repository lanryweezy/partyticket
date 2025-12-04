# Deployment Guide for PartyTicket Nigeria

This guide will help you deploy the PartyTicket Nigeria application to various hosting platforms.

## Prerequisites

- Python 3.8 or higher
- Git installed
- Database (PostgreSQL recommended for production, SQLite for development)
- Payment gateway API keys (Paystack and/or Flutterwave)

## Environment Variables

Create a `.flaskenv` file (or set environment variables on your hosting platform) with the following:

```env
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/dbname
PAYSTACK_PUBLIC_KEY=your-paystack-public-key
PAYSTACK_SECRET_KEY=your-paystack-secret-key
FLUTTERWAVE_PUBLIC_KEY=your-flutterwave-public-key
FLUTTERWAVE_SECRET_KEY=your-flutterwave-secret-key
```

**Important:** Generate a strong SECRET_KEY using:
```python
import secrets
print(secrets.token_hex(32))
```

## Deployment Options

### 1. Heroku

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**:
   ```bash
   heroku create partyticket-nigeria
   ```

3. **Add PostgreSQL addon**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set PAYSTACK_PUBLIC_KEY=your-key
   heroku config:set PAYSTACK_SECRET_KEY=your-key
   heroku config:set FLUTTERWAVE_PUBLIC_KEY=your-key
   heroku config:set FLUTTERWAVE_SECRET_KEY=your-key
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

6. **Run migrations**:
   ```bash
   heroku run flask db upgrade
   ```

### 2. Railway

1. **Connect your GitHub repository** to Railway
2. **Add environment variables** in Railway dashboard
3. **Add PostgreSQL service** if needed
4. **Deploy** - Railway will automatically detect and deploy

### 3. DigitalOcean App Platform

1. **Create a new app** from GitHub repository
2. **Configure environment variables**
3. **Add PostgreSQL database** component
4. **Deploy**

### 4. AWS Elastic Beanstalk

1. **Install EB CLI**:
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB**:
   ```bash
   eb init -p python-3.11 partyticket-nigeria
   ```

3. **Create environment**:
   ```bash
   eb create partyticket-env
   ```

4. **Set environment variables**:
   ```bash
   eb setenv SECRET_KEY=your-key PAYSTACK_PUBLIC_KEY=your-key
   ```

5. **Deploy**:
   ```bash
   eb deploy
   ```

### 5. Self-Hosted (VPS)

1. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql
   ```

2. **Clone repository**:
   ```bash
   git clone https://github.com/yourusername/partyticket-nigeria.git
   cd partyticket-nigeria
   ```

3. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL**:
   ```bash
   sudo -u postgres createdb partyticket
   sudo -u postgres createuser partyticket_user
   ```

5. **Configure Gunicorn**:
   Create `/etc/systemd/system/partyticket.service`:
   ```ini
   [Unit]
   Description=PartyTicket Gunicorn daemon
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/partyticket-nigeria
   Environment="PATH=/path/to/partyticket-nigeria/venv/bin"
   ExecStart=/path/to/partyticket-nigeria/venv/bin/gunicorn --workers 3 --bind unix:/path/to/partyticket-nigeria/partyticket.sock run:app

   [Install]
   WantedBy=multi-user.target
   ```

6. **Configure Nginx**:
   Create `/etc/nginx/sites-available/partyticket`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           include proxy_params;
           proxy_pass http://unix:/path/to/partyticket-nigeria/partyticket.sock;
       }

       location /static {
           alias /path/to/partyticket-nigeria/app/static;
       }
   }
   ```

7. **Start services**:
   ```bash
   sudo systemctl start partyticket
   sudo systemctl enable partyticket
   sudo systemctl restart nginx
   ```

## Database Migrations

After deployment, run migrations:

```bash
flask db upgrade
```

## SSL/HTTPS Setup

For production, always use HTTPS. You can use:
- **Let's Encrypt** (free SSL certificates)
- **Cloudflare** (free SSL + CDN)
- **Your hosting provider's SSL** service

## Monitoring

Consider setting up:
- **Error tracking**: Sentry
- **Analytics**: Google Analytics
- **Uptime monitoring**: UptimeRobot, Pingdom
- **Log aggregation**: Loggly, Papertrail

## Backup Strategy

1. **Database backups**: Set up automated daily backups
2. **File backups**: Backup uploaded files regularly
3. **Configuration backups**: Keep `.flaskenv` secure

## Performance Optimization

1. **Enable caching**: Use Redis or Memcached
2. **CDN**: Use Cloudflare or AWS CloudFront for static files
3. **Database indexing**: Ensure proper indexes on frequently queried fields
4. **Gunicorn workers**: Adjust based on server resources

## Security Checklist

- [ ] Strong SECRET_KEY set
- [ ] HTTPS enabled
- [ ] Database credentials secure
- [ ] Payment API keys protected
- [ ] CSRF protection enabled
- [ ] SQL injection prevention (using ORM)
- [ ] XSS protection enabled
- [ ] Security headers configured
- [ ] Regular security updates

## Troubleshooting

### Application won't start
- Check logs: `heroku logs --tail` or `journalctl -u partyticket`
- Verify environment variables are set
- Check database connection

### Database errors
- Verify DATABASE_URL is correct
- Run migrations: `flask db upgrade`
- Check database permissions

### Static files not loading
- Verify static file path in Nginx config
- Check file permissions
- Clear browser cache

## Support

For deployment issues, check:
- Application logs
- Server logs
- Database logs
- Payment gateway logs


