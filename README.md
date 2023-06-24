# Mega.nz Auto Login and Document Import

This script automates the login process to Mega.nz and allows you to import a document into your Mega.nz account.

## Prerequisites

- Python 3.6 or later
- The Selenium library: `pip install selenium`
- A compatible web driver for your browser (e.g., ChromeDriver for Google Chrome)

## Usage

1. Install the Selenium library:

```
pip install selenium
```


2. Download the appropriate web driver for your browser and place it in a directory. You can find the ChromeDriver for Google Chrome [here](https://sites.google.com/a/chromium.org/chromedriver/).

3. Clone or download the code to your local machine.

4. Replace the following placeholders in the code:

- `'path/to/chromedriver'`: Replace this with the actual path to the web driver executable.
- `'your@email.com'`: Replace this with your Mega.nz login email.
- `'yourpassword'`: Replace this with your Mega.nz login password.
- `'/path/to/document.txt'`: Replace this with the actual path to the document you want to import.

5. Save the modified code file.

6. Run the script using the following command:

```
mega.py
```


The script will automate the login process to your Mega.nz account and import the specified document.

7. After the document is imported, the script will print a success message.

## Note

- This script utilizes the Selenium library to automate the web browsing and interaction with the Mega.nz website.
- Make sure to respect the terms of service and usage policies of Mega.nz while using this script.
