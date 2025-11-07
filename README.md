# InFlow Error Check Gate

Automated validation system for InFlow sales orders that checks pricing, discounts, fees, and business logic compliance.

## Overview

The Error Check Gate automatically validates every sales order upon creation or update via InFlow webhooks. It performs 5 validation checks:

1. **Discount Validation** - Detects excessive or incorrect discounts
2. **TUK Item Validation** - Ensures Touch_Up_Kit items have no discounts
3. **Credit Card Fee Validation** - Verifies 3% fee for credit card payments
4. **Assembly Fee Validation** - Validates assembly fee calculation and discounts
5. **Delivery Fee Validation** - Checks freight fees against delivery records

## Architecture

- **Python Flask** webhook server
- **InFlow API** integration for order data
- **Microsoft Outlook API** for email notifications
- **OneDrive** for delivery record access
- **JSON/CSV** logging for audit trail
- **ngrok** for local development, **serverless** for production

## Project Structure

```
04-error-check-gate/
├── app/
│   ├── main.py                 # Flask webhook server
│   ├── config.py               # Configuration management
│   ├── validators/             # Validation rule modules
│   ├── clients/                # API clients (InFlow, OneDrive, Outlook)
│   ├── services/               # Business logic services
│   └── utils/                  # Utilities (HMAC verification)
├── logs/                       # Validation logs (JSON/CSV)
├── tests/                      # Unit tests
├── serverless/                 # Serverless deployment configs
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables (not in git)
```

## Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv      # Only for running the first time
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
# InFlow API
INFLOW_API_KEY=your_api_key
INFLOW_COMPANY_ID=your_company_id
INFLOW_API_BASE_URL=https://api.inflow.com/v1

# Webhook
WEBHOOK_SECRET=your_webhook_secret

# OneDrive
ONEDRIVE_CLIENT_ID=your_client_id
ONEDRIVE_CLIENT_SECRET=your_client_secret
ONEDRIVE_TENANT_ID=your_tenant_id
DELIVERY_RECORD_FILE_PATH=/path/to/file.xlsx

# Outlook
OUTLOOK_CLIENT_ID=your_client_id
OUTLOOK_CLIENT_SECRET=your_client_secret
OUTLOOK_TENANT_ID=your_tenant_id

# Email
ADMIN_EMAILS=admin1@company.com,admin2@company.com

# Business Logic
CREDIT_CARD_FEE_PERCENTAGE=0.03
```

### 3. Run Local Development Server

```bash
python3 run.py
```

The server will start on `http://localhost:8000`.

### 4. Expose Local Server with ngrok

In a separate terminal:

```bash
ngrok http 8000
```

Copy the ngrok HTTPS URL (e.g., `https://abc123.ngrok.io`).

### 5. Subscribe to InFlow Webhooks

Use the webhook URL from ngrok:

```python
from app.clients.inflow_client import inflow_client

result = inflow_client.subscribe_webhook(
    webhook_url='https://abc123.ngrok.io/webhook/inflow',
    events=['salesOrder.created', 'salesOrder.updated']
)

print(f"Webhook secret: {result['secret']}")
```

Add the returned `secret` to your `.env` file as `WEBHOOK_SECRET`.

## API Endpoints

### Webhook Endpoint

- **POST** `/webhook/inflow` - Receives InFlow webhook events
  - Verifies HMAC signature
  - Fetches order data
  - Runs validations
  - Logs results
  - Sends email notifications

### Manual Validation

- **GET** `/validate/<order_id>` - Manually trigger validation for an order
- **GET** `/history/<order_id>` - Get validation history for an order

### Health Check

- **GET** `/` - Service health check

## Development Phases

The project is developed incrementally with full testing after each phase:

- **Phase 0**: Foundation (webhook server, API clients, logging) ✅
- **Phase 1**: Discount Validation
- **Phase 2**: TUK Item Validation
- **Phase 3**: Credit Card Fee Validation
- **Phase 4**: Assembly Fee Validation
- **Phase 5**: Delivery Fee Validation
- **Phase 6**: Production Deployment

## Testing

### Test Webhook Locally

1. Start the Flask server
2. Start ngrok
3. Create or update a sales order in InFlow
4. Check console logs for validation results
5. Check `logs/` directory for JSON/CSV output

### Manual Validation

```bash
curl http://localhost:5000/validate/<order_id>
```

### View Validation History

```bash
curl http://localhost:5000/history/<order_id>
```

## Email Notifications

Notifications are sent to:
- All admin emails (configured in `.env`)
- Order account manager (extracted from order data)

Emails include:
- Order details
- Validation status
- List of issues
- Suggested fixes

## Logging

### JSON Logs

Individual validation results stored in:
- `logs/validation_YYYYMMDD_HHMMSS_<order_id>.json`

### CSV Logs

Daily summary appended to:
- `logs/validation_log_YYYYMMDD.csv`

Columns: timestamp, order_id, status, error_count, warning_count, issues_summary

## Production Deployment

Deploy to AWS Lambda, Azure Functions, or similar serverless platform:

1. Package application with dependencies
2. Configure environment variables
3. Deploy handler function
4. Update InFlow webhook URL to production endpoint
5. Configure monitoring and alerts

See `serverless/` directory for deployment configurations.

## Troubleshooting

### HMAC Verification Fails

- Ensure `WEBHOOK_SECRET` matches the secret from InFlow webhook subscription
- Check that payload is not modified before verification

### InFlow API Authentication Errors

- Verify `INFLOW_API_KEY` and `INFLOW_COMPANY_ID` are correct
- Check API key permissions in InFlow

### Email Notifications Not Sending

- Verify Outlook API credentials
- Check Azure AD app permissions (Mail.Send)
- Ensure admin emails are configured

### Validation Not Running

- Check that validators are registered in `app/main.py`
- Review console logs for errors
- Test manual validation endpoint

## Documentation

All project documentation is available in the `docs/` directory:

- **[Quick Start Guide](docs/QUICKSTART.md)** - Step-by-step setup instructions
- **[Implementation Plan](docs/plan.md)** - Detailed phase-by-phase plan
- **[Requirements](docs/requirement.md)** - Original project requirements
- **[Phase 0 Summary](docs/PHASE0_COMPLETE.md)** - Foundation completion details
- **[Implementation Status](docs/IMPLEMENTATION_STATUS.md)** - Current progress tracking
- **[Project Summary](docs/PROJECT_SUMMARY.md)** - Executive overview
- **[API Integration Guide](docs/API-Integration-Guide.md)** - InFlow API details
- **[Microsoft Graph Setup](docs/Microsoft-Graph-Setup.md)** - Outlook/OneDrive configuration

## Support

For issues or questions, contact the development team or refer to the project documentation in `docs/`.

