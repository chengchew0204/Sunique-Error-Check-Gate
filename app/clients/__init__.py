"""
Clients package for InFlow Error Check Gate.
Exports all API client instances.
"""

from app.clients.inflow_client import inflow_client
from app.clients.onedrive_client import onedrive_client
from app.clients.sharepoint_client import sharepoint_client
from app.clients.outlook_client import outlook_client

__all__ = ['inflow_client', 'onedrive_client', 'sharepoint_client', 'outlook_client']

