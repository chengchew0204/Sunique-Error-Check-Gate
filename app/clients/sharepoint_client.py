import msal
import requests
from typing import Dict, Any, Optional
import time
from app.config import config


class SharePointClient:
    """
    Client for accessing files from Microsoft SharePoint using MSAL authentication.
    """
    
    def __init__(self, client_id: str, client_secret: str, tenant_id: str, hostname: str, site_name: str):
        """
        Initialize the SharePoint API client.
        
        Args:
            client_id: Azure AD application client ID
            client_secret: Azure AD application client secret
            tenant_id: Azure AD tenant ID
            hostname: SharePoint hostname (e.g., 'suniquecabinetry.sharepoint.com')
            site_name: SharePoint site name (e.g., 'sccr')
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.hostname = hostname
        self.site_name = site_name
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
        
        # Cache for site ID (remains valid for session)
        self._site_id: Optional[str] = None
    
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
    
    def _get_site_id(self) -> str:
        """
        Get the SharePoint site ID (cached after first retrieval).
        
        Returns:
            Site ID string
        
        Raises:
            Exception: If unable to get site ID
        """
        # Return cached site ID if available
        if self._site_id:
            return self._site_id
        
        access_token = self._get_access_token()
        
        # Get site ID using hostname and site name
        endpoint = f"https://graph.microsoft.com/v1.0/sites/{self.hostname}:/sites/{self.site_name}"
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(endpoint, headers=headers)
        
        if response.status_code != 200:
            raise Exception(
                f"Failed to get SharePoint site ID: {response.status_code} - {response.text}"
            )
        
        site_data = response.json()
        site_id = site_data.get('id')
        
        if not site_id:
            raise Exception(f"Site ID not found in response: {site_data}")
        
        # Cache the site ID
        self._site_id = site_id
        print(f"[SharePoint] Got and cached site ID: {site_id}")
        return site_id
    
    def download_file_by_id(self, file_id: str, use_cache: bool = False) -> bytes:
        """
        Download a file from SharePoint using its document ID.
        
        Args:
            file_id: The document ID (e.g., from SharePoint sharing link)
            use_cache: Whether to use cached version if available (default: False for testing)
        
        Returns:
            File content as bytes
        
        Raises:
            Exception: If file download fails
        """
        # Check cache
        cache_key = f"id:{file_id}"
        if use_cache and cache_key in self._cache:
            cache_entry = self._cache[cache_key]
            if time.time() - cache_entry['timestamp'] < self._cache_ttl:
                print(f"[CACHE] Using cached version of file ID: {file_id}")
                return cache_entry['content']
        
        if not use_cache:
            print(f"[NO CACHE] Downloading file by ID: {file_id}")
        
        # Get site ID first
        site_id = self._get_site_id()
        
        # Download file by ID
        access_token = self._get_access_token()
        
        # Construct the SharePoint file download URL using document ID
        # Format: /sites/{site-id}/drive/items/{item-id}/content
        endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{file_id}/content"
        
        print(f"[SharePoint] Downloading from: {endpoint}")
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(endpoint, headers=headers)
        
        if response.status_code != 200:
            raise Exception(
                f"Failed to download file from SharePoint: {response.status_code} - {response.text}"
            )
        
        content = response.content
        
        # Update cache only if caching is enabled
        if use_cache:
            self._cache[cache_key] = {
                'content': content,
                'timestamp': time.time()
            }
            print(f"[CACHE] Downloaded and cached file ID: {file_id}")
        else:
            print(f"[SUCCESS] Downloaded file by ID: {file_id}")
        
        return content
    
    def download_file(self, file_path: str, use_cache: bool = False) -> bytes:
        """
        Download a file from SharePoint site.
        
        Args:
            file_path: Path to the file in SharePoint document library 
                      (e.g., '/Forms & Applications/Delivery Record/Delivery Record Form.xlsx')
            use_cache: Whether to use cached version if available (default: False for testing)
        
        Returns:
            File content as bytes
        
        Raises:
            Exception: If file download fails
        """
        # Check cache
        if use_cache and file_path in self._cache:
            cache_entry = self._cache[file_path]
            if time.time() - cache_entry['timestamp'] < self._cache_ttl:
                print(f"[CACHE] Using cached version of {file_path}")
                return cache_entry['content']
        
        if not use_cache:
            print(f"[NO CACHE] Downloading fresh copy of {file_path}")
        
        # Get site ID first
        site_id = self._get_site_id()
        
        # Download file
        access_token = self._get_access_token()
        
        # Construct the SharePoint file download URL using site ID
        # Format: /sites/{site-id}/drive/root:{file-path}:/content
        # Ensure path starts with /
        if not file_path.startswith('/'):
            file_path = '/' + file_path
        
        encoded_path = requests.utils.quote(file_path)
        endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:{encoded_path}:/content"
        
        print(f"[SharePoint] Downloading from: {endpoint}")
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(endpoint, headers=headers)
        
        if response.status_code != 200:
            raise Exception(
                f"Failed to download file from SharePoint: {response.status_code} - {response.text}"
            )
        
        content = response.content
        
        # Update cache only if caching is enabled
        if use_cache:
            self._cache[file_path] = {
                'content': content,
                'timestamp': time.time()
            }
            print(f"[CACHE] Downloaded and cached file from SharePoint: {file_path}")
        else:
            print(f"[SUCCESS] Downloaded file from SharePoint: {file_path}")
        
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


# Create a singleton instance if SharePoint config is available
sharepoint_client = None

if config.SHAREPOINT_CLIENT_ID and config.SHAREPOINT_CLIENT_SECRET and config.SHAREPOINT_TENANT_ID:
    sharepoint_client = SharePointClient(
        client_id=config.SHAREPOINT_CLIENT_ID,
        client_secret=config.SHAREPOINT_CLIENT_SECRET,
        tenant_id=config.SHAREPOINT_TENANT_ID,
        hostname=config.SHAREPOINT_HOSTNAME,
        site_name=config.SHAREPOINT_SITE_NAME
    )

