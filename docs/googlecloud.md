# Google Cloud

## Description
The Google Cloud provider connects to Google Cloud and retrieves all records associated with a domain.

To enumerate a domain's subdomains, you need to provide a valid project ID and set the `GOOGLE_APPLICATION_CREDENTIALS` to your JSON credential file's full path.

## Create Google Cloud Private Key
To to get the Private key:

1. Navigate to https://cloud.google.com/ and select **Go to console**, or [click here](https://console.cloud.google.com/)
1. Make sure the correct project by checking the drop down at top left of the page. If the project needs to be changed, click the drop down and select the correct project from the popup
1. Select on `API & Services` under Quick Access
1. On the side bar, select `Enabled APIs & services`
1. At the top of the page, select **+ Enable APIs and Services**
1. In the search bar, search for `Cloud DNS API`, and select `Cloud DNS API`
1. On the `Cloud DNS API`, select **Enable**. 
1. Then, on the `Cloud DNS API` page, select the `Credentials` tab
1. Below the `Credentials compatible with this API` section, go to `Service Accounts`, and click on the `Manage service accounts`
1. At the top of the page, select **+ Create Service Account**
1. Give the service a `Service account ID`
1. Click **Create and Continue**
1. Click the `Select a role` dropdown, scroll down to `DNS`, then select `DNS Reader`
1. Then, click **Done**
1. Back on the Service Account page, select the service account you just made
1. Select the `Keys` tab at the top
1. Click the `Add Key` dropdown and select `Create new key`
1. Ensure the type `JSON` is selected and click `Create`
1. This will download a JSON file to your computer, which can be moved to a suitable location
1. Copy down the full path of the credential file's location, including the file's name and extension
1. Save the file path to the `GOOGLE_APPLICATION_CREDENTIALS` environment variable
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
To set up Google Cloud with docker, you will need to mount the JSON credential file.

To mount the file:
On Windows:
```
docker run -v C:\file\path\containing\credentials.json:/app/credentials.json
```
On Linux and MacOS
```
docker run -v /local/path/to/credentials.json:/app/credentials.json
```

To pass the environment variable:
```
-e GOOGLE_APPLICATION_CREDENTIALS='/app/credentials.json'
```

The full command would look like this:
```
docker run punksecurity/dnsreaper -v /local/path/to/credentials.json:/app/credentials.json -e GOOGLE_APPLICATION_CREDENTIALS='/app/credentials.json'
```
