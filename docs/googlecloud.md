# Google Cloud

## Description
The Google Cloud provider connects to Google Cloud and retrieves records associated with a domain.

## Create Google Cloud Private Key
To to get the Private key:

1. Navigate to https://cloud.google.com/ and select **Go to console**, or [click here](https://console.cloud.google.com/)
2. Make sure the correct project by checking the drop down at top left of the page. If the project needs to be changed, click the drop down and select the correct project from the popup
3. Select on `API & Services` under Quick Access
4. On the side bar, select `Enabled APIs & services`
5. At the top of the page, select **+ Enable APIs and Services**
6. In the search bar, search for `Cloud DNS API`, and select `Cloud DNS API`
7. On the `Cloud DNS API`, select **Enable**. 
8. Then, on the `Cloud DNS API` page, select the `Credentials` tab
9. Below the `Credentials compatible with this API` section, go to `Service Accounts`, and click on the `Manage service accounts`
10. At the top of the page, select **+ Create Service Account**
11. Give the service a `Service account ID`
12. Click **Create and Continue**
13. Click the `Select a role` dropdown, scroll down to `DNS`, then select `DNS Reader`
14. Then, click **Done**
15. Back on the Service Account page, select the service account you just made
16. Select the `Keys` tab at the top
17. Click the `Add Key` dropdown and select `Create new key`
18. Ensure the type `JSON` is selected and click `Create`
19. This will download a JSON file to your computer, switch can be moved to a suitable location
20. Copy down the full path of the files location, including the files name and extension
21. Save the file path to the `GOOGLE_APPLICATION_CREDENTIALS` environment variable
    a. On Linux or MacOS:
        ```
        export GOOGLE_APPLICATION_CREDENTIALS="/path/to/json/file.json"
        ```

    b. On Windows:
        Powershell
        ```
        $ENV:GOOGLE_APPLICATION_CREDENTIALS="C:\\path\\to\\file\\file.json"
        ```

        CMD
        ```
        set GOOGLE_APPLICATION_CREDENTIALS="C:\\path\\to\\file\\file.json"
        ```

To get the project id:

1. Navigate to https://cloud.google.com/ and select **Go to console**, or [click here](https://console.cloud.google.com/)
2. The project idea will be shown on the `Welcome page`. If the correct project isn't selected, click on the dropdown at the top left of the page. From here, you can search for your project and copy the project id under the ID column.


## Usage
The `--project-id` option is used to provide your Google Cloud project's ID.

The `GOOGLE_APPLICATION_CREDENTIALS` is an environment variable used to tell DNSReaper the location of your JSON credential file.

## Docker Usage

