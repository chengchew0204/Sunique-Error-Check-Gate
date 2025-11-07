from typing import Dict, Any
from app.validators.base import BaseValidator, ValidationResult
from app.config import config


class CreditCardFeeValidator(BaseValidator):
    """
    Validator for Rule 2: Credit Card Fee Validation
    
    Verify that a 3% credit card fee is correctly applied when payment method is credit card.
    """
    
    def __init__(self):
        super().__init__("Credit Card Fee Validation")
    
    def validate(self, order_data: Dict[Any, Any]) -> ValidationResult:
        """
        Validate credit card fee for all orders.
        
        Args:
            order_data: Complete sales order data from InFlow
        
        Returns:
            ValidationResult with any credit card fee violations
        """
        result = ValidationResult(self.rule_name)
        
        # Check if payment method is credit card
        payment_lines = order_data.get('paymentLines', [])
        
        if not payment_lines:
            result.add_info("No payment lines found in order.")
            return result
        
        is_credit_card_payment = False
        credit_card_payment_amount = 0.0
        credit_card_payment_details = []
        
        for payment_line in payment_lines:
            payment_type = payment_line.get('paymentType', '')
            payment_method = payment_line.get('paymentMethod', '')
            amount = float(payment_line.get('amount', '0'))
            
            # Check if this is a credit card payment
            is_cc = False
            
            # Make comparisons case-insensitive
            payment_type_lower = payment_type.lower()
            payment_method_lower = payment_method.lower()
            
            if payment_type_lower == 'inflowpay':
                # InFlowPay is always credit card
                is_cc = True
                credit_card_payment_details.append(f"InFlowPay: ${amount:.2f}")
            elif payment_type_lower == 'payment':
                # Check if payment method indicates credit card
                if payment_method_lower in ['credit card', 'qb-cc']:
                    is_cc = True
                    credit_card_payment_details.append(f"{payment_method}: ${amount:.2f}")
            
            if is_cc:
                is_credit_card_payment = True
                credit_card_payment_amount += amount
        
        # If not a credit card payment, skip validation
        if not is_credit_card_payment:
            result.add_info("No credit card payments found. Skipping credit card fee validation.")
            return result
        
        result.add_info(f"Credit card payment detected: {', '.join(credit_card_payment_details)}")
        result.add_info(f"Total credit card payment amount: ${credit_card_payment_amount:.2f}")
        
        # Step 4: Check if Z_CREDIT TRANSACTION FEE exists in line items
        transaction_fee_items = self._find_line_item_by_name(order_data, 'Z_CREDIT TRANSACTION FEE', case_sensitive=False)
        
        if not transaction_fee_items:
            result.add_issue(
                "Credit card payment detected but Z_CREDIT TRANSACTION FEE is missing from line items",
                severity='error',
                details={
                    'credit_card_payment_amount': credit_card_payment_amount,
                    'payment_details': credit_card_payment_details
                }
            )
            result.add_suggested_fix(
                f"Add Z_CREDIT TRANSACTION FEE line item with amount between "
                f"${credit_card_payment_amount * 0.029:.2f} and ${credit_card_payment_amount * 0.031:.2f}"
            )
            return result
        
        # Get the transaction fee amount
        transaction_fee_item = transaction_fee_items[0]
        # InFlow API uses 'subTotal' field for line item totals
        transaction_fee_amount = abs(float(transaction_fee_item.get('subTotal', '0')))
        
        result.add_info(f"Found Z_CREDIT TRANSACTION FEE: ${transaction_fee_amount:.2f}")
        
        # Step 5: Validate the fee is within the acceptable range
        # Formula: fee should be between (payment_amount - fee) * 0.029 and (payment_amount - fee) * 0.031
        # This means: fee = base_amount * rate, where base_amount = payment_amount - fee
        # Solving for fee: fee = payment_amount * rate / (1 + rate)
        
        # However, based on the requirement, we need to calculate:
        # base_amount = payment_amount - transaction_fee
        # expected_fee_range = base_amount * 0.029 to base_amount * 0.031
        
        base_amount = credit_card_payment_amount - transaction_fee_amount
        expected_fee_min = base_amount * 0.029
        expected_fee_max = base_amount * 0.031
        
        result.add_info(f"Base amount (payment - fee): ${base_amount:.2f}")
        result.add_info(f"Expected fee range: ${expected_fee_min:.2f} to ${expected_fee_max:.2f}")
        
        # Check if transaction fee is within acceptable range
        if transaction_fee_amount < expected_fee_min or transaction_fee_amount > expected_fee_max:
            actual_rate = (transaction_fee_amount / base_amount * 100) if base_amount > 0 else 0
            
            result.add_issue(
                f"Credit card transaction fee ${transaction_fee_amount:.2f} ({actual_rate:.2f}%) is outside the expected range "
                f"of ${expected_fee_min:.2f} to ${expected_fee_max:.2f} (2.9% to 3.1%)",
                severity='error',
                details={
                    'actual_fee': transaction_fee_amount,
                    'actual_rate_percent': actual_rate,
                    'expected_fee_min': expected_fee_min,
                    'expected_fee_max': expected_fee_max,
                    'base_amount': base_amount,
                    'credit_card_payment_amount': credit_card_payment_amount
                }
            )
            
            suggested_fee = base_amount * 0.03
            result.add_suggested_fix(
                f"Update Z_CREDIT TRANSACTION FEE to ${suggested_fee:.2f} (3.0% of base amount)"
            )
        else:
            actual_rate = (transaction_fee_amount / base_amount * 100) if base_amount > 0 else 0
            result.add_info(
                f"Credit card transaction fee ${transaction_fee_amount:.2f} ({actual_rate:.2f}%) is within acceptable range"
            )
        
        return result

'''

Todo: Implement this validator
(1) Check if the order is paid already(paymentStatus is "Paid"). 
(2) Check the payment method is credit card.(paymentline's paymentType is "Payment" or "InFlowPay").
(3) If the the paymentType in previous step is "Payment", then keep checking if its paymentMethod is "Credit Card" or "QB-CC", if it is, then it's a credit card payment. If it's InFlowPay, then it must be a credit card payment.
(4) Check if "Z_CREDIT TRANSACTION FEE" is in line items. If not, it's an error. If yes, keep checking the next step.
(5) Check if the ("Z_CREDIT TRANSACTION FEE" in lines) falls in the range of ((the amount in paymentLines)-(transaction fee of product = "Z_CREDIT TRANSACTION FEE" in lines))*0.029 ~ ((the amount in paymentLines)-(transaction fee of product = "Z_CREDIT TRANSACTION FEE" in lines))0.031. If not, it's an error.


API Documentation:
Get a sales order

Relationships can be included via the include query parameter.
path Parameters
companyId
required
	
string <uuid>

Your inFlow account companyId
salesOrderId
required
	
string <uuid>

The salesOrderId to be fetched
Responses
Response Schema: application/json
amountPaid	
string <decimal>

The amount that this customer has paid you.
object (TeamMember)
assignedToTeamMemberId	
string or null <uuid>
Array of objects

File attachments included with this sales order. (This is a read-only attribute.)
balance	
string <decimal>

The remaining amount that the customer owes you.
object (Address)
calculateTax2OnTax1	
boolean or null

Whether a secondary tax should be compounded on top of the primary tax
object (TeamMember)
confirmerTeamMemberId	
string or null <uuid>
contactName	
string

The name of the customer's employee that you should contact for this order
object (SalesOrderCostOfGoodsSold)
object (Currency)
currencyId	
string <uuid>
object (LargeCustomFieldValues)
object (Customer)
customerId	
string <uuid>
dueDate	
string or null <date-time>

The date by which payment is due
email	
string

The email address for the customer that you should contact for this order
exchangeRate	
string <decimal>

The exchange rate between the currency in this order and your home currency effective for this order
exchangeRateAutoPulled	
string or null <date-time>

If this exchange rate was automatically pulled, then the date it was set, otherwise null.
externalId	
string

An optional external identifier, for use in integrating with other systems
inventoryStatus	
string
Enum: "Unconfirmed" "Quote" "Unfulfilled" "Started" "Fulfilled"

The inventory-related status of this order. This is a read-only attribute. The inventoryStatus is calculated based on whether all products have been added to pickLines. For orders with shipping, all products also have to be added to packLines and shipLines to mark the order fulfilled.
invoicedDate	
string or null <date-time>

The date that you sent an invoice for this customer
isCancelled	
boolean

Whether this order is cancelled (being cancelled voids any payments and inventory movements)
isCompleted	
boolean

Whether this order is completed (fully shipped and returns processed)
isInvoiced	
boolean

Whether you have issued an invoice to this customer for this order.
isPrioritized	
boolean

Whether this order is prioritized for fulfillment. (This is a read-only attribute.)
isQuote	
boolean

When true, then treat this as a sales quote (where the customer hasn't agreed to purchase yet) instead of an order.
isTaxInclusive	
boolean

When true, then prices should be treated as tax-inclusive.
object (TeamMember)
lastModifiedById	
string <uuid>

The inFlow Team Member, system process, or API key that last modified this sales order. This is set automatically, and cannot be set through the API.
Array of objects

Lines representing which goods have been ordered and returned
object (Location)
locationId	
string or null <uuid>
needsConfirmation	
boolean

When the following conditions are met, then this order needs confirmation before it should be fulfilled: needsConfirmation = True; confirmerTeamMemberId = Null; isQuote = False
object (PercentOrFixedAmount)
orderDate	
string <date-time>

The date this order was placed.
orderFreight	
string or null <decimal>

The amount you charge this customer for shipping
orderNumber	
string

An identifier for this sales order and shown on printed documents.
orderRemarks	
string

Any extra comments on this order
Array of objects

Lines representing which goods have been packed into which boxes for shipping
packRemarks	
string

Any extra comments on this order regarding packing
Array of objects

Lines representing a history of payment details for this order.
Array
amount	
string <decimal>

The amount being paid
datePaid	
string <date-time>

The date this payment or refund was made
lineNum	
integer <int32>

A number representing the sequence of this payment line
paymentMethod	
string

Method of payment
paymentType	
string
Enum: "Payment" "BatchPayment" "ApplyCredit" "ConvertToCredit" "Refund" "InFlowPay"

The type of payment or refund
referenceNumber	
string

A reference number for this payment, e.g. check number
remarks	
string

Any extra remarks about this payment
salesOrderPaymentHistoryLineId	
string <uuid>

The primary identifier for this sales order payment history line. When inserting, you should specify this by generating a GUID. Not shown to users
timestamp	
string <rowversion>

You can optionally include the last-known timestamp when modifying to protect against concurrent modifications.
paymentStatus	
string
Enum: "Unconfirmed" "Quote" "Uninvoiced" "Invoiced" "Partial" "Paid" "Owing"

The payment-related status of this order
object (PaymentTerms)
paymentTermsId	
string or null <uuid>
phone	
string

The phone number for the customer that you should contact for this order
Array of objects

Lines representing which goods have been picked from your warehouse
pickRemarks	
string

Any extra comments on this order regarding picking
poNumber	
string

The customer's Purchase Order number for this order.
object (PricingScheme)
pricingSchemeId	
string or null <uuid>
requestedShipDate	
string or null <date-time>

The date that you should ship this order
Array of objects

Lines representing which returned items have been restocked
restockRemarks	
string

Any extra comments on this order regarding restocking
returnFee	
string or null <decimal>

The amount you charge to this customer for return fees
returnFreight	
string or null <decimal>

The amount that you refund to this customer for returns related to shipping
returnRemarks	
string

Any extra comments on this order regarding returns
salesOrderId	
string <uuid>

The primary identifier for this sales order. When inserting, you should specify this by generating a GUID. Not shown to users
salesRep	
string

The name of the sales rep at your company in charge of this order. Note: this can only be set when legacy free-form sales rep values are allowed.
object (TeamMember)
salesRepTeamMemberId	
string or null <uuid>
sameBillingAndShipping	
boolean

When true, then the shipping address should be the same as the billing address.
Array of objects

Lines representing which boxes have been shipped
shipRemarks	
string

Any extra comments on this order regarding shipping
shipToCompanyName	
string

The ship-to company name shown on printed documents
object (Address)
showShipping	
boolean

Whether this order will be shipped; this controls whether certain fields like Shipping Address will be shown.
source	
string

Where this order originated from, i.e. the name of your app
subTotal	
string <decimal>

The total of line items for this order
tax1	
string <decimal>

The calculated primary tax amount for this order
tax1Name	
string

A short name for display of the primary tax
tax1OnShipping	
boolean

Whether the primary tax applies to shipping/freight costs
tax1Rate	
string or null <decimal>

The default percentage primary tax for this order.
tax2	
string <decimal>

The calculated secondary tax amount for this order
tax2Name	
string

A short name for display of the secondary tax
tax2OnShipping	
boolean

Whether the secondary tax applies to shipping/freight costs
tax2Rate	
string or null <decimal>

The default percentage secondary tax for this order.
object (TaxingScheme)
taxingSchemeId	
string <uuid>
timestamp	
string <rowversion>

You can optionally include the last-known timestamp when modifying to protect against concurrent modifications.
total	
string <decimal>

The total amount the customer should pay, including taxes and shipping

'''