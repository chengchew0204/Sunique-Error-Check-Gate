#!/usr/bin/env python3
"""
Test script to verify email notifications are working.
This creates a fake expired error and triggers the notification.
"""

import sys
import os
from datetime import datetime, timedelta

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.notification_service import notification_service
from app.config import config

def test_email_notification():
    """
    Test email notification by creating a fake validation result.
    """
    print("=" * 60)
    print("TESTING EMAIL NOTIFICATION")
    print("=" * 60)
    print()
    
    # Check email configuration
    print("Email Configuration:")
    print(f"  - Testing Mode: {config.EMAIL_TESTING_MODE}")
    print(f"  - Test Recipient: {config.TEST_EMAIL_RECIPIENT}")
    print(f"  - From Address: {config.EMAIL_FROM_ADDRESS}")
    print(f"  - Admin Emails: {config.ADMIN_EMAILS}")
    print()
    
    # Create fake validation result with an error
    fake_validation_result = {
        'order_id': 'test-order-123',
        'order_number': 'TEST-SO-001',
        'timestamp': datetime.now().isoformat(),
        'status': 'failed',
        'confirmed_count': 1,
        'pending_count': 0,
        'issues': [
            {
                'rule': 'Discount Remark Validation',
                'severity': 'error',
                'message': 'Z_DISCOUNT item(s) found but order remarks are missing',
                'details': {
                    'discount_items': ['Z_DISCOUNT']
                },
                'tracking_status': 'confirmed',
                'error_age_minutes': 35.0
            }
        ],
        'suggested_fixes': [
            'Add order remarks explaining the discount reason'
        ]
    }
    
    # Fake order data
    fake_order_data = {
        'salesOrderId': 'test-order-123',
        'orderNumber': 'TEST-SO-001',
        'customer': {
            'name': 'Test Customer'
        },
        'total': 1000.00,
        'subtotal': 950.00
    }
    
    print("Fake Validation Result:")
    print(f"  - Order: {fake_validation_result['order_number']}")
    print(f"  - Status: {fake_validation_result['status']}")
    print(f"  - Issues: {len(fake_validation_result['issues'])}")
    print()
    
    # Send test email
    print("Sending test email notification...")
    print()
    
    try:
        notification_service.send_validation_failure_notification(
            fake_validation_result,
            fake_order_data
        )
        
        print("=" * 60)
        print("✅ TEST EMAIL SENT SUCCESSFULLY!")
        print("=" * 60)
        print()
        print(f"Check your inbox: {config.TEST_EMAIL_RECIPIENT if config.EMAIL_TESTING_MODE else config.ADMIN_EMAILS}")
        print()
        print("Expected subject: InFlow Order Validation Issues - TEST-SO-001")
        print()
        
    except Exception as e:
        print("=" * 60)
        print("❌ ERROR SENDING EMAIL")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        import traceback
        traceback.print_exc()
        print()
        print("Common issues:")
        print("  1. Outlook API credentials not configured")
        print("  2. Invalid client ID/secret/tenant ID")
        print("  3. Missing Microsoft Graph API permissions")
        print()


if __name__ == '__main__':
    test_email_notification()

