import msal
import requests
from typing import List, Dict, Any, Optional
from app.config import config


class OutlookClient:
    """
    Client for sending emails via Microsoft Outlook API using MSAL authentication.
    """
    
    def __init__(self, client_id: str, client_secret: str, tenant_id: str):
        """
        Initialize the Outlook API client.
        
        Args:
            client_id: Azure AD application client ID
            client_secret: Azure AD application client secret
            tenant_id: Azure AD tenant ID
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]
        
        # Initialize MSAL confidential client application
        self.app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=self.authority
        )
        
        self._access_token = None
    
    def _get_access_token(self) -> str:
        """
        Acquire access token for Microsoft Graph API.
        
        Returns:
            Access token string
        
        Raises:
            Exception: If unable to acquire token
        """
        result = self.app.acquire_token_silent(self.scope, account=None)
        
        if not result:
            result = self.app.acquire_token_for_client(scopes=self.scope)
        
        if "access_token" in result:
            return result["access_token"]
        else:
            error = result.get("error", "Unknown error")
            error_description = result.get("error_description", "No description")
            raise Exception(f"Failed to acquire access token: {error} - {error_description}")
    
    def send_email(
        self,
        to_addresses: List[str],
        subject: str,
        body_html: str,
        from_address: Optional[str] = None,
        cc_addresses: Optional[List[str]] = None
    ) -> Dict[Any, Any]:
        """
        Send an email via Outlook API.
        
        Args:
            to_addresses: List of recipient email addresses
            subject: Email subject
            body_html: Email body in HTML format
            from_address: Sender email address (if not provided, uses authenticated user)
            cc_addresses: List of CC recipient email addresses
        
        Returns:
            Response from the API
        
        Raises:
            Exception: If email sending fails
        """
        access_token = self._get_access_token()
        
        # Construct the email message
        message = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": body_html
                },
                "toRecipients": [
                    {"emailAddress": {"address": addr}} for addr in to_addresses
                ]
            },
            "saveToSentItems": "true"
        }
        
        # Add CC recipients if provided
        if cc_addresses:
            message["message"]["ccRecipients"] = [
                {"emailAddress": {"address": addr}} for addr in cc_addresses
            ]
        
        # Determine the endpoint
        if from_address:
            endpoint = f"https://graph.microsoft.com/v1.0/users/{from_address}/sendMail"
        else:
            endpoint = "https://graph.microsoft.com/v1.0/me/sendMail"
        
        # Send the email
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(endpoint, json=message, headers=headers)
        
        if response.status_code not in [200, 202]:
            raise Exception(
                f"Failed to send email: {response.status_code} - {response.text}"
            )
        
        return {"status": "sent", "status_code": response.status_code}


# Create a singleton instance
outlook_client = None
if config.OUTLOOK_CLIENT_ID and config.OUTLOOK_CLIENT_SECRET and config.OUTLOOK_TENANT_ID:
    outlook_client = OutlookClient(
        client_id=config.OUTLOOK_CLIENT_ID,
        client_secret=config.OUTLOOK_CLIENT_SECRET,
        tenant_id=config.OUTLOOK_TENANT_ID
    )

