SalesOrder
A sales order is for tracking when a customer purchases goods or services from you, along with associated payments, fulfillments, and returns.

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
200 Success
Response Schema: application/json
amountPaid	
string <decimal>
The amount that this customer has paid you.

assignedToTeamMember	
object (TeamMember)
assignedToTeamMemberId	
string <uuid> Nullable
balance	
string <decimal>
The remaining amount that the customer owes you.

billingAddress	
object (Address)
calculateTax2OnTax1	
boolean Nullable
Whether a secondary tax should be compounded on top of the primary tax

confirmerTeamMember	
object (TeamMember)
confirmerTeamMemberId	
string <uuid> Nullable
contactName	
string
The name of the customer's employee that you should contact for this order

costOfGoodsSold	
object (SalesOrderCostOfGoodsSold)
currency	
object (Currency)
currencyId	
string <uuid>
customFields	
object (LargeCustomFieldValues)
customer	
object (Customer)
customerId	
string <uuid>
dueDate	
string <date-time> Nullable
The date by which payment is due

email	
string
The email address for the customer that you should contact for this order

exchangeRate	
string <decimal>
The exchange rate between the currency in this order and your home currency effective for this order

exchangeRateAutoPulled	
string <date-time> Nullable
If this exchange rate was automatically pulled, then the date it was set, otherwise null.

externalId	
string
An optional external identifier, for use in integrating with other systems

inventoryStatus	
string
Enum: "Unconfirmed" "Quote" "Unfulfilled" "Started" "Fulfilled"
The inventory-related status of this order. This is a read-only attribute. The inventoryStatus is calculated based on whether all products have been added to pickLines. For orders with shipping, all products also have to be added to packLines and shipLines to mark the order fulfilled.

invoicedDate	
string <date-time> Nullable
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

lastModifiedBy	
object (TeamMember)
lastModifiedById	
string <uuid>
The inFlow Team Member, system process, or API key that last modified this sales order. This is set automatically, and cannot be set through the API.

lines	
Array of objects
Lines representing which goods have been ordered and returned

location	
object (Location)
locationId	
string <uuid> Nullable
needsConfirmation	
boolean
When the following conditions are met, then this order needs confirmation before it should be fulfilled: needsConfirmation = True; confirmerTeamMemberId = Null; isQuote = False

nonCustomerCost	
object (PercentOrFixedAmount)
orderDate	
string <date-time>
The date this order was placed.

orderFreight	
string <decimal> Nullable
The amount you charge this customer for shipping

orderNumber	
string
An identifier for this sales order and shown on printed documents.

orderRemarks	
string
Any extra comments on this order

packLines	
Array of objects
Lines representing which goods have been packed into which boxes for shipping

packRemarks	
string
Any extra comments on this order regarding packing

paymentLines	
Array of objects
Lines representing a history of payment details for this order.

paymentStatus	
string
Enum: "Unconfirmed" "Quote" "Uninvoiced" "Invoiced" "Partial" "Paid" "Owing"
The payment-related status of this order

paymentTerms	
object (PaymentTerms)
paymentTermsId	
string <uuid> Nullable
phone	
string
The phone number for the customer that you should contact for this order

pickLines	
Array of objects
Lines representing which goods have been picked from your warehouse

pickRemarks	
string
Any extra comments on this order regarding picking

poNumber	
string
The customer's Purchase Order number for this order.

pricingScheme	
object (PricingScheme)
pricingSchemeId	
string <uuid> Nullable
requestedShipDate	
string <date-time> Nullable
The date that you should ship this order

restockLines	
Array of objects
Lines representing which returned items have been restocked

restockRemarks	
string
Any extra comments on this order regarding restocking

returnFee	
string <decimal> Nullable
The amount you charge to this customer for return fees

returnFreight	
string <decimal> Nullable
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

salesRepTeamMember	
object (TeamMember)
salesRepTeamMemberId	
string <uuid> Nullable
sameBillingAndShipping	
boolean
When true, then the shipping address should be the same as the billing address.

shipLines	
Array of objects
Lines representing which boxes have been shipped

shipRemarks	
string
Any extra comments on this order regarding shipping

shipToCompanyName	
string
The ship-to company name shown on printed documents

shippingAddress	
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
string <decimal> Nullable
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
string <decimal> Nullable
The default percentage secondary tax for this order.

taxingScheme	
object (TaxingScheme)
taxingSchemeId	
string <uuid>
timestamp	
string <rowversion>
You can optionally include the last-known timestamp when modifying to protect against concurrent modifications.

total	
string <decimal>
The total amount the customer should pay, including taxes and shipping

get
/{companyId}/sales-orders/{salesOrderId}
https://cloudapi.inflowinventory.com/{companyId}/sales-orders/{salesOrderId}
Response samples
200
Content type
application/json
Copy
Expand allCollapse all
{
"amountPaid": "19.99",
"assignedToTeamMember": {
"accessAllLocations": true,
"accessLocationIds": [],
"accessRights": [],
"canBeSalesRep": true,
"email": "string",
"isActive": true,
"isInternal": true,
"name": "John Doe",
"teamMemberId": "00000000-0000-0000-0000-000000000000"
},
"assignedToTeamMemberId": "00000000-0000-0000-0000-000000000000",
"balance": "19.99",
"billingAddress": {
"address1": "36 Wonderland Ave.",
"address2": "Unit 207",
"addressType": "Commercial",
"city": "Toronto",
"country": "Canada",
"postalCode": "90210",
"remarks": "string",
"state": "Ontario"
},
"calculateTax2OnTax1": true,
"confirmerTeamMember": {
"accessAllLocations": true,
"accessLocationIds": [],
"accessRights": [],
"canBeSalesRep": true,
"email": "string",
"isActive": true,
"isInternal": true,
"name": "John Doe",
"teamMemberId": "00000000-0000-0000-0000-000000000000"
},
"confirmerTeamMemberId": "00000000-0000-0000-0000-000000000000",
"contactName": "string",
"costOfGoodsSold": {
"costOfGoodsSold": "19.99",
"salesOrder": { },
"salesOrderCostOfGoodsSoldId": "string",
"salesOrderId": "00000000-0000-0000-0000-000000000000"
},
"currency": {
"currencyConversions": [],
"currencyId": "00000000-0000-0000-0000-000000000000",
"decimalPlaces": 2,
"decimalSeparator": ".",
"isSymbolFirst": true,
"isoCode": "USD",
"name": "US Dollar",
"negativeType": "Leading",
"symbol": "$",
"thousandsSeparator": ",",
"timestamp": "0000000000310AB6"
},
"currencyId": "00000000-0000-0000-0000-000000000000",
"customFields": {
"custom1": "string",
"custom10": "string",
"custom2": "string",
"custom3": "string",
"custom4": "string",
"custom5": "string",
"custom6": "string",
"custom7": "string",
"custom8": "string",
"custom9": "string"
},
"customer": {
"addresses": [],
"balances": [],
"contactName": "John Smith",
"credits": [],
"customFields": {},
"customerId": "00000000-0000-0000-0000-000000000000",
"defaultBillingAddress": {},
"defaultBillingAddressId": "00000000-0000-0000-0000-000000000000",
"defaultCarrier": "FedEx",
"defaultLocation": {},
"defaultLocationId": "00000000-0000-0000-0000-000000000000",
"defaultPaymentMethod": "Mastercard",
"defaultPaymentTerms": {},
"defaultPaymentTermsId": "00000000-0000-0000-0000-000000000000",
"defaultSalesRep": "string",
"defaultSalesRepTeamMember": {},
"defaultSalesRepTeamMemberId": "00000000-0000-0000-0000-000000000000",
"defaultShippingAddress": {},
"defaultShippingAddressId": "00000000-0000-0000-0000-000000000000",
"discount": "10",
"dues": [],
"email": "john@acmewidget.com",
"fax": "555-123-4567",
"isActive": true,
"lastModifiedBy": {},
"lastModifiedById": "00000000-0000-0000-0000-000000000000",
"lastModifiedDttm": "2020-01-31",
"name": "Acme Widget Co.",
"orderHistory": {},
"phone": "555-123-4567",
"pricingScheme": {},
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"remarks": "string",
"taxExemptNumber": "string",
"taxingScheme": {},
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"website": "www.acmewidget.com"
},
"customerId": "00000000-0000-0000-0000-000000000000",
"dueDate": "2020-01-31",
"email": "string",
"exchangeRate": "1.24",
"exchangeRateAutoPulled": "2020-01-31",
"externalId": "string",
"inventoryStatus": "Unconfirmed",
"invoicedDate": "2020-01-31",
"isCancelled": true,
"isCompleted": true,
"isInvoiced": true,
"isPrioritized": true,
"isQuote": true,
"isTaxInclusive": true,
"lastModifiedBy": {
"accessAllLocations": true,
"accessLocationIds": [],
"accessRights": [],
"canBeSalesRep": true,
"email": "string",
"isActive": true,
"isInternal": true,
"name": "John Doe",
"teamMemberId": "00000000-0000-0000-0000-000000000000"
},
"lastModifiedById": "00000000-0000-0000-0000-000000000000",
"lines": [
{}
],
"location": {
"address": {},
"isActive": true,
"isDefault": true,
"locationId": "00000000-0000-0000-0000-000000000000",
"name": "string",
"timestamp": "0000000000310AB6"
},
"locationId": "00000000-0000-0000-0000-000000000000",
"needsConfirmation": true,
"nonCustomerCost": {
"isPercent": true,
"value": "19.99"
},
"orderDate": "2020-01-31",
"orderFreight": "19.99",
"orderNumber": "SO-000123",
"orderRemarks": "string",
"packLines": [
{}
],
"packRemarks": "string",
"paymentLines": [
{}
],
"paymentStatus": "Unconfirmed",
"paymentTerms": {
"daysDue": 30,
"isActive": true,
"name": "NET 30",
"paymentTermsId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6"
},
"paymentTermsId": "00000000-0000-0000-0000-000000000000",
"phone": "string",
"pickLines": [
{}
],
"pickRemarks": "string",
"poNumber": "string",
"pricingScheme": {
"currency": {},
"currencyId": "00000000-0000-0000-0000-000000000000",
"isActive": true,
"isDefault": true,
"isTaxInclusive": true,
"name": "Retail price",
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"productPrices": [],
"timestamp": "0000000000310AB6"
},
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"requestedShipDate": "2020-01-31",
"restockLines": [
{}
],
"restockRemarks": "string",
"returnFee": "19.99",
"returnFreight": "19.99",
"returnRemarks": "string",
"salesOrderId": "00000000-0000-0000-0000-000000000000",
"salesRep": "string",
"salesRepTeamMember": {
"accessAllLocations": true,
"accessLocationIds": [],
"accessRights": [],
"canBeSalesRep": true,
"email": "string",
"isActive": true,
"isInternal": true,
"name": "John Doe",
"teamMemberId": "00000000-0000-0000-0000-000000000000"
},
"salesRepTeamMemberId": "00000000-0000-0000-0000-000000000000",
"sameBillingAndShipping": true,
"shipLines": [
{}
],
"shipRemarks": "string",
"shipToCompanyName": "string",
"shippingAddress": {
"address1": "36 Wonderland Ave.",
"address2": "Unit 207",
"addressType": "Commercial",
"city": "Toronto",
"country": "Canada",
"postalCode": "90210",
"remarks": "string",
"state": "Ontario"
},
"showShipping": true,
"source": "Acme Widget Co. internal system",
"subTotal": "19.99",
"tax1": "19.99",
"tax1Name": "VAT",
"tax1OnShipping": true,
"tax1Rate": "19.99",
"tax2": "19.99",
"tax2Name": "PST",
"tax2OnShipping": true,
"tax2Rate": "19.99",
"taxingScheme": {
"calculateTax2OnTax1": true,
"defaultTaxCode": {},
"defaultTaxCodeId": "00000000-0000-0000-0000-000000000000",
"isActive": true,
"isDefault": true,
"name": "NYC sales tax",
"tax1Name": "VAT",
"tax1OnShipping": true,
"tax2Name": "PST",
"tax2OnShipping": true,
"taxCodes": [],
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6"
},
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"total": "19.99"
}
List sales orders
Relationships can be included via the include query parameter.
Options for filtering this list:
filter[orderNumber]
filter[inventoryStatus] array of statuses
filter[paymentStatus] array of statuses
filter[customerId]
filter[orderDate] date range object with fromDate and toDate
filter[poNumber]
filter[locationId]
filter[requestedShipDate] date range object with fromDate and toDate
filter[invoicedDate] date range object with fromDate and toDate
filter[total] number range object with fromDate and toDate
filter[balance] number range object with fromDate and toDate
filter[isActive]
filter[smart] (search on order number and customer name)

path Parameters
companyId
required
string <uuid>
Your inFlow account companyId

query Parameters
request	
object (GetCollectionRequest)
Additional query parameter options

Responses
200 Success
Response Schema: application/json
Array 
amountPaid	
string <decimal>
The amount that this customer has paid you.

assignedToTeamMember	
object (TeamMember)
assignedToTeamMemberId	
string <uuid> Nullable
balance	
string <decimal>
The remaining amount that the customer owes you.

billingAddress	
object (Address)
calculateTax2OnTax1	
boolean Nullable
Whether a secondary tax should be compounded on top of the primary tax

confirmerTeamMember	
object (TeamMember)
confirmerTeamMemberId	
string <uuid> Nullable
contactName	
string
The name of the customer's employee that you should contact for this order

costOfGoodsSold	
object (SalesOrderCostOfGoodsSold)
currency	
object (Currency)
currencyId	
string <uuid>
customFields	
object (LargeCustomFieldValues)
customer	
object (Customer)
customerId	
string <uuid>
dueDate	
string <date-time> Nullable
The date by which payment is due

email	
string
The email address for the customer that you should contact for this order

exchangeRate	
string <decimal>
The exchange rate between the currency in this order and your home currency effective for this order

exchangeRateAutoPulled	
string <date-time> Nullable
If this exchange rate was automatically pulled, then the date it was set, otherwise null.

externalId	
string
An optional external identifier, for use in integrating with other systems

inventoryStatus	
string
Enum: "Unconfirmed" "Quote" "Unfulfilled" "Started" "Fulfilled"
The inventory-related status of this order. This is a read-only attribute. The inventoryStatus is calculated based on whether all products have been added to pickLines. For orders with shipping, all products also have to be added to packLines and shipLines to mark the order fulfilled.

invoicedDate	
string <date-time> Nullable
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

lastModifiedBy	
object (TeamMember)
lastModifiedById	
string <uuid>
The inFlow Team Member, system process, or API key that last modified this sales order. This is set automatically, and cannot be set through the API.

lines	
Array of objects
Lines representing which goods have been ordered and returned

location	
object (Location)
locationId	
string <uuid> Nullable
needsConfirmation	
boolean
When the following conditions are met, then this order needs confirmation before it should be fulfilled: needsConfirmation = True; confirmerTeamMemberId = Null; isQuote = False

nonCustomerCost	
object (PercentOrFixedAmount)
orderDate	
string <date-time>
The date this order was placed.

orderFreight	
string <decimal> Nullable
The amount you charge this customer for shipping

orderNumber	
string
An identifier for this sales order and shown on printed documents.

orderRemarks	
string
Any extra comments on this order

packLines	
Array of objects
Lines representing which goods have been packed into which boxes for shipping

packRemarks	
string
Any extra comments on this order regarding packing

paymentLines	
Array of objects
Lines representing a history of payment details for this order.

paymentStatus	
string
Enum: "Unconfirmed" "Quote" "Uninvoiced" "Invoiced" "Partial" "Paid" "Owing"
The payment-related status of this order

paymentTerms	
object (PaymentTerms)
paymentTermsId	
string <uuid> Nullable
phone	
string
The phone number for the customer that you should contact for this order

pickLines	
Array of objects
Lines representing which goods have been picked from your warehouse

pickRemarks	
string
Any extra comments on this order regarding picking

poNumber	
string
The customer's Purchase Order number for this order.

pricingScheme	
object (PricingScheme)
pricingSchemeId	
string <uuid> Nullable
requestedShipDate	
string <date-time> Nullable
The date that you should ship this order

restockLines	
Array of objects
Lines representing which returned items have been restocked

restockRemarks	
string
Any extra comments on this order regarding restocking

returnFee	
string <decimal> Nullable
The amount you charge to this customer for return fees

returnFreight	
string <decimal> Nullable
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

salesRepTeamMember	
object (TeamMember)
salesRepTeamMemberId	
string <uuid> Nullable
sameBillingAndShipping	
boolean
When true, then the shipping address should be the same as the billing address.

shipLines	
Array of objects
Lines representing which boxes have been shipped

shipRemarks	
string
Any extra comments on this order regarding shipping

shipToCompanyName	
string
The ship-to company name shown on printed documents

shippingAddress	
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
string <decimal> Nullable
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
string <decimal> Nullable
The default percentage secondary tax for this order.

taxingScheme	
object (TaxingScheme)
taxingSchemeId	
string <uuid>
timestamp	
string <rowversion>
You can optionally include the last-known timestamp when modifying to protect against concurrent modifications.

total	
string <decimal>
The total amount the customer should pay, including taxes and shipping

get
/{companyId}/sales-orders
https://cloudapi.inflowinventory.com/{companyId}/sales-orders
Response samples
200
Content type
application/json
Copy
Expand allCollapse all
[
{
"amountPaid": "19.99",
"assignedToTeamMember": {},
"assignedToTeamMemberId": "00000000-0000-0000-0000-000000000000",
"balance": "19.99",
"billingAddress": {},
"calculateTax2OnTax1": true,
"confirmerTeamMember": {},
"confirmerTeamMemberId": "00000000-0000-0000-0000-000000000000",
"contactName": "string",
"costOfGoodsSold": {},
"currency": {},
"currencyId": "00000000-0000-0000-0000-000000000000",
"customFields": {},
"customer": {},
"customerId": "00000000-0000-0000-0000-000000000000",
"dueDate": "2020-01-31",
"email": "string",
"exchangeRate": "1.24",
"exchangeRateAutoPulled": "2020-01-31",
"externalId": "string",
"inventoryStatus": "Unconfirmed",
"invoicedDate": "2020-01-31",
"isCancelled": true,
"isCompleted": true,
"isInvoiced": true,
"isPrioritized": true,
"isQuote": true,
"isTaxInclusive": true,
"lastModifiedBy": {},
"lastModifiedById": "00000000-0000-0000-0000-000000000000",
"lines": [],
"location": {},
"locationId": "00000000-0000-0000-0000-000000000000",
"needsConfirmation": true,
"nonCustomerCost": {},
"orderDate": "2020-01-31",
"orderFreight": "19.99",
"orderNumber": "SO-000123",
"orderRemarks": "string",
"packLines": [],
"packRemarks": "string",
"paymentLines": [],
"paymentStatus": "Unconfirmed",
"paymentTerms": {},
"paymentTermsId": "00000000-0000-0000-0000-000000000000",
"phone": "string",
"pickLines": [],
"pickRemarks": "string",
"poNumber": "string",
"pricingScheme": {},
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"requestedShipDate": "2020-01-31",
"restockLines": [],
"restockRemarks": "string",
"returnFee": "19.99",
"returnFreight": "19.99",
"returnRemarks": "string",
"salesOrderId": "00000000-0000-0000-0000-000000000000",
"salesRep": "string",
"salesRepTeamMember": {},
"salesRepTeamMemberId": "00000000-0000-0000-0000-000000000000",
"sameBillingAndShipping": true,
"shipLines": [],
"shipRemarks": "string",
"shipToCompanyName": "string",
"shippingAddress": {},
"showShipping": true,
"source": "Acme Widget Co. internal system",
"subTotal": "19.99",
"tax1": "19.99",
"tax1Name": "VAT",
"tax1OnShipping": true,
"tax1Rate": "19.99",
"tax2": "19.99",
"tax2Name": "PST",
"tax2OnShipping": true,
"tax2Rate": "19.99",
"taxingScheme": {},
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"total": "19.99"
}
]
Insert or update sales order
salesOrderId property is required, please generate a GUID when inserting.
customerId property is required, which should be the primary identifier for a customer.
source property is required, which should be where this order originated from, i.e. the name of your app.
Many of the properties, e.g. Subtotal, and tax amounts, are optional and will be calculated by inFlow if you exclude the properties.
X-OverrideAllowNegativeInventory: TRUE Setting this header to true will allow picking an amount of products that would make inventory levels in that location go into a negative. By default this is FALSE.

path Parameters
companyId
required
string <uuid>
Your inFlow account companyId

Request Body schema: application/json
A sales order to insert or update

amountPaid	
string <decimal>
The amount that this customer has paid you.

assignedToTeamMember	
object (TeamMember)
assignedToTeamMemberId	
string <uuid> Nullable
balance	
string <decimal>
The remaining amount that the customer owes you.

billingAddress	
object (Address)
calculateTax2OnTax1	
boolean Nullable
Whether a secondary tax should be compounded on top of the primary tax

confirmerTeamMember	
object (TeamMember)
confirmerTeamMemberId	
string <uuid> Nullable
contactName	
string
The name of the customer's employee that you should contact for this order

costOfGoodsSold	
object (SalesOrderCostOfGoodsSold)
currency	
object (Currency)
currencyId	
string <uuid>
customFields	
object (LargeCustomFieldValues)
customer	
object (Customer)
customerId	
string <uuid>
dueDate	
string <date-time> Nullable
The date by which payment is due

email	
string
The email address for the customer that you should contact for this order

exchangeRate	
string <decimal>
The exchange rate between the currency in this order and your home currency effective for this order

exchangeRateAutoPulled	
string <date-time> Nullable
If this exchange rate was automatically pulled, then the date it was set, otherwise null.

externalId	
string
An optional external identifier, for use in integrating with other systems

inventoryStatus	
string
Enum: "Unconfirmed" "Quote" "Unfulfilled" "Started" "Fulfilled"
The inventory-related status of this order. This is a read-only attribute. The inventoryStatus is calculated based on whether all products have been added to pickLines. For orders with shipping, all products also have to be added to packLines and shipLines to mark the order fulfilled.

invoicedDate	
string <date-time> Nullable
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

lastModifiedBy	
object (TeamMember)
lastModifiedById	
string <uuid>
The inFlow Team Member, system process, or API key that last modified this sales order. This is set automatically, and cannot be set through the API.

lines	
Array of objects
Lines representing which goods have been ordered and returned

location	
object (Location)
locationId	
string <uuid> Nullable
needsConfirmation	
boolean
When the following conditions are met, then this order needs confirmation before it should be fulfilled: needsConfirmation = True; confirmerTeamMemberId = Null; isQuote = False

nonCustomerCost	
object (PercentOrFixedAmount)
orderDate	
string <date-time>
The date this order was placed.

orderFreight	
string <decimal> Nullable
The amount you charge this customer for shipping

orderNumber	
string
An identifier for this sales order and shown on printed documents.

orderRemarks	
string
Any extra comments on this order

packLines	
Array of objects
Lines representing which goods have been packed into which boxes for shipping

packRemarks	
string
Any extra comments on this order regarding packing

paymentLines	
Array of objects
Lines representing a history of payment details for this order.

paymentStatus	
string
Enum: "Unconfirmed" "Quote" "Uninvoiced" "Invoiced" "Partial" "Paid" "Owing"
The payment-related status of this order

paymentTerms	
object (PaymentTerms)
paymentTermsId	
string <uuid> Nullable
phone	
string
The phone number for the customer that you should contact for this order

pickLines	
Array of objects
Lines representing which goods have been picked from your warehouse

pickRemarks	
string
Any extra comments on this order regarding picking

poNumber	
string
The customer's Purchase Order number for this order.

pricingScheme	
object (PricingScheme)
pricingSchemeId	
string <uuid> Nullable
requestedShipDate	
string <date-time> Nullable
The date that you should ship this order

restockLines	
Array of objects
Lines representing which returned items have been restocked

restockRemarks	
string
Any extra comments on this order regarding restocking

returnFee	
string <decimal> Nullable
The amount you charge to this customer for return fees

returnFreight	
string <decimal> Nullable
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

salesRepTeamMember	
object (TeamMember)
salesRepTeamMemberId	
string <uuid> Nullable
sameBillingAndShipping	
boolean
When true, then the shipping address should be the same as the billing address.

shipLines	
Array of objects
Lines representing which boxes have been shipped

shipRemarks	
string
Any extra comments on this order regarding shipping

shipToCompanyName	
string
The ship-to company name shown on printed documents

shippingAddress	
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
string <decimal> Nullable
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
string <decimal> Nullable
The default percentage secondary tax for this order.

taxingScheme	
object (TaxingScheme)
taxingSchemeId	
string <uuid>
timestamp	
string <rowversion>
You can optionally include the last-known timestamp when modifying to protect against concurrent modifications.

total	
string <decimal>
The total amount the customer should pay, including taxes and shipping

Responses
200 Success
Response Schema: application/json
amountPaid	
string <decimal>
The amount that this customer has paid you.

assignedToTeamMember	
object (TeamMember)
assignedToTeamMemberId	
string <uuid> Nullable
balance	
string <decimal>
The remaining amount that the customer owes you.

billingAddress	
object (Address)
calculateTax2OnTax1	
boolean Nullable
Whether a secondary tax should be compounded on top of the primary tax

confirmerTeamMember	
object (TeamMember)
confirmerTeamMemberId	
string <uuid> Nullable
contactName	
string
The name of the customer's employee that you should contact for this order

costOfGoodsSold	
object (SalesOrderCostOfGoodsSold)
currency	
object (Currency)
currencyId	
string <uuid>
customFields	
object (LargeCustomFieldValues)
customer	
object (Customer)
customerId	
string <uuid>
dueDate	
string <date-time> Nullable
The date by which payment is due

email	
string
The email address for the customer that you should contact for this order

exchangeRate	
string <decimal>
The exchange rate between the currency in this order and your home currency effective for this order

exchangeRateAutoPulled	
string <date-time> Nullable
If this exchange rate was automatically pulled, then the date it was set, otherwise null.

externalId	
string
An optional external identifier, for use in integrating with other systems

inventoryStatus	
string
Enum: "Unconfirmed" "Quote" "Unfulfilled" "Started" "Fulfilled"
The inventory-related status of this order. This is a read-only attribute. The inventoryStatus is calculated based on whether all products have been added to pickLines. For orders with shipping, all products also have to be added to packLines and shipLines to mark the order fulfilled.

invoicedDate	
string <date-time> Nullable
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

lastModifiedBy	
object (TeamMember)
lastModifiedById	
string <uuid>
The inFlow Team Member, system process, or API key that last modified this sales order. This is set automatically, and cannot be set through the API.

lines	
Array of objects
Lines representing which goods have been ordered and returned

location	
object (Location)
locationId	
string <uuid> Nullable
needsConfirmation	
boolean
When the following conditions are met, then this order needs confirmation before it should be fulfilled: needsConfirmation = True; confirmerTeamMemberId = Null; isQuote = False

nonCustomerCost	
object (PercentOrFixedAmount)
orderDate	
string <date-time>
The date this order was placed.

orderFreight	
string <decimal> Nullable
The amount you charge this customer for shipping

orderNumber	
string
An identifier for this sales order and shown on printed documents.

orderRemarks	
string
Any extra comments on this order

packLines	
Array of objects
Lines representing which goods have been packed into which boxes for shipping

packRemarks	
string
Any extra comments on this order regarding packing

paymentLines	
Array of objects
Lines representing a history of payment details for this order.

paymentStatus	
string
Enum: "Unconfirmed" "Quote" "Uninvoiced" "Invoiced" "Partial" "Paid" "Owing"
The payment-related status of this order

paymentTerms	
object (PaymentTerms)
paymentTermsId	
string <uuid> Nullable
phone	
string
The phone number for the customer that you should contact for this order

pickLines	
Array of objects
Lines representing which goods have been picked from your warehouse

pickRemarks	
string
Any extra comments on this order regarding picking

poNumber	
string
The customer's Purchase Order number for this order.

pricingScheme	
object (PricingScheme)
pricingSchemeId	
string <uuid> Nullable
requestedShipDate	
string <date-time> Nullable
The date that you should ship this order

restockLines	
Array of objects
Lines representing which returned items have been restocked

restockRemarks	
string
Any extra comments on this order regarding restocking

returnFee	
string <decimal> Nullable
The amount you charge to this customer for return fees

returnFreight	
string <decimal> Nullable
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

salesRepTeamMember	
object (TeamMember)
salesRepTeamMemberId	
string <uuid> Nullable
sameBillingAndShipping	
boolean
When true, then the shipping address should be the same as the billing address.

shipLines	
Array of objects
Lines representing which boxes have been shipped

shipRemarks	
string
Any extra comments on this order regarding shipping

shipToCompanyName	
string
The ship-to company name shown on printed documents

shippingAddress	
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
string <decimal> Nullable
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
string <decimal> Nullable
The default percentage secondary tax for this order.

taxingScheme	
object (TaxingScheme)
taxingSchemeId	
string <uuid>
timestamp	
string <rowversion>
You can optionally include the last-known timestamp when modifying to protect against concurrent modifications.

total	
string <decimal>
The total amount the customer should pay, including taxes and shipping

put
/{companyId}/sales-orders
https://cloudapi.inflowinventory.com/{companyId}/sales-orders
Request samples
Payload
Content type
application/json
Copy
Expand allCollapse all
{
"amountPaid": "19.99",
"assignedToTeamMember": {
"accessAllLocations": true,
"accessLocationIds": [],
"accessRights": [],
"canBeSalesRep": true,
"email": "string",
"isActive": true,
"isInternal": true,
"name": "John Doe",
"teamMemberId": "00000000-0000-0000-0000-000000000000"
},
"assignedToTeamMemberId": "00000000-0000-0000-0000-000000000000",
"balance": "19.99",
"billingAddress": {
"address1": "36 Wonderland Ave.",
"address2": "Unit 207",
"addressType": "Commercial",
"city": "Toronto",
"country": "Canada",
"postalCode": "90210",
"remarks": "string",
"state": "Ontario"
},
"calculateTax2OnTax1": true,
"confirmerTeamMember": {
"accessAllLocations": true,
"accessLocationIds": [],
"accessRights": [],
"canBeSalesRep": true,
"email": "string",
"isActive": true,
"isInternal": true,
"name": "John Doe",
"teamMemberId": "00000000-0000-0000-0000-000000000000"
},
"confirmerTeamMemberId": "00000000-0000-0000-0000-000000000000",
"contactName": "string",
"costOfGoodsSold": {
"costOfGoodsSold": "19.99",
"salesOrder": { },
"salesOrderCostOfGoodsSoldId": "string",
"salesOrderId": "00000000-0000-0000-0000-000000000000"
},
"currency": {
"currencyConversions": [],
"currencyId": "00000000-0000-0000-0000-000000000000",
"decimalPlaces": 2,
"decimalSeparator": ".",
"isSymbolFirst": true,
"isoCode": "USD",
"name": "US Dollar",
"negativeType": "Leading",
"symbol": "$",
"thousandsSeparator": ",",
"timestamp": "0000000000310AB6"
},
"currencyId": "00000000-0000-0000-0000-000000000000",
"customFields": {
"custom1": "string",
"custom10": "string",
"custom2": "string",
"custom3": "string",
"custom4": "string",
"custom5": "string",
"custom6": "string",
"custom7": "string",
"custom8": "string",
"custom9": "string"
},
"customer": {
"addresses": [],
"balances": [],
"contactName": "John Smith",
"credits": [],
"customFields": {},
"customerId": "00000000-0000-0000-0000-000000000000",
"defaultBillingAddress": {},
"defaultBillingAddressId": "00000000-0000-0000-0000-000000000000",
"defaultCarrier": "FedEx",
"defaultLocation": {},
"defaultLocationId": "00000000-0000-0000-0000-000000000000",
"defaultPaymentMethod": "Mastercard",
"defaultPaymentTerms": {},
"defaultPaymentTermsId": "00000000-0000-0000-0000-000000000000",
"defaultSalesRep": "string",
"defaultSalesRepTeamMember": {},
"defaultSalesRepTeamMemberId": "00000000-0000-0000-0000-000000000000",
"defaultShippingAddress": {},
"defaultShippingAddressId": "00000000-0000-0000-0000-000000000000",
"discount": "10",
"dues": [],
"email": "john@acmewidget.com",
"fax": "555-123-4567",
"isActive": true,
"lastModifiedBy": {},
"lastModifiedById": "00000000-0000-0000-0000-000000000000",
"lastModifiedDttm": "2020-01-31",
"name": "Acme Widget Co.",
"orderHistory": {},
"phone": "555-123-4567",
"pricingScheme": {},
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"remarks": "string",
"taxExemptNumber": "string",
"taxingScheme": {},
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"website": "www.acmewidget.com"
},
"customerId": "00000000-0000-0000-0000-000000000000",
"dueDate": "2020-01-31",
"email": "string",
"exchangeRate": "1.24",
"exchangeRateAutoPulled": "2020-01-31",
"externalId": "string",
"inventoryStatus": "Unconfirmed",
"invoicedDate": "2020-01-31",
"isCancelled": true,
"isCompleted": true,
"isInvoiced": true,
"isPrioritized": true,
"isQuote": true,
"isTaxInclusive": true,
"lastModifiedBy": {
"accessAllLocations": true,
"accessLocationIds": [],
"accessRights": [],
"canBeSalesRep": true,
"email": "string",
"isActive": true,
"isInternal": true,
"name": "John Doe",
"teamMemberId": "00000000-0000-0000-0000-000000000000"
},
"lastModifiedById": "00000000-0000-0000-0000-000000000000",
"lines": [
{}
],
"location": {
"address": {},
"isActive": true,
"isDefault": true,
"locationId": "00000000-0000-0000-0000-000000000000",
"name": "string",
"timestamp": "0000000000310AB6"
},
"locationId": "00000000-0000-0000-0000-000000000000",
"needsConfirmation": true,
"nonCustomerCost": {
"isPercent": true,
"value": "19.99"
},
"orderDate": "2020-01-31",
"orderFreight": "19.99",
"orderNumber": "SO-000123",
"orderRemarks": "string",
"packLines": [
{}
],
"packRemarks": "string",
"paymentLines": [
{}
],
"paymentStatus": "Unconfirmed",
"paymentTerms": {
"daysDue": 30,
"isActive": true,
"name": "NET 30",
"paymentTermsId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6"
},
"paymentTermsId": "00000000-0000-0000-0000-000000000000",
"phone": "string",
"pickLines": [
{}
],
"pickRemarks": "string",
"poNumber": "string",
"pricingScheme": {
"currency": {},
"currencyId": "00000000-0000-0000-0000-000000000000",
"isActive": true,
"isDefault": true,
"isTaxInclusive": true,
"name": "Retail price",
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"productPrices": [],
"timestamp": "0000000000310AB6"
},
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"requestedShipDate": "2020-01-31",
"restockLines": [
{}
],
"restockRemarks": "string",
"returnFee": "19.99",
"returnFreight": "19.99",
"returnRemarks": "string",
"salesOrderId": "00000000-0000-0000-0000-000000000000",
"salesRep": "string",
"salesRepTeamMember": {
"accessAllLocations": true,
"accessLocationIds": [],
"accessRights": [],
"canBeSalesRep": true,
"email": "string",
"isActive": true,
"isInternal": true,
"name": "John Doe",
"teamMemberId": "00000000-0000-0000-0000-000000000000"
},
"salesRepTeamMemberId": "00000000-0000-0000-0000-000000000000",
"sameBillingAndShipping": true,
"shipLines": [
{}
],
"shipRemarks": "string",
"shipToCompanyName": "string",
"shippingAddress": {
"address1": "36 Wonderland Ave.",
"address2": "Unit 207",
"addressType": "Commercial",
"city": "Toronto",
"country": "Canada",
"postalCode": "90210",
"remarks": "string",
"state": "Ontario"
},
"showShipping": true,
"source": "Acme Widget Co. internal system",
"subTotal": "19.99",
"tax1": "19.99",
"tax1Name": "VAT",
"tax1OnShipping": true,
"tax1Rate": "19.99",
"tax2": "19.99",
"tax2Name": "PST",
"tax2OnShipping": true,
"tax2Rate": "19.99",
"taxingScheme": {
"calculateTax2OnTax1": true,
"defaultTaxCode": {},
"defaultTaxCodeId": "00000000-0000-0000-0000-000000000000",
"isActive": true,
"isDefault": true,
"name": "NYC sales tax",
"tax1Name": "VAT",
"tax1OnShipping": true,
"tax2Name": "PST",
"tax2OnShipping": true,
"taxCodes": [],
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6"
},
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"total": "19.99"
}
Response samples
200
Content type
application/json
Copy
Expand allCollapse all
{
"amountPaid": "19.99",
"assignedToTeamMember": {
"accessAllLocations": true,
"accessLocationIds": [],
"accessRights": [],
"canBeSalesRep": true,
"email": "string",
"isActive": true,
"isInternal": true,
"name": "John Doe",
"teamMemberId": "00000000-0000-0000-0000-000000000000"
},
"assignedToTeamMemberId": "00000000-0000-0000-0000-000000000000",
"balance": "19.99",
"billingAddress": {
"address1": "36 Wonderland Ave.",
"address2": "Unit 207",
"addressType": "Commercial",
"city": "Toronto",
"country": "Canada",
"postalCode": "90210",
"remarks": "string",
"state": "Ontario"
},
"calculateTax2OnTax1": true,
"confirmerTeamMember": {
"accessAllLocations": true,
"accessLocationIds": [],
"accessRights": [],
"canBeSalesRep": true,
"email": "string",
"isActive": true,
"isInternal": true,
"name": "John Doe",
"teamMemberId": "00000000-0000-0000-0000-000000000000"
},
"confirmerTeamMemberId": "00000000-0000-0000-0000-000000000000",
"contactName": "string",
"costOfGoodsSold": {
"costOfGoodsSold": "19.99",
"salesOrder": { },
"salesOrderCostOfGoodsSoldId": "string",
"salesOrderId": "00000000-0000-0000-0000-000000000000"
},
"currency": {
"currencyConversions": [],
"currencyId": "00000000-0000-0000-0000-000000000000",
"decimalPlaces": 2,
"decimalSeparator": ".",
"isSymbolFirst": true,
"isoCode": "USD",
"name": "US Dollar",
"negativeType": "Leading",
"symbol": "$",
"thousandsSeparator": ",",
"timestamp": "0000000000310AB6"
},
"currencyId": "00000000-0000-0000-0000-000000000000",
"customFields": {
"custom1": "string",
"custom10": "string",
"custom2": "string",
"custom3": "string",
"custom4": "string",
"custom5": "string",
"custom6": "string",
"custom7": "string",
"custom8": "string",
"custom9": "string"
},
"customer": {
"addresses": [],
"balances": [],
"contactName": "John Smith",
"credits": [],
"customFields": {},
"customerId": "00000000-0000-0000-0000-000000000000",
"defaultBillingAddress": {},
"defaultBillingAddressId": "00000000-0000-0000-0000-000000000000",
"defaultCarrier": "FedEx",
"defaultLocation": {},
"defaultLocationId": "00000000-0000-0000-0000-000000000000",
"defaultPaymentMethod": "Mastercard",
"defaultPaymentTerms": {},
"defaultPaymentTermsId": "00000000-0000-0000-0000-000000000000",
"defaultSalesRep": "string",
"defaultSalesRepTeamMember": {},
"defaultSalesRepTeamMemberId": "00000000-0000-0000-0000-000000000000",
"defaultShippingAddress": {},
"defaultShippingAddressId": "00000000-0000-0000-0000-000000000000",
"discount": "10",
"dues": [],
"email": "john@acmewidget.com",
"fax": "555-123-4567",
"isActive": true,
"lastModifiedBy": {},
"lastModifiedById": "00000000-0000-0000-0000-000000000000",
"lastModifiedDttm": "2020-01-31",
"name": "Acme Widget Co.",
"orderHistory": {},
"phone": "555-123-4567",
"pricingScheme": {},
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"remarks": "string",
"taxExemptNumber": "string",
"taxingScheme": {},
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"website": "www.acmewidget.com"
},
"customerId": "00000000-0000-0000-0000-000000000000",
"dueDate": "2020-01-31",
"email": "string",
"exchangeRate": "1.24",
"exchangeRateAutoPulled": "2020-01-31",
"externalId": "string",
"inventoryStatus": "Unconfirmed",
"invoicedDate": "2020-01-31",
"isCancelled": true,
"isCompleted": true,
"isInvoiced": true,
"isPrioritized": true,
"isQuote": true,
"isTaxInclusive": true,
"lastModifiedBy": {
"accessAllLocations": true,
"accessLocationIds": [],
"accessRights": [],
"canBeSalesRep": true,
"email": "string",
"isActive": true,
"isInternal": true,
"name": "John Doe",
"teamMemberId": "00000000-0000-0000-0000-000000000000"
},
"lastModifiedById": "00000000-0000-0000-0000-000000000000",
"lines": [
{}
],
"location": {
"address": {},
"isActive": true,
"isDefault": true,
"locationId": "00000000-0000-0000-0000-000000000000",
"name": "string",
"timestamp": "0000000000310AB6"
},
"locationId": "00000000-0000-0000-0000-000000000000",
"needsConfirmation": true,
"nonCustomerCost": {
"isPercent": true,
"value": "19.99"
},
"orderDate": "2020-01-31",
"orderFreight": "19.99",
"orderNumber": "SO-000123",
"orderRemarks": "string",
"packLines": [
{}
],
"packRemarks": "string",
"paymentLines": [
{}
],
"paymentStatus": "Unconfirmed",
"paymentTerms": {
"daysDue": 30,
"isActive": true,
"name": "NET 30",
"paymentTermsId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6"
},
"paymentTermsId": "00000000-0000-0000-0000-000000000000",
"phone": "string",
"pickLines": [
{}
],
"pickRemarks": "string",
"poNumber": "string",
"pricingScheme": {
"currency": {},
"currencyId": "00000000-0000-0000-0000-000000000000",
"isActive": true,
"isDefault": true,
"isTaxInclusive": true,
"name": "Retail price",
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"productPrices": [],
"timestamp": "0000000000310AB6"
},
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"requestedShipDate": "2020-01-31",
"restockLines": [
{}
],
"restockRemarks": "string",
"returnFee": "19.99",
"returnFreight": "19.99",
"returnRemarks": "string",
"salesOrderId": "00000000-0000-0000-0000-000000000000",
"salesRep": "string",
"salesRepTeamMember": {
"accessAllLocations": true,
"accessLocationIds": [],
"accessRights": [],
"canBeSalesRep": true,
"email": "string",
"isActive": true,
"isInternal": true,
"name": "John Doe",
"teamMemberId": "00000000-0000-0000-0000-000000000000"
},
"salesRepTeamMemberId": "00000000-0000-0000-0000-000000000000",
"sameBillingAndShipping": true,
"shipLines": [
{}
],
"shipRemarks": "string",
"shipToCompanyName": "string",
"shippingAddress": {
"address1": "36 Wonderland Ave.",
"address2": "Unit 207",
"addressType": "Commercial",
"city": "Toronto",
"country": "Canada",
"postalCode": "90210",
"remarks": "string",
"state": "Ontario"
},
"showShipping": true,
"source": "Acme Widget Co. internal system",
"subTotal": "19.99",
"tax1": "19.99",
"tax1Name": "VAT",
"tax1OnShipping": true,
"tax1Rate": "19.99",
"tax2": "19.99",
"tax2Name": "PST",
"tax2OnShipping": true,
"tax2Rate": "19.99",
"taxingScheme": {
"calculateTax2OnTax1": true,
"defaultTaxCode": {},
"defaultTaxCodeId": "00000000-0000-0000-0000-000000000000",
"isActive": true,
"isDefault": true,
"name": "NYC sales tax",
"tax1Name": "VAT",
"tax1OnShipping": true,
"tax2Name": "PST",
"tax2OnShipping": true,
"taxCodes": [],
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6"
},
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"total": "19.99"
}