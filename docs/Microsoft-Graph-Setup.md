# Microsoft Graph API Setup Guide

This guide explains how to set up Microsoft Graph API access for Outlook email notifications and OneDrive file access.

## Overview

The Error Check Gate uses Microsoft Graph API for:
1. **Outlook API** - Sending email notifications
2. **OneDrive API** - Downloading delivery record Excel file

## Prerequisites

- Azure AD (Active Directory) account with admin access
- Microsoft 365 subscription

## Step 1: Register Azure AD Application

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Fill in:
   - **Name**: InFlow Error Check Gate
   - **Supported account types**: Single tenant
   - **Redirect URI**: Leave empty (we're using client credentials flow)
5. Click **Register**

## Step 2: Create Client Secret

1. In your app registration, go to **Certificates & secrets**
2. Click **New client secret**
3. Set description: "Error Check Gate Secret"
4. Set expiration: Choose based on your security policy (24 months recommended)
5. Click **Add**
6. **Important:** Copy the secret value immediately (you won't see it again)

Save these values:
- **Client ID** (Application ID)
- **Client Secret** (the value you just copied)
- **Tenant ID** (Directory ID, found in Overview)

## Step 3: Configure API Permissions

### For Outlook (Email Sending)

1. In your app registration, go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Select **Application permissions** (not Delegated)
5. Add these permissions:
   - `Mail.Send` - Send mail as any user

### For OneDrive (File Access)

6. Still in **Add a permission** > **Microsoft Graph** > **Application permissions**
7. Add these permissions:
   - `Files.Read.All` - Read files in all site collections
   - Or more specifically: `Sites.Read.All` if files are in SharePoint

### Grant Admin Consent

8. Click **Grant admin consent for [Your Organization]**
9. Confirm the consent

**Important:** Admin consent is required for application permissions.

## Step 4: Configure Email Sending

### Option A: Send as Authenticated User

If you have a service account email:

1. Create a Microsoft 365 user (e.g., `notifications@yourdomain.com`)
2. Assign appropriate license
3. Update the code to use: `from_address="notifications@yourdomain.com"`

### Option B: Send on Behalf of Any User

With `Mail.Send` application permission, you can send as any user in your organization.

**In Outlook client code:**
```python
outlook_client.send_email(
    to_addresses=['recipient@example.com'],
    subject='Test Email',
    body_html='<p>Test message</p>',
    from_address='sender@yourdomain.com'  # Any valid user in your org
)
```

## Step 5: Configure OneDrive Access

### Set File Path

The `DELIVERY_RECORD_FILE_PATH` in `.env` should be:

```
DELIVERY_RECORD_FILE_PATH=/Documents/Delivery Record Form.xlsx
```

**Path Format:**
- Starts with `/`
- Relative to the user's OneDrive root or shared drive
- Include full path with filename and extension

### Alternative: Use SharePoint

If the file is in SharePoint:

1. Add `Sites.Read.All` permission
2. Update OneDrive client to use SharePoint endpoints
3. Modify path to: `/sites/{site-name}/Shared Documents/file.xlsx`

## Step 6: Update Environment Variables

Add to your `.env` file:

```bash
# Outlook API
OUTLOOK_CLIENT_ID=your-application-client-id
OUTLOOK_CLIENT_SECRET=your-client-secret-value
OUTLOOK_TENANT_ID=your-tenant-id

# OneDrive API
ONEDRIVE_CLIENT_ID=your-application-client-id
ONEDRIVE_CLIENT_SECRET=your-client-secret-value
ONEDRIVE_TENANT_ID=your-tenant-id
DELIVERY_RECORD_FILE_PATH=/Documents/Delivery Record Form.xlsx
```

**Note:** You can use the same App Registration for both Outlook and OneDrive, so Client ID, Secret, and Tenant ID will be the same.

## Testing Authentication

### Test Outlook API

```python
from app.clients.outlook_client import outlook_client

outlook_client.send_email(
    to_addresses=['test@yourdomain.com'],
    subject='Test Email from Error Check Gate',
    body_html='<p>This is a test email.</p>'
)
```

### Test OneDrive API

```python
from app.clients.onedrive_client import onedrive_client

file_content = onedrive_client.download_file('/Documents/test.xlsx')
print(f"Downloaded {len(file_content)} bytes")
```

## Troubleshooting

### "Failed to acquire access token"

**Causes:**
- Invalid Client ID, Secret, or Tenant ID
- Client secret expired
- Wrong authentication flow

**Solutions:**
1. Verify credentials in Azure Portal
2. Check if client secret expired, create new one if needed
3. Ensure using `acquire_token_for_client` (not user flow)

### "Insufficient privileges"

**Causes:**
- Missing API permissions
- Admin consent not granted
- Wrong permission type (Delegated vs Application)

**Solutions:**
1. Check API permissions in Azure Portal
2. Click "Grant admin consent"
3. Ensure using Application permissions (not Delegated)

### "Forbidden" when sending email

**Causes:**
- Missing `Mail.Send` permission
- Trying to send from invalid email address

**Solutions:**
1. Verify `Mail.Send` application permission is granted
2. Ensure from_address is a valid user in your organization

### "File not found" for OneDrive

**Causes:**
- Incorrect file path
- Wrong OneDrive user
- File in SharePoint, not personal OneDrive

**Solutions:**
1. Verify file path in OneDrive
2. Use Microsoft Graph Explorer to test path
3. Check if file is in SharePoint instead

## Security Best Practices

1. **Rotate secrets regularly** - Set expiration and create reminders
2. **Use least privilege** - Only grant necessary permissions
3. **Audit access** - Monitor API usage in Azure AD logs
4. **Secure storage** - Never commit secrets to git
5. **Use Azure Key Vault** - For production, store secrets in Key Vault

## Production Considerations

### For Azure Functions Deployment

Use Managed Identity instead of client secrets:

1. Enable System Managed Identity on your Azure Function
2. Grant API permissions to the Managed Identity
3. Update code to use `ManagedIdentityCredential`

### For AWS Lambda Deployment

Store secrets in AWS Secrets Manager or Parameter Store:

1. Create secret in AWS Secrets Manager
2. Grant Lambda execution role permission to read secret
3. Update code to fetch secrets from Secrets Manager at runtime

## Additional Resources

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [MSAL Python Documentation](https://msal-python.readthedocs.io/)
- [Azure AD App Registration Guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) - Test API calls

