import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # InFlow API Configuration
    INFLOW_API_KEY = os.getenv('INFLOW_API_KEY')
    INFLOW_COMPANY_ID = os.getenv('INFLOW_COMPANY_ID')
    INFLOW_API_BASE_URL = os.getenv('INFLOW_API_BASE_URL', 'https://api.inflow.com/v1')
    
    # Webhook Configuration
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
    
    # OneDrive Configuration
    ONEDRIVE_CLIENT_ID = os.getenv('ONEDRIVE_CLIENT_ID')
    ONEDRIVE_CLIENT_SECRET = os.getenv('ONEDRIVE_CLIENT_SECRET')
    ONEDRIVE_TENANT_ID = os.getenv('ONEDRIVE_TENANT_ID')
    DELIVERY_RECORD_FILE_PATH = os.getenv('DELIVERY_RECORD_FILE_PATH')
    
    # SharePoint Configuration (can reuse OneDrive credentials or use separate ones)
    SHAREPOINT_CLIENT_ID = os.getenv('SHAREPOINT_CLIENT_ID', ONEDRIVE_CLIENT_ID)
    SHAREPOINT_CLIENT_SECRET = os.getenv('SHAREPOINT_CLIENT_SECRET', ONEDRIVE_CLIENT_SECRET)
    SHAREPOINT_TENANT_ID = os.getenv('SHAREPOINT_TENANT_ID', ONEDRIVE_TENANT_ID)
    SHAREPOINT_HOSTNAME = os.getenv('SHAREPOINT_HOSTNAME', 'suniquecabinetry.sharepoint.com')
    SHAREPOINT_SITE_NAME = os.getenv('SHAREPOINT_SITE_NAME', 'sccr')
    SHAREPOINT_CACHE_ENABLED = os.getenv('SHAREPOINT_CACHE_ENABLED', 'False').lower() == 'true'
    
    # Delivery Record Form - can use either document ID (preferred) or file path
    # Document ID extracted from SharePoint sharing link (more reliable)
    SHAREPOINT_DELIVERY_RECORD_ID = os.getenv('SHAREPOINT_DELIVERY_RECORD_ID', 'ceb0d1f8-e4e2-4acb-b786-24dbe37c8ca3')
    # Fallback to path if ID doesn't work
    SHAREPOINT_DELIVERY_RECORD_PATH = os.getenv(
        'SHAREPOINT_DELIVERY_RECORD_PATH',
        '/Sunique International Regular Order/Documents/Forms & Applications/Delivery Record Form.xlsx'
    )
    
    # Outlook API Configuration
    OUTLOOK_CLIENT_ID = os.getenv('OUTLOOK_CLIENT_ID')
    OUTLOOK_CLIENT_SECRET = os.getenv('OUTLOOK_CLIENT_SECRET')
    OUTLOOK_TENANT_ID = os.getenv('OUTLOOK_TENANT_ID')
    
    # Email Configuration
    ADMIN_EMAILS = [email.strip() for email in os.getenv('ADMIN_EMAILS', '').split(',') if email.strip()]
    EMAIL_FROM_ADDRESS = os.getenv('EMAIL_FROM_ADDRESS', 'info@suniquecabinetry.com')
    
    # Testing Mode - when True, all emails go to TEST_EMAIL_RECIPIENT
    EMAIL_TESTING_MODE = os.getenv('EMAIL_TESTING_MODE', 'True').lower() == 'true'
    TEST_EMAIL_RECIPIENT = os.getenv('TEST_EMAIL_RECIPIENT', '')
    
    # Business Logic Configuration
    CREDIT_CARD_FEE_PERCENTAGE = float(os.getenv('CREDIT_CARD_FEE_PERCENTAGE', '0.03'))
    TUK_IDENTIFIER_PATTERN = os.getenv('TUK_IDENTIFIER_PATTERN', 'TUK')
    
    # Flask Configuration
    FLASK_PORT = int(os.getenv('FLASK_PORT', '8000'))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Assembly Fee Formula
    # This can be customized based on business requirements
    # Example: base_fee + (num_items * item_fee)
    ASSEMBLY_FEE_BASE = float(os.getenv('ASSEMBLY_FEE_BASE', '0'))
    ASSEMBLY_FEE_PER_ITEM = float(os.getenv('ASSEMBLY_FEE_PER_ITEM', '0'))
    
    @staticmethod
    def validate():
        required_vars = [
            'INFLOW_API_KEY',
            'INFLOW_COMPANY_ID',
            'WEBHOOK_SECRET',
        ]
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    @staticmethod
    def validate_basic():
        """Validate only essential variables (for initial setup without webhook secret)"""
        required_vars = [
            'INFLOW_API_KEY',
            'INFLOW_COMPANY_ID',
        ]
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

config = Config()

