# Sunique API Intro

This is the document for basic API introduction extracted from [https://cloudapi.inflowinventory.com/docs/index.html](https://cloudapi.inflowinventory.com/docs/index.html).

## AdjustmentReason

Adjustment reasons are pre-defined sets of reasons why stock adjustments may be made.

### Methods
- Get adjustment reasons
- List adjustment reasons

## Categories

A category is used for organizing products. Categories themselves can have parent categories and are arranged hierarchically into a tree structure.

### Methods
- Get a category
- List categories

## Currency

A currency, e.g. US dollar, Euro, along with its formatting rules. Read-only.

### Methods
- List currencies
- Get a currency

## Customer

A customer is an individual or business that you sell to.

### Methods
- Get a customer
- List customers
- Insert or update a customer

## CustomFieldDefinitions

### Methods
- Get custom field definitions
- Insert or update custom field definition
- Get all dropdown custom field options for an entity
- Set custom field dropdown options

## CustomFields

### Methods
- Get custom field labels
- Insert or Update custom field labels

## Location

A location most typically represents a warehouse or store. Locations can contain many sublocations, typically representing a bin number or shelf location. Sublocations do not need to be defined in advance. inFlow tracks inventory by location and sublocation.

### Methods
- Get a location
- List locations
- Get suggested sublocations
- Get suggested sublocations for a given product and location

## ManufacturingOrder

A manufacture order is for building finished products from raw materials, along with associated operations, picking, and put-away.

### Methods
- Get a manufacture order
- Insert or update a manufacture order
- List manufacture orders

## OperationType

An OperationType is a type of work done in your manufacturing processes, e.g. assembly, welding.

### Methods
- Get an OperationType
- List OperationTypes

## PaymentTerms

Payment terms describe details about payment, typically focusing on the number of days until payment is due. e.g. NET 30.

### Methods
- Get payment terms
- List payment terms

## PricingScheme

A pricing scheme is a set of prices that are commonly charged to customers, e.g. Retail price, Wholesale price, Canadian price.

### Methods
- Get a pricing scheme
- List pricing schemes

## Product

A product is a type of physical good or service (depending on ItemType) whose cost, inventory levels, sales, and movements can be tracked in inFlow.

### Methods
- Get a product
- List products
- Insert or update product
- Get product inventory summary
- Get multiple product inventory summaries

## ProductCostAdjustment

A product cost adjustment is a recorded action that changes the inventory cost of a product.

### Methods
- Get a product cost adjustment
- List product cost adjustments
- Insert or update product cost adjustment

## PurchaseOrder

A purchase order is for tracking when you purchase goods or services from a vendor, along with associated payments, receiving, and returns.

### Methods
- List purchase orders
- Insert or update purchase order
- Get a purchase order

## SalesOrder

A sales order is for tracking when a customer purchases goods or services from you, along with associated payments, fulfillments, and returns.

### Methods
- Get a sales order
- List sales orders
- Insert or update sales order

## StockAdjustment

A stock adjustment is a document that records some changes to inventory levels.

### Methods
- Get a stock adjustment
- List stock adjustments
- Insert or update a stock adjustment

## StockCount

A stock count is a document that allows you to count the stock in a location.

### Methods
- Get a stock count
- List stock counts
- Insert or update a stock count
- Delete a count sheet
- Get a count sheet
- Insert or update a count sheet

## StockroomScan

### Methods
- List stockroom scans
- Insert or update a stockroom scan

## StockroomUser

A stockroom user is someone who can perform stockroom scans in the inFlow Stockroom mobile app.

### Methods
- Get stockroom users
- List stockroom users

## StockTransfer

A stock transfer is a document that records inventory movements between locations/sublocations.

### Methods
- Get a stock transfer
- List stock transfers
- Insert or update a stock transfer

## TaxCode

A tax code is a named set of percentages for a taxing scheme, e.g. Taxable, Non-Taxable.

### Methods
- Get a tax code
- List tax codes

## TaxingScheme

A taxing scheme is a set of tax rules for sales or purchase orders, e.g. New York City sales tax.

### Methods
- Get a taxing scheme
- List taxing schemes
- Insert or update taxing scheme

## TeamMember

### Methods
- List team members in your inFlow account

## Vendor

A vendor is business (or individual) that you purchase from.

### Methods
- Get a vendor
- List vendors
- Insert or update a vendor

## WebHooks

Subscribe to webhooks to receive notifications when things are updated in inFlow.

### Methods
- List all subscribed webhooks
- Subscribe to a webhook
- Get a webhook subscription
- Unsubscribe from a webhook