from typing import Dict, Any
from app.validators.base import BaseValidator, ValidationResult


class DiscountRemarkValidator(BaseValidator):
    """
    Validator for Rule 5: Discount Remark Validation
    
    Checks if Z_DISCOUNT exists in the order/quote and verifies that
    remarks notes are present when Z_DISCOUNT is used.
    """
    
    def __init__(self):
        super().__init__("Discount Remark Validation")
    
    def validate(self, order_data: Dict[Any, Any], fetched_data: Dict[Any, Any] = None) -> ValidationResult:
        """
        Validate that remarks are present when Z_DISCOUNT is used.
        
        Args:
            order_data: Complete sales order data from InFlow (for compatibility)
            fetched_data: Pre-formatted data from OrderFetcher
        
        Returns:
            ValidationResult with any discount remark violations
        """
        result = ValidationResult(self.rule_name)
        
        # Use fetched data if available (from OrderFetcher)
        if not fetched_data:
            result.add_info("No fetched data available - OrderFetcher may not have run")
            return result
        
        # Get formatted data from OrderFetcher
        line_items = fetched_data.get('line_items', [])
        raw_order_data = fetched_data.get('raw_order_data', {})
        
        if not line_items:
            result.add_info("No line items to validate")
            return result
        
        # Check if Z_DISCOUNT exists in any line item
        has_z_discount = False
        z_discount_lines = []
        
        for item in line_items:
            item_name = item['name']
            item_sku = item['sku']
            line_number = item['line_number']
            
            # Check if this is a Z_DISCOUNT item
            if 'Z_DISCOUNT' in item_name.upper() or 'Z_DISCOUNT' in item_sku.upper():
                has_z_discount = True
                z_discount_lines.append({
                    'line_number': line_number,
                    'sku': item_sku,
                    'name': item_name
                })
        
        # If Z_DISCOUNT exists, check for order remarks
        if has_z_discount:
            order_remarks = raw_order_data.get('orderRemarks', '').strip()
            
            if not order_remarks:
                # No remarks found - add error
                z_discount_details = ', '.join([
                    f"Line {item['line_number']} ({item['sku']})"
                    for item in z_discount_lines
                ])
                
                result.add_issue(
                    f"Z_DISCOUNT item(s) found but order remarks are missing. "
                    f"Please add remarks explaining the discount reason.",
                    severity='error',
                    details={
                        'z_discount_lines': z_discount_lines,
                        'order_remarks': order_remarks,
                        'has_remarks': False
                    }
                )
                result.add_suggested_fix(
                    f"Add order remarks explaining why the discount ({z_discount_details}) was applied"
                )
            else:
                # Remarks found - validation passed
                result.add_info(
                    f"Z_DISCOUNT found on {len(z_discount_lines)} line(s) with remarks present: \"{order_remarks}\""
                )
        else:
            # No Z_DISCOUNT found - nothing to validate
            result.add_info("No Z_DISCOUNT items found in the order")
        
        return result

