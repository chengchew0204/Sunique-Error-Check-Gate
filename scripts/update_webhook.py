#!/usr/bin/env python3
"""
Update InFlow webhook subscription with production URL.

Usage:
    python scripts/update_webhook.py <production_url>

Example:
    python scripts/update_webhook.py https://abc123.execute-api.us-east-1.amazonaws.com/prod
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.clients.inflow_client import inflow_client


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/update_webhook.py <production_url>")
        print("Example: python scripts/update_webhook.py https://abc123.execute-api.us-east-1.amazonaws.com/prod")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    webhook_url = f"{base_url}/webhook/inflow"
    
    print("="*60)
    print("InFlow Webhook Update")
    print("="*60)
    print(f"\nProduction URL: {webhook_url}")
    print(f"\nCompany ID: {inflow_client.company_id}")
    print("\n" + "="*60)
    
    # Confirm with user
    response = input("\nContinue with webhook subscription? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Aborted.")
        sys.exit(0)
    
    print("\n📡 Subscribing to InFlow webhook...")
    
    try:
        # Subscribe to webhook
        result = inflow_client.subscribe_webhook(
            webhook_url=webhook_url,
            events=['SalesOrderCreatedV1', 'SalesOrderUpdatedV1']
        )
        
        print("\n" + "="*60)
        print("✅ Webhook Subscription Successful!")
        print("="*60)
        print(f"\nWebhook ID: {result.get('webHookSubscriptionId')}")
        print(f"Secret: {result.get('secret')}")
        print(f"URL: {result.get('url')}")
        print(f"Events: {result.get('events')}")
        
        print("\n" + "="*60)
        print("IMPORTANT: Update your production environment!")
        print("="*60)
        print("\nFor AWS Lambda:")
        print(f"  serverless deploy function -f webhook --stage prod \\")
        print(f"    --param='WEBHOOK_SECRET={result.get('secret')}'")
        print("\nOr update your .env file and redeploy:")
        print(f"  WEBHOOK_SECRET={result.get('secret')}")
        print("\n" + "="*60)
        
        # Save to file for reference
        with open('webhook_subscription.txt', 'w') as f:
            f.write(f"Webhook ID: {result.get('webHookSubscriptionId')}\n")
            f.write(f"Secret: {result.get('secret')}\n")
            f.write(f"URL: {result.get('url')}\n")
            f.write(f"Events: {result.get('events')}\n")
        
        print("\n💾 Subscription details saved to: webhook_subscription.txt")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

