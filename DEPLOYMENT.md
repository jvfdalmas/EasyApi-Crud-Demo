# Production Deployment Guide

This guide walks you through deploying the EasyAPI CRUD Demo application on an Ubuntu EC2 server with Nginx.

## Prerequisites

- Ubuntu EC2 instance with sudo access
- Domain name pointing to your EC2 instance (optional, can use IP address)
- Python 3.8+ and Node.js 18+ installed

## Project Structure

```
easyapi-crud-demo/
├── backend/
│   ├── app/
│   │   ├── config.py          # Configuration settings
│   │   ├── db.py              # Async SQLAlchemy setup
│   │   ├── main.py            # FastAPI application
│   │   ├── models.py          # Database models
│   │   ├── routes.py          # API routes
│   │   └── schemas.py         # Pydantic schemas
│   ├── alembic/               # Database migrations
│   ├── alembic.ini            # Alembic configuration
│   ├── backend.service        # Systemd service file
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── api.ts             # API client
│   │   ├── main.ts            # Application entry point
│   │   └── style.css          # Styles
│   ├── package.json           # Node.js dependencies
│   └── vite.config.js         # Vite configuration
└── easyapi-crud-demo.nginx    # Nginx configuration
```

## Step-by-Step Deployment

### 1. Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-venv nginx git curl

# Install Node.js (if not already installed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### 2. Deploy the Application

```bash
# Create application directory
sudo mkdir -p /var/www/easyapi-crud-demo
sudo chown $USER:$USER /var/www/easyapi-crud-demo

# Copy your project files to the server
# (Use scp, rsync, or git clone)
cd /var/www/easyapi-crud-demo
# Example: git clone https://github.com/yourusername/easyapi-crud-demo.git .
```

### 3. Backend Setup

```bash
# Navigate to backend directory
cd /var/www/easyapi-crud-demo/backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables (optional, create .env file)
cat > .env << EOF
APP_ENV=production
DATABASE_URL=sqlite+aiosqlite:///./app.db
ALLOWED_ORIGINS=http://your-domain.com,https://your-domain.com
EOF

# Initialize database with Alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Test the backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
# Test: curl http://localhost:8000/api/health
# Stop with Ctrl+C
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd /var/www/easyapi-crud-demo/frontend

# Install Node.js dependencies
npm install

# Build the frontend for production
npm run build

# Copy built files to Nginx directory
sudo mkdir -p /var/www/frontend
sudo cp -r dist/* /var/www/frontend/
sudo chown -R www-data:www-data /var/www/frontend
```

### 5. Configure Systemd Service

```bash
# Copy the systemd service file
sudo cp /var/www/easyapi-crud-demo/backend/backend.service /etc/systemd/system/

# Update the service file with correct paths and settings
sudo nano /etc/systemd/system/backend.service

# Make sure to update:
# - WorkingDirectory path
# - Environment variables (DATABASE_URL, ALLOWED_ORIGINS)
# - User/Group (use www-data or create a dedicated user)

# Set correct ownership for backend files
sudo chown -R www-data:www-data /var/www/easyapi-crud-demo/backend

# Reload systemd and enable the service
sudo systemctl daemon-reload
sudo systemctl enable backend.service
sudo systemctl start backend.service

# Check service status
sudo systemctl status backend.service
```

### 6. Configure Nginx

```bash
# Copy Nginx configuration
sudo cp /var/www/easyapi-crud-demo/easyapi-crud-demo.nginx /etc/nginx/sites-available/easyapi-crud-demo

# Update the configuration file
sudo nano /etc/nginx/sites-available/easyapi-crud-demo
# Replace 'your-domain.com' with your actual domain or server IP

# Enable the site
sudo ln -s /etc/nginx/sites-available/easyapi-crud-demo /etc/nginx/sites-enabled/

# Remove default Nginx site (optional)
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### 7. Firewall Configuration

```bash
# Allow HTTP and HTTPS traffic
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable
```

### 8. SSL Certificate (Optional but Recommended)

```bash
# Install Certbot for Let's Encrypt
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

## Verification

1. **Backend Health Check:**
   ```bash
   curl http://your-domain.com/health
   # Should return: {"status":"ok"}
   ```

2. **Frontend Access:**
   - Open `http://your-domain.com` in your browser
   - You should see the Items management interface

3. **API Functionality:**
   ```bash
   # Test creating an item
   curl -X POST http://your-domain.com/api/items/ \
        -H "Content-Type: application/json" \
        -d '{"name":"Test Item"}'
   
   # Test listing items
   curl http://your-domain.com/api/items/
   ```

## Monitoring and Maintenance

### Service Management

```bash
# Check backend service status
sudo systemctl status backend.service

# View backend logs
sudo journalctl -u backend.service -f

# Restart backend service
sudo systemctl restart backend.service

# Check Nginx status
sudo systemctl status nginx

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Database Management

```bash
# Navigate to backend directory
cd /var/www/easyapi-crud-demo/backend
source venv/bin/activate

# Create new migration after model changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# View migration history
alembic history
```

### Updates and Maintenance

```bash
# To update the application:
cd /var/www/easyapi-crud-demo

# Pull latest changes (if using git)
git pull origin main

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart backend.service

# Update frontend
cd ../frontend
npm install
npm run build
sudo cp -r dist/* /var/www/frontend/
sudo systemctl reload nginx
```

## Troubleshooting

### Common Issues

1. **Backend service fails to start:**
   ```bash
   sudo journalctl -u backend.service -n 50
   # Check for Python import errors or database connection issues
   ```

2. **Frontend not loading:**
   ```bash
   sudo nginx -t  # Check Nginx configuration
   sudo tail -f /var/log/nginx/error.log
   ```

3. **API requests failing:**
   - Check if backend service is running: `sudo systemctl status backend.service`
   - Verify Nginx proxy configuration
   - Check firewall settings: `sudo ufw status`

4. **Database issues:**
   ```bash
   cd /var/www/easyapi-crud-demo/backend
   source venv/bin/activate
   alembic current  # Check current migration
   alembic upgrade head  # Apply pending migrations
   ```

### Performance Optimization

1. **Increase Gunicorn workers** (in `backend.service`):
   ```
   ExecStart=.../gunicorn app.main:app -w 8 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000
   ```

2. **Enable Nginx caching** for static assets (already configured in provided config)

3. **Database optimization:**
   - Consider PostgreSQL for production instead of SQLite
   - Add database indexes for frequently queried fields

## Security Considerations

1. **Keep system updated:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Use environment variables** for sensitive configuration
3. **Enable SSL/TLS** with Let's Encrypt
4. **Configure proper firewall rules**
5. **Regular backups** of database and application files
6. **Monitor logs** for suspicious activity

## Support

For issues or questions:
- Check the application logs: `sudo journalctl -u backend.service -f`
- Review Nginx logs: `sudo tail -f /var/log/nginx/error.log`
- Verify service status: `sudo systemctl status backend.service nginx`
