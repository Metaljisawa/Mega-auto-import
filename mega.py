import mega

# Authenticate to Mega.nz using your email and password
mega_client = mega.MegaClient()
mega_client.login('your@email.com', 'yourpassword')

# Create a folder in Mega.nz
folder_name = 'Recherche Master'
folder = mega_client.create_folder(folder_name)
print(F'Folder has been created with Name "{folder_name}" and URL: "https://mega.nz/folder/{folder["h"]}".')

# Iterate through all the files in the "Recherche Master" folder on your local storage
local_folder = '/path/to/Recherche Master'
for root, dirs, files in os.walk(local_folder):
    for file in files:
        # Construct the file's path on your local machine
        local_file_path = os.path.join(root, file)
        # Upload the file to Mega.nz
        mega_client.upload(local_file_path, folder['h'])
