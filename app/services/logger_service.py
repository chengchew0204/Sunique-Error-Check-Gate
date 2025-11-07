import json
import csv
import os
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path


class LoggerService:
    """
    Service for logging validation results to JSON and CSV files.
    """
    
    def __init__(self, log_directory: str = "logs"):
        """
        Initialize the logger service.
        
        Args:
            log_directory: Directory to store log files
        """
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)
    
    def log_validation_result(self, validation_result: Dict[Any, Any], order_data: Dict[Any, Any] = None) -> None:
        """
        Log a validation result to monthly CSV log file.
        
        Args:
            validation_result: Dictionary containing validation results with structure:
                {
                    'order_id': str,
                    'status': 'passed' | 'warning' | 'failed',
                    'timestamp': str (ISO format),
                    'issues': List[Dict],
                    'suggested_fixes': List[str]
                }
            order_data: Complete sales order data from InFlow (optional, for CSV logging)
        """
        # Log to CSV only
        self._log_to_csv(validation_result, order_data)
    
    def _log_to_json(self, validation_result: Dict[Any, Any]) -> None:
        """
        Write validation result to a timestamped JSON file.
        
        Args:
            validation_result: Validation result dictionary
        """
        timestamp = validation_result.get('timestamp', datetime.now().isoformat())
        order_id = validation_result.get('order_id', 'unknown')
        order_number = validation_result.get('order_number', 'N/A')
        
        # Create filename with timestamp and order ID
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        filename = f"validation_{dt.strftime('%Y%m%d_%H%M%S')}_{order_id}.json"
        filepath = self.log_directory / filename
        
        # Write JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(validation_result, f, indent=2, ensure_ascii=False)
        
        print(f"Validation result logged to JSON: {filepath} (Order: {order_number})")
    
    def _log_to_csv(self, validation_result: Dict[Any, Any], order_data: Dict[Any, Any] = None) -> None:
        """
        Append validation result to monthly CSV log file.
        
        Args:
            validation_result: Validation result dictionary
            order_data: Complete sales order data from InFlow (optional)
        """
        timestamp = validation_result.get('timestamp', datetime.now().isoformat())
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        # Create monthly CSV filename
        filename = f"validation_log_{dt.strftime('%Y%m')}.csv"
        filepath = self.log_directory / filename
        
        # Extract account manager
        account_manager = 'N/A'
        if order_data:
            # Try to get from salesRepTeamMember object first (preferred)
            sales_rep_member = order_data.get('salesRepTeamMember')
            if isinstance(sales_rep_member, dict) and sales_rep_member:
                name = sales_rep_member.get('name', '').strip()
                if name:
                    account_manager = name
            
            # Fall back to legacy salesRep string field
            if account_manager == 'N/A':
                sales_rep = order_data.get('salesRep', '').strip()
                if sales_rep:
                    account_manager = sales_rep
        
        # Categorize errors by validator
        issues = validation_result.get('issues', [])
        error_count = sum(1 for issue in issues if issue.get('severity') == 'error')
        
        discount_error = 0
        credit_card_error = 0
        assembly_error = 0
        delivery_fee_error = 0
        discount_remarks_error = 0
        return_reason_error = 0
        
        for issue in issues:
            if issue.get('severity') != 'error':
                continue
            rule = issue.get('rule', '').lower()
            if 'return reason' in rule:
                return_reason_error = 1
            elif 'remark' in rule:
                discount_remarks_error = 1
            elif 'discount' in rule:
                discount_error = 1
            elif 'credit card' in rule:
                credit_card_error = 1
            elif 'assembly' in rule:
                assembly_error = 1
            elif 'delivery' in rule:
                delivery_fee_error = 1
        
        # Summarize issues (only errors, limit to first 3)
        issues_summary = '; '.join([
            f"{issue.get('rule', 'unknown')}: {issue.get('message', '')}"
            for issue in issues if issue.get('severity') == 'error'
        ][:3])
        
        row = {
            'timestamp': timestamp,
            'order_number': validation_result.get('order_number', 'N/A'),
            'status': validation_result.get('status', ''),
            'account_manager': account_manager,
            'error_count': error_count,
            'discount_error': discount_error,
            'credit_card_error': credit_card_error,
            'assembly_error': assembly_error,
            'delivery_fee_error': delivery_fee_error,
            'discount_remarks_error': discount_remarks_error,
            'return_reason_error': return_reason_error,
            'issues_summary': issues_summary
        }
        
        # Check if file exists to determine if we need to write headers
        file_exists = filepath.exists()
        
        # Write to CSV
        with open(filepath, 'a', newline='', encoding='utf-8') as f:
            fieldnames = ['timestamp', 'order_number', 'status', 'account_manager', 
                          'error_count', 'discount_error', 'credit_card_error', 
                          'assembly_error', 'delivery_fee_error', 'discount_remarks_error', 
                          'return_reason_error', 'issues_summary']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(row)
        
        print(f"Validation result logged to CSV: {filepath} (Order: {validation_result.get('order_number', 'N/A')})")
    
    def get_validation_history(self, order_id: str) -> List[Dict[Any, Any]]:
        """
        Retrieve validation history for a specific order from CSV logs.
        
        Args:
            order_id: Sales order ID (not used anymore since we log by order_number)
        
        Returns:
            Empty list (CSV logs don't support individual order lookup)
        """
        # Note: CSV logs are consolidated monthly and indexed by order_number, not order_id
        # To retrieve history for a specific order, you would need to parse all CSV files
        # and filter by order_number, which is not efficient.
        # This functionality is deprecated in favor of monthly CSV reports.
        print("Note: get_validation_history is deprecated. Use monthly CSV logs for reporting.")
        return []


# Create a singleton instance
logger_service = LoggerService()

