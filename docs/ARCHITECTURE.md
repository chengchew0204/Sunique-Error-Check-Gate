# Validator Architecture - Separation of Concerns

## Overview

The validation system uses a two-tier architecture:
1. **Rule 0: Order Data Fetcher** - Fetches and formats data from InFlow API
2. **Validation Rules (1-5)** - Perform validation logic using pre-formatted data

This separation ensures:
- Clean code with single responsibility
- No redundant API calls
- Validators only contain business logic
- Easy to test and maintain

---

## Architecture Flow

```
InFlow Order (webhook)
        ↓
┌───────────────────────────────────┐
│  1. OrderFetcher (Rule 0)         │
│     - Fetches order from API      │
│     - Formats line items          │
│     - Extracts customer info      │
│     - Stores in fetched_data      │
└───────────────┬───────────────────┘
                ↓
        fetched_data {}
                ↓
┌───────────────────────────────────┐
│  2. DiscountValidator (Rule 1)    │
│     - Receives fetched_data       │
│     - Validates discounts         │
│     - Returns issues              │
└───────────────────────────────────┘
                ↓
┌───────────────────────────────────┐
│  3. Other Validators (Rules 2-5)  │
│     - Receive fetched_data        │
│     - Perform validation          │
│     - Return issues               │
└───────────────────────────────────┘
                ↓
        Validation Report
```

---

## File Structure

```
app/validators/
├── rule-0-order_fetcher.py    # Data fetcher (MUST RUN FIRST)
├── rule-1-discount.py         # Discount validation
├── rule-2-credit_card.py      # Credit card fee validation (TODO)
├── rule-3-assembly_fee.py     # Assembly fee validation (TODO)
├── rule-4-delivery_fee.py     # Delivery fee validation (TODO)
├── rule-finalizer.py          # Final step: Notification & processing (TODO)
└── base.py                    # Base classes
```

---

## Rule 0: OrderFetcher

**Purpose:** Fetch and format ALL order data from InFlow API

**Responsibilities:**
- Fetch order details (order number, subtotal, total, etc.)
- Extract and format line items (SKU, name, quantity, price, discount, subtotal)
- Extract customer information (name, default discount)
- Store formatted data in `fetched_data` dictionary

**Output Data Structure:**
```python
{
    'order_info': {
        'order_id': 'uuid',
        'order_number': 'SQ-000336',
        'subtotal': '2677.35',
        'total': '2898.23',
        'customer_id': 'uuid',
        # ... more fields
    },
    'line_items': [
        {
            'line_number': 1,
            'product_id': 'uuid',
            'sku': 'SW-B12',
            'name': 'SW-B12',
            'quantity': '9.0000',
            'unit_price': '326.78',
            'discount_value': '50.00000',
            'discount_is_percent': True,
            'discount_display': '50.00000%',
            'line_total': '1470.51'
        },
        # ... more items
    ],
    'customer_info': {
        'customer_id': 'uuid',
        'name': 'Customer Name',
        'email': 'email@example.com',
        'default_discount': '10'
    }
}
```

---

## Validation Rules (1-5)

**Purpose:** Perform validation logic using pre-formatted data

**Signature:**
```python
def validate(self, order_data: Dict[Any, Any], fetched_data: Dict[Any, Any] = None) -> ValidationResult:
    """
    Args:
        order_data: Raw order data (for compatibility, rarely used)
        fetched_data: Pre-formatted data from OrderFetcher
    
    Returns:
        ValidationResult with issues and suggested fixes
    """
```

**Key Points:**
- Receive `fetched_data` from OrderFetcher
- NO API calls - data already fetched
- Only contain validation logic
- Return issues and suggested fixes

---

## Rule 1: DiscountValidator Example

```python
# OLD WAY (before refactoring):
def validate(self, order_data):
    # Fetch line items
    lines = order_data.get('lines', [])
    # Extract product info
    product = line['product']
    # Extract discount...
    # (lots of data extraction code)
    
    # Finally validate
    if discount > allowed:
        add_issue()

# NEW WAY (after refactoring):
def validate(self, order_data, fetched_data=None):
    # Get pre-formatted data
    line_items = fetched_data['line_items']
    customer_info = fetched_data['customer_info']
    
    # Just validate (clean and simple)
    for item in line_items:
        if float(item['discount_value']) > float(customer_info['default_discount']):
            result.add_issue(f"Discount {item['discount_value']}% exceeds allowed {customer_info['default_discount']}%")
```

---

## ValidationService Flow

The `validation_service.py` orchestrates the flow:

1. **Run OrderFetcher first**
   ```python
   if validator.rule_name == "Order Data Fetcher":
       result = validator.validate(order_data)
       fetched_data = result.fetched_data
   ```

2. **Pass fetched_data to other validators**
   ```python
   else:
       result = validator.validate(order_data, fetched_data=fetched_data)
   ```

---

## Benefits

### 1. **Separation of Concerns**
- Data fetching is separate from validation logic
- Each rule has a single responsibility

### 2. **No Redundant API Calls**
- Fetch data once, use many times
- Faster execution
- Lower API usage

### 3. **Cleaner Code**
- Validators are pure logic
- Easy to read and understand
- Less code in each validator

### 4. **Easier Testing**
- Can test validators with mock data
- Don't need to mock API calls
- Unit tests are simpler

### 5. **Consistent Data Format**
- All validators use the same data structure
- No inconsistencies between validators

---

## Adding New Validators

When creating a new validation rule:

1. **Create new file:** `app/validators/rule-X-name.py`

2. **Use this template:**
```python
from typing import Dict, Any
from app.validators.base import BaseValidator, ValidationResult

class MyValidator(BaseValidator):
    def __init__(self):
        super().__init__("My Validation Rule")
    
    def validate(self, order_data: Dict[Any, Any], fetched_data: Dict[Any, Any] = None) -> ValidationResult:
        result = ValidationResult(self.rule_name)
        
        # Get pre-formatted data
        if not fetched_data:
            result.add_info("No fetched data available")
            return result
        
        order_info = fetched_data.get('order_info', {})
        line_items = fetched_data.get('line_items', [])
        customer_info = fetched_data.get('customer_info', {})
        
        # YOUR VALIDATION LOGIC HERE
        for item in line_items:
            # Check something
            if some_condition:
                result.add_issue("Issue found", severity='error')
        
        return result
```

3. **Register in `main.py`:**
```python
from app.validators import MyValidator
my_validator = MyValidator()
validation_service.register_validator(my_validator)
```

**IMPORTANT:** OrderFetcher must always be registered FIRST!

---

## Console Output

The system now displays:

```
============================================================
Validator 'Order Data Fetcher': PASSED
============================================================

Details:
  - Order: SQ-000336 | Subtotal: $2677.35 | Total: $2898.23
  - Customer: Luis Morales (ID: uuid)
  - Found 2 line items in the order
  - Line 1: SKU: SW-B12 | Name: SW-B12 | Qty: 9.0000 | Unit Price: $326.78 | Discount: 50% | Subtotal: $1470.51
  - Line 2: SKU: SW-B30 | Name: SW-B30 | Qty: 4.0000 | Unit Price: $603.42 | Discount: 50% | Subtotal: $1206.84
============================================================

============================================================
Validator 'Discount Validation': PASSED
============================================================

Details:
  - Discount validation completed for 2 line items
  - Customer default discount: 0%
============================================================
```

---

## Summary

**Before:** Each validator fetched and parsed data independently
**After:** OrderFetcher fetches once, all validators use formatted data

This creates a clean, maintainable, and efficient validation system! ✅

