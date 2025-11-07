from typing import Dict, Any, List
from datetime import datetime
from app.validators.base import BaseValidator, ValidationResult
from app.services.error_tracker_service import error_tracker_service


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
        
        # Process errors through error tracking system
        tracked_errors = self._process_error_tracking(
            order_id, 
            order_number, 
            all_issues
        )
        
        # Determine overall status
        status = self._determine_status(tracked_errors['current_issues'])
        
        # Construct validation report
        validation_report = {
            'order_id': order_id,
            'order_number': order_number,
            'timestamp': timestamp,
            'status': status,
            'issues': tracked_errors['current_issues'],
            'suggested_fixes': all_suggested_fixes,
            'validator_results': validator_results,
            'resolved_issues': tracked_errors['resolved_issues'],
            'pending_count': tracked_errors['pending_count'],
            'confirmed_count': tracked_errors['confirmed_count']
        }
        
        return validation_report
    
    def _process_error_tracking(self, order_id: str, order_number: str, 
                                issues: List[Dict[Any, Any]]) -> Dict[str, Any]:
        """
        Process errors through the error tracking system with 30-minute grace period.
        
        Args:
            order_id: Sales order ID
            order_number: Order number for display
            issues: List of validation issues from validators
        
        Returns:
            Dictionary with:
                - current_issues: List of issues with tracking status
                - resolved_issues: List of auto-resolved issues
                - pending_count: Count of pending errors
                - confirmed_count: Count of confirmed errors
        """
        # Get currently tracked error hashes for this order
        previously_tracked_hashes = error_tracker_service.get_tracked_error_hashes(order_id)
        
        current_error_hashes = []
        current_issues_with_status = []
        pending_count = 0
        confirmed_count = 0
        
        # Process each error
        for issue in issues:
            # Only track actual errors, not warnings or info
            if issue.get('severity') != 'error':
                current_issues_with_status.append(issue)
                continue
            
            # Generate unique hash for this error
            error_hash = error_tracker_service.generate_error_hash(
                order_id=order_id,
                rule_name=issue.get('rule', ''),
                message=issue.get('message', ''),
                details=issue.get('details', {})
            )
            
            current_error_hashes.append(error_hash)
            
            # Track the error (add new or update existing)
            error_tracker_service.track_error(
                order_id=order_id,
                error_hash=error_hash,
                error_data=issue,
                order_number=order_number
            )
            
            # Check if error has exceeded grace period
            is_confirmed = error_tracker_service.is_error_confirmed(order_id, error_hash)
            age_minutes = error_tracker_service.check_error_age(order_id, error_hash)
            
            # Create issue copy with tracking status
            tracked_issue = issue.copy()
            tracked_issue['tracking_status'] = 'confirmed' if is_confirmed else 'pending'
            tracked_issue['error_age_minutes'] = age_minutes
            tracked_issue['error_hash'] = error_hash
            
            if is_confirmed:
                confirmed_count += 1
            else:
                pending_count += 1
            
            current_issues_with_status.append(tracked_issue)
        
        # Find resolved errors (previously tracked but not in current results)
        resolved_issues = []
        for prev_hash in previously_tracked_hashes:
            if prev_hash not in current_error_hashes:
                # This error has been resolved
                pending_errors = error_tracker_service.get_pending_errors(order_id)
                if prev_hash in pending_errors:
                    resolved_error_data = pending_errors[prev_hash]['error_details']
                    resolved_issues.append({
                        'rule': resolved_error_data.get('rule', 'Unknown'),
                        'message': resolved_error_data.get('message', 'Unknown error'),
                        'resolved_at': datetime.now().isoformat(),
                        'error_hash': prev_hash
                    })
                    # Clear from tracking
                    error_tracker_service.clear_error(order_id, prev_hash)
        
        return {
            'current_issues': current_issues_with_status,
            'resolved_issues': resolved_issues,
            'pending_count': pending_count,
            'confirmed_count': confirmed_count
        }
    
    def _determine_status(self, issues: List[Dict[Any, Any]]) -> str:
        """
        Determine overall validation status based on issues.
        
        Args:
            issues: List of validation issues
        
        Returns:
            'passed', 'warning', 'pending', or 'failed'
        """
        if not issues:
            return 'passed'
        
        # Check for confirmed errors
        has_confirmed_errors = any(
            issue.get('severity') == 'error' and 
            issue.get('tracking_status') == 'confirmed' 
            for issue in issues
        )
        
        # Check for pending errors
        has_pending_errors = any(
            issue.get('severity') == 'error' and 
            issue.get('tracking_status') == 'pending' 
            for issue in issues
        )
        
        # Check for warnings (non-error issues)
        has_warnings = any(
            issue.get('severity') != 'error' 
            for issue in issues
        )
        
        if has_confirmed_errors:
            return 'failed'
        elif has_pending_errors:
            return 'pending'
        elif has_warnings:
            return 'warning'
        else:
            return 'passed'


# Create a singleton instance
validation_service = ValidationService()

