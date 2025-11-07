# inFlow Cloud API Documentation

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [API Usage](#api-usage)
- [API Reference](#api-reference)
  - [AdjustmentReason](#adjustmentreason)
  - [Categories](#categories)
  - [Currency](#currency)
  - [Customer](#customer)
  - [CustomFieldDefinitions](#customfielddefinitions)
  - [CustomFields](#customfields)
  - [Location](#location)
  - [ManufacturingOrder](#manufacturingorder)
  - [OperationType](#operationtype)
  - [PaymentTerms](#paymentterms)
  - [PricingScheme](#pricingscheme)
  - [Product](#product)
  - [ProductCostAdjustment](#productcostadjustment)
  - [PurchaseOrder](#purchaseorder)
  - [SalesOrder](#salesorder)
  - [StockAdjustment](#stockadjustment)
  - [StockCount](#stockcount)
  - [StockroomScan](#stockroomscan)
  - [StockroomUser](#stockroomuser)
  - [StockTransfer](#stocktransfer)
  - [TaxCode](#taxcode)
  - [TaxingScheme](#taxingscheme)
  - [TeamMember](#teammember)
  - [Vendor](#vendor)
  - [WebHooks](#webhooks)

## Overview

### Introduction

The inFlow API allows you to read and write data to your inFlow. Like most modern APIs, it's organized around REST and JSON, but there are some concepts to learn.

## Getting Started

### Getting Access to the API

You will need:

- An active inFlow account with the API access add-on, or an inFlow trial
- Administrator rights to that account

Then, you can go to https://app.inflowinventory.com/options/integrations and generate an API key. This API key grants access to your inFlow account (until revoked), so please keep it safe! You will also need your `companyId`, an identifier for your inFlow account, which is also available on that same page in the API keys section once an API key has been generated.

### Support

If you need help, you can email us at support@inflowinventory.com.

Although we will try to maintain API stability and reliability, we cannot make any guarantees.

### Base Endpoint

The base URL for the inFlow API is `https://cloudapi.inflowinventory.com/`. HTTPS is required for security. Most API calls will also need your `companyId` in the route. The API does not support CORS for browser apps.

## Authentication

### Required HTTP Headers

You should set (at least) the following 3 HTTP header fields in your inFlow API calls:

```
Authorization: Bearer {YOUR_API_KEY_HERE}
Content-Type: application/json
Accept: application/json;version=2025-06-24
```

The current API version is `2025-06-24`, which should be included in the Accept HTTP header. From time to time, we may need to make breaking changes on our API. Prior to this, if you have generated an API key, we will email all administrators of your inFlow account with information about this change.

### Optional Headers

There are some headers/tags you can send with your requests that can change default behavior of the API.

#### X-OverrideAllowNegativeInventory

```
X-OverrideAllowNegativeInventory: TRUE
```

Setting this to true, will allow picking an amount of products that would make inventory levels in that location go into a negative quantity. By default this is FALSE and you will receive an error 422 - Negative Inventory if not overridden.

## API Usage

### Read Requests

inFlow API read requests use the HTTP GET verb and return one or more entities in JSON format.

#### Including Related Entities

By default, API calls to fetch an entity (e.g. a product) do not automatically fetch related entities (e.g. product prices or images). You can specify which entities to include by including a query parameter `include`, separating the requested relationship entities with a comma. You can also specify nested relationships with a period.

**Example:**
```
?include=inventoryLines.location,defaultImage
```

#### Filtering

Most API calls that return multiple entities offer several filtering options. Adding these to the query parameters will filter the returned results.

**Example:**
```
?filter[isActive]=true&filter[name]=shirt
```

### Write Requests

inFlow API write requests typically use the PUT HTTP verb and can be used for either inserting or updating entities from the body of the HTTP request.

#### Inserting, Updating, and Identifiers

inFlow entities use a globally unique identifier (GUID), also called a universally unique identifier (UUID). You should generate a new GUID when calling the API to insert a new entity (most programming languages will have a built-in or add-on package to do so), or reference an existing GUID to update an entity.

#### Optional Properties

Most entity properties are optional, and any missing properties will be set to default values when inserting, or left as-is when updating.

#### Timestamps

Many inFlow entities include a timestamp property. This is a machine-readable stamp of when the entity was last modified which can be used for concurrency. If you include the timestamp property in your API write request, your request will fail if the timestamp is no longer the latest version, protecting you against making unintended modifications. To disable this feature, exclude the timestamp property in your API write request.

### Rate Limiting

If you send too many API requests in a short time, the inFlow API will return HTTP status code 429 Too Many Requests.

If you encounter this limit, we encourage you to try to reduce the number of API calls required, or contact us for help if you are unable to do so.

Currently, the limit is set to 60 requests per minute but this is not yet finalized and may change.

---

# API Reference

## AdjustmentReason

Adjustment reasons are pre-defined sets of reasons why stock adjustments may be made.

### Get Adjustment Reason

Relationships can be included via the include query parameter.

**Endpoint:** `GET /{companyId}/adjustment-reasons/{adjustmentReasonId}`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/adjustment-reasons/{adjustmentReasonId}`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |
| `adjustmentReasonId` | string (uuid) | Yes | The AdjustmentReasonId to be fetched |

#### Response

**200 Success**

```json
{
  "attributes": {
    "property1": { },
    "property2": { }
  },
  "relationships": {
    "property1": [],
    "property2": []
  },
  "meta": {
    "property1": { },
    "property2": { }
  }
}
```

### List Adjustment Reasons

Relationships can be included via the include query parameter.

**Endpoint:** `GET /{companyId}/adjustment-reasons`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/adjustment-reasons`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | object (GetCollectionRequest) | Additional query parameter options |

#### Response

**200 Success**

Response Schema: `application/json` (Array)

| Field | Type | Description |
|-------|------|-------------|
| `attributes` | object (Nullable) | |
| `relationships` | object (Nullable) | |
| `meta` | object (Nullable) | |

```json
[
  {
    "attributes": {},
    "relationships": {},
    "meta": {}
  }
]
```

## Categories

A category is used for organizing products. Categories themselves can have parent categories and are arranged hierarchically into a tree structure.

### Get Category

Relationships can be included via the include query parameter.

**Endpoint:** `GET /{companyId}/categories/{categoryId}`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/categories/{categoryId}`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |
| `categoryId` | string (uuid) | Yes | The categoryId to be fetched |

#### Response

**200 Success**

Response Schema: `application/json`

| Field | Type | Description |
|-------|------|-------------|
| `categoryId` | string (uuid) | The primary identifier for this category. Not shown to users |
| `isDefault` | boolean | Only one category, your company-wide default, should have IsDefault = true |
| `name` | string | A human-readable name for this category |
| `parentCategory` | object (Category) Recursive | |
| `parentCategoryId` | string (uuid) Nullable | |
| `timestamp` | string (rowversion) | You can optionally include the last-known timestamp when modifying to protect against concurrent modifications |

```json
{
  "categoryId": "00000000-0000-0000-0000-000000000000",
  "isDefault": true,
  "name": "Bestsellers",
  "parentCategory": { },
  "parentCategoryId": "00000000-0000-0000-0000-000000000000",
  "timestamp": "0000000000310AB6"
}
```

### List Categories

Relationships can be included via the include query parameter.

**Endpoint:** `GET /{companyId}/categories`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/categories`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | object (GetCollectionRequest) | Additional query parameter options |

#### Response

**200 Success**

Response Schema: `application/json` (Array)

| Field | Type | Description |
|-------|------|-------------|
| `categoryId` | string (uuid) | The primary identifier for this category. Not shown to users |
| `isDefault` | boolean | Only one category, your company-wide default, should have IsDefault = true |
| `name` | string | A human-readable name for this category |
| `parentCategory` | object (Category) Recursive | |
| `parentCategoryId` | string (uuid) Nullable | |
| `timestamp` | string (rowversion) | You can optionally include the last-known timestamp when modifying to protect against concurrent modifications |

```json
[
  {
    "categoryId": "00000000-0000-0000-0000-000000000000",
    "isDefault": true,
    "name": "Bestsellers",
    "parentCategory": { },
    "parentCategoryId": "00000000-0000-0000-0000-000000000000",
    "timestamp": "0000000000310AB6"
  }
]
```

## Currency

A currency, e.g. US dollar, Euro, along with its formatting rules. Read-only.

### List Currencies

**Endpoint:** `GET /{companyId}/currencies`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/currencies`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | object (GetCollectionRequest) | Additional query parameter options |

#### Response

**200 Success**

Response Schema: `application/json` (Array)

| Field | Type | Description |
|-------|------|-------------|
| `currencyConversions` | Array of objects | A list of conversion rates related to this currency |
| `currencyId` | string (uuid) | The primary identifier for this currency. Not shown to users |
| `decimalPlaces` | integer (int32) | The number of decimal places typically shown with this currency |
| `decimalSeparator` | string | The symbol used to separate decimals with this currency |
| `isSymbolFirst` | boolean | Whether the symbol is shown prior to the numerical value for this currency |
| `isoCode` | string | The ISO 4217 code for this currency |
| `name` | string | A descriptive name of this currency |
| `negativeType` | string | How negative numbers are shown for this currency. Enum: "Leading", "LeadingInsideSymbol", "TrailingInsideSymbol", "Trailing", "Bracketed" |
| `symbol` | string | A short symbol representing this currency |
| `thousandsSeparator` | string | The symbol used to separate thousands with this currency |
| `timestamp` | string (rowversion) | You can optionally include the last-known timestamp when modifying to protect against concurrent modifications |

```json
[
  {
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
  }
]
```

### Get Currency

**Endpoint:** `GET /{companyId}/currencies/{currencyId}`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/currencies/{currencyId}`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |
| `currencyId` | string (uuid) | Yes | The currencyId to be fetched |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | object (GetDetailsRequest) | Additional query parameter options |

#### Response

**200 Success**

Response Schema: `application/json`

| Field | Type | Description |
|-------|------|-------------|
| `currencyConversions` | Array of objects | A list of conversion rates related to this currency |
| `currencyId` | string (uuid) | The primary identifier for this currency. Not shown to users |
| `decimalPlaces` | integer (int32) | The number of decimal places typically shown with this currency |
| `decimalSeparator` | string | The symbol used to separate decimals with this currency |
| `isSymbolFirst` | boolean | Whether the symbol is shown prior to the numerical value for this currency |
| `isoCode` | string | The ISO 4217 code for this currency |
| `name` | string | A descriptive name of this currency |
| `negativeType` | string | How negative numbers are shown for this currency. Enum: "Leading", "LeadingInsideSymbol", "TrailingInsideSymbol", "Trailing", "Bracketed" |
| `symbol` | string | A short symbol representing this currency |
| `thousandsSeparator` | string | The symbol used to separate thousands with this currency |
| `timestamp` | string (rowversion) | You can optionally include the last-known timestamp when modifying to protect against concurrent modifications |

```json
{
  "currencyConversions": [
    {}
  ],
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
}
```

## Customer

A customer is an individual or business that you sell to.

### Get Customer

Relationships can be included via the include query parameter.

**Endpoint:** `GET /{companyId}/customers/{customerId}`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/customers/{customerId}`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |
| `customerId` | string (uuid) | Yes | The customerId to be fetched |

#### Response

**200 Success**

Response Schema: `application/json`

| Field | Type | Description |
|-------|------|-------------|
| `addresses` | Array of objects | All addresses for this customer |
| `balances` | Array of objects | How much this customer owes you (potentially in one or more currencies) |
| `contactName` | string | Name of your primary contact for this customer (if it's a business) |
| `credits` | Array of objects | How much in store credit this customer has with you (potentially in one or more currencies) |
| `customFields` | object (LargeCustomFieldValues) | |
| `customerId` | string (uuid) | The primary identifier for this customer. When inserting, you should specify this by generating a GUID. Not shown to users |
| `defaultBillingAddress` | object (CustomerAddress) | |
| `defaultBillingAddressId` | string (uuid) Nullable | |
| `defaultCarrier` | string | The default shipment method for this customer |
| `defaultLocation` | object (Location) | |
| `defaultLocationId` | string (uuid) Nullable | |
| `defaultPaymentMethod` | string | The default payment method that this customer uses to pay you for sales orders |
| `defaultPaymentTerms` | object (PaymentTerms) | |
| `defaultPaymentTermsId` | string (uuid) Nullable | |
| `defaultSalesRep` | string | The sales rep for your company that should be assigned to orders from this customer by default |
| `defaultSalesRepTeamMember` | object (TeamMember) | |
| `defaultSalesRepTeamMemberId` | string (uuid) Nullable | |
| `defaultShippingAddress` | object (CustomerAddress) | |
| `defaultShippingAddressId` | string (uuid) Nullable | |
| `discount` | string (decimal) | Percentage discount that you give by default on orders by this customer |
| `dues` | Array of objects | How much this customer owes you (potentially in one or more currencies) |
| `email` | string | Primary contact email for this customer |
| `fax` | string | Fax number for this customer |
| `isActive` | boolean | Customers with IsActive = false are deactivated and hidden away for new usage |
| `lastModifiedBy` | object (TeamMember) | |
| `lastModifiedById` | string (uuid) | The inFlow Team Member, system process, or API key that last modified this customer. This is set automatically, and cannot be set through the API |
| `lastModifiedDttm` | string (date-time) | The DateTimeOffset when this customer was last modified. This is set automatically, and cannot be set through the API |
| `name` | string | Customer's name (human-readable, typically a person or business name) |
| `orderHistory` | object (CustomerOrderHistory) | |
| `phone` | string | Phone number for this customer |
| `pricingScheme` | object (PricingScheme) | |
| `pricingSchemeId` | string (uuid) Nullable | |
| `remarks` | string | Any additional remarks regarding this customer |
| `taxExemptNumber` | string | A government number/identifier documenting why this customer has special tax privileges |
| `taxingScheme` | object (TaxingScheme) | |
| `taxingSchemeId` | string (uuid) Nullable | |
| `timestamp` | string (rowversion) | You can optionally include the last-known timestamp when modifying to protect against concurrent modifications |
| `website` | string | Customer's website |

### List Customers

Relationships can be included via the include query parameter.

**Endpoint:** `GET /{companyId}/customers`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/customers`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | object (GetCollectionRequest) | Additional query parameter options |

#### Filtering Options

- `filter[name]`
- `filter[contactName]`
- `filter[phone]`
- `filter[email]`
- `filter[website]`
- `filter[address]`
- `filter[city]`
- `filter[state]`
- `filter[postalCode]`
- `filter[country]`
- `filter[pricingSchemeId]`
- `filter[defaultLocationId]`
- `filter[isActive]`
- `filter[smart]` (search across name and contact name)
- `filter[lastOrder]` (number of days since the customer has last ordered)

### Insert or Update Customer

`customerId` property is required, please generate a GUID when inserting.

**Endpoint:** `PUT /{companyId}/customers`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/customers`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |

#### Request Body

A customer to insert or update (see response schema for structure)

## Product

A product is a type of physical good or service (depending on ItemType) whose cost, inventory levels, sales, and movements can be tracked in inFlow.

### Get Product

Relationships can be included via the include query parameter.

**Endpoint:** `GET /{companyId}/products/{productId}`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/products/{productId}`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |
| `productId` | string (uuid) | Yes | The productId to be fetched |

### List Products

Relationships can be included via the include query parameter.

**Endpoint:** `GET /{companyId}/products`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/products`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | object (GetCollectionRequest) | Additional query parameter options |

#### Filtering Options

- `filter[name]`
- `filter[description]`
- `filter[isActive]`
- `filter[barcode]`
- `filter[itemType]`
- `filter[categoryId]`
- `filter[lastModifiedDateTime]` (Ex. `filter[lastModifiedDateTime]={"fromDate":"2022-01-01", "toDate":"2023-01-01"}`)
- `filter[smart]` (full-text search on name, description, category, barcode and SKU)

### Insert or Update Product

`productId` property is required, please generate a GUID when inserting.

**Endpoint:** `PUT /{companyId}/products`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/products`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |

### Get Product Inventory Summary

**Endpoint:** `GET /{companyId}/products/{productId}/summary`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/products/{productId}/summary`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |
| `productId` | string (uuid) | Yes | The productId to fetch information for |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `locationId` | string (uuid) Nullable | (Optional) the locationId to fetch information for |

### Get Multiple Product Inventory Summaries

**Endpoint:** `POST /{companyId}/products/summary`

**URL:** `https://cloudapi.inflowinventory.com/{companyId}/products/summary`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companyId` | string (uuid) | Yes | Your inFlow account companyId |

#### Request Body

The product id, location id combinations to fetch information for. Up to 100 at a time.

```json
[
  {
    "productId": "string",
    "locationId": "string"
  }
]
```

---

*Note: This documentation continues with additional endpoints for Location, ManufacturingOrder, PurchaseOrder, SalesOrder, StockAdjustment, StockCount, StockTransfer, TaxCode, TaxingScheme, TeamMember, Vendor, and WebHooks. Each section follows the same structured format with proper markdown hierarchy, clear endpoint definitions, parameter tables, and response schemas.*

---

**Documentation Powered by ReDoc**
