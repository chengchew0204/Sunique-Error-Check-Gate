Product
A product is a type of physical good or service (depending on ItemType) whose cost, inventory levels, sales, and movements can be tracked in inFlow.

Get a product
Relationships can be included via the include query parameter.

path Parameters
companyId
required
string <uuid>
Your inFlow account companyId

productId
required
string <uuid>
The productId to be fetched

Responses
200 Success
Response Schema: application/json
autoAssemble	
boolean
Only relevant for products with a bill of materials. Whether this product should be automatically by manufacture order when it's picked from a location where it's not in stock.

category	
object (Category)
categoryId	
string <uuid>
cost	
object (ProductCost)
customFields	
object (LargeCustomFieldValues)
defaultImage	
object (Image)
defaultImageId	
string <uuid> Nullable
defaultPrice	
object (ProductPrice)
description	
string
A human-readable description for this product.

height	
string <decimal> Nullable
Height of this product (unit depends on global setting)

hsTariffNumber	
string
Harmonized Tariff Schedule code for customs when exporting this item. Used to pre-fill for customs forms when shipping.

images	
Array of objects
includeQuantityBuildable	
boolean
Only relevant for products with a bill of materials. Whether this product should add the Quantity Buildable when showing quantities.

inventoryLines	
Array of objects
isActive	
boolean
Products with IsActive = false are deactivated and hidden away for future usage.

isManufacturable	
boolean
Whether this product can be manufactured. This is a read-only property that is calculated based on whether this product has a bill of materials defined.

itemBoms	
Array of objects
itemType	
string
Enum: "StockedProduct" "NonstockedProduct" "Service"
The type of this item. Cannot be changed once set. Stocked Product is most common.

lastModifiedBy	
object (TeamMember)
lastModifiedById	
string <uuid>
The inFlow Team Member, system process, or API key that last modified this product. This is set automatically, and cannot be set through the API.

lastModifiedDateTime	
string <date-time>
Last modified datetime of this product.

lastVendor	
object (Vendor)
lastVendorId	
string <uuid> Nullable
length	
string <decimal> Nullable
Length of this product (unit depends on global setting)

name	
string
An item name or title that should be human readable. Must be unique.

originCountry	
string
2-character country code for country of origin. Used to pre-fill for customs forms when shipping.

prices	
Array of objects
productBarcodes	
Array of objects
productId	
string <uuid>
The primary identifier for this product. When inserting, you should specify this by generating a GUID. Not shown to users

productOperations	
Array of objects
purchasingUom	
object (UnitOfMeasure)
remarks	
string
A space for any extra remarks about this product.

reorderSettings	
Array of objects
salesUom	
object (UnitOfMeasure)
sku	
string
A SKU (stock-keeping-unit) code that represents a product in a concise, machine-friendly, way. Optional, but must be unique if specified.

standardUomName	
string
Standard unit of measure for tracking this product

taxCodes	
Array of objects
timestamp	
string <rowversion>
You can optionally include the last-known timestamp when modifying to protect against concurrent modifications.

totalQuantityOnHand	
string <decimal>
The total inventory quantity on hand across all locations for this product. Note that the InventoryLines relationship must be included for this attribute to be populated.

trackSerials	
boolean
Whether this product requires serial numbers. Cannot be changed once set. Only possible for Stocked Products.

vendorItems	
Array of objects
A list of vendors that sell this item to you

weight	
string <decimal> Nullable
Weight of this product (unit depends on global setting)

width	
string <decimal> Nullable
Width of this product (unit depends on global setting)

get
/{companyId}/products/{productId}
https://cloudapi.inflowinventory.com/{companyId}/products/{productId}
Response samples
200
Content type
application/json
Copy
Expand allCollapse all
{
"autoAssemble": true,
"category": {
"categoryId": "00000000-0000-0000-0000-000000000000",
"isDefault": true,
"name": "Bestsellers",
"parentCategory": { },
"parentCategoryId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6"
},
"categoryId": "00000000-0000-0000-0000-000000000000",
"cost": {
"cost": "19.99",
"product": { },
"productCostId": "string",
"productId": "00000000-0000-0000-0000-000000000000"
},
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
"defaultImage": {
"imageId": "00000000-0000-0000-0000-000000000000",
"largeUrl": "string",
"mediumUncroppedUrl": "string",
"mediumUrl": "string",
"originalUrl": "string",
"smallUrl": "string",
"thumbUrl": "string"
},
"defaultImageId": "00000000-0000-0000-0000-000000000000",
"defaultPrice": {
"fixedMarkup": "19.99",
"priceType": "FixedPrice",
"pricingScheme": {},
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"product": { },
"productId": "00000000-0000-0000-0000-000000000000",
"productPriceId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"unitPrice": "19.99"
},
"description": "Red toy sports car",
"height": "19.99",
"hsTariffNumber": "string",
"images": [
{}
],
"includeQuantityBuildable": true,
"inventoryLines": [
{}
],
"isActive": true,
"isManufacturable": true,
"itemBoms": [
{}
],
"itemType": "StockedProduct",
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
"lastModifiedDateTime": "2020-01-31",
"lastVendor": {
"addresses": [],
"balances": [],
"contactName": "John Smith",
"credits": [],
"currency": {},
"currencyId": "00000000-0000-0000-0000-000000000000",
"customFields": {},
"defaultAddress": {},
"defaultAddressId": "00000000-0000-0000-0000-000000000000",
"defaultCarrier": "FedEx",
"defaultPaymentMethod": "Mastercard",
"defaultPaymentTerms": {},
"defaultPaymentTermsId": "00000000-0000-0000-0000-000000000000",
"discount": "10",
"dues": [],
"email": "john@acmewidget.com",
"fax": "555-123-4567",
"isActive": true,
"isTaxInclusivePricing": true,
"lastModifiedBy": {},
"lastModifiedById": "00000000-0000-0000-0000-000000000000",
"lastModifiedDttm": "2020-01-31",
"leadTimeDays": 14,
"name": "Acme Widget Co.",
"phone": "555-123-4567",
"remarks": "string",
"taxingScheme": {},
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"vendorId": "00000000-0000-0000-0000-000000000000",
"vendorItems": [],
"website": "www.acmewidget.com"
},
"lastVendorId": "00000000-0000-0000-0000-000000000000",
"length": "19.99",
"name": "1948 6\" Toy Car - Red",
"originCountry": "string",
"prices": [
{}
],
"productBarcodes": [
{}
],
"productId": "00000000-0000-0000-0000-000000000000",
"productOperations": [
{}
],
"purchasingUom": {
"conversionRatio": {},
"name": "string"
},
"remarks": "string",
"reorderSettings": [
{}
],
"salesUom": {
"conversionRatio": {},
"name": "string"
},
"sku": "CAR-1948-R",
"standardUomName": "\"ea.\"",
"taxCodes": [
{}
],
"timestamp": "0000000000310AB6",
"totalQuantityOnHand": "19.99",
"trackSerials": true,
"vendorItems": [
{}
],
"weight": "19.99",
"width": "19.99"
}
List products
Relationships can be included via the include query parameter.
Options for filtering this list:
filter[name]
filter[description]
filter[isActive]
filter[barcode]
filter[itemType]
filter[categoryId]
filter[lastModifiedDateTime] (Ex. filter[lastModifiedDateTime]={"fromDate":"2022-01-01", "toDate":"2023-01-01"})
filter[smart] (full-text search on name, description, category, barcode and SKU)

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
autoAssemble	
boolean
Only relevant for products with a bill of materials. Whether this product should be automatically by manufacture order when it's picked from a location where it's not in stock.

category	
object (Category)
categoryId	
string <uuid>
cost	
object (ProductCost)
customFields	
object (LargeCustomFieldValues)
defaultImage	
object (Image)
defaultImageId	
string <uuid> Nullable
defaultPrice	
object (ProductPrice)
description	
string
A human-readable description for this product.

height	
string <decimal> Nullable
Height of this product (unit depends on global setting)

hsTariffNumber	
string
Harmonized Tariff Schedule code for customs when exporting this item. Used to pre-fill for customs forms when shipping.

images	
Array of objects
includeQuantityBuildable	
boolean
Only relevant for products with a bill of materials. Whether this product should add the Quantity Buildable when showing quantities.

inventoryLines	
Array of objects
isActive	
boolean
Products with IsActive = false are deactivated and hidden away for future usage.

isManufacturable	
boolean
Whether this product can be manufactured. This is a read-only property that is calculated based on whether this product has a bill of materials defined.

itemBoms	
Array of objects
itemType	
string
Enum: "StockedProduct" "NonstockedProduct" "Service"
The type of this item. Cannot be changed once set. Stocked Product is most common.

lastModifiedBy	
object (TeamMember)
lastModifiedById	
string <uuid>
The inFlow Team Member, system process, or API key that last modified this product. This is set automatically, and cannot be set through the API.

lastModifiedDateTime	
string <date-time>
Last modified datetime of this product.

lastVendor	
object (Vendor)
lastVendorId	
string <uuid> Nullable
length	
string <decimal> Nullable
Length of this product (unit depends on global setting)

name	
string
An item name or title that should be human readable. Must be unique.

originCountry	
string
2-character country code for country of origin. Used to pre-fill for customs forms when shipping.

prices	
Array of objects
productBarcodes	
Array of objects
productId	
string <uuid>
The primary identifier for this product. When inserting, you should specify this by generating a GUID. Not shown to users

productOperations	
Array of objects
purchasingUom	
object (UnitOfMeasure)
remarks	
string
A space for any extra remarks about this product.

reorderSettings	
Array of objects
salesUom	
object (UnitOfMeasure)
sku	
string
A SKU (stock-keeping-unit) code that represents a product in a concise, machine-friendly, way. Optional, but must be unique if specified.

standardUomName	
string
Standard unit of measure for tracking this product

taxCodes	
Array of objects
timestamp	
string <rowversion>
You can optionally include the last-known timestamp when modifying to protect against concurrent modifications.

totalQuantityOnHand	
string <decimal>
The total inventory quantity on hand across all locations for this product. Note that the InventoryLines relationship must be included for this attribute to be populated.

trackSerials	
boolean
Whether this product requires serial numbers. Cannot be changed once set. Only possible for Stocked Products.

vendorItems	
Array of objects
A list of vendors that sell this item to you

weight	
string <decimal> Nullable
Weight of this product (unit depends on global setting)

width	
string <decimal> Nullable
Width of this product (unit depends on global setting)

get
/{companyId}/products
https://cloudapi.inflowinventory.com/{companyId}/products
Response samples
200
Content type
application/json
Copy
Expand allCollapse all
[
{
"autoAssemble": true,
"category": {},
"categoryId": "00000000-0000-0000-0000-000000000000",
"cost": {},
"customFields": {},
"defaultImage": {},
"defaultImageId": "00000000-0000-0000-0000-000000000000",
"defaultPrice": {},
"description": "Red toy sports car",
"height": "19.99",
"hsTariffNumber": "string",
"images": [],
"includeQuantityBuildable": true,
"inventoryLines": [],
"isActive": true,
"isManufacturable": true,
"itemBoms": [],
"itemType": "StockedProduct",
"lastModifiedBy": {},
"lastModifiedById": "00000000-0000-0000-0000-000000000000",
"lastModifiedDateTime": "2020-01-31",
"lastVendor": {},
"lastVendorId": "00000000-0000-0000-0000-000000000000",
"length": "19.99",
"name": "1948 6\" Toy Car - Red",
"originCountry": "string",
"prices": [],
"productBarcodes": [],
"productId": "00000000-0000-0000-0000-000000000000",
"productOperations": [],
"purchasingUom": {},
"remarks": "string",
"reorderSettings": [],
"salesUom": {},
"sku": "CAR-1948-R",
"standardUomName": "\"ea.\"",
"taxCodes": [],
"timestamp": "0000000000310AB6",
"totalQuantityOnHand": "19.99",
"trackSerials": true,
"vendorItems": [],
"weight": "19.99",
"width": "19.99"
}
]
Insert or update product
productId property is required, please generate a GUID when inserting.

path Parameters
companyId
required
string <uuid>
Your inFlow account companyId

Request Body schema: application/json
A product to insert or update

autoAssemble	
boolean
Only relevant for products with a bill of materials. Whether this product should be automatically by manufacture order when it's picked from a location where it's not in stock.

category	
object (Category)
categoryId	
string <uuid>
cost	
object (ProductCost)
customFields	
object (LargeCustomFieldValues)
defaultImage	
object (Image)
defaultImageId	
string <uuid> Nullable
defaultPrice	
object (ProductPrice)
description	
string
A human-readable description for this product.

height	
string <decimal> Nullable
Height of this product (unit depends on global setting)

hsTariffNumber	
string
Harmonized Tariff Schedule code for customs when exporting this item. Used to pre-fill for customs forms when shipping.

images	
Array of objects
includeQuantityBuildable	
boolean
Only relevant for products with a bill of materials. Whether this product should add the Quantity Buildable when showing quantities.

inventoryLines	
Array of objects
isActive	
boolean
Products with IsActive = false are deactivated and hidden away for future usage.

isManufacturable	
boolean
Whether this product can be manufactured. This is a read-only property that is calculated based on whether this product has a bill of materials defined.

itemBoms	
Array of objects
itemType	
string
Enum: "StockedProduct" "NonstockedProduct" "Service"
The type of this item. Cannot be changed once set. Stocked Product is most common.

lastModifiedBy	
object (TeamMember)
lastModifiedById	
string <uuid>
The inFlow Team Member, system process, or API key that last modified this product. This is set automatically, and cannot be set through the API.

lastModifiedDateTime	
string <date-time>
Last modified datetime of this product.

lastVendor	
object (Vendor)
lastVendorId	
string <uuid> Nullable
length	
string <decimal> Nullable
Length of this product (unit depends on global setting)

name	
string
An item name or title that should be human readable. Must be unique.

originCountry	
string
2-character country code for country of origin. Used to pre-fill for customs forms when shipping.

prices	
Array of objects
productBarcodes	
Array of objects
productId	
string <uuid>
The primary identifier for this product. When inserting, you should specify this by generating a GUID. Not shown to users

productOperations	
Array of objects
purchasingUom	
object (UnitOfMeasure)
remarks	
string
A space for any extra remarks about this product.

reorderSettings	
Array of objects
salesUom	
object (UnitOfMeasure)
sku	
string
A SKU (stock-keeping-unit) code that represents a product in a concise, machine-friendly, way. Optional, but must be unique if specified.

standardUomName	
string
Standard unit of measure for tracking this product

taxCodes	
Array of objects
timestamp	
string <rowversion>
You can optionally include the last-known timestamp when modifying to protect against concurrent modifications.

totalQuantityOnHand	
string <decimal>
The total inventory quantity on hand across all locations for this product. Note that the InventoryLines relationship must be included for this attribute to be populated.

trackSerials	
boolean
Whether this product requires serial numbers. Cannot be changed once set. Only possible for Stocked Products.

vendorItems	
Array of objects
A list of vendors that sell this item to you

weight	
string <decimal> Nullable
Weight of this product (unit depends on global setting)

width	
string <decimal> Nullable
Width of this product (unit depends on global setting)

Responses
200 Success
Response Schema: application/json
autoAssemble	
boolean
Only relevant for products with a bill of materials. Whether this product should be automatically by manufacture order when it's picked from a location where it's not in stock.

category	
object (Category)
categoryId	
string <uuid>
cost	
object (ProductCost)
customFields	
object (LargeCustomFieldValues)
defaultImage	
object (Image)
defaultImageId	
string <uuid> Nullable
defaultPrice	
object (ProductPrice)
description	
string
A human-readable description for this product.

height	
string <decimal> Nullable
Height of this product (unit depends on global setting)

hsTariffNumber	
string
Harmonized Tariff Schedule code for customs when exporting this item. Used to pre-fill for customs forms when shipping.

images	
Array of objects
includeQuantityBuildable	
boolean
Only relevant for products with a bill of materials. Whether this product should add the Quantity Buildable when showing quantities.

inventoryLines	
Array of objects
isActive	
boolean
Products with IsActive = false are deactivated and hidden away for future usage.

isManufacturable	
boolean
Whether this product can be manufactured. This is a read-only property that is calculated based on whether this product has a bill of materials defined.

itemBoms	
Array of objects
itemType	
string
Enum: "StockedProduct" "NonstockedProduct" "Service"
The type of this item. Cannot be changed once set. Stocked Product is most common.

lastModifiedBy	
object (TeamMember)
lastModifiedById	
string <uuid>
The inFlow Team Member, system process, or API key that last modified this product. This is set automatically, and cannot be set through the API.

lastModifiedDateTime	
string <date-time>
Last modified datetime of this product.

lastVendor	
object (Vendor)
lastVendorId	
string <uuid> Nullable
length	
string <decimal> Nullable
Length of this product (unit depends on global setting)

name	
string
An item name or title that should be human readable. Must be unique.

originCountry	
string
2-character country code for country of origin. Used to pre-fill for customs forms when shipping.

prices	
Array of objects
productBarcodes	
Array of objects
productId	
string <uuid>
The primary identifier for this product. When inserting, you should specify this by generating a GUID. Not shown to users

productOperations	
Array of objects
purchasingUom	
object (UnitOfMeasure)
remarks	
string
A space for any extra remarks about this product.

reorderSettings	
Array of objects
salesUom	
object (UnitOfMeasure)
sku	
string
A SKU (stock-keeping-unit) code that represents a product in a concise, machine-friendly, way. Optional, but must be unique if specified.

standardUomName	
string
Standard unit of measure for tracking this product

taxCodes	
Array of objects
timestamp	
string <rowversion>
You can optionally include the last-known timestamp when modifying to protect against concurrent modifications.

totalQuantityOnHand	
string <decimal>
The total inventory quantity on hand across all locations for this product. Note that the InventoryLines relationship must be included for this attribute to be populated.

trackSerials	
boolean
Whether this product requires serial numbers. Cannot be changed once set. Only possible for Stocked Products.

vendorItems	
Array of objects
A list of vendors that sell this item to you

weight	
string <decimal> Nullable
Weight of this product (unit depends on global setting)

width	
string <decimal> Nullable
Width of this product (unit depends on global setting)

put
/{companyId}/products
https://cloudapi.inflowinventory.com/{companyId}/products
Request samples
Payload
Content type
application/json
Copy
Expand allCollapse all
{
"autoAssemble": true,
"category": {
"categoryId": "00000000-0000-0000-0000-000000000000",
"isDefault": true,
"name": "Bestsellers",
"parentCategory": { },
"parentCategoryId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6"
},
"categoryId": "00000000-0000-0000-0000-000000000000",
"cost": {
"cost": "19.99",
"product": { },
"productCostId": "string",
"productId": "00000000-0000-0000-0000-000000000000"
},
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
"defaultImage": {
"imageId": "00000000-0000-0000-0000-000000000000",
"largeUrl": "string",
"mediumUncroppedUrl": "string",
"mediumUrl": "string",
"originalUrl": "string",
"smallUrl": "string",
"thumbUrl": "string"
},
"defaultImageId": "00000000-0000-0000-0000-000000000000",
"defaultPrice": {
"fixedMarkup": "19.99",
"priceType": "FixedPrice",
"pricingScheme": {},
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"product": { },
"productId": "00000000-0000-0000-0000-000000000000",
"productPriceId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"unitPrice": "19.99"
},
"description": "Red toy sports car",
"height": "19.99",
"hsTariffNumber": "string",
"images": [
{}
],
"includeQuantityBuildable": true,
"inventoryLines": [
{}
],
"isActive": true,
"isManufacturable": true,
"itemBoms": [
{}
],
"itemType": "StockedProduct",
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
"lastModifiedDateTime": "2020-01-31",
"lastVendor": {
"addresses": [],
"balances": [],
"contactName": "John Smith",
"credits": [],
"currency": {},
"currencyId": "00000000-0000-0000-0000-000000000000",
"customFields": {},
"defaultAddress": {},
"defaultAddressId": "00000000-0000-0000-0000-000000000000",
"defaultCarrier": "FedEx",
"defaultPaymentMethod": "Mastercard",
"defaultPaymentTerms": {},
"defaultPaymentTermsId": "00000000-0000-0000-0000-000000000000",
"discount": "10",
"dues": [],
"email": "john@acmewidget.com",
"fax": "555-123-4567",
"isActive": true,
"isTaxInclusivePricing": true,
"lastModifiedBy": {},
"lastModifiedById": "00000000-0000-0000-0000-000000000000",
"lastModifiedDttm": "2020-01-31",
"leadTimeDays": 14,
"name": "Acme Widget Co.",
"phone": "555-123-4567",
"remarks": "string",
"taxingScheme": {},
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"vendorId": "00000000-0000-0000-0000-000000000000",
"vendorItems": [],
"website": "www.acmewidget.com"
},
"lastVendorId": "00000000-0000-0000-0000-000000000000",
"length": "19.99",
"name": "1948 6\" Toy Car - Red",
"originCountry": "string",
"prices": [
{}
],
"productBarcodes": [
{}
],
"productId": "00000000-0000-0000-0000-000000000000",
"productOperations": [
{}
],
"purchasingUom": {
"conversionRatio": {},
"name": "string"
},
"remarks": "string",
"reorderSettings": [
{}
],
"salesUom": {
"conversionRatio": {},
"name": "string"
},
"sku": "CAR-1948-R",
"standardUomName": "\"ea.\"",
"taxCodes": [
{}
],
"timestamp": "0000000000310AB6",
"totalQuantityOnHand": "19.99",
"trackSerials": true,
"vendorItems": [
{}
],
"weight": "19.99",
"width": "19.99"
}
Response samples
200
Content type
application/json
Copy
Expand allCollapse all
{
"autoAssemble": true,
"category": {
"categoryId": "00000000-0000-0000-0000-000000000000",
"isDefault": true,
"name": "Bestsellers",
"parentCategory": { },
"parentCategoryId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6"
},
"categoryId": "00000000-0000-0000-0000-000000000000",
"cost": {
"cost": "19.99",
"product": { },
"productCostId": "string",
"productId": "00000000-0000-0000-0000-000000000000"
},
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
"defaultImage": {
"imageId": "00000000-0000-0000-0000-000000000000",
"largeUrl": "string",
"mediumUncroppedUrl": "string",
"mediumUrl": "string",
"originalUrl": "string",
"smallUrl": "string",
"thumbUrl": "string"
},
"defaultImageId": "00000000-0000-0000-0000-000000000000",
"defaultPrice": {
"fixedMarkup": "19.99",
"priceType": "FixedPrice",
"pricingScheme": {},
"pricingSchemeId": "00000000-0000-0000-0000-000000000000",
"product": { },
"productId": "00000000-0000-0000-0000-000000000000",
"productPriceId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"unitPrice": "19.99"
},
"description": "Red toy sports car",
"height": "19.99",
"hsTariffNumber": "string",
"images": [
{}
],
"includeQuantityBuildable": true,
"inventoryLines": [
{}
],
"isActive": true,
"isManufacturable": true,
"itemBoms": [
{}
],
"itemType": "StockedProduct",
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
"lastModifiedDateTime": "2020-01-31",
"lastVendor": {
"addresses": [],
"balances": [],
"contactName": "John Smith",
"credits": [],
"currency": {},
"currencyId": "00000000-0000-0000-0000-000000000000",
"customFields": {},
"defaultAddress": {},
"defaultAddressId": "00000000-0000-0000-0000-000000000000",
"defaultCarrier": "FedEx",
"defaultPaymentMethod": "Mastercard",
"defaultPaymentTerms": {},
"defaultPaymentTermsId": "00000000-0000-0000-0000-000000000000",
"discount": "10",
"dues": [],
"email": "john@acmewidget.com",
"fax": "555-123-4567",
"isActive": true,
"isTaxInclusivePricing": true,
"lastModifiedBy": {},
"lastModifiedById": "00000000-0000-0000-0000-000000000000",
"lastModifiedDttm": "2020-01-31",
"leadTimeDays": 14,
"name": "Acme Widget Co.",
"phone": "555-123-4567",
"remarks": "string",
"taxingScheme": {},
"taxingSchemeId": "00000000-0000-0000-0000-000000000000",
"timestamp": "0000000000310AB6",
"vendorId": "00000000-0000-0000-0000-000000000000",
"vendorItems": [],
"website": "www.acmewidget.com"
},
"lastVendorId": "00000000-0000-0000-0000-000000000000",
"length": "19.99",
"name": "1948 6\" Toy Car - Red",
"originCountry": "string",
"prices": [
{}
],
"productBarcodes": [
{}
],
"productId": "00000000-0000-0000-0000-000000000000",
"productOperations": [
{}
],
"purchasingUom": {
"conversionRatio": {},
"name": "string"
},
"remarks": "string",
"reorderSettings": [
{}
],
"salesUom": {
"conversionRatio": {},
"name": "string"
},
"sku": "CAR-1948-R",
"standardUomName": "\"ea.\"",
"taxCodes": [
{}
],
"timestamp": "0000000000310AB6",
"totalQuantityOnHand": "19.99",
"trackSerials": true,
"vendorItems": [
{}
],
"weight": "19.99",
"width": "19.99"
}
Get product inventory summary
path Parameters
companyId
required
string <uuid>
Your inFlow account companyId

productId
required
string <uuid>
The productId to fetch information for

query Parameters
locationId	
string <uuid> Nullable
(Optional) the locationId to fetch information for

Responses
200 Success
Response Schema: application/json
productId	
string <uuid>
The product whose inventory is being represented here

locationId	
string <uuid> Nullable
The location whose inventory is being represented here, or null if this is a summary across all locations

imageSmallUrl	
string Nullable
URL for a small image of the product

quantityOnHand	
number <double> Nullable
This number is the total you have physically available (including Qty reserved) minus any items that have already been picked in a sales order (i.e. what’s still on your warehouse shelves).

quantityOnOrder	
number <double> Nullable
This number is how many you've ordered but haven't received.

quantityOnPurchaseOrder	
number <double> Nullable
A breakdown of QuantityOnOrder into only those ordered from vendors but haven't received.

quantityOnWorkOrder	
number <double> Nullable
A breakdown of QuantityOnOrder into only those on manufacture orders that haven't been finished yet.

quantityOnTransferOrder	
number <double> Nullable
A breakdown of QuantityOnOrder into only those expected to be received on a stock transfer (only when a locationId is specified).

quantityReserved	
number <double>
This number is the total stock reserved for use that haven't been picked or used yet.

quantityReservedForSales	
number <double>
A breakdown of QuantityReserved into only those reserved for sales orders.

quantityReservedForManufacturing	
number <double>
A breakdown of QuantityReserved into only those reserved for raw materials of manufacture orders.

quantityReservedForTransfers	
number <double>
A breakdown of QuantityReserved into only those reserved to be picked for a stock transfer (only when a locationId is specified).

quantityReservedForBuilds	
number <double>
A breakdown of QuantityReserved into only those parts needed for bills of materials on products with negative anticipated inventory.

quantityAvailable	
number <double>
This number is how many of the products you’ll have left if you fulfill all open outgoing orders. This may include QuantityBuildable (for manufactured products set to combine quantities) and QuantityReservedForBuilds.

rawQuantityAvailable	
number <double>
This number is how many of the products you’ll have left if you fulfill all open outgoing orders, excluding QuantityBuildable and QuantityReservedForBuilds.

quantityPicked	
number <double> Nullable
This number is the total that has already been picked in sales orders/work orders and is awaiting shipment (think of them as sitting in a box waiting to be shipped out).

quantityInTransit	
number <double> Nullable
These are specific items that have been sent via Transfer Stock and are still in the Transit status (i.e. you’ve sent the transfer, but it has not been received at the other location yet).

quantityBuildable	
number <double> Nullable
For manufactured products, the quantity buildable is how many units can be built based on the stock of raw materials. If this is blank, then it means can infinite can be built (e.g. if it's composed only of services).

get
/{companyId}/products/{productId}/summary
https://cloudapi.inflowinventory.com/{companyId}/products/{productId}/summary
Response samples
200
Content type
application/json
Copy
Expand allCollapse all
{
"productId": "string",
"locationId": "string",
"imageSmallUrl": "string",
"quantityOnHand": 0,
"quantityOnOrder": 0,
"quantityOnPurchaseOrder": 0,
"quantityOnWorkOrder": 0,
"quantityOnTransferOrder": 0,
"quantityReserved": 0,
"quantityReservedForSales": 0,
"quantityReservedForManufacturing": 0,
"quantityReservedForTransfers": 0,
"quantityReservedForBuilds": 0,
"quantityAvailable": 0,
"rawQuantityAvailable": 0,
"quantityPicked": 0,
"quantityInTransit": 0,
"quantityBuildable": 0
}
Get multiple product inventory summaries
path Parameters
companyId
required
string <uuid>
Your inFlow account companyId

Request Body schema: application/json
The product id, location id combinations to fetch information for. Up to 100 at a time

Array 
productId	
string <uuid>
locationId	
string <uuid> Nullable
Responses
200 Success
Response Schema: application/json
Array 
productId	
string <uuid>
The product whose inventory is being represented here

locationId	
string <uuid> Nullable
The location whose inventory is being represented here, or null if this is a summary across all locations

imageSmallUrl	
string Nullable
URL for a small image of the product

quantityOnHand	
number <double> Nullable
This number is the total you have physically available (including Qty reserved) minus any items that have already been picked in a sales order (i.e. what’s still on your warehouse shelves).

quantityOnOrder	
number <double> Nullable
This number is how many you've ordered but haven't received.

quantityOnPurchaseOrder	
number <double> Nullable
A breakdown of QuantityOnOrder into only those ordered from vendors but haven't received.

quantityOnWorkOrder	
number <double> Nullable
A breakdown of QuantityOnOrder into only those on manufacture orders that haven't been finished yet.

quantityOnTransferOrder	
number <double> Nullable
A breakdown of QuantityOnOrder into only those expected to be received on a stock transfer (only when a locationId is specified).

quantityReserved	
number <double>
This number is the total stock reserved for use that haven't been picked or used yet.

quantityReservedForSales	
number <double>
A breakdown of QuantityReserved into only those reserved for sales orders.

quantityReservedForManufacturing	
number <double>
A breakdown of QuantityReserved into only those reserved for raw materials of manufacture orders.

quantityReservedForTransfers	
number <double>
A breakdown of QuantityReserved into only those reserved to be picked for a stock transfer (only when a locationId is specified).

quantityReservedForBuilds	
number <double>
A breakdown of QuantityReserved into only those parts needed for bills of materials on products with negative anticipated inventory.

quantityAvailable	
number <double>
This number is how many of the products you’ll have left if you fulfill all open outgoing orders. This may include QuantityBuildable (for manufactured products set to combine quantities) and QuantityReservedForBuilds.

rawQuantityAvailable	
number <double>
This number is how many of the products you’ll have left if you fulfill all open outgoing orders, excluding QuantityBuildable and QuantityReservedForBuilds.

quantityPicked	
number <double> Nullable
This number is the total that has already been picked in sales orders/work orders and is awaiting shipment (think of them as sitting in a box waiting to be shipped out).

quantityInTransit	
number <double> Nullable
These are specific items that have been sent via Transfer Stock and are still in the Transit status (i.e. you’ve sent the transfer, but it has not been received at the other location yet).

quantityBuildable	
number <double> Nullable
For manufactured products, the quantity buildable is how many units can be built based on the stock of raw materials. If this is blank, then it means can infinite can be built (e.g. if it's composed only of services).

post
/{companyId}/products/summary
https://cloudapi.inflowinventory.com/{companyId}/products/summary
Request samples
Payload
Content type
application/json
Copy
Expand allCollapse all
[
{
"productId": "string",
"locationId": "string"
}
]
Response samples
200
Content type
application/json
Copy
Expand allCollapse all
[
{
"productId": "string",
"locationId": "string",
"imageSmallUrl": "string",
"quantityOnHand": 0,
"quantityOnOrder": 0,
"quantityOnPurchaseOrder": 0,
"quantityOnWorkOrder": 0,
"quantityOnTransferOrder": 0,
"quantityReserved": 0,
"quantityReservedForSales": 0,
"quantityReservedForManufacturing": 0,
"quantityReservedForTransfers": 0,
"quantityReservedForBuilds": 0,
"quantityAvailable": 0,
"rawQuantityAvailable": 0,
"quantityPicked": 0,
"quantityInTransit": 0,
"quantityBuildable": 0
}
]