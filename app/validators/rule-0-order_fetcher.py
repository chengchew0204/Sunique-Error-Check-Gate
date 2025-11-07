from typing import Dict, Any, List
from app.validators.base import BaseValidator, ValidationResult


class OrderFetcher(BaseValidator):
    """
    Rule 0: Order Data Fetcher
    
    Fetches and formats all order data from InFlow API.
    This is not a validation rule, but a data preparation step.
    Other validators will use the formatted data from this fetcher.
    """
    
    def __init__(self):
        super().__init__("Order Data Fetcher")
    
    def validate(self, order_data: Dict[Any, Any]) -> ValidationResult:
        """
        Fetch and format order data for other validators to use.
        
        Args:
            order_data: Raw order data from InFlow API
        
        Returns:
            ValidationResult containing formatted order information
        """
        result = ValidationResult(self.rule_name)
        
        # Extract order-level information
        order_info = self._extract_order_info(order_data)
        
        # Extract and format line items
        line_items = self._extract_line_items(order_data)
        
        # Extract customer information
        customer_info = self._extract_customer_info(order_data)
        
        # Store formatted data in the result for other validators to use
        # We'll store this in the ValidationResult object
        result.fetched_data = {
            'order_info': order_info,
            'line_items': line_items,
            'customer_info': customer_info,
            'raw_order_data': order_data
        }
        
        # Display summary
        result.add_info(f"Order: {order_info['order_number']} | Subtotal: ${order_info['subtotal']} | Total: ${order_info['total']}")
        result.add_info(f"Customer: {customer_info['name']} (ID: {customer_info['customer_id']})")
        result.add_info(f"Found {len(line_items)} line items in the order")
        
        # Display line item details
        for item in line_items:
            info_parts = [
                f"Name: {item['name']}",
                f"SKU: {item['sku']}",
                f"Qty: {item['quantity']}",
                f"Unit Price: ${item['unit_price']}",
                f"Discount: {item['discount_display']}",
                f"Subtotal: ${item['line_total']}"
            ]
            result.add_info(f"Line {item['line_number']}: {' | '.join(info_parts)}")
        
        return result
    
    def _extract_order_info(self, order_data: Dict[Any, Any]) -> Dict[str, Any]:
        """
        Extract order-level information.
        
        Returns:
            Dictionary with order information
        """
        return {
            'order_id': order_data.get('salesOrderId', 'N/A'),
            'order_number': order_data.get('orderNumber', 'N/A'),
            'subtotal': order_data.get('subTotal', '0'),
            'total': order_data.get('total', '0'),
            'tax1': order_data.get('tax1', '0'),
            'tax2': order_data.get('tax2', '0'),
            'order_freight': order_data.get('orderFreight', '0'),
            'order_date': order_data.get('orderDate', 'N/A'),
            'customer_id': order_data.get('customerId', 'N/A'),
            'location_id': order_data.get('locationId', 'N/A'),
            'is_quote': order_data.get('isQuote', False),
            'payment_status': order_data.get('paymentStatus', 'N/A'),
            'inventory_status': order_data.get('inventoryStatus', 'N/A')
        }
    
    def _extract_line_items(self, order_data: Dict[Any, Any]) -> List[Dict[str, Any]]:
        """
        Extract and format line items from order data.
        
        Returns:
            List of formatted line item dictionaries
        """
        # Get raw line items
        raw_lines = order_data.get('lines', [])
        if not raw_lines:
            raw_lines = order_data.get('lineItems', [])
        
        formatted_items = []
        
        for idx, line_item in enumerate(raw_lines, 1):
            # Extract product information
            product = line_item.get('product', {})
            if isinstance(product, dict):
                product_name = product.get('name', 'Unknown')
                product_sku = product.get('sku', 'N/A')
            else:
                product_name = 'Unknown'
                product_sku = 'N/A'
            
            # Extract quantity
            quantity_data = line_item.get('quantity', {})
            if isinstance(quantity_data, dict):
                quantity = quantity_data.get('standardQuantity', '0')
            else:
                quantity = str(quantity_data)
            
            # Extract pricing
            unit_price = line_item.get('unitPrice', '0')
            
            # Extract discount
            discount_data = line_item.get('discount', {})
            if isinstance(discount_data, dict):
                discount_value = discount_data.get('value', '0')
                is_percent = discount_data.get('isPercent', True)
                discount_display = f"{discount_value}%" if is_percent else f"${discount_value}"
            else:
                discount_value = str(discount_data)
                is_percent = True
                discount_display = f"{discount_data}%"
            
            # Extract or calculate line total
            line_total = line_item.get('lineTotal') or line_item.get('total') or line_item.get('subTotal')
            if not line_total or line_total == '0':
                try:
                    qty_num = float(quantity)
                    price_num = float(unit_price)
                    disc_num = float(discount_value)
                    if is_percent:
                        line_total = f"{(qty_num * price_num * (1 - disc_num/100)):.2f}"
                    else:
                        line_total = f"{(qty_num * price_num - disc_num):.2f}"
                except (ValueError, TypeError):
                    line_total = '0.00'
            
            # Create formatted line item
            formatted_item = {
                'line_number': idx,
                'product_id': line_item.get('productId', 'N/A'),
                'sku': product_sku,
                'name': product_name,
                'quantity': quantity,
                'unit_price': unit_price,
                'discount_value': discount_value,
                'discount_is_percent': is_percent,
                'discount_display': discount_display,
                'line_total': line_total,
                'raw_line_item': line_item  # Keep raw data for reference
            }
            
            formatted_items.append(formatted_item)
        
        return formatted_items
    
    def _extract_customer_info(self, order_data: Dict[Any, Any]) -> Dict[str, Any]:
        """
        Extract customer information from order data.
        
        Returns:
            Dictionary with customer information
        """
        customer = order_data.get('customer', {})
        
        if isinstance(customer, dict):
            return {
                'customer_id': order_data.get('customerId', 'N/A'),
                'name': customer.get('name', 'Unknown'),
                'email': customer.get('email', 'N/A'),
                'default_discount': customer.get('discount', '0'),
                'raw_customer': customer  # Keep raw data for reference
            }
        else:
            return {
                'customer_id': order_data.get('customerId', 'N/A'),
                'name': 'Unknown',
                'email': 'N/A',
                'default_discount': '0',
                'raw_customer': {}
            }

