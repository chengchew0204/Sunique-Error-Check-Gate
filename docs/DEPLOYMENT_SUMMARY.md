# AWS Lambda Deployment Summary

## 🎉 Deployment Status: SUCCESS!

Your InFlow Error Check Gate application has been successfully deployed to AWS Lambda.

**Deployment Date:** November 11, 2025  
**Region:** us-east-2 (Ohio)  
**AWS Account:** 519975955103

---

## 📍 Production Endpoints

### Main Webhook Endpoint (for InFlow)
```
POST https://ahl9t9ati7.execute-api.us-east-2.amazonaws.com/prod/webhook/inflow
```

### Health Check
```
GET https://ahl9t9ati7.execute-api.us-east-2.amazonaws.com/prod/
```

### Manual Validation
```
GET https://ahl9t9ati7.execute-api.us-east-2.amazonaws.com/prod/validate/{order_id}
```

### Validation History
```
GET https://ahl9t9ati7.execute-api.us-east-2.amazonaws.com/prod/history/{order_id}
```

### Monitor Endpoints
```
POST https://ahl9t9ati7.execute-api.us-east-2.amazonaws.com/prod/monitor/check
GET  https://ahl9t9ati7.execute-api.us-east-2.amazonaws.com/prod/monitor/status
```

---

## 📊 Deployed Functions

| Function | Size | Purpose |
|----------|------|---------|
| `webhook` | 74 MB | Main webhook handler for InFlow events |
| `errorMonitor` | 74 MB | Scheduled function (runs every 5 minutes) to check pending errors |

---

## ⏭️ Next Steps

### 1. Update InFlow Webhook Subscription

You need to update your InFlow webhook to point to the new production URL:

```python
# Run this script
cd /Users/zackwu204/CursorAI/Sunique/04-error-check-gate
source venv/bin/activate
python3

# Then in Python:
from app.clients.inflow_client import inflow_client

# List existing webhooks
existing = inflow_client.list_webhook_subscriptions()
print("Existing webhooks:", existing)

# Subscribe with production URL
result = inflow_client.subscribe_webhook(
    webhook_url='https://ahl9t9ati7.execute-api.us-east-2.amazonaws.com/prod/webhook/inflow',
    events=['salesOrder.created', 'salesOrder.updated']
)

print(f"\n✅ Production Webhook Created!")
print(f"Webhook ID: {result['webHookSubscriptionId']}")
print(f"Secret: {result['secret']}")
print(f"\n⚠️  IMPORTANT: Save the secret and update your .env file!")
```

### 2. Update WEBHOOK_SECRET in Lambda

After getting the new webhook secret:

**Option A: Via AWS Console**
1. Go to AWS Lambda console: https://console.aws.amazon.com/lambda/
2. Find function: `inflow-error-check-gate-prod-webhook`
3. Configuration → Environment variables
4. Edit `WEBHOOK_SECRET` with the new value
5. Save

**Option B: Update .env and Redeploy**
1. Update `WEBHOOK_SECRET` in your local `.env` file
2. Run: `serverless deploy --stage prod`

### 3. Test with Real Order

1. Create or update a sales order in InFlow
2. Check CloudWatch logs:
   ```bash
   cd /Users/zackwu204/CursorAI/Sunique/04-error-check-gate
   serverless logs -f webhook --stage prod --tail
   ```
3. Verify validation runs and emails are sent

### 4. Monitor Your Deployment

#### View Logs
```bash
# Real-time webhook logs
serverless logs -f webhook --stage prod --tail

# Error monitor logs
serverless logs -f errorMonitor --stage prod --tail
```

#### AWS CloudWatch Console
- Go to: https://console.aws.amazon.com/cloudwatch/
- Log groups:
  - `/aws/lambda/inflow-error-check-gate-prod-webhook`
  - `/aws/lambda/inflow-error-check-gate-prod-errorMonitor`

### 5. Set Up Billing Alerts

1. Go to AWS Billing Dashboard
2. Create a budget alert for $10/month
3. Set notifications at 80% and 100%

---

## 🔧 Useful Commands

### Deploy Updates
```bash
cd /Users/zackwu204/CursorAI/Sunique/04-error-check-gate
set -a && source .env && set +a
serverless deploy --stage prod
```

### Deploy Only Function (Faster)
```bash
serverless deploy function -f webhook --stage prod
```

### View Deployment Info
```bash
serverless info --stage prod
```

### Invoke Function Manually
```bash
serverless invoke -f webhook --stage prod --data '{"httpMethod":"GET","path":"/"}'
```

### Remove Deployment (Cleanup)
```bash
serverless remove --stage prod
```

---

## 💰 Cost Estimate

With your webhook use case:
- **Lambda:** $0 (likely under 1M requests/month - FREE tier)
- **API Gateway:** $0 (likely under 1M requests/month - FREE tier)
- **CloudWatch Logs:** ~$0.50/month
- **S3 (deployment bucket):** ~$0.10/month
- **Total:** ~$0.60 - $2/month

---

## 🔄 Scheduled Error Monitor

The `errorMonitor` function runs automatically **every 5 minutes** to check for expired pending errors (30-minute grace period). This replaces the background thread from your local deployment.

---

## 📝 Important Notes

1. **Logs Storage:** Validation logs are stored in `/tmp/logs` in Lambda (temporary)
   - Logs are cleared when Lambda container is recycled
   - All logs are also in CloudWatch Logs (permanent)
   - Consider storing logs in S3 or database for long-term persistence

2. **Environment Variables:** All environment variables from `.env` are injected into Lambda
   - To update: modify `.env` locally and redeploy
   - Or update directly in AWS Lambda console

3. **Local Development:** You can still run locally with:
   ```bash
   python3 run.py
   ```

4. **Stop Local ngrok:** You no longer need ngrok running!

---

## 🆘 Troubleshooting

### Webhook Not Receiving Events
1. Check InFlow webhook subscription is active and points to production URL
2. Test endpoint manually: `curl https://ahl9t9ati7.execute-api.us-east-2.amazonaws.com/prod/`
3. Check HMAC signature verification in logs
4. Verify `WEBHOOK_SECRET` matches InFlow subscription

### High Latency
1. Lambda cold start: first request takes longer (~1-2 seconds)
2. Increase Lambda memory in `serverless.yml` → `memorySize: 1024`
3. Redeploy

### Errors in Logs
1. View CloudWatch logs for detailed stack traces
2. Check environment variables are set correctly
3. Verify all required API credentials are valid

---

## 📚 Documentation

- **Project Docs:** `/Users/zackwu204/CursorAI/Sunique/04-error-check-gate/docs/`
- **AWS Lambda Docs:** https://docs.aws.amazon.com/lambda/
- **Serverless Framework:** https://www.serverless.com/framework/docs/

---

## ✅ Deployment Checklist

- [x] AWS account configured
- [x] Serverless Framework installed
- [x] Application deployed to Lambda
- [x] Health check endpoint working
- [x] Monitor endpoint working
- [ ] InFlow webhook updated to production URL
- [ ] Tested with real order
- [ ] Billing alerts configured
- [ ] Documentation reviewed

---

**Congratulations! Your application is now running in production on AWS Lambda! 🚀**

For questions or issues, refer to the documentation in the `docs/` directory.

