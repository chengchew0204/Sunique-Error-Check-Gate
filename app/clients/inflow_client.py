import requests
from typing import Dict, Any, Optional, List
import time
from app.config import config


class InFlowClient:
    """
    Client for interacting with the InFlow Inventory API.
    Handles authentication, rate limiting, and retries.
    """
    
    def __init__(self, api_key: str, company_id: str, base_url: str):
        """
        Initialize the InFlow API client.
        
        Args:
            api_key: InFlow API key
            company_id: InFlow company ID
            base_url: Base URL for InFlow API
        """
        self.api_key = api_key
        self.company_id = company_id
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json;version=2025-06-24'
        })
    
    def _make_request(self, method: str, endpoint: str, max_retries: int = 3, **kwargs) -> Dict[Any, Any]:
        """
        Make an API request with retry logic.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            max_retries: Maximum number of retry attempts
            **kwargs: Additional arguments to pass to requests
        
        Returns:
            JSON response as dictionary
        
        Raises:
            Exception: If request fails after all retries
        """
        url = f"{self.base_url}/{self.company_id}/{endpoint.lstrip('/')}"
        
        # Add Content-Type header for PUT/POST/PATCH requests
        if method.upper() in ['PUT', 'POST', 'PATCH'] and 'json' in kwargs:
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Content-Type'] = 'application/json'
        
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    print(f"Rate limited. Retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.HTTPError as e:
                # Print detailed error for debugging
                print(f"HTTP Error: {e}")
                if hasattr(e.response, 'text'):
                    print(f"Response body: {e.response.text}")
                if attempt == max_retries - 1:
                    raise
            
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise Exception(f"InFlow API request failed after {max_retries} attempts: {e}")
                
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Request failed, retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
        
        raise Exception("Failed to complete request")
    
    def get_sales_order(self, order_id: str) -> Dict[Any, Any]:
        """
        Fetch full sales order details.
        
        Args:
            order_id: Sales order ID
        
        Returns:
            Complete sales order data including line items, customer info, payment details
        """
        # Add a small delay to allow InFlow to process the order
        import time
        time.sleep(2)  # Wait 2 seconds for InFlow to process
        
        # Include line items and other related data in the response
        # According to InFlow API docs, relationships must be explicitly included
        # Use nested include to get product details within lines
        # Include paymentLines for credit card fee validation
        # Include salesRepTeamMember to get account manager details
        return self._make_request(
            'GET', 
            f'sales-orders/{order_id}?include=lines.product,customer,location,paymentLines,salesRepTeamMember'
        )
    
    def get_customer(self, customer_id: str) -> Dict[Any, Any]:
        """
        Fetch customer details including discount rules.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            Customer data with discount policies
        """
        return self._make_request('GET', f'customers/{customer_id}')
    
    def get_product(self, product_id: str) -> Dict[Any, Any]:
        """
        Fetch product details.
        
        Args:
            product_id: Product ID
        
        Returns:
            Product data including category and pricing info
        """
        return self._make_request('GET', f'products/{product_id}')
    
    def list_webhooks(self) -> List[Dict[Any, Any]]:
        """
        List all subscribed webhooks.
        
        Returns:
            List of webhook subscriptions
        """
        return self._make_request('GET', 'webhooks')
    
    def subscribe_webhook(self, webhook_url: str, events: List[str], webhook_id: Optional[str] = None) -> Dict[Any, Any]:
        """
        Subscribe to InFlow webhooks.
        
        Args:
            webhook_url: URL to receive webhook events
            events: List of events to subscribe to (e.g., ['salesOrder.created', 'salesOrder.updated'])
            webhook_id: Optional webhook subscription ID (will be generated if not provided)
        
        Returns:
            Webhook subscription details including secret key
        """
        import uuid
        
        payload = {
            'url': webhook_url,
            'events': events,
            'webHookSubscriptionId': webhook_id or str(uuid.uuid4()),
            'webHookSubscriptionRequestId': str(uuid.uuid4())
        }
        
        return self._make_request('PUT', 'webhooks', json=payload)
    
    def get_webhook(self, webhook_id: str) -> Dict[Any, Any]:
        """
        Get webhook subscription details.
        
        Args:
            webhook_id: Webhook subscription ID
        
        Returns:
            Webhook subscription details
        """
        return self._make_request('GET', f'webhooks/{webhook_id}')
    
    def unsubscribe_webhook(self, webhook_id: str) -> None:
        """
        Unsubscribe from a webhook.
        
        Args:
            webhook_id: Webhook subscription ID
        """
        self._make_request('DELETE', f'webhooks/{webhook_id}')


# Create a singleton instance
inflow_client = InFlowClient(
    api_key=config.INFLOW_API_KEY or '',
    company_id=config.INFLOW_COMPANY_ID or '',
    base_url=config.INFLOW_API_BASE_URL
)

