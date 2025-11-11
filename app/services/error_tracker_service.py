import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path


class ErrorTrackerService:
    """
    Service for tracking pending errors with 30-minute grace period.
    Errors are stored in a file-based JSON format and persist across restarts.
    """
    
    def __init__(self, storage_file: str = "logs/pending_errors.json"):
        """
        Initialize the error tracker service.
        
        Args:
            storage_file: Path to JSON file for storing pending errors
        """
        # Use LOGS_DIR environment variable if set (for Lambda)
        import os
        logs_dir = os.environ.get('LOGS_DIR', 'logs')
        if storage_file.startswith('logs/'):
            storage_file = storage_file.replace('logs/', f'{logs_dir}/', 1)
        
        self.storage_file = Path(storage_file)
        self.storage_file.parent.mkdir(exist_ok=True)
        self._ensure_storage_file()
    
    def _ensure_storage_file(self) -> None:
        """
        Ensure the storage file exists with valid JSON structure.
        """
        if not self.storage_file.exists():
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
    
    def _load_errors(self) -> Dict[str, Dict[str, Any]]:
        """
        Load pending errors from storage file.
        
        Returns:
            Dictionary of pending errors by order_id
        """
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_errors(self, errors: Dict[str, Dict[str, Any]]) -> None:
        """
        Save pending errors to storage file.
        
        Args:
            errors: Dictionary of pending errors to save
        """
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(errors, f, indent=2, ensure_ascii=False)
    
    def generate_error_hash(self, order_id: str, rule_name: str, message: str, 
                           details: Dict[Any, Any] = None) -> str:
        """
        Generate a unique hash for an error to track it across webhook calls.
        
        Args:
            order_id: Sales order ID
            rule_name: Name of the validation rule
            message: Error message
            details: Additional error details (optional)
        
        Returns:
            MD5 hash string
        """
        # Use first 100 chars of message to avoid minor variations
        message_key = message[:100]
        
        # Include line numbers or SKUs if available in details
        detail_keys = []
        if details:
            if 'line_number' in details:
                detail_keys.append(str(details['line_number']))
            if 'sku' in details:
                detail_keys.append(str(details['sku']))
            if 'product_sku' in details:
                detail_keys.append(str(details['product_sku']))
        
        # Create hash key
        hash_input = f"{order_id}|{rule_name}|{message_key}|{'|'.join(detail_keys)}"
        return hashlib.md5(hash_input.encode('utf-8')).hexdigest()
    
    def track_error(self, order_id: str, error_hash: str, error_data: Dict[Any, Any],
                    order_number: str = 'N/A') -> None:
        """
        Track a new error or update an existing one.
        
        Args:
            order_id: Sales order ID
            error_hash: Unique hash for this error
            error_data: Complete error information
            order_number: Order number for display
        """
        errors = self._load_errors()
        
        # Initialize order entry if not exists
        if order_id not in errors:
            errors[order_id] = {}
        
        current_time = datetime.now().isoformat()
        
        # If error already exists, update last_seen
        if error_hash in errors[order_id]:
            errors[order_id][error_hash]['last_seen'] = current_time
        else:
            # New error - create entry
            errors[order_id][error_hash] = {
                'first_seen': current_time,
                'last_seen': current_time,
                'order_number': order_number,
                'error_details': error_data
            }
        
        self._save_errors(errors)
    
    def check_error_age(self, order_id: str, error_hash: str) -> Optional[float]:
        """
        Check how long an error has been pending (in minutes).
        
        Args:
            order_id: Sales order ID
            error_hash: Unique hash for the error
        
        Returns:
            Age in minutes, or None if error not found
        """
        errors = self._load_errors()
        
        if order_id not in errors or error_hash not in errors[order_id]:
            return None
        
        first_seen_str = errors[order_id][error_hash]['first_seen']
        first_seen = datetime.fromisoformat(first_seen_str)
        age = datetime.now() - first_seen
        
        return age.total_seconds() / 60.0
    
    def is_error_confirmed(self, order_id: str, error_hash: str, 
                          grace_period_minutes: int = 30) -> bool:
        """
        Check if an error has exceeded the grace period and should be confirmed.
        
        Args:
            order_id: Sales order ID
            error_hash: Unique hash for the error
            grace_period_minutes: Grace period in minutes (default 30)
        
        Returns:
            True if error should be confirmed, False if still pending
        """
        age = self.check_error_age(order_id, error_hash)
        
        if age is None:
            return False
        
        return age >= grace_period_minutes
    
    def clear_error(self, order_id: str, error_hash: str) -> bool:
        """
        Remove a resolved error from tracking.
        
        Args:
            order_id: Sales order ID
            error_hash: Unique hash for the error
        
        Returns:
            True if error was removed, False if not found
        """
        errors = self._load_errors()
        
        if order_id not in errors or error_hash not in errors[order_id]:
            return False
        
        del errors[order_id][error_hash]
        
        # Clean up empty order entries
        if not errors[order_id]:
            del errors[order_id]
        
        self._save_errors(errors)
        return True
    
    def get_pending_errors(self, order_id: str) -> Dict[str, Dict[Any, Any]]:
        """
        Get all pending errors for a specific order.
        
        Args:
            order_id: Sales order ID
        
        Returns:
            Dictionary of error hashes to error data
        """
        errors = self._load_errors()
        return errors.get(order_id, {})
    
    def get_all_expired_errors(self, grace_period_minutes: int = 30) -> List[Dict[Any, Any]]:
        """
        Get all errors that have exceeded the grace period.
        
        Args:
            grace_period_minutes: Grace period in minutes (default 30)
        
        Returns:
            List of expired error entries with order_id and error_hash
        """
        errors = self._load_errors()
        expired = []
        
        cutoff_time = datetime.now() - timedelta(minutes=grace_period_minutes)
        
        for order_id, order_errors in errors.items():
            for error_hash, error_data in order_errors.items():
                first_seen = datetime.fromisoformat(error_data['first_seen'])
                if first_seen <= cutoff_time:
                    expired.append({
                        'order_id': order_id,
                        'error_hash': error_hash,
                        'order_number': error_data.get('order_number', 'N/A'),
                        'first_seen': error_data['first_seen'],
                        'age_minutes': (datetime.now() - first_seen).total_seconds() / 60.0,
                        'error_details': error_data['error_details']
                    })
        
        return expired
    
    def get_tracked_error_hashes(self, order_id: str) -> List[str]:
        """
        Get list of all error hashes currently tracked for an order.
        
        Args:
            order_id: Sales order ID
        
        Returns:
            List of error hash strings
        """
        pending_errors = self.get_pending_errors(order_id)
        return list(pending_errors.keys())


# Create a singleton instance
error_tracker_service = ErrorTrackerService()

