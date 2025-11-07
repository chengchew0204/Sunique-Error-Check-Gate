from flask import Flask, request, jsonify
from typing import Dict, Any
import json

from app.config import config
from app.utils.hmac_verifier import HMACVerifier
from app.clients.inflow_client import inflow_client
from app.services.validation_service import validation_service
from app.services.logger_service import logger_service
from app.services.notification_service import notification_service


app = Flask(__name__)

# Initialize HMAC verifier
hmac_verifier = HMACVerifier(config.WEBHOOK_SECRET or '')


@app.route('/')
def index():
    """
    Health check endpoint.
    """
    return jsonify({
        'status': 'running',
        'service': 'InFlow Error Check Gate',
        'version': '1.0.0'
    })


@app.route('/webhook/inflow', methods=['POST'])
def inflow_webhook():
    """
    Webhook endpoint for InFlow events.
    Receives salesOrder.created and salesOrder.updated events.
    """
    try:
        # Get raw payload and signature header
        payload = request.get_data()
        signature_header = request.headers.get('x-inflow-hmac-sha256')
        
        # Verify HMAC signature
        if not hmac_verifier.verify(payload, signature_header):
            print("Invalid HMAC signature")
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Parse webhook payload
        webhook_data = json.loads(payload)
        
        # Log the entire payload for debugging
        print("="*60)
        print("WEBHOOK RECEIVED:")
        print(json.dumps(webhook_data, indent=2))
        print("="*60)
        
        # Extract event details - InFlow uses 'eventType' and 'salesOrderId' at root level
        event_type = webhook_data.get('eventType', webhook_data.get('event', 'unknown'))
        sales_order_id = webhook_data.get('salesOrderId') or webhook_data.get('data', {}).get('salesOrderId')
        
        print(f"Received webhook event: {event_type}")
        
        if not sales_order_id:
            print(f"No salesOrderId in webhook payload. Keys present: {list(webhook_data.keys())}")
            return jsonify({'error': 'Missing salesOrderId', 'received_keys': list(webhook_data.keys())}), 400
        
        # Process only sales order events
        # InFlow uses event types like 'SalesOrderCreatedV1', 'SalesOrderUpdatedV1'
        if not ('SalesOrder' in event_type or event_type in ['salesOrder.created', 'salesOrder.updated']):
            print(f"Ignoring event type: {event_type}")
            return jsonify({'status': 'ignored', 'message': 'Not a sales order event'}), 200
        
        # Fetch full order data from InFlow API
        print(f"Fetching order data for: {sales_order_id}")
        order_data = inflow_client.get_sales_order(sales_order_id)
        
        # Extract order number for logging
        order_number = order_data.get('orderNumber', 'N/A')
        print(f"Order Number: {order_number}")
        
        # Run validation
        print(f"Running validation for order: {sales_order_id} ({order_number})")
        validation_result = validation_service.validate_order(order_data)
        
        # Log validation results
        logger_service.log_validation_result(validation_result, order_data)
        
        # Send notification if there are issues
        if validation_result['status'] in ['warning', 'failed']:
            print(f"Sending notification for order: {sales_order_id} ({order_number})")
            notification_service.send_validation_failure_notification(
                validation_result,
                order_data
            )
        
        # Return success response
        return jsonify({
            'status': 'processed',
            'order_id': sales_order_id,
            'order_number': order_number,
            'validation_status': validation_result['status'],
            'issues_count': len(validation_result['issues'])
        }), 200
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/validate/<order_id>', methods=['GET'])
def validate_order_manual(order_id: str):
    """
    Manual validation endpoint for testing.
    Allows triggering validation for a specific order ID.
    """
    try:
        # Fetch order data
        print(f"Manual validation requested for order: {order_id}")
        order_data = inflow_client.get_sales_order(order_id)
        
        # Extract order number for logging
        order_number = order_data.get('orderNumber', 'N/A')
        print(f"Order Number: {order_number}")
        
        # Run validation
        validation_result = validation_service.validate_order(order_data)
        
        # Log results
        logger_service.log_validation_result(validation_result, order_data)
        
        # Return validation results
        return jsonify(validation_result), 200
    
    except Exception as e:
        print(f"Error in manual validation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/history/<order_id>', methods=['GET'])
def get_validation_history(order_id: str):
    """
    Get validation history for a specific order.
    """
    try:
        history = logger_service.get_validation_history(order_id)
        return jsonify({
            'order_id': order_id,
            'history_count': len(history),
            'history': history
        }), 200
    
    except Exception as e:
        print(f"Error retrieving validation history: {e}")
        return jsonify({'error': str(e)}), 500


def initialize_validators():
    """
    Initialize and register all validators.
    This function will be expanded as we implement each validation rule.
    
    IMPORTANT: OrderFetcher (Rule 0) must be registered FIRST!
    It fetches and formats data for all other validators.
    """
    from app.validators import (
        OrderFetcher, 
        DiscountValidator, 
        CreditCardFeeValidator, 
        AssemblyFeeValidator,
        DeliveryFeeValidator,
        DiscountRemarkValidator
    )
    
    # Rule 0: Order Data Fetcher (MUST BE FIRST!)
    # This fetches and formats all order data for other validators
    order_fetcher = OrderFetcher()
    validation_service.register_validator(order_fetcher)
    
    # Phase 1: Discount validation
    discount_validator = DiscountValidator()
    validation_service.register_validator(discount_validator)
    
    # Phase 2: Credit card fee validation
    credit_card_validator = CreditCardFeeValidator()
    validation_service.register_validator(credit_card_validator)
    
    # Phase 3: Assembly fee validation
    assembly_fee_validator = AssemblyFeeValidator()
    validation_service.register_validator(assembly_fee_validator)
    
    # Phase 4: Delivery fee validation
    delivery_fee_validator = DeliveryFeeValidator()
    validation_service.register_validator(delivery_fee_validator)
    
    # Phase 5: Discount remark validation
    discount_remark_validator = DiscountRemarkValidator()
    validation_service.register_validator(discount_remark_validator)
    
    print(f"Validators initialized: {len(validation_service.validators)} registered")


if __name__ == '__main__':
    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        exit(1)
    
    # Initialize validators
    initialize_validators()
    
    # Run Flask app
    print(f"Starting InFlow Error Check Gate on port {config.FLASK_PORT}")
    app.run(
        host='0.0.0.0',
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )

