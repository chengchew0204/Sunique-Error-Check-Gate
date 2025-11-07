# InFlow API Integration Guide

This guide explains how to integrate with the InFlow API for the Error Check Gate system.

## Authentication

InFlow uses Bearer token authentication. Include your API key in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
```

## Base URL

```
https://api.inflow.com/v1/{companyId}
```

## Key Endpoints Used

### Get Sales Order

```
GET /{companyId}/salesorders/{salesOrderId}
```

**Response Structure:**
```json
{
  "salesOrderId": "uuid",
  "orderNumber": "SO-12345",
  "customer": {
    "customerId": "uuid",
    "name": "Customer Name",
    "email": "customer@example.com"
  },
  "lineItems": [
    {
      "lineItemId": "uuid",
      "product": {
        "productId": "uuid",
        "name": "Product Name",
        "sku": "SKU-123"
      },
      "quantity": 10,
      "unitPrice": 100.00,
      "discount": 5.00,
      "discountPercent": 5.0,
      "total": 950.00
    }
  ],
  "subtotal": 950.00,
  "tax": 95.00,
  "total": 1045.00,
  "status": "Open",
  "paymentMethod": "Credit Card",
  "paid": false,
  "customFields": []
}
```

### Get Customer

```
GET /{companyId}/customers/{customerId}
```

**Response Structure:**
```json
{
  "customerId": "uuid",
  "name": "Customer Name",
  "email": "customer@example.com",
  "discountPercent": 10.0,
  "customFields": []
}
```

### Get Product

```
GET /{companyId}/products/{productId}
```

**Response Structure:**
```json
{
  "productId": "uuid",
  "name": "Product Name",
  "sku": "SKU-123",
  "category": "Category Name",
  "unitPrice": 100.00,
  "customFields": []
}
```

## Webhooks

### Subscribe to Webhook

```
PUT /{companyId}/webhooks
```

**Request Body:**
```json
{
  "url": "https://your-domain.com/webhook/inflow",
  "events": [
    "salesOrder.created",
    "salesOrder.updated"
  ],
  "webHookSubscriptionId": "uuid",
  "webHookSubscriptionRequestId": "uuid"
}
```

**Response:**
```json
{
  "webHookSubscriptionId": "uuid",
  "url": "https://your-domain.com/webhook/inflow",
  "events": ["salesOrder.created", "salesOrder.updated"],
  "secret": "base64-encoded-secret-key"
}
```

**Important:** Save the `secret` key for HMAC verification.

### Webhook Payload

When a sales order event occurs, InFlow sends:

```json
{
  "event": "salesOrder.updated",
  "data": {
    "salesOrderId": "uuid"
  },
  "timestamp": "2025-10-28T12:00:00Z"
}
```

**Headers:**
- `Content-Type: application/json`
- `x-inflow-hmac-sha256: base64-encoded-signature`

### HMAC Verification

To verify webhook authenticity:

1. Get the raw request body (bytes)
2. Get the `x-inflow-hmac-sha256` header
3. Calculate HMAC-SHA256 using the webhook secret
4. Base64-encode the calculated HMAC
5. Compare with the header value using constant-time comparison

**Python Example:**
```python
import hmac
import hashlib
import base64

secret = webhook_secret.encode('utf-8')
payload = request.get_data()  # Raw bytes
signature_header = request.headers.get('x-inflow-hmac-sha256')

# Calculate HMAC
calculated_hmac = hmac.new(secret, payload, hashlib.sha256).digest()
expected_signature = base64.b64decode(signature_header)

# Verify
is_valid = hmac.compare_digest(calculated_hmac, expected_signature)
```

## Rate Limiting

InFlow API may implement rate limiting. The client handles:

- **429 Too Many Requests**: Automatic retry with backoff
- **Retry-After header**: Respect the suggested wait time
- **Exponential backoff**: For other errors

## Error Handling

Common HTTP status codes:

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Invalid or missing API key
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Best Practices

1. **Cache API responses** when appropriate (customer data, product data)
2. **Implement retry logic** with exponential backoff
3. **Verify HMAC signatures** for all webhook requests
4. **Log all API interactions** for debugging
5. **Monitor rate limits** and adjust request frequency
6. **Use batch operations** when available to reduce API calls

## Testing

### Test with InFlow Sandbox

If available, use InFlow's sandbox environment for testing:

```
INFLOW_API_BASE_URL=https://sandbox-api.inflow.com/v1
```

### Manual API Testing

Use curl to test API endpoints:

```bash
curl -X GET "https://api.inflow.com/v1/{companyId}/salesorders/{orderId}" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

### Webhook Testing

Use the provided test script:

```bash
python scripts/test_webhook.py <order_id>
```

Or use tools like:
- **ngrok**: Expose local server
- **Postman**: Send test webhook requests
- **curl**: Manual webhook testing

## Additional Resources

- InFlow API Documentation: [Official Docs]
- Webhook Testing Tools: ngrok, RequestBin, Webhook.site
- HMAC Verification: [RFC 2104](https://tools.ietf.org/html/rfc2104)

