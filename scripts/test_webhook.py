#!/usr/bin/env python3
"""
Script to test webhook endpoint locally with sample data.

Usage:
    python scripts/test_webhook.py [order_id]
"""

import sys
import os
import json
import hmac
import hashlib
import base64
import requests

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.config import config


def test_webhook(order_id: str = "test-order-123"):
    """
    Send a test webhook request to the local server.
    
    Args:
        order_id: The order ID to test with
    """
    # Prepare test payload
    payload = {
        "event": "salesOrder.updated",
        "data": {
            "salesOrderId": order_id
        },
        "timestamp": "2025-10-28T12:00:00Z"
    }
    
    payload_json = json.dumps(payload)
    payload_bytes = payload_json.encode('utf-8')
    
    # Generate HMAC signature
    if config.WEBHOOK_SECRET:
        secret_key = config.WEBHOOK_SECRET.encode('utf-8')
        signature = hmac.new(secret_key, payload_bytes, hashlib.sha256).digest()
        signature_b64 = base64.b64encode(signature).decode('utf-8')
    else:
        print("Warning: WEBHOOK_SECRET not set in .env")
        signature_b64 = "invalid-signature-for-testing"
    
    # Send request
    url = "http://localhost:5000/webhook/inflow"
    headers = {
        "Content-Type": "application/json",
        "x-inflow-hmac-sha256": signature_b64
    }
    
    print(f"Sending test webhook to {url}")
    print(f"Order ID: {order_id}")
    print(f"Payload: {payload_json}")
    print()
    
    try:
        response = requests.post(url, data=payload_bytes, headers=headers)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        print()
        
        if response.status_code == 200:
            print("Test successful!")
        else:
            print("Test failed!")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server.")
        print("Make sure the Flask server is running (python app/main.py)")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    order_id = sys.argv[1] if len(sys.argv) > 1 else "test-order-123"
    test_webhook(order_id)

