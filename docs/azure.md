# Azure DNS
Azure DNS is a hosting service for DNS domains that provides DNS resolution via the Azure infrastructure.
[Docs](https://docs.microsoft.com/en-us/python/api/overview/azure/dns?view=azure-python)

There are multiple ways to authenticate with Azure.  We only endorse the use of Service Princples, as username and passwords should only be backed with MFA.

To interact with Azure DNS zone the following are required:
- Subsciption ID
- Tenant ID
- Client ID
- Client Secret

## Create Application registration
We use application registration to create a service principle , which can be used instead of a user account for a very specific task in an automated/non-interactive function. 

Please review [Microsoft Docs](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app) for more details.

1. Sign in to the [Azure portal](https://portal.azure.com/).
2. Search for and select **Azure Active Directory**
3. Under Manage, select **App registrations** > **New registration**
4. Enter a display Name for your application e.g. dnsReaper
6. Specify who can use the application, sometimes called its sign-in audience.  We recommend using **Accounts in this organizational directory only**
7. Don't enter anything for Redirect URI.
8. Select **Register** to complete the initial app registration.
9. Select **Overview** 
10. Make a record of the following fields
    - Application (Client) ID
    - Directory (tenant) ID
11. Select **Certificates & secrets** > **Client secrets** > **New client secret**
12. Add a description for your client secret.
Select an expiration for the secret or specify a custom lifetime.
    - Client secret lifetime is limited to two years (24 months) or less. You can't specify a custom lifetime longer than 24 months.
    - Microsoft recommends that you set an expiration value of less than 12 months.
13. Select Add.
14. Record the secret's value for use in your client application code. This secret value is never displayed again after you leave this page, so make a note or save it in a password vault.
15. Select **API permission** > **Client secrets** > **New client secret**
16. Click on **Crant admin consent**

## Assign Service Principle to DNS zones
We now need to assign the service principle permissions on the DNS zones which are in scope.

1. Sign in to the [Azure portal](https://portal.azure.com/).
2. Search for and select **DNS zones**
3. For each of the DNS zones do the following
    1. Click on the DNS name
    2. Select **Access control (IAM)** > **Add role assignment**
    3. Select **Reader**
    4. Click **next**
    5. Click on **+ Select members**
    6. Type in the Application resgitration name created above e.g. dnsReaper
    7. Click on **Review + assign**
    8. Click on **Review + assign**

## TODO - Future enhancements
- Client certificates
- Enhancements to README