# Webhook Update Summary

## ✅ Completed Successfully!

Your InFlow webhook has been updated and configured to work with your production AWS Lambda deployment.

---

## 📋 What Was Done

### 1. ✅ Created New InFlow Webhook Subscription

**Webhook Details:**
- **Webhook ID:** `a6af9336-e0b7-4824-b9af-b117b243ed2d`
- **Production URL:** `https://ahl9t9ati7.execute-api.us-east-2.amazonaws.com/prod/webhook/inflow`
- **Events:** `salesOrder.updated`
- **Status:** Active

### 2. ✅ Updated Webhook Secret

**New Webhook Secret:**
```
[SECRET REDACTED - Stored in AWS Lambda environment variables and local .env file]
```

**Updated in:**
- ✅ AWS Lambda `inflow-error-check-gate-prod-webhook` function
- ✅ AWS Lambda `inflow-error-check-gate-prod-errorMonitor` function  
- ✅ Local `.env` file

---

## 🧪 Testing with Real InFlow Order

To verify everything is working, you need to test with a **real InFlow order**:

### Step 1: Monitor Logs in Real-Time

Open a terminal and run:
```bash
cd /Users/zackwu204/CursorAI/Sunique/04-error-check-gate
serverless logs -f webhook --stage prod --tail
```

Keep this terminal open to see real-time logs.

### Step 2: Trigger a Webhook Event

In InFlow, do ONE of the following:
1. **Create a new sales order**, OR
2. **Update an existing sales order** (change any field)

### Step 3: Check the Logs

You should see output like:
```
WEBHOOK RECEIVED:
{
  "eventType": "salesOrder.updated",
  "salesOrderId": "actual-order-id"
}

Fetching order data for: actual-order-id
Order Number: SO-12345
Running validation for order: actual-order-id (SO-12345)
```

### Step 4: Verify Results

- ✅ **Logs show webhook received** → Webhook is working!
- ✅ **Validation runs** → Application is working!
- ✅ **Email notification sent** (if errors found) → Notification system working!

---

## 🔍 Verification Checklist

Use this checklist to verify everything:

- [x] InFlow webhook created and pointing to production URL
- [x] Lambda environment variables updated with new secret
- [x] Local `.env` file updated with new secret
- [ ] Test with real InFlow order (create or update order)
- [ ] Logs show webhook received successfully
- [ ] Validation runs without errors
- [ ] Email notification sent if issues found

---

## 📊 View Logs

### Real-Time Logs (Terminal)
```bash
# Webhook logs
serverless logs -f webhook --stage prod --tail

# Error monitor logs  
serverless logs -f errorMonitor --stage prod --tail
```

### AWS CloudWatch Console
1. Go to: https://console.aws.amazon.com/cloudwatch/
2. Navigate to **Logs → Log groups**
3. Find:
   - `/aws/lambda/inflow-error-check-gate-prod-webhook`
   - `/aws/lambda/inflow-error-check-gate-prod-errorMonitor`

---

## 🐛 Troubleshooting

### Issue: Webhook not receiving events

**Check:**
1. Webhook is active in InFlow
2. Test by creating/updating an order in InFlow
3. Check CloudWatch logs for any requests

**Solution:**
```bash
# Check Lambda configuration
aws lambda get-function-configuration \
  --function-name inflow-error-check-gate-prod-webhook \
  --region us-east-2 | grep WEBHOOK_SECRET
```

### Issue: "Invalid signature" error

**Possible Causes:**
1. Old webhook secret still in use
2. InFlow webhook needs to be recreated

**Solution:**
```bash
# Verify Lambda has the correct secret
aws lambda get-function-configuration \
  --function-name inflow-error-check-gate-prod-webhook \
  --region us-east-2 | grep "WEBHOOK_SECRET"

# Should show: "WEBHOOK_SECRET": "whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Issue: No validation running

**Check:**
1. Lambda logs show order data fetched successfully
2. Validators are registered
3. No Python errors in logs

**Solution:**
Check logs for detailed error messages:
```bash
serverless logs -f webhook --stage prod --tail
```

---

## 📝 Important Notes

### Webhook Secret Security
- **Never commit** `WEBHOOK_SECRET` to Git
- **Keep it secure** - it validates that webhooks are from InFlow
- **Already in `.gitignore`** - your `.env` file is protected

### Multiple Webhooks
If you had old webhooks (like from ngrok), you can delete them:

```python
from app.clients.inflow_client import inflow_client

# Get webhook ID from InFlow dashboard
old_webhook_id = 'old-webhook-id-here'

# Delete old webhook
inflow_client.unsubscribe_webhook(old_webhook_id)
```

### Testing Mode
Your email is currently in **testing mode**:
- `EMAIL_TESTING_MODE=True`
- `TEST_EMAIL_RECIPIENT=zackwu204@gmail.com`

All validation emails will go to `zackwu204@gmail.com` for testing.

**To enable production emails:**
1. Update `.env`: `EMAIL_TESTING_MODE=False`
2. Redeploy: `serverless deploy --stage prod`

---

## 🎯 Next Steps

1. **✅ Test with Real Order** - Create/update an order in InFlow
2. **✅ Verify Logs** - Check CloudWatch or terminal logs
3. **✅ Check Email** - Verify notification email received (if errors)
4. **✅ Monitor for 24 hours** - Ensure everything runs smoothly
5. **⏭️ Set up billing alerts** - Monitor AWS costs

---

## 📞 Quick Commands Reference

```bash
# View real-time webhook logs
serverless logs -f webhook --stage prod --tail

# Check Lambda configuration
aws lambda get-function-configuration \
  --function-name inflow-error-check-gate-prod-webhook \
  --region us-east-2

# Test health check
curl https://ahl9t9ati7.execute-api.us-east-2.amazonaws.com/prod/

# Redeploy if needed
cd /Users/zackwu204/CursorAI/Sunique/04-error-check-gate
set -a && source .env && set +a
serverless deploy --stage prod
```

---

## ✅ Summary

**Your webhook is now live and ready!** 🎉

- ✅ Production webhook URL configured in InFlow
- ✅ Webhook secret updated in Lambda
- ✅ All environment variables synchronized
- ✅ Ready to process real InFlow orders

**Test it now by creating or updating a sales order in InFlow!**

For any issues, check the logs using:
```bash
serverless logs -f webhook --stage prod --tail
```

---

**Last Updated:** November 11, 2025  
**Webhook ID:** a6af9336-e0b7-4824-b9af-b117b243ed2d  
**Production URL:** https://ahl9t9ati7.execute-api.us-east-2.amazonaws.com/prod/webhook/inflow

