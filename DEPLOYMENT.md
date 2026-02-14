# Deployment Guide

This guide covers deploying the E-commerce Chatbot to various platforms.

## Table of Contents
- [Docker Deployment](#docker-deployment)
- [Heroku Deployment](#heroku-deployment)
- [AWS Deployment](#aws-deployment)
- [Production Configuration](#production-configuration)

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV FLASK_DEBUG=False
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000

# Expose port
EXPOSE 5000

# Run with gunicorn
RUN pip install gunicorn eventlet
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "app:app"]
```

### 2. Create .dockerignore

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.git
.gitignore
*.md
tests/
.vscode/
.idea/
```

### 3. Build and Run

```bash
# Build image
docker build -t ecommerce-chatbot .

# Run container
docker run -d -p 5000:5000 \
  -e SECRET_KEY="your-secret-key" \
  --name chatbot \
  ecommerce-chatbot

# Check logs
docker logs chatbot

# Stop container
docker stop chatbot
```

### 4. Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  chatbot:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_DEBUG=False
      - FLASK_HOST=0.0.0.0
      - FLASK_PORT=5000
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

## Heroku Deployment

### 1. Create Procfile

```
web: gunicorn -k eventlet -w 1 app:app
```

### 2. Create runtime.txt

```
python-3.9.18
```

### 3. Deploy

```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-chatbot-app

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set FLASK_DEBUG=False

# Deploy
git push heroku main

# Open app
heroku open
```

## AWS Deployment

### Option 1: AWS Elastic Beanstalk

1. Install AWS EB CLI:
```bash
pip install awsebcli
```

2. Initialize EB:
```bash
eb init -p python-3.9 chatbot-app
```

3. Create environment:
```bash
eb create chatbot-prod
```

4. Deploy:
```bash
eb deploy
```

5. Set environment variables:
```bash
eb setenv SECRET_KEY="your-secret-key" FLASK_DEBUG=False
```

### Option 2: AWS EC2

1. Launch EC2 instance (Ubuntu)
2. SSH into instance
3. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip nginx
```

4. Clone repository:
```bash
git clone <your-repo>
cd Chatbot-E-commerce-Project
```

5. Install Python packages:
```bash
pip3 install -r requirements.txt
pip3 install gunicorn eventlet
```

6. Configure nginx:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

7. Create systemd service:
```ini
[Unit]
Description=E-commerce Chatbot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Chatbot-E-commerce-Project
Environment="SECRET_KEY=your-secret-key"
Environment="FLASK_DEBUG=False"
ExecStart=/usr/local/bin/gunicorn -k eventlet -w 1 --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

8. Start service:
```bash
sudo systemctl start chatbot
sudo systemctl enable chatbot
```

## Production Configuration

### Security Checklist

- [ ] Generate strong SECRET_KEY
- [ ] Set FLASK_DEBUG=False
- [ ] Use HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Regular backups
- [ ] Security updates

### Generate Secret Key

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### SSL/HTTPS Setup

Using Let's Encrypt with nginx:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Environment Variables in Production

Never hardcode secrets. Use:
- Environment variables
- Secret management services (AWS Secrets Manager, HashiCorp Vault)
- Configuration management tools

### Monitoring and Logging

1. **Application Logging:**
```python
import logging
logging.basicConfig(
    filename='chatbot.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

2. **Monitoring Tools:**
- AWS CloudWatch
- Datadog
- New Relic
- Prometheus + Grafana

### Performance Optimization

1. **Use Production WSGI Server:**
```bash
gunicorn -k eventlet -w 4 --bind 0.0.0.0:5000 app:app
```

2. **Enable Caching:**
- Redis for session storage
- CDN for static files

3. **Database for Products:**
- Replace in-memory catalog with PostgreSQL/MySQL
- Add database connection pooling

4. **Load Balancing:**
- Multiple application instances
- nginx/HAProxy as load balancer

### Scaling Considerations

1. **Horizontal Scaling:**
- Multiple app instances
- Shared session storage (Redis)
- Load balancer

2. **Vertical Scaling:**
- Increase instance size
- More workers
- Better hardware

3. **Database Scaling:**
- Read replicas
- Connection pooling
- Query optimization

## Troubleshooting

### Application Won't Start
- Check logs: `docker logs <container>` or `journalctl -u chatbot`
- Verify environment variables
- Check port availability

### 502 Bad Gateway
- Verify application is running
- Check nginx/proxy configuration
- Verify port forwarding

### WebSocket Not Working
- Ensure WebSocket support in proxy
- Check CORS configuration
- Verify Socket.IO version compatibility

## Rollback Strategy

1. **Docker:**
```bash
docker pull ecommerce-chatbot:previous-version
docker stop chatbot
docker run -d ecommerce-chatbot:previous-version
```

2. **Git-based:**
```bash
git revert <commit-hash>
git push
# Trigger deployment
```

3. **Blue-Green Deployment:**
- Maintain two identical environments
- Switch traffic after testing new version
- Quick rollback by switching back

## Support

For deployment issues:
- Check application logs
- Review server logs
- Verify network configuration
- Contact DevOps team

---

**Remember:** Always test deployments in a staging environment before production!
