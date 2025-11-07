from typing import Dict, Any, List
from datetime import datetime
from app.validators.base import BaseValidator, ValidationResult


class ValidationService:
    """
    Orchestrates validation of sales orders using multiple validation rules.
    """
    
    def __init__(self):
        """
        Initialize the validation service.
        """
        self.validators: List[BaseValidator] = []
    
    def register_validator(self, validator: BaseValidator) -> None:
        """
        Register a validator to be used in validation.
        
        Args:
            validator: Instance of a validator class
        """
        self.validators.append(validator)
        print(f"Registered validator: {validator.rule_name}")
    
    def validate_order(self, order_data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Validate a sales order using all registered validators.
        
        Args:
            order_data: Complete sales order data from InFlow
        
        Returns:
            Aggregated validation report with structure:
            {
                'order_id': str,
                'order_number': str,
                'timestamp': str,
                'status': 'passed' | 'warning' | 'failed',
                'issues': List[Dict],
                'suggested_fixes': List[str],
                'validator_results': List[Dict]
            }
        """
        order_id = order_data.get('salesOrderId', 'unknown')
        order_number = order_data.get('orderNumber', 'N/A')
        timestamp = datetime.now().isoformat()
        
        all_issues = []
        all_suggested_fixes = []
        validator_results = []
        fetched_data = None
        
        # Run all validators
        for validator in self.validators:
            try:
                # Check if this is the OrderFetcher (Rule 0)
                # OrderFetcher should always run first and provide data to other validators
                if validator.rule_name == "Order Data Fetcher":
                    result = validator.validate(order_data)
                    # Capture the fetched data for other validators
                    fetched_data = result.fetched_data if hasattr(result, 'fetched_data') else None
                else:
                    # Pass fetched data to other validators
                    # Check if validator accepts fetched_data parameter
                    try:
                        result = validator.validate(order_data, fetched_data=fetched_data)
                    except TypeError:
                        # Fallback for validators that don't accept fetched_data yet
                        result = validator.validate(order_data)
                
                validator_results.append(result.to_dict())
                
                # Collect issues and fixes
                all_issues.extend(result.issues)
                all_suggested_fixes.extend(result.suggested_fixes)
                
                # Display validation result with details
                status_text = 'PASSED' if result.passed else 'FAILED'
                print(f"\n{'='*60}")
                print(f"Validator '{validator.rule_name}': {status_text}")
                print(f"{'='*60}")
                
                # Display info messages (e.g., line item details)
                if hasattr(result, 'info_messages') and result.info_messages:
                    print(f"\nDetails:")
                    for info in result.info_messages:
                        print(f"  - {info}")
                
                # Display issues if any
                if result.issues:
                    print(f"\nIssues Found ({len(result.issues)}):")
                    for idx, issue in enumerate(result.issues, 1):
                        print(f"  {idx}. [{issue['severity'].upper()}] {issue['message']}")
                
                # Display suggested fixes if any
                if result.suggested_fixes:
                    print(f"\nSuggested Fixes:")
                    for idx, fix in enumerate(result.suggested_fixes, 1):
                        print(f"  {idx}. {fix}")
                
                print(f"{'='*60}\n")
            
            except Exception as e:
                print(f"Error running validator '{validator.rule_name}': {e}")
                # Add error as an issue
                all_issues.append({
                    'rule': validator.rule_name,
                    'message': f"Validator error: {str(e)}",
                    'severity': 'error',
                    'details': {}
                })
        
        # Determine overall status
        status = self._determine_status(all_issues)
        
        # Construct validation report
        validation_report = {
            'order_id': order_id,
            'order_number': order_number,
            'timestamp': timestamp,
            'status': status,
            'issues': all_issues,
            'suggested_fixes': all_suggested_fixes,
            'validator_results': validator_results
        }
        
        return validation_report
    
    def _determine_status(self, issues: List[Dict[Any, Any]]) -> str:
        """
        Determine overall validation status based on issues.
        
        Args:
            issues: List of validation issues
        
        Returns:
            'passed', 'warning', or 'failed'
        """
        if not issues:
            return 'passed'
        
        # Check if there are any errors (not just warnings)
        has_errors = any(issue.get('severity') == 'error' for issue in issues)
        
        if has_errors:
            return 'failed'
        else:
            return 'warning'


# Create a singleton instance
validation_service = ValidationService()

