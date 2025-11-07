#!/usr/bin/env python3
"""
Simple runner script for the InFlow Error Check Gate application.
Run this from the project root directory.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import and run the app
from app.main import app, initialize_validators, config

if __name__ == '__main__':
    # Validate basic configuration first
    try:
        config.validate_basic()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nPlease check your .env file and ensure all required variables are set:")
        print("- INFLOW_API_KEY")
        print("- INFLOW_COMPANY_ID")
        sys.exit(1)
    
    # Check for WEBHOOK_SECRET and warn if missing
    if not config.WEBHOOK_SECRET:
        print("\n" + "="*60)
        print("⚠️  WARNING: WEBHOOK_SECRET not set yet")
        print("="*60)
        print("\nThis is OK for initial setup. Follow these steps:")
        print("\n1. Keep this server running")
        print("2. In another terminal, start ngrok:")
        print("   ngrok http 8000")
        print("\n3. Copy the HTTPS URL from ngrok")
        print("\n4. Subscribe to InFlow webhooks:")
        print("   python scripts/subscribe_webhook.py https://YOUR-NGROK-URL.ngrok-free.app")
        print("\n5. Copy the WEBHOOK_SECRET to your .env file")
        print("6. Restart this server")
        print("\n" + "="*60 + "\n")
    
    # Initialize validators
    initialize_validators()
    
    # Run Flask app
    print(f"Starting InFlow Error Check Gate on port {config.FLASK_PORT}")
    app.run(
        host='0.0.0.0',
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )

