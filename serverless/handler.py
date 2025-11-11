"""
Serverless handler for AWS Lambda / Azure Functions deployment.

This handler wraps the Flask application for serverless execution.
"""

import json
import sys
import os

# Add parent directory to path so we can import app module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app, initialize_validators


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    
    Args:
        event: Lambda event object
        context: Lambda context object
    
    Returns:
        Response object with statusCode, headers, and body
    """
    # Initialize validators on cold start
    initialize_validators()
    
    # Convert Lambda event to Flask-compatible format
    # Handle API Gateway proxy integration format
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    headers = event.get('headers', {})
    body = event.get('body', '')
    
    # Create a test request context
    with app.test_request_context(
        path=path,
        method=http_method,
        headers=headers,
        data=body
    ):
        try:
            # Process the request
            response = app.full_dispatch_request()
            
            # Convert Flask response to Lambda response
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }


def azure_function_handler(req):
    """
    Azure Functions handler.
    
    Args:
        req: Azure Functions HttpRequest object
    
    Returns:
        Azure Functions HttpResponse object
    """
    import azure.functions as func
    
    # Initialize validators on cold start
    initialize_validators()
    
    # Convert Azure Functions request to Flask-compatible format
    with app.test_request_context(
        path=req.url,
        method=req.method,
        headers=req.headers,
        data=req.get_body()
    ):
        try:
            # Process the request
            response = app.full_dispatch_request()
            
            # Convert Flask response to Azure Functions response
            return func.HttpResponse(
                body=response.get_data(),
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except Exception as e:
            return func.HttpResponse(
                body=json.dumps({'error': str(e)}),
                status_code=500,
                headers={'Content-Type': 'application/json'}
            )

