#!/usr/bin/env python3
"""
Script to subscribe to InFlow webhooks.

Usage:
    python scripts/subscribe_webhook.py <ngrok_url>

Example:
    python scripts/subscribe_webhook.py https://abc123.ngrok.io
"""

import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.clients.inflow_client import inflow_client


def subscribe_webhook(ngrok_url: str):
    """
    Subscribe to InFlow webhooks for sales order events.
    
    Args:
        ngrok_url: The ngrok HTTPS URL (e.g., https://abc123.ngrok.io)
    """
    # Ensure URL doesn't end with /
    ngrok_url = ngrok_url.rstrip('/')
    
    webhook_url = f"{ngrok_url}/webhook/inflow"
    
    print(f"Subscribing to InFlow webhooks...")
    print(f"Webhook URL: {webhook_url}")
    print()
    
    try:
        result = inflow_client.subscribe_webhook(
            webhook_url=webhook_url,
            events=['salesOrder.created', 'salesOrder.updated']
        )
        
        print("Webhook subscription successful!")
        print()
        print(f"Webhook Subscription ID: {result['webHookSubscriptionId']}")
        print(f"Secret Key: {result['secret']}")
        print()
        print("IMPORTANT: Add this to your .env file:")
        print(f"WEBHOOK_SECRET={result['secret']}")
        print()
        print("Then restart your Flask server.")
        
    except Exception as e:
        print(f"Error subscribing to webhook: {e}")
        sys.exit(1)


def list_webhooks():
    """
    List all current webhook subscriptions.
    """
    print("Fetching current webhook subscriptions...")
    print()
    
    try:
        webhooks = inflow_client.list_webhooks()
        
        if not webhooks:
            print("No webhook subscriptions found.")
        else:
            print(f"Found {len(webhooks)} webhook subscription(s):")
            print()
            for i, webhook in enumerate(webhooks, 1):
                print(f"{i}. Webhook ID: {webhook['webHookSubscriptionId']}")
                print(f"   URL: {webhook['url']}")
                print(f"   Events: {', '.join(webhook['events'])}")
                print()
    
    except Exception as e:
        print(f"Error listing webhooks: {e}")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} <ngrok_url>     - Subscribe to webhook")
        print(f"  {sys.argv[0]} --list          - List current webhooks")
        print()
        print("Example:")
        print(f"  {sys.argv[0]} https://abc123.ngrok.io")
        sys.exit(1)
    
    if sys.argv[1] == '--list':
        list_webhooks()
    else:
        ngrok_url = sys.argv[1]
        subscribe_webhook(ngrok_url)

