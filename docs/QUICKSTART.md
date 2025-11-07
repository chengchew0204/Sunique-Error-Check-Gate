# Quick Start Guide

This guide will help you get the InFlow Error Check Gate up and running quickly.

## Prerequisites

- Python 3.9 or higher
- InFlow account with API access
- Microsoft Azure AD app registrations for Outlook and OneDrive
- ngrok account (for local testing)

## Step 1: Clone and Setup

```bash
cd 04-error-check-gate
bash setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Create a `.env` file template

## Step 2: Configure Environment Variables

Edit the `.env` file with your credentials:

```bash
nano .env  # or use your preferred editor
```

Required variables:
- `INFLOW_API_KEY` - Your InFlow API key
- `INFLOW_COMPANY_ID` - Your InFlow company ID
- `WEBHOOK_SECRET` - Will be generated after webhook subscription
- `ADMIN_EMAILS` - Comma-separated list of admin email addresses

Optional (for email notifications):
- `OUTLOOK_CLIENT_ID`
- `OUTLOOK_CLIENT_SECRET`
- `OUTLOOK_TENANT_ID`

Optional (for delivery fee validation):
- `ONEDRIVE_CLIENT_ID`
- `ONEDRIVE_CLIENT_SECRET`
- `ONEDRIVE_TENANT_ID`
- `DELIVERY_RECORD_FILE_PATH`

## Step 3: Start the Server

```bash
source venv/bin/activate
python app/main.py
```

You should see:
```
Starting InFlow Error Check Gate on port 5000
* Running on http://0.0.0.0:5000
```

## Step 4: Expose with ngrok

In a new terminal window:

```bash
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`).

## Step 5: Subscribe to InFlow Webhooks

Create a Python script to subscribe:

```python
from app.clients.inflow_client import inflow_client

result = inflow_client.subscribe_webhook(
    webhook_url='https://YOUR_NGROK_URL.ngrok.io/webhook/inflow',
    events=['salesOrder.created', 'salesOrder.updated']
)

print(f"Webhook ID: {result['webHookSubscriptionId']}")
print(f"Secret: {result['secret']}")
```

Or use the InFlow API directly:

```bash
curl -X PUT "https://api.inflow.com/v1/YOUR_COMPANY_ID/webhooks" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://YOUR_NGROK_URL.ngrok.io/webhook/inflow",
    "events": ["salesOrder.created", "salesOrder.updated"],
    "webHookSubscriptionId": "GENERATE_A_UUID",
    "webHookSubscriptionRequestId": "GENERATE_A_UUID"
  }'
```

## Step 6: Update Webhook Secret

Add the returned `secret` to your `.env` file:

```bash
WEBHOOK_SECRET=the_secret_from_subscription
```

Restart the Flask server.

## Step 7: Test the System

### Test 1: Health Check

```bash
curl http://localhost:5000/
```

Expected response:
```json
{
  "status": "running",
  "service": "InFlow Error Check Gate",
  "version": "1.0.0"
}
```

### Test 2: Manual Validation

```bash
curl http://localhost:5000/validate/YOUR_ORDER_ID
```

### Test 3: Create a Test Order

1. Go to your InFlow account
2. Create or update a sales order
3. Watch the Flask server logs
4. Check the `logs/` directory for validation results

## Troubleshooting

### "Missing required environment variables"

Make sure you've filled in all required variables in `.env`:
- `INFLOW_API_KEY`
- `INFLOW_COMPANY_ID`
- `WEBHOOK_SECRET`

### "Invalid HMAC signature"

- Verify `WEBHOOK_SECRET` matches the secret from webhook subscription
- Make sure you're using the HTTPS URL from ngrok

### "Failed to acquire access token"

For Outlook/OneDrive integration:
- Check Azure AD app credentials
- Verify app permissions in Azure Portal
- Ensure admin consent has been granted

### Webhook not receiving events

- Verify ngrok is running and URL is correct
- Check InFlow webhook subscription is active
- Test with manual validation endpoint first

## Next Steps

Once Phase 0 is working:

1. **Phase 1**: Implement discount validation
2. **Phase 2**: Implement TUK item validation
3. **Phase 3**: Implement credit card fee validation
4. **Phase 4**: Implement assembly fee validation
5. **Phase 5**: Implement delivery fee validation
6. **Phase 6**: Deploy to production

See `plan.md` for detailed implementation steps.

## Getting Help

- Check `README.md` for detailed documentation
- Review `plan.md` for implementation phases
- Check the `logs/` directory for error details
- Look at console output for debugging information

