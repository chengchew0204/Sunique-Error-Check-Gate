from typing import Dict, Any, List, Optional
from app.clients.outlook_client import outlook_client
from app.config import config


class NotificationService:
    """
    Service for sending email notifications about validation failures.
    """
    
    def __init__(self, outlook_client_instance, admin_emails: List[str], 
                 from_address: str = None, testing_mode: bool = False, 
                 test_recipient: str = None):
        """
        Initialize the notification service.
        
        Args:
            outlook_client_instance: Instance of OutlookClient
            admin_emails: List of admin email addresses
            from_address: Email address to send from
            testing_mode: If True, all emails go to test_recipient
            test_recipient: Email address to receive test emails
        """
        self.outlook_client = outlook_client_instance
        self.admin_emails = admin_emails
        self.from_address = from_address
        self.testing_mode = testing_mode
        self.test_recipient = test_recipient
    
    def send_validation_failure_notification(
        self,
        validation_result: Dict[Any, Any],
        order_data: Dict[Any, Any]
    ) -> None:
        """
        Send email notification for validation failures or warnings.
        Only sends for confirmed errors, not pending ones.
        
        Args:
            validation_result: Dictionary containing validation results
            order_data: Full sales order data from InFlow
        """
        status = validation_result.get('status', 'unknown')
        
        # Only send notifications for confirmed failures and warnings
        # Do NOT send for 'passed' or 'pending' statuses
        if status in ['passed', 'pending']:
            if status == 'pending':
                pending_count = validation_result.get('pending_count', 0)
                print(f"Skipping notification for pending errors (count: {pending_count}, waiting for 30-minute grace period)")
            return
        
        # Check if Outlook client is configured
        if not self.outlook_client:
            print("=" * 60)
            print("EMAIL ERROR: Outlook client not initialized")
            print("Please configure these environment variables in .env:")
            print("  - OUTLOOK_CLIENT_ID")
            print("  - OUTLOOK_CLIENT_SECRET")
            print("  - OUTLOOK_TENANT_ID")
            print("=" * 60)
            return
        
        # Extract recipient emails
        recipients = self._get_recipients(order_data)
        
        # Override recipients if in testing mode
        if self.testing_mode and self.test_recipient:
            print("=" * 60)
            print("TESTING MODE: Redirecting all emails to test recipient")
            print(f"Original recipients: {recipients}")
            print(f"Test recipient: {self.test_recipient}")
            print("=" * 60)
            recipients = [self.test_recipient]
        
        if not recipients:
            print("=" * 60)
            print("EMAIL ERROR: No recipients configured")
            print(f"ADMIN_EMAILS in config: {self.admin_emails}")
            print("Please configure ADMIN_EMAILS in .env file")
            print("=" * 60)
            return
        
        # Generate email content
        subject = self._generate_subject(validation_result, order_data)
        body_html = self._generate_body_html(validation_result, order_data)
        
        # Send email
        try:
            self.outlook_client.send_email(
                to_addresses=recipients,
                subject=subject,
                body_html=body_html,
                from_address=self.from_address
            )
            print("=" * 60)
            print(f"EMAIL SENT SUCCESSFULLY")
            print(f"To: {', '.join(recipients)}")
            print(f"Subject: {subject}")
            print("=" * 60)
        except Exception as e:
            print("=" * 60)
            print(f"EMAIL ERROR: Failed to send")
            print(f"Error: {str(e)}")
            print("=" * 60)
            raise
    
    def _get_recipients(self, order_data: Dict[Any, Any]) -> List[str]:
        """
        Get list of email recipients (admins + account manager).
        
        Args:
            order_data: Sales order data
        
        Returns:
            List of email addresses
        """
        recipients = list(self.admin_emails)
        
        # Try to extract account manager email from order data
        # This depends on InFlow's data structure - adjust as needed
        account_manager_email = None
        
        # Check various possible locations for account manager email
        if 'customFields' in order_data:
            for field in order_data.get('customFields', []):
                # Handle case where field might be a string instead of dict
                if isinstance(field, dict):
                    if field.get('name', '').lower() in ['account manager email', 'account_manager_email']:
                        account_manager_email = field.get('value')
                        break
        
        # Alternative: check if there's a sales rep or assigned user
        if not account_manager_email and 'assignedTo' in order_data:
            assigned_to = order_data.get('assignedTo', {})
            account_manager_email = assigned_to.get('email')
        
        if account_manager_email and account_manager_email not in recipients:
            recipients.append(account_manager_email)
        
        return recipients
    
    def _generate_subject(self, validation_result: Dict[Any, Any], order_data: Dict[Any, Any]) -> str:
        """
        Generate email subject line.
        
        Args:
            validation_result: Validation results
            order_data: Sales order data
        
        Returns:
            Email subject string
        """
        order_id = validation_result.get('order_id', 'Unknown')
        status = validation_result.get('status', 'unknown').upper()
        order_number = order_data.get('orderNumber', order_id)
        
        return f"[InFlow Validation {status}] Order #{order_number} - Action Required"
    
    def _generate_body_html(self, validation_result: Dict[Any, Any], order_data: Dict[Any, Any]) -> str:
        """
        Generate HTML email body.
        
        Args:
            validation_result: Validation results
            order_data: Sales order data
        
        Returns:
            HTML email body
        """
        order_id = validation_result.get('order_id', 'Unknown')
        order_number = order_data.get('orderNumber', order_id)
        status = validation_result.get('status', 'unknown')
        issues = validation_result.get('issues', [])
        suggested_fixes = validation_result.get('suggested_fixes', [])
        customer_name = order_data.get('customer', {}).get('name', 'Unknown Customer')
        
        # Determine status color
        status_color = {
            'passed': '#28a745',
            'warning': '#ffc107',
            'failed': '#dc3545'
        }.get(status, '#6c757d')
        
        # Build issues HTML (only show confirmed errors, not pending ones)
        issues_html = ""
        issue_counter = 0
        for issue in issues:
            # Skip pending errors in notification
            if issue.get('tracking_status') == 'pending':
                continue
            
            issue_counter += 1
            severity = issue.get('severity', 'error')
            severity_icon = '⚠️' if severity == 'warning' else '❌'
            severity_color = '#ffc107' if severity == 'warning' else '#dc3545'
            
            issues_html += f"""
            <div style="margin-bottom: 15px; padding: 10px; border-left: 4px solid {severity_color}; background-color: #f8f9fa;">
                <strong>{severity_icon} Issue #{issue_counter}: {issue.get('rule', 'Unknown Rule')}</strong><br>
                <span style="color: #6c757d;">{issue.get('message', 'No message provided')}</span>
            </div>
            """
        
        # Build suggested fixes HTML
        fixes_html = ""
        if suggested_fixes:
            fixes_html = "<h3>Suggested Fixes:</h3><ul>"
            for fix in suggested_fixes:
                fixes_html += f"<li>{fix}</li>"
            fixes_html += "</ul>"
        
        # Compose email body
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: {status_color}; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
                .content {{ background-color: #ffffff; padding: 20px; border: 1px solid #dee2e6; border-radius: 0 0 5px 5px; }}
                .order-info {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #dee2e6; font-size: 12px; color: #6c757d; text-align: center; }}
                .btn {{ display: inline-block; padding: 12px 24px; margin: 20px 0; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }}
                .btn:hover {{ background-color: #0056b3; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>InFlow Order Validation {status.upper()}</h1>
                </div>
                <div class="content">
                    <div class="order-info">
                        <strong>Order Number:</strong> {order_number}<br>
                        <strong>Order ID:</strong> {order_id}<br>
                        <strong>Customer:</strong> {customer_name}<br>
                        <strong>Status:</strong> <span style="color: {status_color}; font-weight: bold;">{status.upper()}</span>
                    </div>
                    
                    <h3>Validation Issues Detected:</h3>
                    {issues_html}
                    
                    {fixes_html}
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://app.inflowinventory.com/sales-orders/{order_id}" class="btn" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                            Open Order in InFlow
                        </a>
                    </div>
                    
                    <p style="margin-top: 20px; color: #6c757d;">
                        Please review the order and make the necessary corrections.
                    </p>
                </div>
                <div class="footer">
                    This is an automated message from the InFlow Error Check Gate system.<br>
                    Timestamp: {validation_result.get('timestamp', 'Unknown')}
                </div>
            </div>
        </body>
        </html>
        """
        
        return html


# Create a singleton instance
notification_service = NotificationService(
    outlook_client_instance=outlook_client,
    admin_emails=config.ADMIN_EMAILS,
    from_address=config.EMAIL_FROM_ADDRESS,
    testing_mode=config.EMAIL_TESTING_MODE,
    test_recipient=config.TEST_EMAIL_RECIPIENT
)

