#!/usr/bin/env python3
"""
Simple script to view pending errors in DynamoDB.
"""

import sys
import os
from datetime import datetime

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.dynamodb_error_tracker import DynamoDBErrorTracker

def view_pending_errors():
    """
    View all pending errors from DynamoDB table.
    """
    print("=" * 80)
    print("PENDING ERRORS IN DYNAMODB")
    print("=" * 80)
    print()
    
    try:
        tracker = DynamoDBErrorTracker()
        
        # Get all items from table
        response = tracker.table.scan()
        items = response.get('Items', [])
        
        if not items:
            print("✅ No pending errors currently tracked!")
            print()
            print("This means:")
            print("  - All orders are passing validation, OR")
            print("  - All errors are within 30-minute grace period and haven't expired yet, OR")
            print("  - All expired errors have been notified and removed")
            print()
            return
        
        print(f"Found {len(items)} pending error(s):\n")
        
        # Display each error
        for idx, item in enumerate(items, 1):
            order_id = item.get('order_id', 'Unknown')
            order_number = item.get('order_number', 'N/A')
            error_hash = item.get('error_hash', 'Unknown')
            first_detected = item.get('first_detected', 'Unknown')
            error_details = item.get('error_details', {})
            
            # Calculate age
            try:
                detected_time = datetime.fromisoformat(first_detected)
                age = datetime.utcnow() - detected_time
                age_minutes = age.total_seconds() / 60
            except:
                age_minutes = 0
            
            print(f"{idx}. Order: {order_number} (ID: {order_id})")
            print(f"   Error Hash: {error_hash}")
            print(f"   First Detected: {first_detected}")
            print(f"   Age: {age_minutes:.1f} minutes")
            print(f"   Rule: {error_details.get('rule', 'Unknown')}")
            print(f"   Message: {error_details.get('message', 'Unknown')}")
            print(f"   Severity: {error_details.get('severity', 'Unknown')}")
            
            # Status
            if age_minutes < 30:
                remaining = 30 - age_minutes
                print(f"   Status: ⏳ PENDING ({remaining:.1f} minutes until notification)")
            else:
                print(f"   Status: ⚠️  EXPIRED (should be notified soon)")
            
            print()
        
        print("=" * 80)
        print(f"Total Pending Errors: {len(items)}")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error accessing DynamoDB: {e}")
        import traceback
        traceback.print_exc()


def view_expired_errors():
    """
    View only errors that have exceeded the grace period.
    """
    print("=" * 80)
    print("EXPIRED ERRORS (Ready for Notification)")
    print("=" * 80)
    print()
    
    try:
        tracker = DynamoDBErrorTracker()
        expired = tracker.get_all_expired_errors(grace_period_minutes=30)
        
        if not expired:
            print("✅ No expired errors found!")
            print("All errors are either within grace period or have been notified.")
            print()
            return
        
        print(f"Found {len(expired)} expired error(s):\n")
        
        for idx, error in enumerate(expired, 1):
            print(f"{idx}. Order: {error['order_number']} (ID: {error['order_id']})")
            print(f"   Age: {error['age_minutes']:.1f} minutes")
            print(f"   Rule: {error['error_details'].get('rule', 'Unknown')}")
            print(f"   Message: {error['error_details'].get('message', 'Unknown')}")
            print(f"   Action: Will be notified on next errorMonitor run")
            print()
        
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='View pending errors in DynamoDB')
    parser.add_argument('--expired', action='store_true', 
                       help='Show only expired errors (> 30 min)')
    
    args = parser.parse_args()
    
    if args.expired:
        view_expired_errors()
    else:
        view_pending_errors()

