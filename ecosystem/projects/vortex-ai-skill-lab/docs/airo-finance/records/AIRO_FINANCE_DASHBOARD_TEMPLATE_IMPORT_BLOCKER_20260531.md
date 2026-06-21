# AIRO Finance — Dashboard Template Import API Blocker Record

**Date**: 2026-05-31  
**Task**: Dashboard Excel Template Import Recovery Pass  
**Status**: BLOCKED — API import failed due to disabled OAuth client and service permissions  

---

## Blocker Analysis

We attempted to automate the import of `docs/airo-finance/references/AIRO_Finance_Dashboard_reference_20260531.xlsx` as the template sheet `_AIRO_Dashboard_Template_Claude` using Google Drive & Sheets APIs. However, the automated process is blocked due to the following API/credential failures:

### 1. Disabled OAuth Client ID (`696470833277`)
* **Impacted Credentials**: 
  * `~/.local/share/airo-personal-workflow/google/token.local.json`
  * `~/.config/airo-personal-workflow/oauth-token.json`
  * Stored credentials in `gogcli` keyring (`earnsai9997@gmail.com`)
* **Error Encountered**:
  ```
  round trip: base token source: oauth2: "disabled_client" "The OAuth client was disabled."
  ```
* **Details**: The primary OAuth Client ID used by the project tools has been disabled on the Google Cloud Console. Any request to refresh or authenticate using these credentials fails with `disabled_client`, preventing both Sheets and Drive API access.

### 2. Google Sheets API Disabled in Clasp Project (`1072944905499`)
* **Impacted Credentials**: `~/.clasprc.json` (associated with user `progamer6918@gmail.com`)
* **Errors Encountered**:
  * **Drive API (list)**: `SUCCESS`
  * **Sheets API (get)**: 
    ```
    Google Sheets API has not been used in project 1072944905499 before or it is disabled. 
    Enable it by visiting https://console.developers.google.com/apis/api/sheets.googleapis.com/overview?project=1072944905499
    ```
  * **Enable Service Attempt**: `PERMISSION_DENIED`
* **Details**: While these credentials have working Drive API access, the default clasp project `1072944905499` has the Sheets API disabled. Since this is Google's public project, our active account does not have administrative permissions to enable the service.

### 3. Insufficient Scopes on `gcloud` Credentials (`progamer6918@gmail.com`)
* **Impacted Credentials**: Active `gcloud` SDK login session
* **Errors Encountered**:
  ```
  Request had insufficient authentication scopes. (ACCESS_TOKEN_SCOPE_INSUFFICIENT)
  ```
* **Details**: Sourcing the access token directly from `gcloud auth print-access-token` fails for Sheets and Drive API requests because the session only has Cloud Platform management scopes. Authorizing Sheets and Drive scopes requires running the interactive browser-based `gcloud auth application-default login` command, which is blocked by the user's requirement not to use interactive/browser flows.

---

## Action Plan & Recommendation

Because the API import flow has failed, we must halt the automated process as specified in the instructions.

### Manual Import Workaround (Method A)
Please manually import the reference sheet via your web browser:
1. Open the target spreadsheet in Google Sheets: [AIRO Finance (1CKARXGurxZ0Rby3-_iisVS0_r65JM6ZaT6tbAJUF7sU)](https://docs.google.com/spreadsheets/d/1CKARXGurxZ0Rby3-_iisVS0_r65JM6ZaT6tbAJUF7sU/)
2. Go to **File → Import**
3. Select the **Upload** tab and drag-and-drop the reference Excel file:
   `docs/airo-finance/references/AIRO_Finance_Dashboard_reference_20260531.xlsx`
4. In the import dialog, select:
   * **Import location**: `Insert new sheet(s)`
   * **Convert numbers, dates, and formulas**: `Yes`
5. Click **Import data**.
6. Google Sheets will create a new sheet tab named `Dashboard`.
7. **Rename** the imported sheet exactly to:
   `_AIRO_Dashboard_Template_Claude`
8. Keep it visible so we can verify the formatting.
