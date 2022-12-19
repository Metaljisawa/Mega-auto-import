# Mega-auto-import
Auto-import a folder after any updates from this folder, to upload it in Mega.nz

# Mega Uploader

This script allows you to automatically upload a folder from your local storage to Mega.nz.

## Prerequisites

- Python 3.6 or later
- The `mega.py` library: `pip install mega.py`

## Usage

To use the script, you will need to provide your Mega.nz email and password in the `login` function.

```python
mega_client = mega.MegaClient()
mega_client.login('your@email.com', 'yourpassword')
```
You can then specify the local folder you want to upload and the name of the folder you want to create in Mega.nz:
```python
local_folder = '/path/to/local/folder'
folder_name = 'Mega Folder'
```
Finally, run the script with the python command:

```python
python script.py
```
The script will create a folder with the specified name in Mega.nz and upload all the files in the local folder to the Mega.nz folder.

##Note

The mega.py library provides many other functions that you can use to access and manipulate your Mega.nz account, such as downloading files, deleting files, and moving files between folders. You can find more information about these functions in the library's documentation.
