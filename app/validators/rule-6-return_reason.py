from typing import Dict, Any
from app.validators.base import BaseValidator, ValidationResult


class ReturnReasonValidator(BaseValidator):
    """
    Validator for Rule 6: Return Reason Validation
    
    Checks if the order contains return items (negative quantity) and verifies that
    the "Return Reason (Require If Return)" field (Custom Field 4) is present.
    """
    
    def __init__(self):
        super().__init__("Return Reason Validation")
    
    def validate(self, order_data: Dict[Any, Any], fetched_data: Dict[Any, Any] = None) -> ValidationResult:
        """
        Validate that return reason is present when return items exist.
        
        Args:
            order_data: Complete sales order data from InFlow (for compatibility)
            fetched_data: Pre-formatted data from OrderFetcher
        
        Returns:
            ValidationResult with any return reason violations
        """
        result = ValidationResult(self.rule_name)
        
        # Use fetched data if available (from OrderFetcher)
        if not fetched_data or not isinstance(fetched_data, dict):
            result.add_info("No fetched data available - OrderFetcher may not have run")
            return result
        
        # Get formatted data from OrderFetcher
        try:
            line_items = fetched_data.get('line_items', [])
            raw_order_data = fetched_data.get('raw_order_data', {})
        except AttributeError as e:
            result.add_info(f"Error accessing fetched data: {e}")
            return result
        
        # Validate data types
        if not isinstance(line_items, list):
            result.add_info(f"Invalid line_items type: {type(line_items)}")
            return result
        
        if not isinstance(raw_order_data, dict):
            result.add_info(f"Invalid raw_order_data type: {type(raw_order_data)}")
            return result
        
        if not line_items:
            result.add_info("No line items to validate")
            return result
        
        # Check if order contains return items (negative quantity)
        has_return_items = False
        return_item_lines = []
        
        for item in line_items:
            # Ensure item is a dictionary
            if not isinstance(item, dict):
                continue
                
            quantity_str = item.get('quantity', '0')
            item_name = item.get('name', 'Unknown')
            item_sku = item.get('sku', 'N/A')
            line_number = item.get('line_number', 0)
            
            # Convert quantity to float for comparison
            try:
                quantity = float(quantity_str)
            except (ValueError, TypeError):
                quantity = 0
            
            # Check if quantity is negative (return item)
            if quantity < 0:
                has_return_items = True
                return_item_lines.append({
                    'line_number': line_number,
                    'sku': item_sku,
                    'name': item_name,
                    'quantity': quantity_str
                })
        
        # If return items exist, check for return reason in Custom Field 4
        if has_return_items:
            # Get custom fields from raw order data
            # customFields is an object with properties: custom1, custom2, custom3, custom4, etc.
            custom_fields = raw_order_data.get('customFields', {})
            
            # Custom Field 4 is the "Return Reason (Require If Return)" field
            return_reason = None
            if isinstance(custom_fields, dict):
                return_reason = custom_fields.get('custom4', '').strip()
            
            if not return_reason:
                # No return reason found - add error
                return_details = ', '.join([
                    f"Line {item['line_number']} ({item['sku']}, Qty: {item['quantity']})"
                    for item in return_item_lines
                ])
                
                result.add_issue(
                    f"Return item(s) found but return reason is missing. "
                    f"Please provide a reason in Custom Field 4 (Return Reason).",
                    severity='error',
                    details={
                        'return_item_lines': return_item_lines,
                        'return_reason': return_reason,
                        'has_return_reason': False
                    }
                )
                result.add_suggested_fix(
                    f"Add return reason in Custom Field 4 explaining why items ({return_details}) are being returned"
                )
            else:
                # Return reason found - validation passed
                result.add_info(
                    f"Return item(s) found on {len(return_item_lines)} line(s) with return reason present: \"{return_reason}\""
                )
        else:
            # No return items found - nothing to validate
            result.add_info("No return items (negative quantity) found in the order")
        
        return result

