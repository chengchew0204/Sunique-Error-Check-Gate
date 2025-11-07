from typing import Dict, Any, Optional
from app.validators.base import BaseValidator, ValidationResult
from app.config import config
import csv
import os
import re


class AssemblyFeeValidator(BaseValidator):
    """
    Validator for Rule 3: Assembly Fee Validation
    
    Assembly fee should always be correct and must not have any discount applied.
    """
    
    def __init__(self):
        super().__init__("Assembly Fee Validation")
        self.product_categories = self._load_product_categories()
    
    def _load_product_categories(self) -> Dict[str, str]:
        """
        Load product categories from CSV file.
        
        Returns:
            Dictionary mapping product codes to categories
        """
        categories = {}
        csv_path = os.path.join(
            os.path.dirname(__file__),
            'data',
            'product-category.csv'
        )
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product = row.get('Product', '').strip()
                    category = row.get('Product Category', '').strip()
                    if product and category:
                        categories[product] = category
        except Exception as e:
            print(f"Warning: Could not load product categories: {e}")
        
        return categories
    
    def _get_search_name_from_product(self, product_name: str) -> str:
        """
        Extract search name from product name by removing prefixes.
        Example: SW-VS30 -> VS30
        
        Args:
            product_name: Full product name
        
        Returns:
            Search name without prefix
        """
        # Remove common prefixes (e.g., SW-, TUK-, etc.)
        # Match pattern: letters followed by dash/hyphen
        match = re.match(r'^[A-Za-z]+-(.+)$', product_name)
        if match:
            return match.group(1)
        return product_name
    
    def _get_product_category(self, product_name: str) -> Optional[str]:
        """
        Get product category by looking up the search name.
        
        Args:
            product_name: Product name to look up
        
        Returns:
            Product category or None if not found
        """
        search_name = self._get_search_name_from_product(product_name)
        return self.product_categories.get(search_name)
    
    def _calculate_assembly_fee_for_product(self, product_name: str, quantity: float) -> float:
        """
        Calculate assembly fee for a single product.
        
        Args:
            product_name: Name of the product
            quantity: Quantity ordered
        
        Returns:
            Assembly fee amount
        """
        category = self._get_product_category(product_name)
        
        if not category:
            return 0.0  # Default to free if category not found
        
        # Assembly fee rules based on category
        if category == 'Accessories':
            return 0.0
        elif category in ['Base Cabinet', 'Vanity Cabinet', 'Wall Cabinet']:
            return quantity * 15.0
        elif category == 'Tall Cabinet':
            return quantity * 30.0
        else:
            return 0.0  # Default to free for unknown categories
    
    def validate(self, order_data: Dict[Any, Any], fetched_data: Dict[Any, Any] = None) -> ValidationResult:
        """
        Validate assembly fee calculation and discount.
        
        Args:
            order_data: Complete sales order data from InFlow
            fetched_data: Pre-formatted data from OrderFetcher
        
        Returns:
            ValidationResult with any assembly fee violations
        """
        result = ValidationResult(self.rule_name)
        
        # Use fetched data if available
        if not fetched_data:
            result.add_info("No fetched data available - OrderFetcher may not have run")
            return result
        
        order_info = fetched_data.get('order_info', {})
        line_items = fetched_data.get('line_items', [])
        
        # (1) Check if the order is paid (case-insensitive)
        payment_status = order_info.get('payment_status', 'N/A')
        if payment_status.lower() != 'paid':
            result.add_info(f"Order payment status is '{payment_status}' (not Paid) - skipping assembly fee validation")
            return result
        
        # (2) Find assembly fee line item
        assembly_fee_item = None
        for item in line_items:
            item_name = item.get('name', '').upper()
            item_sku = item.get('sku', '').upper()
            if 'Z_ASSEMBLY FEE' in item_name or 'Z_ASSEMBLY FEE' in item_sku:
                assembly_fee_item = item
                break
        
        # If no assembly fee line item, skip validation
        if not assembly_fee_item:
            result.add_info("No assembly fee line item found - skipping assembly fee validation")
            return result
        
        # (3) Check if assembly fee has discount applied
        assembly_fee_discount = float(assembly_fee_item.get('discount_value', 0))
        if assembly_fee_discount > 0:
            result.add_issue(
                f"Assembly fee line item has a discount of {assembly_fee_discount}% applied. "
                f"Assembly fees should not have any discount.",
                severity='error',
                details={
                    'line_number': assembly_fee_item.get('line_number'),
                    'sku': assembly_fee_item.get('sku'),
                    'name': assembly_fee_item.get('name'),
                    'discount': assembly_fee_discount
                }
            )
        
        # (4) Calculate expected assembly fee
        expected_fee = 0.0
        assembly_breakdown = []
        
        for item in line_items:
            item_name = item.get('name', '')
            item_sku = item.get('sku', '')
            
            # Skip the assembly fee line item itself
            if 'Z_ASSEMBLY FEE' in item_name.upper() or 'Z_ASSEMBLY FEE' in item_sku.upper():
                continue
            
            # Skip other Z_ items (like Z_DISCOUNT, Z_DELIVERY FEE, etc.)
            if item_name.startswith('Z_') or item_sku.startswith('Z_'):
                continue
            
            try:
                quantity = float(item.get('quantity', 0))
                if quantity <= 0:
                    continue
                
                # Calculate assembly fee for this product
                fee = self._calculate_assembly_fee_for_product(item_name, quantity)
                
                if fee > 0:
                    expected_fee += fee
                    category = self._get_product_category(item_name)
                    assembly_breakdown.append({
                        'name': item_name,
                        'sku': item_sku,
                        'quantity': quantity,
                        'category': category,
                        'fee': fee
                    })
            except (ValueError, TypeError) as e:
                result.add_info(f"Skipped line {item.get('line_number')} due to invalid data: {e}")
        
        # (4.5) Compare actual vs expected assembly fee
        actual_fee = abs(float(assembly_fee_item.get('line_total', 0)))
        
        # Allow for small floating point differences (within 1 cent)
        fee_difference = abs(actual_fee - expected_fee)
        
        if fee_difference > 0.01:
            result.add_issue(
                f"Assembly fee amount is incorrect. "
                f"Expected: ${expected_fee:.2f}, Actual: ${actual_fee:.2f}, Difference: ${fee_difference:.2f}",
                severity='error',
                details={
                    'line_number': assembly_fee_item.get('line_number'),
                    'expected_fee': expected_fee,
                    'actual_fee': actual_fee,
                    'difference': fee_difference,
                    'breakdown': assembly_breakdown
                }
            )
            
            # Add detailed breakdown as suggested fix
            if assembly_breakdown:
                # Build the breakdown as a single HTML block
                breakdown_html = "Expected assembly fee breakdown:<ul style='margin-top: 5px; margin-bottom: 5px;'>"
                for item in assembly_breakdown:
                    breakdown_html += (
                        f"<li>{item['name']} ({item['sku']}): "
                        f"{item['quantity']} x ${item['fee'] / item['quantity']:.2f} = ${item['fee']:.2f} "
                        f"[Category: {item['category']}]</li>"
                    )
                breakdown_html += f"</ul>Total Expected: ${expected_fee:.2f}"
                result.add_suggested_fix(breakdown_html)
        
        # Add summary information
        result.add_info(f"Assembly fee validation completed")
        result.add_info(f"Assembly fee line item found: {assembly_fee_item.get('name')}")
        result.add_info(f"Expected assembly fee: ${expected_fee:.2f}")
        result.add_info(f"Actual assembly fee: ${actual_fee:.2f}")
        result.add_info(f"Products with assembly fee: {len(assembly_breakdown)}")
        
        return result

'''

Todo: Implement this validator
(1) Check if the order is paid already(paymentStatus is "Paid"). (case-insensitive)
(2) Check if the order has an assembly fee line item. If not, then skip this validator. If yes, keep checking the next step.
(3) Check if the assembly fee line item has a discount applied. If yes, then it's an error. If no, then keep checking the next step.
(4) Check if the assembly fee line item's amount is correct.
    (4.1) Check the datasheet "/validators/data/product-category.csv" to get the product category.
    (4.2) Get the product name and quantity from the order data for each product line items.
    (4.3) Use the calculation formula for reference to calculate the expected assembly fee amount.
        Assembly Fee Calculation in script.js
        The assembly fee calculation in this project follows a category-based pricing system. Here's how it works:
        Main Flow
        script.jsLines 2425-2522
        async function processAssemblyCalculation() {    const step = document.getElementById('step-assembly');        try {        // Update progress bar - start assembly calculation        updateProgressBar('assembly', 'start', 'Calculating assembly fees...');                step.querySelector('span').textContent = 'Calculating assembly fees...';                // Check if assembly is required globally        if (!currentQuoteData.assemblyRequired) {            // No assembly required - set fee to $0            currentQuoteData.assembly = {                itemCount: 0,                fee: 0,                breakdown: []            };                        // Mark step as completed            step.className = 'processing-step completed';            step.querySelector('i').className = 'fas fa-check-circle';            step.querySelector('span').textContent = 'Assembly calculation completed (No assembly required)';                        // Update progress bar - complete assembly calculation            updateProgressBar('assembly', 'complete', 'Assembly calculation completed (No assembly required)');                        return;        }                // Calculate assembly fees based on product categories        let totalAssemblyFee = 0;        let totalAssemblyItems = 0;        const assemblyBreakdown = [];        const totalProducts = currentQuoteData.products.length;                // Update initial progress        updateProgressBar('assembly', 'progress', 'Analyzing product categories for assembly...', 10);                for (let i = 0; i < currentQuoteData.products.length; i++) {            const product = currentQuoteData.products[i];                        // Update progress for current product            const productProgress = 20 + ((i + 0.5) / totalProducts) * 60; // 20% to 80% range            updateProgressBar('assembly', 'progress', `Calculating assembly for ${product.name} (${i + 1}/${totalProducts})`, productProgress);                        const assemblyFee = calculateAssemblyFeeForProduct(product.name, product.quantity);                        if (assemblyFee > 0) {                totalAssemblyFee += assemblyFee;                totalAssemblyItems += product.quantity;                                assemblyBreakdown.push({                    name: product.name,                    quantity: product.quantity,                    category: getProductCategory(product.name),                    fee: assemblyFee                });            }                        // Update progress after each product            const completedProgress = 20 + ((i + 1) / totalProducts) * 60;            updateProgressBar('assembly', 'progress', `Processed ${i + 1}/${totalProducts} products for assembly`, completedProgress);                        // Small delay to make progress visible (only if there are multiple products)            if (totalProducts > 1 && i < totalProducts - 1) {                await new Promise(resolve => setTimeout(resolve, 100));            }        }                // Final calculation progress        updateProgressBar('assembly', 'progress', 'Finalizing assembly fee calculations...', 90);                currentQuoteData.assembly = {            itemCount: totalAssemblyItems,            fee: totalAssemblyFee,            breakdown: assemblyBreakdown        };                        // Mark step as completed        step.className = 'processing-step completed';        step.querySelector('i').className = 'fas fa-check-circle';        step.querySelector('span').textContent = 'Assembly calculation completed';                // Update progress bar - complete assembly calculation        updateProgressBar('assembly', 'complete', 'Assembly calculation completed');            } catch (error) {        step.className = 'processing-step error';        step.querySelector('i').className = 'fas fa-exclamation-circle';        step.querySelector('span').textContent = 'Assembly calculation failed';                // Update progress bar - error in assembly calculation        updateProgressBar('assembly', 'error', 'Assembly calculation failed');                throw error;    }}
        Category-Based Fee Calculation
        script.jsLines 4114-4134
        function calculateAssemblyFeeForProduct(productName, quantity) {    const category = getProductCategory(productName);        if (!category) {        return 0; // Default to free if category not found    }        // Assembly fee rules based on category    switch (category) {        case 'Accessories':            return 0; // Free        case 'Base Cabinet':        case 'Vanity Cabinet':        case 'Wall Cabinet':            return quantity * 15; // $15 per product        case 'Tall Cabinet':            return quantity * 30; // $30 per product        default:            return 0; // Default to free for unknown categories    }}
        Product Category Lookup
        script.jsLines 3993-3996
        function getProductCategory(productName) {    const searchName = getSearchNameFromProduct(productName);    return productCategoryData.get(searchName) || null;}
        Assembly Fee Pricing Structure
        Category	Fee per Item
        Accessories	$0 (Free)
        Base Cabinet	$15
        Vanity Cabinet	$15
        Wall Cabinet	$15
        Tall Cabinet	$30
        Unknown/Not Found	$0 (Free)
        Key Points
        Product categories are loaded from CSV file (product-category.csv) at initialization
        Product name parsing: The system removes prefixes (e.g., SW-VS30 → VS30) before looking up the category
        Quantity-based: The fee is multiplied by the quantity ordered
        Safe defaults: Unknown categories default to $0 (free)
        Added as line item: The total assembly fee is added to the inFlow quote as a Z_ASSEMBLY FEE product
        script.jsLines 4172-4176
        // Assembly fee product configurationconst ASSEMBLY_FEE_PRODUCT = {    name: 'Z_ASSEMBLY FEE',    unitPrice: 15};
    (4.4) what happens when a product is not in the product-category list:
        What Happens - Code Flow
        script.jsLines 4114-4134
        function calculateAssemblyFeeForProduct(productName, quantity) {    const category = getProductCategory(productName);        if (!category) {        return 0; // Default to free if category not found    }        // Assembly fee rules based on category    switch (category) {        case 'Accessories':            return 0; // Free        case 'Base Cabinet':        case 'Vanity Cabinet':        case 'Wall Cabinet':            return quantity * 15; // $15 per product        case 'Tall Cabinet':            return quantity * 30; // $30 per product        default:            return 0; // Default to free for unknown categories    }}
        The Result
        Products not found in the category list will:
        ✅ Return 0 (no assembly fee charged)
        ✅ Not appear in the assembly breakdown
        ✅ Not cause any errors or failures
        ⚠️ Silently default to FREE assembly (no fee)
        Here's the logic path:
        // Step 1: Product lookupgetProductCategory(productName) → returns null if not found// Step 2: Check resultif (!category) {    return 0;  // ← Product gets FREE assembly by default}
    (4.5) Check if the assembly fee line item's amount is correct. If not, then it's an error.

'''