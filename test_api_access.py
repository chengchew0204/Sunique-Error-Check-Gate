#!/usr/bin/env python3
"""
Test if we can access InFlow API at all with the current credentials.
"""
import requests

API_KEY = 'F3ACB9920EF7786F4664373E1DF6F865C20F93302FFC75543E93F5BC3A7E8738-1'
COMPANY_ID = '8963ca96-7ab5-4a29-b4b5-46935ed4e989'
BASE_URL = 'https://cloudapi.inflowinventory.com'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json;version=2025-06-24'
}

print("Testing InFlow API Access...")
print(f"Company ID: {COMPANY_ID}")
print("="*60)

# Test 1: List sales orders
print("\nTest 1: List sales orders (GET /salesorders)")
url = f"{BASE_URL}/{COMPANY_ID}/salesorders?limit=5"
response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")
print()

if response.status_code != 200:
    # Try with different endpoint format
    print("Test 2: Try /sales-orders instead...")
    url = f"{BASE_URL}/{COMPANY_ID}/sales-orders?limit=5"
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
    print()

# Test 3: Try to get the specific order that failed (with hyphen!)
print("Test 3: Get specific order with correct endpoint...")
order_id = "566b2161-283e-4a67-b338-b7b312d7f06f"
url = f"{BASE_URL}/{COMPANY_ID}/sales-orders/{order_id}"
response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")
print()

# Test 4: Check if we need different path
print("Test 4: List webhooks to verify company ID...")
url = f"{BASE_URL}/{COMPANY_ID}/webhooks"
response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")
print()

if response.status_code == 200:
    import json
    webhooks = response.json()
    print(f"Found {len(webhooks)} webhook(s)")
    for wh in webhooks:
        print(f"  - Webhook ID: {wh.get('webHookSubscriptionId')}")
        print(f"    URL: {wh.get('url')}")
        print(f"    Events: {wh.get('events')}")