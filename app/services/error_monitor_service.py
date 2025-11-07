import time
from datetime import datetime
from typing import Dict, Any, List
from threading import Thread
from app.services.error_tracker_service import error_tracker_service
from app.clients.inflow_client import inflow_client
from app.services.logger_service import logger_service
from app.services.notification_service import notification_service


class ErrorMonitorService:
    """
    Background service that actively monitors pending errors and triggers
    notifications when they exceed the grace period.
    """
    
    def __init__(self, check_interval_minutes: int = 10):
        """
        Initialize the error monitor service.
        
        Args:
            check_interval_minutes: How often to check for expired errors (default: 10)
        """
        self.check_interval_minutes = check_interval_minutes
        self.check_interval_seconds = check_interval_minutes * 60
        self.running = False
        self.monitor_thread = None
    
    def start(self):
        """
        Start the background monitoring thread.
        """
        if self.running:
            print("Error monitor is already running")
            return
        
        self.running = True
        self.monitor_thread = Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"Error monitor started - checking every {self.check_interval_minutes} minutes")
        print("Initial check will run immediately...")
    
    def trigger_check(self):
        """
        Manually trigger an immediate check for expired errors.
        Can be called from an endpoint for testing or immediate processing.
        """
        print("Manual check triggered")
        self._check_expired_errors()
    
    def get_status(self) -> dict:
        """
        Get the current status of the monitor service.
        
        Returns:
            Dictionary with monitor status information
        """
        return {
            'running': self.running,
            'check_interval_minutes': self.check_interval_minutes,
            'thread_alive': self.monitor_thread.is_alive() if self.monitor_thread else False
        }
    
    def stop(self):
        """
        Stop the background monitoring thread.
        """
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("Error monitor stopped")
    
    def _monitor_loop(self):
        """
        Main monitoring loop that runs in background thread.
        """
        # Do an initial check immediately on startup
        try:
            self._check_expired_errors()
        except Exception as e:
            print(f"Error in initial check: {e}")
            import traceback
            traceback.print_exc()
        
        # Then continue with regular interval checks
        while self.running:
            # Sleep for the check interval
            time.sleep(self.check_interval_seconds)
            
            try:
                self._check_expired_errors()
            except Exception as e:
                print(f"Error in monitor loop: {e}")
                import traceback
                traceback.print_exc()
    
    def _check_expired_errors(self):
        """
        Check for errors that have exceeded the grace period and trigger notifications.
        """
        print("="*60)
        print(f"ERROR MONITOR: Checking for expired errors at {datetime.now().isoformat()}")
        print("="*60)
        
        # Get all errors that have exceeded 30 minutes
        expired_errors = error_tracker_service.get_all_expired_errors(grace_period_minutes=30)
        
        if not expired_errors:
            print("No expired errors found")
            return
        
        print(f"Found {len(expired_errors)} expired error(s)")
        
        # Group expired errors by order_id
        orders_with_expired_errors: Dict[str, List[Dict[Any, Any]]] = {}
        for expired_error in expired_errors:
            order_id = expired_error['order_id']
            if order_id not in orders_with_expired_errors:
                orders_with_expired_errors[order_id] = []
            orders_with_expired_errors[order_id].append(expired_error)
        
        # Process each order with expired errors
        for order_id, errors in orders_with_expired_errors.items():
            try:
                self._process_expired_order(order_id, errors)
            except Exception as e:
                print(f"Error processing expired errors for order {order_id}: {e}")
                import traceback
                traceback.print_exc()
    
    def _process_expired_order(self, order_id: str, expired_errors: List[Dict[Any, Any]]):
        """
        Process an order with expired errors - log and send notification.
        
        Args:
            order_id: Sales order ID
            expired_errors: List of expired error entries
        """
        print(f"\nProcessing order: {order_id}")
        print(f"Order number: {expired_errors[0]['order_number']}")
        print(f"Expired errors: {len(expired_errors)}")
        
        # Fetch current order data from InFlow to get latest info
        try:
            order_data = inflow_client.get_sales_order(order_id)
        except Exception as e:
            print(f"Failed to fetch order data for {order_id}: {e}")
            return
        
        order_number = order_data.get('orderNumber', expired_errors[0]['order_number'])
        timestamp = datetime.now().isoformat()
        
        # Build validation result from expired errors
        issues = []
        for expired_error in expired_errors:
            error_details = expired_error['error_details'].copy()
            error_details['tracking_status'] = 'confirmed'
            error_details['error_age_minutes'] = expired_error['age_minutes']
            issues.append(error_details)
        
        # Create validation result structure
        validation_result = {
            'order_id': order_id,
            'order_number': order_number,
            'timestamp': timestamp,
            'status': 'failed',
            'issues': issues,
            'suggested_fixes': [],
            'validator_results': [],
            'resolved_issues': [],
            'pending_count': 0,
            'confirmed_count': len(expired_errors)
        }
        
        print(f"Logging confirmed errors for order {order_number}")
        
        # Log the confirmed errors
        logger_service.log_validation_result(validation_result, order_data)
        
        # Send notification
        print(f"Sending notification for order {order_number}")
        try:
            notification_service.send_validation_failure_notification(
                validation_result,
                order_data
            )
            
            # Clear expired errors from tracking after successful notification
            # This prevents duplicate notifications
            for expired_error in expired_errors:
                error_hash = expired_error['error_hash']
                error_tracker_service.clear_error(order_id, error_hash)
                print(f"Cleared confirmed error from tracking: {error_hash[:8]}...")
            
        except Exception as e:
            print(f"Failed to send notification: {e}")
            print(f"Errors will remain in tracking and retry on next check")
            import traceback
            traceback.print_exc()
            return
        
        print(f"Successfully processed expired errors for order {order_number}")


# Create a singleton instance
error_monitor_service = ErrorMonitorService(check_interval_minutes=10)

