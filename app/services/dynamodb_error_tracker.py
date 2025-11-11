"""
DynamoDB-based error tracker service for persistent storage across Lambda invocations.
This replaces the file-based tracker to handle Lambda container recycling.
"""

import json
import boto3
from boto3.dynamodb.types import TypeSerializer
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, Any, List
import hashlib


class DynamoDBErrorTracker:
    """
    Service for tracking pending errors with 30-minute grace period using DynamoDB.
    Errors persist across Lambda container lifecycles.
    """
    
    def __init__(self, table_name: str = "inflow-pending-errors"):
        """
        Initialize the DynamoDB error tracker service.
        
        Args:
            table_name: Name of DynamoDB table for storing pending errors
        """
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
        self.table = self.dynamodb.Table(table_name)
        self.grace_period_minutes = 30
    
    def generate_error_hash(self, order_id: str, rule_name: str, 
                          message: str, details: Dict[str, Any]) -> str:
        """
        Generate a unique hash for an error.
        """
        hash_input = f"{order_id}:{rule_name}:{message}:{json.dumps(details, sort_keys=True)}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    def _convert_floats_to_decimals(self, obj: Any) -> Any:
        """
        Recursively convert all float values to Decimal for DynamoDB compatibility.
        """
        if isinstance(obj, float):
            return Decimal(str(obj))
        elif isinstance(obj, dict):
            return {k: self._convert_floats_to_decimals(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_floats_to_decimals(item) for item in obj]
        else:
            return obj
    
    def track_error(self, order_id: str, error_hash: str, 
                   error_data: Dict[str, Any], order_number: str = "") -> None:
        """
        Track a new error or update existing error timestamp.
        """
        now = datetime.utcnow()
        
        try:
            # Convert error_data floats to Decimals for DynamoDB
            error_data_clean = self._convert_floats_to_decimals(error_data)
            
            # Try to get existing error
            response = self.table.get_item(
                Key={'order_id': order_id, 'error_hash': error_hash}
            )
            
            if 'Item' in response:
                # Error already exists - update last_seen
                self.table.update_item(
                    Key={'order_id': order_id, 'error_hash': error_hash},
                    UpdateExpression='SET last_seen = :last_seen',
                    ExpressionAttributeValues={':last_seen': now.isoformat()}
                )
                print(f"Updated existing error: {error_hash}")
            else:
                # New error - add to table
                self.table.put_item(
                    Item={
                        'order_id': order_id,
                        'error_hash': error_hash,
                        'order_number': order_number,
                        'first_detected': now.isoformat(),
                        'last_seen': now.isoformat(),
                        'error_details': error_data_clean,
                        'ttl': int((now + timedelta(days=7)).timestamp())  # Auto-delete after 7 days
                    }
                )
                print(f"Added new pending error: {error_hash}")
        
        except Exception as e:
            print(f"Error tracking in DynamoDB: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to just logging
    
    def is_error_confirmed(self, order_id: str, error_hash: str) -> bool:
        """
        Check if an error has exceeded the grace period.
        """
        try:
            response = self.table.get_item(
                Key={'order_id': order_id, 'error_hash': error_hash}
            )
            
            if 'Item' not in response:
                return False
            
            item = response['Item']
            first_detected = datetime.fromisoformat(item['first_detected'])
            age = datetime.utcnow() - first_detected
            
            return age.total_seconds() / 60 >= self.grace_period_minutes
        
        except Exception as e:
            print(f"Error checking confirmation status: {e}")
            return False
    
    def check_error_age(self, order_id: str, error_hash: str) -> float:
        """
        Get the age of an error in minutes.
        """
        try:
            response = self.table.get_item(
                Key={'order_id': order_id, 'error_hash': error_hash}
            )
            
            if 'Item' not in response:
                return 0.0
            
            item = response['Item']
            first_detected = datetime.fromisoformat(item['first_detected'])
            age = datetime.utcnow() - first_detected
            
            return age.total_seconds() / 60
        
        except Exception as e:
            print(f"Error checking age: {e}")
            return 0.0
    
    def get_tracked_error_hashes(self, order_id: str) -> List[str]:
        """
        Get all error hashes currently tracked for an order.
        """
        try:
            response = self.table.query(
                KeyConditionExpression='order_id = :order_id',
                ExpressionAttributeValues={':order_id': order_id}
            )
            
            return [item['error_hash'] for item in response.get('Items', [])]
        
        except Exception as e:
            print(f"Error getting tracked hashes: {e}")
            return []
    
    def get_pending_errors(self, order_id: str) -> Dict[str, Any]:
        """
        Get all pending errors for an order.
        """
        try:
            response = self.table.query(
                KeyConditionExpression='order_id = :order_id',
                ExpressionAttributeValues={':order_id': order_id}
            )
            
            errors = {}
            for item in response.get('Items', []):
                errors[item['error_hash']] = {
                    'first_detected': item['first_detected'],
                    'last_seen': item['last_seen'],
                    'error_details': item['error_details'],
                    'order_number': item.get('order_number', '')
                }
            
            return errors
        
        except Exception as e:
            print(f"Error getting pending errors: {e}")
            return {}
    
    def clear_error(self, order_id: str, error_hash: str) -> None:
        """
        Remove an error from tracking (resolved).
        """
        try:
            self.table.delete_item(
                Key={'order_id': order_id, 'error_hash': error_hash}
            )
            print(f"Cleared resolved error: {error_hash}")
        
        except Exception as e:
            print(f"Error clearing from DynamoDB: {e}")
    
    def get_all_expired_errors(self, grace_period_minutes: int = None) -> List[Dict[str, Any]]:
        """
        Get all errors that have exceeded the grace period across all orders.
        
        Args:
            grace_period_minutes: Override the default grace period (uses self.grace_period_minutes if None)
        """
        if grace_period_minutes is None:
            grace_period_minutes = self.grace_period_minutes
        
        try:
            response = self.table.scan()
            items = response.get('Items', [])
            
            # Continue scanning if there are more items
            while 'LastEvaluatedKey' in response:
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response.get('Items', []))
            
            expired = []
            now = datetime.utcnow()
            
            for item in items:
                first_detected = datetime.fromisoformat(item['first_detected'])
                age = now - first_detected
                
                if age.total_seconds() / 60 >= grace_period_minutes:
                    expired.append({
                        'order_id': item['order_id'],
                        'order_number': item.get('order_number', ''),
                        'error_hash': item['error_hash'],
                        'first_detected': item['first_detected'],
                        'age_minutes': age.total_seconds() / 60,
                        'error_details': item['error_details']
                    })
            
            return expired
        
        except Exception as e:
            print(f"Error scanning for expired errors: {e}")
            import traceback
            traceback.print_exc()
            return []


# Create singleton instance
try:
    dynamodb_error_tracker = DynamoDBErrorTracker()
    print("DynamoDB error tracker initialized")
except Exception as e:
    print(f"Warning: Could not initialize DynamoDB error tracker: {e}")
    dynamodb_error_tracker = None

