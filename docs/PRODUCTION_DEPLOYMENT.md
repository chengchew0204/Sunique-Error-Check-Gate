# Production Deployment Guide

This guide explains how to deploy the InFlow Error Check Gate to production and replace ngrok.

## Option 1: AWS Lambda with Serverless Framework (Recommended)

### Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **Serverless Framework** installed globally

### Installation

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Configure AWS credentials
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region (us-east-1)

# Install Serverless Framework
npm install -g serverless

# Install Serverless plugin for Python
npm install --save-dev serverless-python-requirements
```

### Deployment Steps

```bash
# 1. Navigate to project directory
cd /Users/zackwu204/CursorAI/Sunique/04-error-check-gate

# 2. Ensure all environment variables are set in your .env file
# These will be used by the serverless.yml configuration

# 3. Deploy to AWS Lambda
cd serverless
serverless deploy --stage prod

# Output will show your production URLs:
# endpoints:
#   POST - https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/webhook/inflow
#   GET - https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/
#   GET - https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/validate/{order_id}
#   GET - https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/history/{order_id}
```

### Update InFlow Webhook

After deployment, update your InFlow webhook subscription:

```python
from app.clients.inflow_client import inflow_client

# Unsubscribe old webhook (optional)
# inflow_client.unsubscribe_webhook(old_webhook_id)

# Subscribe with new production URL
result = inflow_client.subscribe_webhook(
    webhook_url='https://YOUR-API-GATEWAY-URL.amazonaws.com/prod/webhook/inflow',
    events=['salesOrder.created', 'salesOrder.updated']
)

print(f"Production Webhook ID: {result['webHookSubscriptionId']}")
print(f"Secret: {result['secret']}")

# Update WEBHOOK_SECRET in AWS Lambda environment variables
```

### Useful Commands

```bash
# View logs
serverless logs -f webhook --stage prod --tail

# Update function (faster than full deploy)
serverless deploy function -f webhook --stage prod

# Remove deployment
serverless remove --stage prod

# View deployment info
serverless info --stage prod
```

### Advantages
- ✅ **Pay per request** (very cost-effective)
- ✅ **Auto-scaling** (handles traffic spikes automatically)
- ✅ **No server management**
- ✅ **High availability**
- ✅ **Already configured in your project**

### Costs
- First **1 million requests per month**: FREE
- After that: ~$0.20 per million requests
- Extremely affordable for webhook processing

---

## Option 2: Traditional Cloud Server (EC2, DigitalOcean, etc.)

Deploy Flask as a regular web server with gunicorn.

### Setup on Ubuntu Server

```bash
# 1. SSH into your server
ssh user@your-server-ip

# 2. Clone your repository
git clone <your-repo-url>
cd 04-error-check-gate

# 3. Run setup
bash setup.sh

# 4. Create .env file with production credentials
nano .env

# 5. Install and configure nginx as reverse proxy
sudo apt update
sudo apt install nginx

# 6. Create nginx configuration
sudo nano /etc/nginx/sites-available/inflow-webhook
```

**Nginx Configuration:**

```nginx
server {
    listen 80;
    server_name your-domain.com;  # or use IP address

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/inflow-webhook /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 7. Install and configure SSL with Let's Encrypt (required for webhooks)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com

# 8. Create systemd service for Flask app
sudo nano /etc/systemd/system/inflow-webhook.service
```

**Systemd Service File:**

```ini
[Unit]
Description=InFlow Error Check Gate
After=network.target

[Service]
User=your-user
WorkingDirectory=/home/your-user/04-error-check-gate
Environment="PATH=/home/your-user/04-error-check-gate/venv/bin"
ExecStart=/home/your-user/04-error-check-gate/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl start inflow-webhook
sudo systemctl enable inflow-webhook
sudo systemctl status inflow-webhook

# Your production URL will be: https://your-domain.com/webhook/inflow
```

### Advantages
- ✅ Full control over the server
- ✅ Can handle long-running processes
- ✅ No cold starts

### Disadvantages
- ❌ Monthly costs ($5-50+)
- ❌ You manage updates and security
- ❌ Need to handle scaling manually

---

## Option 3: Heroku (Quick & Easy)

Fast deployment with minimal configuration.

### Steps

```bash
# 1. Install Heroku CLI
brew tap heroku/brew && brew install heroku

# 2. Login to Heroku
heroku login

# 3. Create Heroku app
cd /Users/zackwu204/CursorAI/Sunique/04-error-check-gate
heroku create your-app-name

# 4. Create Procfile
echo "web: gunicorn app.main:app" > Procfile

# 5. Set environment variables
heroku config:set INFLOW_API_KEY=your_key
heroku config:set INFLOW_COMPANY_ID=your_id
heroku config:set WEBHOOK_SECRET=your_secret
# ... set all other variables

# 6. Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Your production URL: https://your-app-name.herokuapp.com/webhook/inflow
```

### Advantages
- ✅ Very easy to deploy
- ✅ Free tier available
- ✅ Automatic SSL

### Disadvantages
- ❌ Free tier sleeps after 30 min of inactivity (not suitable for webhooks)
- ❌ Paid tier: $7/month minimum

---

## Option 4: Azure Functions

Similar to AWS Lambda, already has handler code in your project.

```11:54:serverless/handler.py
def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    
    Args:
        event: Lambda event object
        context: Lambda context object
    
    Returns:
        Response object with statusCode, headers, and body
    """
    # Initialize validators on cold start
    initialize_validators()
    
    # Convert Lambda event to Flask-compatible format
    # Handle API Gateway proxy integration format
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    headers = event.get('headers', {})
    body = event.get('body', '')
    
    # Create a test request context
    with app.test_request_context(
        path=path,
        method=http_method,
        headers=headers,
        data=body
    ):
        try:
            # Process the request
            response = app.full_dispatch_request()
            
            # Convert Flask response to Lambda response
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }


def azure_function_handler(req):
    """
    Azure Functions handler.
    
    Args:
        req: Azure Functions HttpRequest object
    
    Returns:
        Azure Functions HttpResponse object
    """
```

### Steps

```bash
# Install Azure Functions Core Tools
brew tap azure/functions
brew install azure-functions-core-tools@4

# Install Azure CLI
brew install azure-cli

# Login
az login

# Create Function App
az functionapp create --resource-group YourResourceGroup \
  --consumption-plan-location eastus \
  --runtime python --runtime-version 3.9 \
  --functions-version 4 \
  --name inflow-webhook-app \
  --storage-account yourstorageaccount

# Deploy (requires function.json and host.json configuration)
func azure functionapp publish inflow-webhook-app
```

---

## Comparison Table

| Feature | AWS Lambda | EC2/VPS | Heroku | Azure Functions |
|---------|-----------|---------|--------|-----------------|
| **Cost** | $0 - $20/mo | $5 - $50/mo | $7+/mo | $0 - $20/mo |
| **Setup Complexity** | Medium | High | Low | Medium |
| **Scalability** | Automatic | Manual | Automatic | Automatic |
| **Cold Starts** | Yes (~1s) | No | Yes | Yes (~1s) |
| **Maintenance** | None | High | Low | None |
| **Already Configured** | ✅ Yes | ❌ No | ❌ No | ⚠️ Partial |

---

## Recommended Approach: AWS Lambda

For your webhook use case, **AWS Lambda is ideal** because:

1. ✅ **Already configured** - just run `serverless deploy`
2. ✅ **Cost-effective** - probably free forever at webhook volumes
3. ✅ **No maintenance** - AWS handles everything
4. ✅ **Reliable** - 99.95% uptime SLA
5. ✅ **Fast deployment** - push changes in seconds

---

## Migration Checklist

- [ ] Choose deployment platform
- [ ] Set up cloud account and credentials
- [ ] Deploy application to production
- [ ] Test production endpoint (health check)
- [ ] Update InFlow webhook subscription with production URL
- [ ] Update WEBHOOK_SECRET in production environment
- [ ] Test with real webhook event
- [ ] Monitor logs for 24 hours
- [ ] Shut down ngrok
- [ ] Document production URL and credentials

---

## Monitoring & Logs

### AWS Lambda
```bash
# View real-time logs
serverless logs -f webhook --stage prod --tail

# Or use AWS CloudWatch in the console
```

### Traditional Server
```bash
# View Flask logs
sudo journalctl -u inflow-webhook -f

# View nginx logs
sudo tail -f /var/log/nginx/error.log
```

---

## Troubleshooting Production Issues

### Webhook not receiving events
1. Check InFlow webhook subscription is active
2. Test endpoint manually: `curl https://your-production-url/`
3. Check HMAC signature verification
4. Review logs for errors

### High latency
1. Increase Lambda memory (faster CPU)
2. Optimize API calls to InFlow
3. Consider caching frequently accessed data

### Cost concerns
1. Monitor AWS billing dashboard
2. Set up billing alerts
3. Review CloudWatch logs for errors causing retries

---

## Need Help?

If you need assistance with deployment:
1. Check cloud provider documentation
2. Review deployment logs for errors
3. Test endpoints with curl before updating InFlow
4. Start with staging environment before production

