## Project Documentation: 05-error-check-gate

### Objective

The goal of this project is to design and implement an Error Check Gate for the InFlow system that automatically validates every quote or sales order upon creation or update.
This ensures accuracy in pricing, discounts, fees, and business logic before the data is finalized or synced to external systems.

### Core Trigger Logic

Whenever a Quote or Sales Order is created or updated, the system should trigger the Error Check Gate module.
This module will analyze all relevant line items and metadata, then return a list of validation results (warnings or errors).

### Validation Rules
1. Discount Validation

Objective: Detect if a customer or product has been given an incorrect or excessive discount.

Logic:
Retrieve the standard discount rules per customer and product category from the customer database.
Compare the applied discount against the expected or allowed discount range.
If the applied discount exceeds the limit, flag an “Excessive Discount” error.

2. TUK Item Validation

Rule: Touch_Up_Kit items must not have any discount applied.

Logic:
Identify all line items containing “TUK” in the product name or SKU.
If the quote or order applies a discount to TUK items, flag a “TUK Discount Violation” error.

3. Credit Card Fee Validation - only for paid orders

Rule: Verify that a 3% credit card fee is correctly applied to the total amount when the payment method is credit card.

Logic:

Check the payment method type in the order metadata.
Confirm that credit card orders with 3% of subtotal exists.
If missing or incorrect, flag a “Credit Card Fee Missing or Incorrect” error.

4. Assembly Fee Validation

Rule: The assembly fee should always be correct and must not have any discount applied.

Logic:
Locate the “Assembly Fee” line item.
(1) Validate that the value matches the correct computation formula (defined in business logic).
(2) Ensure no discount is applied to this line.
If any violation occurs, flag an “Invalid Assembly Fee” error.

5. Deliver Fee Validation

Rule: Only for sales order within "Delivery Record Form.xlsx", if the order number is in ​"Delivery Record Form.xlsx", then check if the sales order on inflow correctly charge (just exists) the freight fee(Yes/No). 

Note: Same order can only be created once in the "Delivery Record Form.xlsx". If same order number appears twice within same date -> error.


### System Behavior

The Error Check Gate should return:
 - A status summary (passed, warning, failed)
 - A list of detected issues
 - Optional suggested fixes (e.g., “Remove discount from TUK item”)
 - Integrate an email notification to alert users when a quote or order fails validation.

