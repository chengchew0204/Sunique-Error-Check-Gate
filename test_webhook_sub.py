#!/usr/bin/env python3
"""
Direct test of webhook subscription to debug the issue.
"""
import requests
import uuid
import json

# Your credentials
API_KEY = 'F3ACB9920EF7786F4664373E1DF6F865C20F93302FFC75543E93F5BC3A7E8738-1'
COMPANY_ID = '8963ca96-7ab5-4a29-b4b5-46935ed4e989'
BASE_URL = 'https://cloudapi.inflowinventory.com'
WEBHOOK_URL = 'https://inertial-enterally-lavon.ngrok-free.dev/webhook/inflow'

# Prepare the payload
payload = {
    "url": WEBHOOK_URL,
    "events": ["salesOrder.created", "salesOrder.updated"],
    "webHookSubscriptionId": str(uuid.uuid4()),
    "webHookSubscriptionRequestId": str(uuid.uuid4())
}

url = f"{BASE_URL}/{COMPANY_ID}/webhooks"

print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print()

# Try with json parameter (requests sets Content-Type automatically)
print("Attempt 1: Using json parameter...")
response = requests.put(
    url,
    json=payload,
    headers={
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
print()

if response.status_code != 200:
    # Try with explicit Content-Type
    print("Attempt 2: Using data parameter with explicit Content-Type...")
    response = requests.put(
        url,
        data=json.dumps(payload),
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print()

if response.status_code == 200:
    result = response.json()
    print("SUCCESS!")
    print(f"Webhook ID: {result.get('webHookSubscriptionId')}")
    print(f"Secret: {result.get('secret')}")
    print()
    print("Add this to your .env file:")
    print(f"WEBHOOK_SECRET={result.get('secret')}")
else:
    # Try with no Accept header
    print("Attempt 3: No Accept header...")
    response = requests.put(
        url,
        json=payload,
        headers={
            'Authorization': f'Bearer {API_KEY}'
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print()
    
    if response.status_code == 200:
        result = response.json()
        print("SUCCESS!")
        print(f"Webhook ID: {result.get('webHookSubscriptionId')}")
        print(f"Secret: {result.get('secret')}")
        print()
        print("Add this to your .env file:")
        print(f"WEBHOOK_SECRET={result.get('secret')}")
    else:
        # Try with vnd.api+json Accept header
        print("Attempt 4: Using application/vnd.api+json...")
        response = requests.put(
            url,
            json=payload,
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Accept': 'application/vnd.api+json'
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("\nSUCCESS!")
            print(f"Webhook ID: {result.get('webHookSubscriptionId')}")
            print(f"Secret: {result.get('secret')}")
            print()
            print("Add this to your .env file:")
            print(f"WEBHOOK_SECRET={result.get('secret')}")
        else:
            # Try with versioned Accept header (from working config!)
            print("\nAttempt 5: Using versioned Accept header...")
            response = requests.put(
                url,
                json=payload,
                headers={
                    'Authorization': f'Bearer {API_KEY}',
                    'Accept': 'application/json;version=2025-06-24'
                }
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print("\n🎉 SUCCESS!")
                print(f"Webhook ID: {result.get('webHookSubscriptionId')}")
                print(f"Secret: {result.get('secret')}")
                print()
                print("Add this to your .env file:")
                print(f"WEBHOOK_SECRET={result.get('secret')}")

