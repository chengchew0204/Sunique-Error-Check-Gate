# Error Check Gate Implementation Plan

## Architecture Overview

Python webhook server (Flask/FastAPI) that:
- Receives InFlow webhooks for `salesOrder.created` and `salesOrder.updated`
- Verifies HMAC signature for security
- Fetches full order data from InFlow API
- Runs 5 validation rules
- Logs results to JSON/CSV
- Sends email notifications via Outlook API for failures
- Deploys locally with ngrok (dev) and as serverless function (production)

## Development Strategy

**Incremental Feature-by-Feature Implementation**: Each validation rule will be fully implemented, tested with real InFlow data via ngrok, and verified before proceeding to the next feature.

## Project Structure

```
04-error-check-gate/
├── app/
│   ├── main.py                 # Flask webhook server
│   ├── config.py               # Configuration and settings
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── base.py                   # Base validator class
│   │   ├── rule-0-order_fetcher.py   # Rule 0: Order data fetcher
│   │   ├── rule-1-discount.py        # Rule 1: Discount validation (includes TUK and Z items)
│   │   ├── rule-2-credit_card.py     # Rule 2: Credit card fee validation
│   │   ├── rule-3-assembly_fee.py    # Rule 3: Assembly fee validation
│   │   ├── rule-4-delivery_fee.py    # Rule 4: Delivery fee validation
│   │   └── rule-finalizer.py         # Final step: Notification & processing
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── inflow_client.py   # InFlow API client
│   │   ├── onedrive_client.py # OneDrive API client
│   │   └── outlook_client.py  # Outlook API for emails
│   ├── services/
│   │   ├── __init__.py
│   │   ├── validation_service.py  # Orchestrates validation
│   │   ├── notification_service.py # Email notification logic
│   │   └── logger_service.py      # JSON/CSV logging
│   └── utils/
│       ├── __init__.py
│       └── hmac_verifier.py   # Webhook HMAC verification
├── logs/                      # JSON/CSV validation logs
├── tests/                     # Unit tests
├── serverless/
│   ├── handler.py            # AWS Lambda/Azure Functions handler
│   └── serverless.yml        # Deployment config
├── requirements.txt
├── .env.example
├── README.md
└── ngrok-config.yml          # ngrok configuration
```

## Implementation Phases

### Phase 0: Foundation Setup ✅

**Completed:**
- Created project structure and directories
- Installed dependencies (Flask, requests, openpyxl, pandas, msal, python-dotenv)
- Set up configuration management in `config.py`
- Implemented webhook server (`app/main.py`) with HMAC verification
- Built InFlow API client (`app/clients/inflow_client.py`) with authentication
- Created Outlook API client (`app/clients/outlook_client.py`) for emails
- Created OneDrive API client (`app/clients/onedrive_client.py`) for file access
- Implemented base validator class (`app/validators/base.py`)
- Implemented logger service for JSON/CSV logging
- Implemented notification service with email templates
- Created validation service orchestrator
- Set up ngrok configuration
- Created README and setup documentation
- Created serverless deployment templates

**Testing**: Ready to verify webhook receives InFlow events, HMAC validation works, and can fetch order data from InFlow API

**Next Steps for Testing Phase 0:**
1. Create `.env` file with actual credentials
2. Run setup script: `bash setup.sh`
3. Start Flask server: `python app/main.py`
4. Start ngrok: `ngrok http 5000`
5. Subscribe to InFlow webhooks using ngrok URL
6. Create or update a test sales order in InFlow
7. Verify webhook is received and order data is fetched
8. Check console logs for successful processing

---

### Phase 1: Feature 1 - Discount Validation

**Implementation** (`app/validators/rule-1-discount.py`):
- Fetch customer discount rules from InFlow API
- Compare applied discount vs. allowed range for each line item
- Flag "Excessive Discount" error if discount exceeds limit
- Return validation result with suggested fixes

**Integration**:
- Register discount validator in `app/main.py`
- Log results to JSON/CSV
- Send email notification if errors found

**Testing**:
- Create test sales orders in InFlow with various discount scenarios:
  - Order with normal discount (should pass)
  - Order with excessive discount (should fail)
  - Order with no discount (should pass)
- Verify correct detection of excessive discounts
- Confirm email notifications sent to admins + account manager
- Review logs for accuracy in `logs/` directory

**Go/No-Go**: Only proceed to Phase 2 after full verification

---

### Phase 2: Feature 2 - Credit Card Fee Validation

**Implementation** (`app/validators/rule-2-credit_card.py`):
- Check payment method in order metadata
- For credit card payments on paid orders, verify 3% fee line item exists
- Calculate expected fee: `subtotal * 0.03`
- Flag "Credit Card Fee Missing or Incorrect" error
- Return validation result with suggested fixes

**Integration**:
- Register credit card fee validator in `app/main.py`
- Update logging and email templates

**Testing**:
- Create test orders with payment scenarios:
  - Paid order with credit card and correct fee (should pass)
  - Paid order with credit card but missing fee (should fail)
  - Paid order with credit card but incorrect fee amount (should fail)
  - Paid order with cash/other payment method (should pass/skip)
  - Unpaid order (should pass/skip)
- Verify correct fee calculation and detection
- Confirm notifications and logs

**Go/No-Go**: Only proceed to Phase 3 after full verification

---

### Phase 3: Feature 3 - Assembly Fee Validation

**Implementation** (`app/validators/rule-3-assembly_fee.py`):
- Locate "Assembly Fee" line item in order
- Validate amount matches business logic formula (define in config)
- Ensure no discount applied to assembly fee
- Flag "Invalid Assembly Fee" error if violations found
- Return validation result with suggested fixes

**Integration**:
- Register assembly fee validator in `app/main.py`
- Update logging and email templates

**Testing**:
- Define assembly fee calculation formula in business requirements
- Create test orders with assembly fee scenarios:
  - Order with correct assembly fee, no discount (should pass)
  - Order with incorrect assembly fee amount (should fail)
  - Order with discounted assembly fee (should fail)
  - Order without assembly fee (depends on business rules)
- Verify detection logic and calculation accuracy
- Confirm notifications and logs

**Go/No-Go**: Only proceed to Phase 4 after full verification

---

### Phase 4: Feature 4 - Delivery Fee Validation

**Implementation** (`app/validators/rule-4-delivery_fee.py`):
- Integrate OneDrive client to download "Delivery Record Form.xlsx"
- Parse Excel file to extract order numbers and dates
- Detect duplicate order numbers on same date (flag error)
- Check if freight fee line item exists when order is in delivery record
- Flag "Delivery Fee Missing" or "Duplicate Delivery Record" error
- Return validation result with suggested fixes
- Implement file caching to reduce API calls (5-minute TTL)

**Integration**:
- Register delivery fee validator in `app/main.py`
- Update logging and email templates

**Testing**:
- Prepare test delivery records in OneDrive Excel file
- Create test order scenarios:
  - Order in delivery record with freight fee (should pass)
  - Order in delivery record without freight fee (should fail)
  - Order not in delivery record (should pass/skip)
  - Duplicate order number in delivery record (should fail)
- Verify Excel parsing, caching works correctly
- Test cache expiration (wait 5+ minutes)
- Confirm notifications and logs

**Go/No-Go**: Only proceed to deployment after full verification

---

### Phase 6: Production Deployment

**Tasks:**
- Create serverless handler wrapper (already created in `serverless/handler.py`)
- Choose deployment platform (AWS Lambda or Azure Functions)
- Package application with dependencies
- Configure production environment variables
- Deploy to serverless platform
- Update InFlow webhook subscription URL to production endpoint
- Configure CloudWatch/Azure Monitor logging and alerts
- Perform end-to-end production testing
- Document deployment and maintenance procedures
- Set up monitoring dashboards
- Configure backup and disaster recovery

**Testing:**
- Test production webhook endpoint with real InFlow events
- Verify all 5 validation rules work correctly in production
- Test email notifications from production
- Verify logs are being stored correctly
- Load test with multiple concurrent webhooks
- Test error handling and recovery

---

## Key Configuration Items

**Environment Variables (.env)**
- `INFLOW_API_KEY`, `INFLOW_COMPANY_ID`
- `ONEDRIVE_CLIENT_ID`, `ONEDRIVE_CLIENT_SECRET`, `ONEDRIVE_TENANT_ID`
- `OUTLOOK_CLIENT_ID`, `OUTLOOK_CLIENT_SECRET`, `OUTLOOK_TENANT_ID`
- `WEBHOOK_SECRET` (from InFlow webhook subscription)
- `ADMIN_EMAILS` (comma-separated list)
- `DELIVERY_RECORD_FILE_PATH` (OneDrive file path/ID)

**Business Logic Config (config.py)**
- Assembly fee calculation formula
- Credit card fee percentage (3%)
- Delivery record Excel sheet name and column mappings
- TUK identification patterns

## Dependencies (requirements.txt)

```
flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
openpyxl==3.1.2
pandas==2.1.3
msal==1.26.0
gunicorn==21.2.0
```

## Current Status

**Phase 0: COMPLETED ✅**

All foundation components have been implemented:
- Project structure created
- All core services implemented
- Webhook server ready
- API clients ready
- Logging and notification services ready
- Validator base classes ready
- Documentation complete

**Next Action: Begin Phase 0 Testing**

Follow the testing steps outlined in Phase 0 to verify the foundation is working correctly before implementing Phase 1 (Discount Validation).

