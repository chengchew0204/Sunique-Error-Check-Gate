from typing import Dict, Any, Optional
import io
import pandas as pd
from app.validators.base import BaseValidator, ValidationResult


class DeliveryFeeValidator(BaseValidator):
    """
    Validator for Rule 4: Delivery Fee Validation
    
    Check if freight fee is correctly charged for orders in the Delivery Record Form.
    
    Rules:
    1. Only validate orders with paymentStatus = "Paid"
    2. Check if order exists in SharePoint Delivery Record Form
    
    IN TOWN ORDERS (from "In Town" tab):
    3a. If "Handling" is "Yes": orderFreight + z_handling fee must be >= $250
    3b. If "Handling" is "No": z_handling fee should not exist, orderFreight must be >= $150
    
    OUT OF TOWN ORDERS (from "Out of Town" tab):
    4. Shipment Quote Amount must not exceed orderFreight
    """
    
    def __init__(self):
        super().__init__("Delivery Fee Validation")
        # NO CACHING - removed self._delivery_records_cache
    
    def validate(self, order_data: Dict[Any, Any], fetched_data: Dict[Any, Any] = None) -> ValidationResult:
        """
        Validate delivery fee against delivery records.
        
        Args:
            order_data: Complete sales order data from InFlow
            fetched_data: Pre-formatted data from OrderFetcher
        
        Returns:
            ValidationResult with any delivery fee violations
        """
        result = ValidationResult(self.rule_name)
        
        # Use fetched data if available
        if not fetched_data:
            result.add_info("No fetched data available - OrderFetcher may not have run")
            return result
        
        order_info = fetched_data.get('order_info', {})
        line_items = fetched_data.get('line_items', [])
        
        # Step 1: Check if order is paid
        payment_status = order_info.get('payment_status', '')
        if payment_status.lower() != 'paid':
            result.add_info(f"Order payment status is '{payment_status}' - skipping delivery fee validation (only validates paid orders)")
            return result
        
        order_number = order_info.get('order_number', '')
        order_freight = float(order_info.get('order_freight', '0'))
        
        # Step 2: Download and parse Delivery Record Form (always fresh)
        try:
            # Clear any existing cache in SharePoint client
            from app.clients.sharepoint_client import sharepoint_client
            if sharepoint_client:
                sharepoint_client.clear_cache()
            
            delivery_records = self._get_delivery_records()
            in_town_df = delivery_records['in_town']
            out_of_town_df = delivery_records['out_of_town']
        except Exception as e:
            result.add_issue(
                f"Failed to download/parse Delivery Record Form: {str(e)}",
                severity='warning',
                details={'error': str(e)}
            )
            return result
        
        # Step 3: Check if order exists in "In Town" tab first
        order_record = self._find_order_in_records(in_town_df, order_number)
        order_location = None
        
        if order_record is not None:
            # Order found in "In Town" tab
            order_location = 'in_town'
            result.add_info(f"Order {order_number} found in Delivery Record Form (In Town)")
        else:
            # Not in "In Town", check "Out of Town" tab
            order_record = self._find_order_in_records(out_of_town_df, order_number)
            
            if order_record is not None:
                order_location = 'out_of_town'
                result.add_info(f"Order {order_number} found in Delivery Record Form (Out of Town)")
            else:
                result.add_info(f"Order {order_number} not found in Delivery Record Form - skipping validation")
                return result
        
        # Step 4-6: Validate based on order location
        if order_location == 'in_town':
            # IN TOWN VALIDATION
            self._validate_in_town_order(result, order_record, order_number, order_freight, line_items)
        elif order_location == 'out_of_town':
            # OUT OF TOWN VALIDATION
            self._validate_out_of_town_order(result, order_record, order_number, order_freight)
        
        return result
    
    def _validate_in_town_order(self, result: ValidationResult, order_record: Dict[str, Any], 
                                 order_number: str, order_freight: float, line_items: list) -> None:
        """
        Validate "In Town" order delivery fees.
        
        Args:
            result: ValidationResult to add issues/info to
            order_record: Order record from delivery form
            order_number: Order number
            order_freight: Order freight amount
            line_items: List of line items from order
        """
        # Check handling status
        # Handle column name variations (might have newlines)
        handling_value = None
        for key in order_record.keys():
            normalized_key = key.replace('\n', '').replace('\r', '').strip()
            if normalized_key.lower() == 'handling':
                handling_value = order_record[key]
                break
        
        handling = str(handling_value if handling_value is not None else '').strip().lower()
        result.add_info(f"Handling status from delivery record: '{handling}'")
        
        # Find z_handling fee in line items
        z_handling_fee = self._get_z_handling_fee(line_items)
        has_z_handling = z_handling_fee is not None
        z_handling_amount = float(z_handling_fee['line_total']) if has_z_handling else 0.0
        
        # Validate based on handling status
        if handling == 'yes':
            # Handling = Yes: orderFreight + z_handling fee must be >= $250
            total_delivery_cost = order_freight + z_handling_amount
            
            if total_delivery_cost < 250:
                result.add_issue(
                    f"Order requires handling service but total delivery cost (Freight + Z_Handling Fee: ${total_delivery_cost:.2f}) "
                    f"is less than $250 (orderFreight: ${order_freight:.2f}, z_handling: ${z_handling_amount:.2f})",
                    severity='error',
                    details={
                        'order_number': order_number,
                        'order_freight': order_freight,
                        'z_handling_amount': z_handling_amount,
                        'total_delivery_cost': total_delivery_cost,
                        'required_minimum': 250,
                        'handling_required': True
                    }
                )
            else:
                result.add_info(
                    f"Handling service fees validated: Total ${total_delivery_cost:.2f} "
                    f"(freight: ${order_freight:.2f} + handling: ${z_handling_amount:.2f}) >= $250"
                )
        
        elif handling == 'no':
            # Handling = No: z_handling fee should not exist
            if has_z_handling:
                result.add_issue(
                    f"Order does not require handling service but z_handling fee "
                    f"(${z_handling_amount:.2f}) is present on line {z_handling_fee['line_number']}",
                    severity='error',
                    details={
                        'order_number': order_number,
                        'z_handling_amount': z_handling_amount,
                        'line_number': z_handling_fee['line_number'],
                        'handling_required': False
                    }
                )
            
            # Handling = No: orderFreight must be >= $150
            if order_freight < 150:
                result.add_issue(
                    f"Order delivery fee (${order_freight:.2f}) is less than $150 "
                    f"(no handling service required)",
                    severity='error',
                    details={
                        'order_number': order_number,
                        'order_freight': order_freight,
                        'required_minimum': 150,
                        'handling_required': False
                    }
                )
            else:
                result.add_info(
                    f"Delivery fee validated: ${order_freight:.2f} >= $150 (no handling service)"
                )
        else:
            result.add_info(f"Handling status is '{handling}' (expected 'yes' or 'no') - skipping validation")
    
    def _validate_out_of_town_order(self, result: ValidationResult, order_record: Dict[str, Any],
                                     order_number: str, order_freight: float) -> None:
        """
        Validate "Out of Town" order delivery fees.
        
        Args:
            result: ValidationResult to add issues/info to
            order_record: Order record from delivery form
            order_number: Order number
            order_freight: Order freight amount
        """
        # Find "Shipment Quote Amount" field (handle column name variations)
        shipment_quote_amount = None
        for key in order_record.keys():
            normalized_key = key.replace('\n', '').replace('\r', '').strip()
            if normalized_key.lower() == 'shipment quote amount':
                shipment_quote_amount = order_record[key]
                break
        
        # Convert to float, handle NaN or empty values
        try:
            if pd.isna(shipment_quote_amount) or shipment_quote_amount == '' or shipment_quote_amount is None:
                result.add_info(f"No shipment quote amount found for order {order_number} - skipping validation")
                return
            
            shipment_quote = float(shipment_quote_amount)
        except (ValueError, TypeError) as e:
            result.add_info(f"Invalid shipment quote amount: '{shipment_quote_amount}' - skipping validation")
            return
        
        result.add_info(f"Shipment quote amount: ${shipment_quote:.2f}, Order freight: ${order_freight:.2f}")
        
        # Check if shipment quote exceeds order freight
        if shipment_quote > order_freight:
            result.add_issue(
                f"Shipment quote amount (${shipment_quote:.2f}) exceeds order freight (${order_freight:.2f})",
                severity='error',
                details={
                    'order_number': order_number,
                    'shipment_quote_amount': shipment_quote,
                    'order_freight': order_freight,
                    'difference': shipment_quote - order_freight
                }
            )
        else:
            result.add_info(
                f"Out of Town delivery fee validated: Shipment quote ${shipment_quote:.2f} <= Order freight ${order_freight:.2f}"
            )
    
    def _get_delivery_records(self) -> Dict[str, pd.DataFrame]:
        """
        Download and parse the Delivery Record Form from SharePoint.
        ALWAYS downloads fresh data - NO LOCAL CACHING.
        
        NOTE: SharePoint has its own server-side caching. Changes made in Excel Online
        may take 10-30 seconds to appear in the API. This is a Microsoft limitation,
        not a bug in our code.
        
        Returns:
            Dictionary with 'in_town' and 'out_of_town' DataFrames
        
        Raises:
            Exception: If download or parsing fails
        """
        # NO LOCAL CACHING - Always download fresh data from SharePoint
        try:
            from app.clients.sharepoint_client import sharepoint_client
            from app.config import config
            
            if sharepoint_client is None:
                raise Exception("SharePoint client not configured - check environment variables")
            
            # ALWAYS download fresh file (use_cache=False)
            use_cache = False  # Force no cache regardless of config
            
            # Try downloading by document ID first (preferred method)
            file_id = config.SHAREPOINT_DELIVERY_RECORD_ID
            if file_id:
                file_content = sharepoint_client.download_file_by_id(file_id, use_cache=use_cache)
            else:
                # Fallback to path-based download
                file_path = config.SHAREPOINT_DELIVERY_RECORD_PATH
                file_content = sharepoint_client.download_file(file_path, use_cache=use_cache)
            
            # Parse Excel file - create fresh BytesIO object
            excel_file = io.BytesIO(file_content)
            
            # Read both sheets using ExcelFile to ensure fresh reads
            with pd.ExcelFile(excel_file, engine='openpyxl') as xls:
                in_town_df = pd.read_excel(xls, sheet_name="In Town")
                out_of_town_df = pd.read_excel(xls, sheet_name="Out of Town")
            
            # Return both DataFrames
            records = {
                'in_town': in_town_df,
                'out_of_town': out_of_town_df
            }
            
            return records
            
        except Exception as e:
            raise Exception(f"Failed to get delivery records: {str(e)}")
    
    def _find_order_in_records(self, df: pd.DataFrame, order_number: str) -> Optional[Dict[str, Any]]:
        """
        Find an order in the delivery records DataFrame.
        
        Args:
            df: DataFrame containing delivery records
            order_number: Order number to search for
        
        Returns:
            Dictionary with order record data, or None if not found
        """
        # Look for column "Sales Order#(FD)" - handle variations with newlines
        # The column name might have newline characters like "Sales Order#\n(FD)"
        order_column = None
        for col in df.columns:
            # Normalize column name by removing whitespace and newlines
            normalized_col = col.replace('\n', '').replace('\r', '').strip()
            if normalized_col == "Sales Order#(FD)":
                order_column = col
                break
        
        if order_column is None:
            raise Exception(f"Column 'Sales Order#(FD)' not found in Delivery Record Form. Available columns: {list(df.columns)}")
        
        # Find matching order (handle both string and numeric formats)
        matches = df[df[order_column].astype(str).str.strip() == str(order_number).strip()]
        
        if len(matches) == 0:
            return None
        
        # Return the match as dictionary (if multiple, use last one)
        return matches.iloc[-1].to_dict()
    
    def _get_z_handling_fee(self, line_items: list) -> Optional[Dict[str, Any]]:
        """
        Find the z_handling fee line item.
        
        Args:
            line_items: List of line items from OrderFetcher
        
        Returns:
            Line item dictionary if found, None otherwise
        """
        for item in line_items:
            item_sku = item.get('sku', '').upper()
            item_name = item.get('name', '').upper()
            
            # Check if this is the z_handling fee item
            if 'Z_HANDLING' in item_sku or 'Z_HANDLING' in item_name:
                return item
        
        return None


'''

Todo: Implement this validator

(1) Check if the order is already paid (paymentStatus is "Paid" or "paid").

    - If not, skip this validator.

    - If yes, proceed to the next step.

(2) Download and parse the Delivery Record Form from SharePoint.(File link:https://suniquecabinetry.sharepoint.com/:x:/r/sites/sccr/Shared%20Documents/Forms%20%26%20Applications/Delivery%20Record/Delivery%20Record%20Form.xlsx?d=wceb0d1f8e4e24acbb78624dbe37c8ca3&csf=1&web=1&e=W8Tmhn)

(3) Check if the order number exists in the Delivery Record Form (located in the "In Town" tab, field "Sales Order#(FD)").

    - If not, skip this validator.

    - If yes, proceed to the next step.

(4) Check if the "Handling" column value is "Yes" or "yes".

(5) If the order number exists in the Delivery Record Form and the "Handling" column is "Yes" or "yes":

    - Then orderFreight + z_handling fee (SKU: z_handling fee, line item within the order) must be greater than $250.

    - If not, flag an error.

    - If yes, proceed to the next step.

(6) If the order number exists in the Delivery Record Form and the "Handling" column is "No" or "no":

    - The z_handling fee should not appear in the line items. If it does, flag an error.

    - The orderFreight must be greater than $150. If not, flag an error.

    - If all conditions are met, proceed to the next step.

Now, i would like to start implementing the logics for "Out of Town" orders. (If the order is not in the "In Town" tab, check the "Out of Town" tab.)
Check the "Out of Town" tab in the Delivery Record Form. Check the "Sales Order#(FD)" column to see if the order number exists.
If it does, proceed to the next step. If it does not, skip this validator.
Check the "Shipment Quote Amount" Field to see if it is greater than "orderFreight". If it is, flag an error. If it is not, proceed to the next step.

'''