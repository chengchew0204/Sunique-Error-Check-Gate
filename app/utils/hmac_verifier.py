import hmac
import hashlib
import base64
from typing import Optional


class HMACVerifier:
    """
    Verifies HMAC signatures from InFlow webhooks.
    InFlow sends a base64-encoded HMAC-SHA256 signature in the x-inflow-hmac-sha256 header.
    """
    
    def __init__(self, secret_key: str):
        """
        Initialize the HMAC verifier with a secret key.
        
        Args:
            secret_key: The webhook subscription secret key from InFlow
        """
        self.secret_key = secret_key.encode('utf-8')
    
    def verify(self, payload: bytes, signature_header: Optional[str]) -> bool:
        """
        Verify the HMAC signature of a webhook payload.
        
        Args:
            payload: The raw webhook payload bytes
            signature_header: The x-inflow-hmac-sha256 header value (base64-encoded)
        
        Returns:
            True if the signature is valid, False otherwise
        """
        if not signature_header:
            return False
        
        try:
            # Decode the base64-encoded signature from the header
            expected_signature = base64.b64decode(signature_header)
            
            # Calculate the HMAC-SHA256 signature
            calculated_hmac = hmac.new(
                self.secret_key,
                payload,
                hashlib.sha256
            ).digest()
            
            # Compare signatures using constant-time comparison
            return hmac.compare_digest(calculated_hmac, expected_signature)
        
        except Exception as e:
            print(f"Error verifying HMAC signature: {e}")
            return False

