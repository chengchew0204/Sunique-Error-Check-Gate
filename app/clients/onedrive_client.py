import msal
import requests
from typing import Dict, Any, Optional
import io
import time
from app.config import config


class OneDriveClient:
    """
    Client for accessing files from Microsoft OneDrive using MSAL authentication.
    """
    
    def __init__(self, client_id: str, client_secret: str, tenant_id: str):
        """
        Initialize the OneDrive API client.
        
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
        
        # Cache for file downloads (with TTL)
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl = 300  # 5 minutes
    
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
    
    def download_file(self, file_path: str, use_cache: bool = True) -> bytes:
        """
        Download a file from OneDrive.
        
        Args:
            file_path: Path to the file in OneDrive (e.g., '/Documents/file.xlsx')
            use_cache: Whether to use cached version if available
        
        Returns:
            File content as bytes
        
        Raises:
            Exception: If file download fails
        """
        # Check cache
        if use_cache and file_path in self._cache:
            cache_entry = self._cache[file_path]
            if time.time() - cache_entry['timestamp'] < self._cache_ttl:
                print(f"Using cached version of {file_path}")
                return cache_entry['content']
        
        # Download file
        access_token = self._get_access_token()
        
        # Construct the file download URL
        # This assumes the file path is relative to the user's drive
        # Adjust the endpoint as needed based on your OneDrive setup
        encoded_path = requests.utils.quote(file_path)
        endpoint = f"https://graph.microsoft.com/v1.0/me/drive/root:{encoded_path}:/content"
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(endpoint, headers=headers)
        
        if response.status_code != 200:
            raise Exception(
                f"Failed to download file from OneDrive: {response.status_code} - {response.text}"
            )
        
        content = response.content
        
        # Update cache
        self._cache[file_path] = {
            'content': content,
            'timestamp': time.time()
        }
        
        print(f"Downloaded file from OneDrive: {file_path}")
        return content
    
    def clear_cache(self, file_path: Optional[str] = None) -> None:
        """
        Clear the file cache.
        
        Args:
            file_path: Specific file to clear from cache, or None to clear all
        """
        if file_path:
            self._cache.pop(file_path, None)
        else:
            self._cache.clear()


# Create a singleton instance
onedrive_client = None
if config.ONEDRIVE_CLIENT_ID and config.ONEDRIVE_CLIENT_SECRET and config.ONEDRIVE_TENANT_ID:
    onedrive_client = OneDriveClient(
        client_id=config.ONEDRIVE_CLIENT_ID,
        client_secret=config.ONEDRIVE_CLIENT_SECRET,
        tenant_id=config.ONEDRIVE_TENANT_ID
    )

