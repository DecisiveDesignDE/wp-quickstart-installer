import tempfile
import os
import requests
import zipfile
import shutil
import json
from ftplib import FTP  # Add this import
import paramiko  # Add this import

def create_temp_folder():
    temp_dir = tempfile.mkdtemp()
    return temp_dir, f"Temporary folder created at: {temp_dir}"

def download_wordpress(temp_folder):
    url = "https://wordpress.org/latest.zip"
    file_path = os.path.join(temp_folder, "wordpress.zip")
    
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return file_path, f"WordPress downloaded successfully to {file_path}"
    else:
        return None, "Failed to download WordPress."

def unzip_wordpress(zip_path, temp_folder):
    if zip_path and os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)
        extracted_path = os.path.join(temp_folder, "wordpress")
        if os.path.exists(extracted_path):
            return extracted_path, f"WordPress extracted to {extracted_path}"
    
    return None, "WordPress zip file not found or extraction failed."

def extract_zip(file_path, destination_folder):
    if file_path and os.path.exists(file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
        return f"Extracted {file_path} to {destination_folder}"
    return f"Extraction failed for {file_path}" 

def get_plugin_download_url(plugin_slug):
    api_url = f"https://api.wordpress.org/plugins/info/1.2/?action=plugin_information&slug={plugin_slug}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("download_link")
    
    return None

def download_plugin(plugin_slug, temp_folder):
    plugin_url = get_plugin_download_url(plugin_slug)
    if not plugin_url:
        return None, f"Failed to retrieve download URL for {plugin_slug}"
    
    file_path = os.path.join(temp_folder, f"{plugin_slug}.zip")
    response = requests.get(plugin_url, stream=True)
    
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return file_path, f"{plugin_slug} downloaded successfully to {file_path}"
    else:
        return None, f"Failed to download {plugin_slug}."

def get_theme_download_url(theme_slug):
    api_url = f"https://api.wordpress.org/themes/info/1.2/?action=theme_information&request[slug]={theme_slug}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("download_link")
    
    return None

def download_theme(theme_slug, temp_folder):
    theme_url = get_theme_download_url(theme_slug)
    if not theme_url:
        return None, f"Failed to retrieve download URL for {theme_slug}"
    
    file_path = os.path.join(temp_folder, f"{theme_slug}.zip")
    response = requests.get(theme_url, stream=True)
    
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return file_path, f"{theme_slug} downloaded successfully to {file_path}"
    else:
        return None, f"Failed to download {theme_slug}."

def install_plugins_and_themes(plugin_files, theme_files, wordpress_folder):
    plugins_folder = os.path.join(wordpress_folder, "wp-content", "plugins")
    themes_folder = os.path.join(wordpress_folder, "wp-content", "themes")
    os.makedirs(plugins_folder, exist_ok=True)
    os.makedirs(themes_folder, exist_ok=True)
    
    messages = []
    for plugin in plugin_files:
        if plugin:
            messages.append(extract_zip(plugin, plugins_folder))
    
    for theme in theme_files:
        if theme:
            messages.append(extract_zip(theme, themes_folder))
    
    messages.append("All plugins and themes installed successfully.")
    return messages

def upload_via_ftp(server, username, password, port, wordpress_folder):
    ftp = FTP()
    ftp.connect(server, int(port))
    ftp.login(username, password)
    print("FTP_CONNECTION_OPENED")
    print("UPLOADING_FILES")
    for root, dirs, files in os.walk(wordpress_folder):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                ftp.storbinary(f'STOR {os.path.relpath(file_path, wordpress_folder)}', f)
    ftp.quit()
    print("ALL_FILES_UPLOADED")

def upload_via_sftp(server, username, password, port, wordpress_folder):
    transport = paramiko.Transport((server, int(port)))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    print("FTP_CONNECTION_OPENED")
    print("UPLOADING_FILES")
    for root, dirs, files in os.walk(wordpress_folder):
        for file in files:
            file_path = os.path.join(root, file)
            sftp.put(file_path, os.path.relpath(file_path, wordpress_folder))
    sftp.close()
    transport.close()
    print("ALL_FILES_UPLOADED")

def main():
    temp_folder, msg = create_temp_folder()
    print(msg)
    
    wordpress_zip, msg = download_wordpress(temp_folder)
    print(msg)
    
    wordpress_folder, msg = unzip_wordpress(wordpress_zip, temp_folder)
    print(msg)
    
    # Read selected options from file
    with open("selections.json", "r") as file:
        selections = json.load(file)
    
    selected_plugins = selections.get("plugins", [])
    selected_themes = selections.get("themes", [])
    
    for plugin in selected_plugins:
        file_path, msg = download_plugin(plugin, temp_folder)
        print(msg)
    
    for theme in selected_themes:
        file_path, msg = download_theme(theme, temp_folder)
        print(msg)
    
    plugin_files = [os.path.join(temp_folder, f"{plugin}.zip") for plugin in selected_plugins]
    theme_files = [os.path.join(temp_folder, f"{theme}.zip") for theme in selected_themes]
    messages = install_plugins_and_themes(plugin_files, theme_files, wordpress_folder)
    
    for msg in messages:
        print(msg)
    
    # Check final status
    if os.path.exists(wordpress_folder) and os.path.exists(os.path.join(wordpress_folder, "wp-content")):
        print("Installation completed successfully.")
    else:
        print("Installation failed. Please check the logs.")
    
    # Read connection data from file
    with open("connection_data.json", "r") as f:
        connection_data = json.load(f)
    
    server = connection_data["server"]
    username = connection_data["username"]
    password = connection_data["password"]
    port = connection_data["port"]
    connection_type = connection_data["connection_type"]
    
    # Upload contents via FTP or SFTP
    if connection_type == "FTP":
        upload_via_ftp(server, username, password, port, wordpress_folder)
    else:
        upload_via_sftp(server, username, password, port, wordpress_folder)
    
    # Delete the temporary folder
    try:
        os.remove(wordpress_zip)
        shutil.rmtree(temp_folder)
        print(f"Temporary folder {temp_folder} deleted successfully.")
    except Exception as e:
        print(f"Failed to delete temporary folder {temp_folder}. Error: {e}")
    
    print("SCRIPT_DONE")  # Final signal for 05.py

if __name__ == "__main__":
    main()
