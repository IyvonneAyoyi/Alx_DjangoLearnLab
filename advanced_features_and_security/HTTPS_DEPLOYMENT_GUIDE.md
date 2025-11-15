# HTTPS and Secure Deployment Configuration Guide

## Overview

This guide provides comprehensive instructions for configuring HTTPS and secure redirects in your Django LibraryProject application. It covers both development and production environments.

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Production Environment Configuration](#production-environment-configuration)
3. [Security Settings Reference](#security-settings-reference)
4. [Web Server Configuration](#web-server-configuration)
5. [SSL/TLS Certificate Setup](#ssltls-certificate-setup)
6. [Testing HTTPS Configuration](#testing-https-configuration)
7. [Troubleshooting](#troubleshooting)

## Development Environment Setup

### Running in Development Mode

By default, the application runs in development mode with reduced security settings to allow local testing:

```bash
# Development mode (default)
python manage.py runserver

# With environment variable explicit
ENVIRONMENT=development python manage.py runserver
```

In development mode:
- `SECURE_SSL_REDIRECT = False` - Allows HTTP connections
- `SECURE_HSTS_SECONDS = 0` - HSTS not enforced
- `SESSION_COOKIE_SECURE = False` - Cookies sent over HTTP
- `CSRF_COOKIE_SECURE = False` - CSRF cookies sent over HTTP
- `DEBUG = True` - Debug mode enabled

### Development with Self-Signed HTTPS Certificate

To test HTTPS locally:

```bash
# Generate self-signed certificate (valid for 365 days)
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run server with HTTPS using django-extensions
pip install django-extensions
python manage.py runserver_plus --cert cert

# Or use Gunicorn with SSL
pip install gunicorn
gunicorn --certfile=cert.pem --keyfile=key.pem --bind 0.0.0.0:8443 LibraryProject.wsgi
```

## Production Environment Configuration

### Setting Up Production Environment

```bash
# Set production environment variable
export ENVIRONMENT=production

# Or on Windows PowerShell
$env:ENVIRONMENT = 'production'

# Run the application
python manage.py runserver
# or with Gunicorn
gunicorn LibraryProject.wsgi --bind 0.0.0.0:8000
```

In production mode, the following security settings are automatically enabled:

### Production Security Settings

```python
# HTTPS Redirect
SECURE_SSL_REDIRECT = True  # All HTTP requests redirect to HTTPS

# HSTS (HTTP Strict-Transport-Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year (31536000 seconds)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply to subdomains
SECURE_HSTS_PRELOAD = True  # Allow inclusion in HSTS preload list

# Secure Cookies
SESSION_COOKIE_SECURE = True  # Session cookies over HTTPS only
CSRF_COOKIE_SECURE = True  # CSRF cookies over HTTPS only

# Browser Security Headers
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME sniffing
SECURE_BROWSER_XSS_FILTER = True  # Enable XSS filtering
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'  # Control referrer info
```

## Security Settings Reference

### 1. HTTPS Redirect Configuration

#### SECURE_SSL_REDIRECT
```python
SECURE_SSL_REDIRECT = True  # In production
```
- **Purpose**: Redirects all HTTP requests to HTTPS
- **HTTP Status**: 301 Permanent Redirect
- **Development**: Set to False
- **Production**: Set to True (requires valid SSL certificate)

#### SECURE_PROXY_SSL_HEADER
```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```
- **Purpose**: Tells Django that HTTPS is being used when behind a proxy/load balancer
- **Use**: When using Nginx, Apache with mod_proxy, or cloud load balancers
- **Development**: Set to None
- **Production**: Set when using a reverse proxy

### 2. HTTP Strict-Transport-Security (HSTS)

#### SECURE_HSTS_SECONDS
```python
SECURE_HSTS_SECONDS = 31536000  # 1 year in seconds
```
- **Purpose**: Tells browsers to only use HTTPS for the specified duration
- **Value**: Number of seconds (31536000 = 1 year)
- **Development**: 0 (disabled)
- **Production**: 31536000 (minimum 1 year recommended)

#### SECURE_HSTS_INCLUDE_SUBDOMAINS
```python
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```
- **Purpose**: Applies HSTS policy to all subdomains
- **Development**: False
- **Production**: True

#### SECURE_HSTS_PRELOAD
```python
SECURE_HSTS_PRELOAD = True
```
- **Purpose**: Allows inclusion in browser HSTS preload lists
- **Development**: False
- **Production**: True
- **Note**: Required for full HSTS protection

### 3. Secure Cookie Settings

#### SESSION_COOKIE_SECURE
```python
SESSION_COOKIE_SECURE = True
```
- **Purpose**: Session cookies only sent over HTTPS
- **Prevents**: Man-in-the-middle attacks
- **Development**: False
- **Production**: True

#### CSRF_COOKIE_SECURE
```python
CSRF_COOKIE_SECURE = True
```
- **Purpose**: CSRF protection cookies only sent over HTTPS
- **Development**: False
- **Production**: True

#### HTTP-Only Cookies
```python
SESSION_COOKIE_HTTPONLY = True  # Default: True
CSRF_COOKIE_HTTPONLY = True  # Default: True
```
- **Purpose**: Prevents JavaScript access to cookies
- **Default**: Already True (do not change)
- **Protection**: Mitigates XSS attacks

### 4. Security Headers

#### X-Frame-Options
```python
X_FRAME_OPTIONS = 'DENY'
```
- **Options**:
  - 'DENY' - Page cannot be displayed in frame
  - 'SAMEORIGIN' - Can be displayed in frame on same origin
  - 'ALLOW-FROM' - Can be displayed in frame on specific origin
- **Purpose**: Prevents clickjacking attacks
- **Default**: 'DENY' (recommended)

#### SECURE_CONTENT_TYPE_NOSNIFF
```python
SECURE_CONTENT_TYPE_NOSNIFF = True
```
- **Purpose**: Prevents browser MIME type sniffing
- **Header**: X-Content-Type-Options: nosniff
- **Default**: True

#### SECURE_BROWSER_XSS_FILTER
```python
SECURE_BROWSER_XSS_FILTER = True
```
- **Purpose**: Enables browser's built-in XSS protection
- **Header**: X-XSS-Protection: 1; mode=block
- **Default**: True

#### SECURE_REFERRER_POLICY
```python
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
```
- **Options**:
  - 'no-referrer'
  - 'no-referrer-when-downgrade'
  - 'same-origin'
  - 'origin'
  - 'strict-origin'
  - 'origin-when-cross-origin'
  - 'strict-origin-when-cross-origin'
- **Purpose**: Controls how much referrer information is shared

### 5. Content Security Policy

```python
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'"),
    'style-src': ("'self'", "'unsafe-inline'"),
    'img-src': ("'self'", "data:", "https:"),
    'font-src': ("'self'",),
    'connect-src': ("'self'",),
    'frame-ancestors': ("'none'",),
    'base-uri': ("'self'",),
}
```
- **Purpose**: Restricts which resources can be loaded
- **Header**: Content-Security-Policy

## Web Server Configuration

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/libraryproject

upstream django_app {
    server 127.0.0.1:8000;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com www.example.com;
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    # SSL Certificate and Key
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Proxy settings
    location / {
        proxy_pass http://django_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files
    location /static/ {
        alias /path/to/staticfiles/;
        expires 30d;
    }
    
    # Media files
    location /media/ {
        alias /path/to/media/;
        expires 7d;
    }
}
```

### Apache Configuration

```apache
# /etc/apache2/sites-available/libraryproject.conf

# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    Redirect permanent / https://example.com/
</VirtualHost>

# HTTPS Server
<VirtualHost *:443>
    ServerName example.com
    ServerAlias www.example.com
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "DENY"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    
    # Proxy Settings
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    
    # Set X-Forwarded-Proto header
    RequestHeader set X-Forwarded-Proto https
    
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/libraryproject_access.log combined
    ErrorLog ${APACHE_LOG_DIR}/libraryproject_error.log
</VirtualHost>

# Enable SSL module
# a2enmod ssl
# a2enmod headers
# a2enmod proxy
```

## SSL/TLS Certificate Setup

### Using Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate for Nginx
sudo certbot certonly --nginx -d example.com -d www.example.com

# Generate certificate for Apache
sudo certbot certonly --apache -d example.com -d www.example.com

# Auto-renewal (runs twice daily)
sudo certbot renew --dry-run

# Manual renewal
sudo certbot renew
```

### Using Self-Signed Certificates (Development Only)

```bash
# Generate self-signed certificate (valid for 365 days)
openssl req -x509 -newkey rsa:4096 -nodes \
    -out cert.pem -keyout key.pem -days 365 \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=example.com"
```

### Certificate Configuration

Update Django settings for proxy HTTPS:

```python
# In settings.py for production with reverse proxy
if IS_PRODUCTION:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

## Testing HTTPS Configuration

### 1. Test HTTPS Redirect

```bash
# Should redirect from HTTP to HTTPS
curl -I http://example.com
# Response should show: HTTP/1.1 301 Moved Permanently

# HTTPS should work
curl -I https://example.com
# Response should show: HTTP/1.1 200 OK
```

### 2. Check Security Headers

```bash
# View all security headers
curl -I https://example.com

# Should include headers like:
# Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
```

### 3. Test Cookie Security

```python
# In Django shell
from django.test import Client

client = Client()
response = client.get('/login/')

# Check if cookies are marked as Secure
for cookie_name, cookie in client.cookies.items():
    print(f"{cookie_name}: Secure={cookie.get('secure', 'Not set')}")
```

### 4. SSL Lab Test

Visit [SSL Labs](https://www.ssllabs.com/ssltest/) and enter your domain for comprehensive SSL testing.

### 5. Security Headers Test

Visit [Security Headers](https://securityheaders.com/) to check your security headers.

## Troubleshooting

### Issue: "SECURE_SSL_REDIRECT is True but HTTPS is not configured"

**Solution**: 
- Ensure SSL certificates are installed
- Configure reverse proxy with proper X-Forwarded-Proto header
- Check SECURE_PROXY_SSL_HEADER setting in production

### Issue: "CSRF verification failed. Request aborted"

**Solution**:
- Verify CSRF_TRUSTED_ORIGINS includes your domain
- Check that CSRF_COOKIE_SECURE matches your protocol
- Ensure CSRF token is included in forms

### Issue: "Cookies not being set securely"

**Solution**:
```python
# Verify in development mode
SESSION_COOKIE_SECURE = False  # For development
# Set to True in production
SESSION_COOKIE_SECURE = IS_PRODUCTION
```

### Issue: "HSTS error or certificate pinning issues"

**Solution**:
- Ensure certificates are valid before enabling HSTS
- Start with low SECURE_HSTS_SECONDS (e.g., 3600)
- Gradually increase to 31536000 after verification
- Remove SECURE_HSTS_PRELOAD if experiencing issues

### Issue: "Mixed content warning in browser"

**Solution**:
- Ensure all resources (CSS, JS, images) are loaded over HTTPS
- Update template URLs to use https://
- Use relative URLs when possible

## Environment Variables

Create a `.env` file for environment configuration:

```bash
# .env file
ENVIRONMENT=production
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
```

Load in settings.py:

```python
import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
IS_PRODUCTION = ENVIRONMENT == 'production'
DEBUG = os.getenv('DEBUG', 'True') == 'True'
```

## Summary of Security Configuration

| Setting | Development | Production |
|---------|-------------|-----------|
| SECURE_SSL_REDIRECT | False | True |
| SECURE_HSTS_SECONDS | 0 | 31536000 |
| SECURE_HSTS_INCLUDE_SUBDOMAINS | False | True |
| SECURE_HSTS_PRELOAD | False | True |
| SESSION_COOKIE_SECURE | False | True |
| CSRF_COOKIE_SECURE | False | True |
| DEBUG | True | False |

## References

- [Django Security Documentation](https://docs.djangoproject.com/en/5.2/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
- [Let's Encrypt](https://letsencrypt.org/)
