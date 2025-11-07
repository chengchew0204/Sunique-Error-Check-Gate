# InFlow Webhook API Documentation

## Overview

InFlow provides webhooks to receive real-time notifications when entities are created or updated in your account.

## Webhook Events

Available events:
- `customer.created` - New customer created
- `customer.updated` - Customer information updated
- `vendor.created` - New vendor created
- `vendor.updated` - Vendor information updated
- `purchaseOrder.created` - New purchase order created
- `purchaseOrder.updated` - Purchase order updated
- `salesOrder.created` - New sales order created ✅ (Used by Error Check Gate)
- `salesOrder.updated` - Sales order updated ✅ (Used by Error Check Gate)
- `product.created` - New product created
- `product.updated` - Product information updated

## Security

All webhook requests include a `x-inflow-hmac-sha256` header containing a base64-encoded HMAC-SHA256 signature. This signature is generated using:
- The webhook subscription's secret key
- The request body (raw bytes)

You should verify this signature to ensure the request came from InFlow.

### HMAC Verification Algorithm

```python
import hmac
import hashlib
import base64

# Get the raw request body and signature header
payload = request.get_data()  # Raw bytes
signature_header = request.headers.get('x-inflow-hmac-sha256')

# Decode the signature from base64
expected_signature = base64.b64decode(signature_header)

# Calculate the HMAC using your secret key
secret_key = YOUR_WEBHOOK_SECRET.encode('utf-8')
calculated_hmac = hmac.new(secret_key, payload, hashlib.sha256).digest()

# Compare using constant-time comparison
is_valid = hmac.compare_digest(calculated_hmac, expected_signature)
```

## Webhook Subscription Management

### List All Webhooks

**Endpoint:** `GET /{companyId}/webhooks`

**Response:**
```json
[
  {
    "webHookSubscriptionId": "uuid",
    "url": "https://your-domain.com/webhook/inflow",
    "events": ["salesOrder.created", "salesOrder.updated"],
    "secret": "secret-key-only-shown-at-creation"
  }
]
```

### Subscribe to Webhook

**Endpoint:** `PUT /{companyId}/webhooks`

**Request:**
```json
{
  "url": "https://your-domain.com/webhook/inflow",
"events": [
    "salesOrder.created",
    "salesOrder.updated"
  ],
  "webHookSubscriptionId": "generated-uuid",
  "webHookSubscriptionRequestId": "generated-uuid"
}
```

**Response:**
```json
{
  "webHookSubscriptionId": "generated-uuid",
  "url": "https://your-domain.com/webhook/inflow",
  "events": ["salesOrder.created", "salesOrder.updated"],
  "secret": "base64-encoded-secret-key"
}
```

**Important:** The `secret` is only returned when creating the subscription. Save it securely.

### Get Webhook Details

**Endpoint:** `GET /{companyId}/webhooks/{webHookId}`

**Response:**
```json
{
  "webHookSubscriptionId": "uuid",
  "url": "https://your-domain.com/webhook/inflow",
  "events": ["salesOrder.created", "salesOrder.updated"]
}
```

Note: Secret is not included in GET responses.

### Unsubscribe from Webhook

**Endpoint:** `DELETE /{companyId}/webhooks/{webHookId}`

**Response:** `200 OK`

## Webhook Payload

When an event occurs, InFlow sends a POST request to your webhook URL.

### Request Headers

```
Content-Type: application/json
x-inflow-hmac-sha256: base64-encoded-signature
```

### Request Body

```json
{
  "event": "salesOrder.updated",
  "data": {
    "salesOrderId": "uuid-of-the-sales-order"
  },
  "timestamp": "2025-10-28T12:00:00Z"
}
```

### Payload Fields

- `event` (string): The event type that triggered the webhook
- `data` (object): Event-specific data
  - For sales orders: Contains `salesOrderId`
- `timestamp` (string): ISO 8601 timestamp when the event occurred

## Handling Webhooks

### Best Practices

1. **Verify HMAC Signature** - Always verify before processing
2. **Respond Quickly** - Return 200 OK immediately, process asynchronously
3. **Fetch Full Data** - Webhook contains only ID, fetch full data via API
4. **Handle Retries** - InFlow may retry failed webhooks
5. **Log Everything** - Log all webhook requests for debugging
6. **Idempotency** - Handle duplicate webhooks gracefully

### Example Implementation

```python
@app.route('/webhook/inflow', methods=['POST'])
def inflow_webhook():
    # Get payload and signature
    payload = request.get_data()
    signature = request.headers.get('x-inflow-hmac-sha256')
    
    # Verify HMAC
    if not verify_hmac(payload, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    # Parse webhook data
    webhook_data = json.loads(payload)
    event_type = webhook_data.get('event')
    
    # Process only relevant events
    if event_type in ['salesOrder.created', 'salesOrder.updated']:
        sales_order_id = webhook_data['data']['salesOrderId']
        
        # Respond immediately
        # Process asynchronously in background
        process_order_async(sales_order_id)
    
    return jsonify({'status': 'received'}), 200
```

## Webhook Delivery

### Retry Policy

InFlow will retry failed webhook deliveries:
- Initial attempt immediately
- Retries with exponential backoff
- Maximum retry attempts: (varies by InFlow configuration)

### Expected Response

Your endpoint should return:
- Status code: `200` or `202`
- Response time: < 30 seconds (recommended < 5 seconds)

### Failure Scenarios

InFlow considers a webhook failed if:
- Response status code is not 2xx
- Request times out (typically 30 seconds)
- Connection error occurs

## Testing Webhooks

### Local Development with ngrok

1. Start your local server:
   ```bash
   python app/main.py
   ```

2. Expose with ngrok:
   ```bash
   ngrok http 5000
   ```

3. Subscribe using ngrok URL:
   ```bash
   python scripts/subscribe_webhook.py https://abc123.ngrok.io
   ```

4. Create or update a sales order in InFlow

5. Watch your server logs for incoming webhooks

### Manual Testing

Send a test webhook request:

```bash
python scripts/test_webhook.py <order_id>
```

Or use curl:

```bash
curl -X POST http://localhost:5000/webhook/inflow \
  -H "Content-Type: application/json" \
  -H "x-inflow-hmac-sha256: <calculated-signature>" \
  -d '{
    "event": "salesOrder.updated",
    "data": {"salesOrderId": "test-order-123"},
    "timestamp": "2025-10-28T12:00:00Z"
  }'
```

## Troubleshooting

### Webhooks Not Received

**Possible causes:**
- Webhook subscription not active
- URL not accessible (firewall, ngrok expired)
- InFlow service issues

**Solutions:**
1. Verify subscription: `python scripts/subscribe_webhook.py --list`
2. Test endpoint: `curl http://your-url/webhook/inflow`
3. Check InFlow service status

### Invalid Signature Errors

**Possible causes:**
- Wrong webhook secret
- Modified request body before verification
- Incorrect HMAC calculation

**Solutions:**
1. Verify `WEBHOOK_SECRET` matches subscription secret
2. Use raw request body for HMAC calculation
3. Check base64 encoding/decoding

### Timeouts

**Possible causes:**
- Slow processing in webhook handler
- Synchronous API calls blocking response
- Database queries taking too long

**Solutions:**
1. Return 200 OK immediately
2. Process webhook asynchronously (queue, background task)
3. Optimize API calls and database queries

## Monitoring

Monitor webhook health:
- Response time percentiles (p50, p95, p99)
- Error rate
- Retry rate
- Processing time

Set up alerts for:
- High error rate (> 5%)
- Slow response times (> 5 seconds)
- Missing webhooks (compare with InFlow events)

## Security Considerations

1. **Always verify HMAC** - Never trust webhook without verification
2. **Use HTTPS** - Webhook URL must be HTTPS in production
3. **Rotate secrets** - Periodically create new webhook subscriptions
4. **Rate limiting** - Implement rate limiting on webhook endpoint
5. **Audit logs** - Log all webhook requests for security audit

## Additional Resources

- [InFlow API Documentation](https://api.inflow.com/docs)
- [HMAC Authentication RFC](https://tools.ietf.org/html/rfc2104)
- [Webhook Security Best Practices](https://webhooks.dev)
