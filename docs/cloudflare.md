# Cloudflare

This page contains specific information about the Cloudflare provider module.

Our Cloudflare provider will utilise the Cloudflare client provider located in [github](https://github.com/cloudflare/python-cloudflare)

The Cloudflare module will require read only rights to the Domain zones in Cloudflare, in order to read the DNS records.

## Create Cloudflare token

To get started creating an API Token, 

1. Log in to the Cloudflare dashboard
2. Go to User Profile -> API Tokens 
3. From the API Token home screen select **Create Token**.
4. Select **Use Template** on the **Edit zone DNS**
5. Change the **Token Name** from **Edit zone DNS** to **Read zone DNS**
5. Change the permission from **Edit** to **Read**
6. This step is optional, but you can edit the **Zone Resource** to restrict to a specific account or Domain DNS.
7. Click **Continue to summary**
8. Extract the API token and store in a safe location

