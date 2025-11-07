from typing import Dict, Any
from app.validators.base import BaseValidator, ValidationResult


class DiscountValidator(BaseValidator):
    """
    Validator for Rule 1: Discount Validation
    
    Detects if a customer or product has been given an incorrect or excessive discount.
    Uses pre-fetched data from OrderFetcher (Rule 0).
    """
    
    def __init__(self):
        super().__init__("Discount Validation")
    
    def validate(self, order_data: Dict[Any, Any], fetched_data: Dict[Any, Any] = None) -> ValidationResult:
        """
        Validate discount rules for the sales order.
        
        Args:
            order_data: Complete sales order data from InFlow (for compatibility)
            fetched_data: Pre-formatted data from OrderFetcher
        
        Returns:
            ValidationResult with any discount violations
        """
        result = ValidationResult(self.rule_name)
        
        # Use fetched data if available (from OrderFetcher)
        if not fetched_data:
            result.add_info("No fetched data available - OrderFetcher may not have run")
            return result
        
        # Get formatted data from OrderFetcher
        order_info = fetched_data.get('order_info', {})
        line_items = fetched_data.get('line_items', [])
        customer_info = fetched_data.get('customer_info', {})
        
        if not line_items:
            result.add_info("No line items to validate")
            return result
        
        # Get customer's default discount rate
        customer_discount = float(customer_info.get('default_discount', '0'))
        
        # Get order subtotal for percentage calculations
        order_subtotal = float(order_info.get('subtotal', '0'))
        
        # Track Z_DISCOUNT items for rule 4
        z_discount_amount = 0.0
        has_z_discount = False
        
        # Track original prices (before discounts) for accurate discount percentage calculation
        total_original_price = 0.0
        
        # Validate each line item
        for item in line_items:
            try:
                line_discount = float(item['discount_value'])
                item_name = item['name']
                item_sku = item['sku']
                line_number = item['line_number']
                line_total = float(item['line_total'])
                
                # Calculate original price (before discount) for this line item
                # If discount is percentage-based: original = line_total / (1 - discount/100)
                # If discount is fixed amount: original = line_total + discount
                is_z_discount_item = 'Z_DISCOUNT' in item_name.upper() or 'Z_DISCOUNT' in item_sku.upper()
                
                if not is_z_discount_item:
                    if item['discount_is_percent'] and line_discount > 0:
                        # Reverse percentage discount: original = discounted / (1 - discount%)
                        original_price = line_total / (1 - (line_discount / 100))
                    elif not item['discount_is_percent'] and line_discount > 0:
                        # Reverse fixed discount: original = discounted + discount_amount
                        original_price = line_total + line_discount
                    else:
                        # No discount applied
                        original_price = line_total
                    
                    total_original_price += original_price
                
                # Rule 1: Check if line item discount exceeds customer's default discount
                if item['discount_is_percent'] and line_discount > customer_discount:
                    result.add_issue(
                        f"Line {line_number} ({item_sku} - {item_name}): "
                        f"Discount {line_discount}% exceeds customer's allowed {customer_discount}%",
                        severity='error',
                        details={
                            'line_number': line_number,
                            'sku': item_sku,
                            'name': item_name,
                            'line_discount': line_discount,
                            'customer_discount': customer_discount
                        }
                    )
                    result.add_suggested_fix(
                        f"Reduce discount on Line {line_number} ({item_name}) from {line_discount}% to {customer_discount}% or less"
                    )
                
                # Rule 2: TUK items should have 0% discount
                if 'TUK' in item_name.upper() and line_discount > 0:
                    result.add_issue(
                        f"Line {line_number} ({item_sku} - {item_name}): "
                        f"TUK items should not have discount, but has {line_discount}% discount",
                        severity='error',
                        details={
                            'line_number': line_number,
                            'sku': item_sku,
                            'name': item_name,
                            'discount': line_discount
                        }
                    )
                    result.add_suggested_fix(
                        f"Remove discount from Line {line_number} ({item_name}) - TUK items must have 0% discount"
                    )
                
                # Rule 3: Items starting with "Z" should have 0% discount
                # Exclude Z_DISCOUNT from this check as it's a special discount line item
                if not is_z_discount_item and (item_name.startswith('Z') or item_sku.startswith('Z')) and line_discount > 0:
                    result.add_issue(
                        f"Line {line_number} ({item_sku} - {item_name}): "
                        f"Items starting with 'Z' should not have discount, but has {line_discount}% discount",
                        severity='error',
                        details={
                            'line_number': line_number,
                            'sku': item_sku,
                            'name': item_name,
                            'discount': line_discount
                        }
                    )
                    result.add_suggested_fix(
                        f"Remove discount from Line {line_number} ({item_name}) - Z items must have 0% discount"
                    )
                
                # Track Z_DISCOUNT items for rule 4
                if is_z_discount_item:
                    has_z_discount = True
                    # Use absolute value since Z_DISCOUNT is typically negative
                    z_discount_amount = abs(line_total)
                    
            except (ValueError, TypeError) as e:
                # Skip items with invalid discount values
                result.add_info(f"Line {item.get('line_number', '?')}: Skipped due to invalid data - {str(e)}")
        
        # Rule 4: Check if total discount (including Z_DISCOUNT) exceeds threshold
        # Threshold = max(70%, customer_discount%)
        # Calculation: Use original prices (before discounts) vs final subtotal
        if total_original_price > 0:
            # Calculate actual total discount amount
            # Total discount = Original Price - Final Subtotal (which includes Z_DISCOUNT effect)
            total_discount_amount = total_original_price - order_subtotal
            actual_discount_percentage = (total_discount_amount / total_original_price) * 100
            
            # Determine threshold: use customer discount if > 70%, otherwise use 70%
            discount_threshold = max(70.0, customer_discount)
            
            if actual_discount_percentage > discount_threshold:
                result.add_issue(
                    f"Total discount ${total_discount_amount:.2f} ({actual_discount_percentage:.1f}%) "
                    f"exceeds allowed threshold of {discount_threshold:.1f}%",
                    severity='error',
                    details={
                        'total_discount_amount': total_discount_amount,
                        'total_original_price': total_original_price,
                        'order_subtotal': order_subtotal,
                        'actual_percentage': actual_discount_percentage,
                        'threshold': discount_threshold,
                        'customer_discount': customer_discount,
                        'has_z_discount': has_z_discount,
                        'z_discount_amount': z_discount_amount if has_z_discount else 0
                    }
                )
                # Calculate how much discount needs to be reduced
                max_allowed_discount = total_original_price * (discount_threshold / 100)
                excess_discount = total_discount_amount - max_allowed_discount
                result.add_suggested_fix(
                    f"Reduce total discount by ${excess_discount:.2f} to meet the {discount_threshold:.1f}% threshold "
                    f"(Current: ${total_discount_amount:.2f}, Maximum allowed: ${max_allowed_discount:.2f})"
                )


        
        # Add summary information
        result.add_info(f"Discount validation completed for {len(line_items)} line items")
        result.add_info(f"Customer default discount: {customer_discount}%")
        if total_original_price > 0:
            total_discount_amount = total_original_price - order_subtotal
            actual_discount_percentage = (total_discount_amount / total_original_price) * 100
            discount_threshold = max(70.0, customer_discount)
            result.add_info(
                f"Total discount: ${total_discount_amount:.2f} ({actual_discount_percentage:.1f}% of original ${total_original_price:.2f}), "
                f"threshold: {discount_threshold:.1f}%"
            )
            if has_z_discount and z_discount_amount > 0:
                result.add_info(f"Includes Z_DISCOUNT: ${z_discount_amount:.2f}")
        
        return result