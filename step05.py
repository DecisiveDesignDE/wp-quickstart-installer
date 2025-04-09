import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import winsound
import json
import sys
import tempfile
import os
import requests
import zipfile
import shutil
from ftplib import FTP
import paramiko

PLUGIN_SLUGS = {
    "Elementor": "elementor",
    "Contact Form 7": "contact-form-7",
    "Yoast SEO": "wordpress-seo",
    "WooCommerce": "woocommerce",
    "LiteSpeed Cache": "litespeed-cache",
    "Really Simple SSL": "really-simple-ssl",
    "Yoast Duplicate Post": "duplicate-post",
    "WP Mail SMTP": "wp-mail-smtp",
    "Autoptimize": "autoptimize",
    "Duplicator": "duplicator",
    "WP Fastest Cache": "wp-fastest-cache"
}

THEME_SLUGS = {
    "Hello Elementor": "hello-elementor",
    "Astra": "astra",
    "Kadence": "kadence",
    "GeneratePress": "generatepress",
    "Storefront": "storefront",
    "Hello Biz": "hello-biz"
}

class Step05(tk.Frame):
    def __init__(self, parent, controller, selected_plugins, selected_themes):
        super().__init__(parent)
        self.controller = controller
        self.selected_plugins = selected_plugins
        self.selected_themes = selected_themes
        self.configure(bg="#f4f4f4")

        self.installation_thread = None  # Initialize the installation thread

        # Headline
        title_label = tk.Label(self, text="Installation", font=("Arial", 18, "bold"), bg="#f4f4f4")
        title_label.pack(pady=(20, 10))

        # Installation Notice
        notice_text = (
            "We will now install WordPress, the selected Plugin(s) and Theme(s) to your server. ",
            "Again, please make sure to backup your files if the folder is not empty.",
            "Only if everything is correct, you may start by clicking the button"
        )
        notice_label = tk.Label(self, text=notice_text, wraplength=750, justify="left", bg="#f4f4f4", font=("Arial", 12))
        notice_label.pack(pady=(10, 20), padx=20)

        # List of selected installations
        install_frame = tk.Frame(self, bg="#f4f4f4")
        install_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Subheading
        subheading_label = tk.Label(install_frame, text="The following will be installed", font=("Arial", 12, "bold"), bg="#f4f4f4")
        subheading_label.pack(anchor="w")

        install_list_frame = tk.Frame(install_frame, bg="#f4f4f4")
        install_list_frame.pack(fill=tk.BOTH, expand=True)

        install_list_scrollbar = tk.Scrollbar(install_list_frame)
        install_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.install_list = tk.Text(install_list_frame, wrap=tk.WORD, height=4, font=("Arial", 12), bg="white", state=tk.DISABLED, yscrollcommand=install_list_scrollbar.set)
        self.install_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        install_list_scrollbar.config(command=self.install_list.yview)

        # Populate install list
        self.install_list.config(state=tk.NORMAL)
        self.install_list.insert(tk.END, "WordPress Core\n")
        for plugin in self.selected_plugins:
            self.install_list.insert(tk.END, f"{plugin} (Plugin)\n")
        for theme in self.selected_themes:
            self.install_list.insert(tk.END, f"{theme} (Theme)\n")
        self.install_list.config(state=tk.DISABLED)

        # Start Button
        start_button = ttk.Button(self, text="START", command=self.start_installation, style="Bold.TButton")
        start_button.pack(pady=10)
        self.start_button = start_button  # Store reference to the start button

        # Status List
        status_frame = tk.Frame(self, bg="#f4f4f4")
        status_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        status_list_scrollbar = tk.Scrollbar(status_frame)
        status_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.status_list = tk.Text(status_frame, wrap=tk.WORD, height=3, font=("Arial", 12), bg="white", state=tk.DISABLED, yscrollcommand=status_list_scrollbar.set)
        self.status_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        status_list_scrollbar.config(command=self.status_list.yview)

        # Button frame
        button_frame = tk.Frame(self, bg="#f4f4f4")
        button_frame.pack(pady=20)

        prev_button = ttk.Button(button_frame, text="< Prev", command=lambda: controller.show_frame("Step04"))
        prev_button.grid(row=0, column=0, padx=10)
        self.prev_button = prev_button  # Store reference to the prev button

        self.next_button = ttk.Button(button_frame, text="> Next", command=lambda: controller.show_frame("Step06"), state=tk.DISABLED)
        self.next_button.grid(row=0, column=1, padx=10)

        # Styling
        style = ttk.Style()
        style.configure("Bold.TButton", font=("Arial", 12, "bold"), padding=10)

    def start_installation(self):
        self.start_button.pack_forget()  # Remove the start button
        self.progress_label = tk.Label(self, text="Now installing your WordPress, Themes and Plugins...", font=("Arial", 12), bg="#f4f4f4")
        self.progress_label.pack(pady=10)
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 100

        self.status_list.config(state=tk.NORMAL)
        self.status_list.insert(tk.END, "Starting installation...\nPlease wait as this may take a few minutes.\n")
        self.status_list.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.prev_button.config(state=tk.DISABLED)  # Disable the prev button

        # Update confirmation message
        confirm_label = tk.Label(self, text="This may take several minutes depending on how many Themes and Plugins were chosen. \nPlease be patient and do not close the installation window.", font=("Arial", 12, "bold"), bg="#f4f4f4")
        confirm_label.pack(pady=10)

        def run_installation():
            try:
                temp_folder, msg = self.create_temp_folder()
                self.update_status(msg)

                wordpress_zip, msg = self.download_wordpress(temp_folder)
                self.update_status(msg)

                wordpress_folder, msg = self.unzip_wordpress(wordpress_zip, temp_folder)
                self.update_status(msg)

                for plugin in self.selected_plugins:
                    file_path, msg = self.download_plugin(plugin, temp_folder)
                    self.update_status(msg)

                for theme in self.selected_themes:
                    file_path, msg = self.download_theme(theme, temp_folder)
                    self.update_status(msg)

                plugin_files = [os.path.join(temp_folder, f"{plugin}.zip") for plugin in self.selected_plugins]
                theme_files = [os.path.join(temp_folder, f"{theme}.zip") for theme in self.selected_themes]
                messages = self.install_plugins_and_themes(plugin_files, theme_files, wordpress_folder)

                for msg in messages:
                    self.update_status(msg)

                if os.path.exists(wordpress_folder) and os.path.exists(os.path.join(wordpress_folder, "wp-content")):
                    self.update_status("Installation completed successfully.")
                else:
                    self.update_status("Installation failed. Please check the logs.")

                with open("connection_data.json", "r") as f:
                    connection_data = json.load(f)

                server = connection_data["server"]
                username = connection_data["username"]
                password = connection_data["password"]
                port = connection_data["port"]
                connection_type = connection_data["connection_type"]

                if connection_type == "FTP":
                    self.upload_via_ftp(server, username, password, port, wordpress_folder)
                else:
                    self.upload_via_sftp(server, username, password, port, wordpress_folder)

                try:
                    os.remove(wordpress_zip)
                    shutil.rmtree(temp_folder)
                    self.update_status(f"Temporary folder {temp_folder} deleted successfully.")
                except Exception as e:
                    self.update_status(f"Failed to delete temporary folder {temp_folder}. Error: {e}")

                self.update_status("SCRIPT_DONE")
                self.next_button.config(state=tk.NORMAL)
                self.prev_button.config(state=tk.NORMAL)  # Enable the prev button
                self.show_success_message()
            except Exception as e:
                self.update_status(f"An error occurred: {e}")

        self.installation_thread = threading.Thread(target=run_installation)
        self.installation_thread.start()

    def stop(self):
        if self.installation_thread and self.installation_thread.is_alive():
            self.installation_thread.join(timeout=1)  # Attempt to stop the thread

    def update_status(self, message):
        self.status_list.config(state=tk.NORMAL)
        self.status_list.insert(tk.END, message + "\n")
        self.status_list.config(state=tk.DISABLED)
        self.status_list.see(tk.END)

    def create_temp_folder(self):
        temp_dir = tempfile.mkdtemp()
        return temp_dir, f"Temporary folder created at: {temp_dir}"

    def download_wordpress(self, temp_folder):
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

    def unzip_wordpress(self, zip_path, temp_folder):
        if zip_path and os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_folder)
            extracted_path = os.path.join(temp_folder, "wordpress")
            if os.path.exists(extracted_path):
                return extracted_path, f"WordPress extracted to {extracted_path}"

        return None, "WordPress zip file not found or extraction failed."

    def extract_zip(self, file_path, destination_folder):
        if file_path and os.path.exists(file_path):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(destination_folder)
            return f"Extracted {file_path} to {destination_folder}"
        return f"Extraction failed for {file_path}"

    def get_plugin_download_url(self, plugin_name):
        plugin_slug = PLUGIN_SLUGS.get(plugin_name, plugin_name.lower().replace(" ", "-"))  # Use correct slug
        api_url = f"https://api.wordpress.org/plugins/info/1.2/?action=plugin_information&slug={plugin_slug}"
        response = requests.get(api_url)

        print(f"🔎 Plugin API URL: {api_url}")  # Debugging
        print(f"🔎 API Response Status: {response.status_code}")  
        print(f"🔎 API Response Text: {response.text}")  

        if response.status_code == 200:
            try:
                data = response.json()
                if "download_link" in data:
                    return data["download_link"]
                else:
                    print(f"❌ No download link found in API response for {plugin_name}: {data}")
                    return None
            except json.JSONDecodeError:
                print(f"❌ JSON decoding error for {plugin_name}. Response: {response.text}")
                return None  
        else:
            print(f"❌ API request failed for {plugin_name}. Status code: {response.status_code}")
        return None

    def get_theme_download_url(self, theme_name):
        theme_slug = THEME_SLUGS.get(theme_name, theme_name.lower().replace(" ", "-"))  # Use correct slug
        api_url = f"https://api.wordpress.org/themes/info/1.2/?action=theme_information&slug={theme_slug}"
        response = requests.get(api_url)

        print(f"🔎 Theme API URL: {api_url}")  # Debugging
        print(f"🔎 API Response Status: {response.status_code}")  
        print(f"🔎 API Response Text: {response.text}")  

        if response.status_code == 200:
            try:
                data = response.json()
                if "download_link" in data:
                    return data["download_link"]
                else:
                    print(f"❌ No download link found in API response for {theme_name}: {data}")
                    return None
            except json.JSONDecodeError:
                print(f"❌ JSON decoding error for {theme_name}. Response: {response.text}")
                return None
        else:
            print(f"❌ API request failed for {theme_name}. Status code: {response.status_code}")
        return None

    def download_plugin(self, plugin_slug, temp_folder):
        plugin_url = self.get_plugin_download_url(plugin_slug)
        if not plugin_url:
            return None, f"Failed to retrieve download URL for {plugin_slug}"

        file_path = os.path.join(temp_folder, f"{plugin_slug}.zip")
        response = requests.get(plugin_url, stream=True)

        if response.status_code == 200:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:  # ✅ Ensure file exists before returning success
                return file_path, f"{plugin_slug} downloaded successfully to {file_path}"
            else:
                return None, f"❌ Download failed: {plugin_slug}.zip is empty!"
        else:
            return None, f"❌ Failed to download {plugin_slug}. Status code: {response.status_code}"

    def download_theme(self, theme_slug, temp_folder):
        theme_url = self.get_theme_download_url(theme_slug)
        if not theme_url:
            return None, f"Failed to retrieve download URL for {theme_slug}"

        file_path = os.path.join(temp_folder, f"{theme_slug}.zip")
        response = requests.get(theme_url, stream=True)

        if response.status_code == 200:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:  # ✅ Ensure file exists before returning success
                return file_path, f"{theme_slug} downloaded successfully to {file_path}"
            else:
                return None, f"❌ Download failed: {theme_slug}.zip is empty!"
        else:
            return None, f"❌ Failed to download {theme_slug}. Status code: {response.status_code}"

    def install_plugins_and_themes(self, plugin_files, theme_files, wordpress_folder):
        plugins_folder = os.path.join(wordpress_folder, "wp-content", "plugins")
        themes_folder = os.path.join(wordpress_folder, "wp-content", "themes")
        os.makedirs(plugins_folder, exist_ok=True)
        os.makedirs(themes_folder, exist_ok=True)

        messages = []
        for plugin in plugin_files:
            if plugin:
                messages.append(self.extract_zip(plugin, plugins_folder))

        for theme in theme_files:
            if theme:
                messages.append(self.extract_zip(theme, themes_folder))

        messages.append("All plugins and themes installed successfully.")
        return messages

    def upload_via_ftp(self, server, username, password, port, wordpress_folder):
        try:
            self.update_status("FTP_CONNECTION_OPENED")
            ftp = FTP()
            ftp.connect(server, int(port))
            ftp.login(username, password)
            self.update_status("UPLOADING_FILES")

            def ftp_mkdirs(ftp, path):
                """Recursively create directories on the FTP server."""
                dirs = path.split("/")
                current_path = ""
                for dir in dirs:
                    if dir:
                        current_path += f"/{dir}"
                        try:
                            ftp.cwd(current_path)
                        except Exception:
                            try:
                                ftp.mkd(current_path)
                                ftp.cwd(current_path)
                                self.update_status(f"📂 Created directory: {current_path}")
                            except Exception as e:
                                self.update_status(f"❌ Failed to create directory {current_path}: {e}")
                                return False
                return True

            total_files = sum([len(files) for _, _, files in os.walk(wordpress_folder)])
            uploaded_files = 0

            for root, dirs, files in os.walk(wordpress_folder):
                relative_path = os.path.relpath(root, wordpress_folder).replace("\\", "/")
                if relative_path != ".":
                    if not ftp_mkdirs(ftp, relative_path):
                        self.update_status(f"⚠️ Skipping folder due to directory creation failure: {relative_path}")
                        continue

                for file in files:
                    file_path = os.path.join(root, file)
                    remote_path = f"{relative_path}/{file}".replace("\\", "/")

                    if os.path.exists(file_path):
                        try:
                            self.update_status(f"⬆ Uploading: {file_path} -> {remote_path}")
                            with open(file_path, "rb") as f:
                                ftp.storbinary(f"STOR {remote_path}", f)
                            uploaded_files += 1
                            self.progress_bar["value"] = (uploaded_files / total_files) * 100
                        except Exception as e:
                            self.update_status(f"❌ Failed to upload {file_path} -> {remote_path}: {e}")
                    else:
                        self.update_status(f"⚠️ Skipping missing file: {file_path}")

            ftp.quit()
            self.update_status("✅ ALL_FILES_UPLOADED")

        except Exception as e:
            self.update_status(f"❌ An error occurred during FTP upload: {e}")

    def upload_via_sftp(self, server, username, password, port, wordpress_folder):
        try:
            self.update_status("SFTP_CONNECTION_OPENED")
            transport = paramiko.Transport((server, int(port)))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            self.update_status("UPLOADING_FILES")

            def sftp_mkdirs(sftp, path):
                """Recursively create directories on the SFTP server if they do not exist."""
                dirs = path.split("/")
                current_path = ""
                for dir in dirs:
                    if dir:
                        current_path += f"/{dir}"
                        try:
                            sftp.stat(current_path)  # Check if directory exists
                        except FileNotFoundError:
                            self.update_status(f"📂 Creating directory: {current_path}")
                            try:
                                sftp.mkdir(current_path)
                            except Exception as e:
                                self.update_status(f"❌ Failed to create directory {current_path}: {e}")
                                return False
                return True

            total_files = sum([len(files) for _, _, files in os.walk(wordpress_folder)])
            uploaded_files = 0

            for root, dirs, files in os.walk(wordpress_folder):
                relative_path = os.path.relpath(root, wordpress_folder).replace("\\", "/")
                if relative_path != ".":
                    if not sftp_mkdirs(sftp, relative_path):
                        self.update_status(f"⚠️ Skipping folder due to directory creation failure: {relative_path}")
                        continue  # Skip this folder if we can't create it

                for file in files:
                    file_path = os.path.join(root, file)
                    remote_path = os.path.join(relative_path, file).replace("\\", "/")

                    if os.path.exists(file_path):  # ✅ Ensure file exists before uploading
                        try:
                            self.update_status(f"⬆ Uploading: {file_path} -> {remote_path}")
                            sftp.put(file_path, remote_path)
                            uploaded_files += 1
                            self.progress_bar["value"] = (uploaded_files / total_files) * 100
                        except Exception as e:
                            self.update_status(f"❌ Failed to upload {file_path} -> {remote_path}: {e}")
                    else:
                        self.update_status(f"⚠️ Skipping missing file: {file_path}")

            sftp.close()
            transport.close()
            self.update_status("✅ ALL_FILES_UPLOADED")

        except Exception as e:
            self.update_status(f"❌ An error occurred during SFTP upload: {e}")

    def show_success_message(self):
        success_window = tk.Toplevel(self)
        success_window.title("Success")
        success_window.geometry("300x150")
        success_window.configure(bg="#f4f4f4")

        success_label = tk.Label(success_window, text="Congratulations! Installation succeeded.", font=("Arial", 12), bg="#f4f4f4")
        success_label.pack(pady=20)

        ok_button = ttk.Button(success_window, text="OK", command=success_window.destroy, style="Bold.TButton")
        ok_button.pack(pady=10)

        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)

    def update_selections(self, selected_plugins, selected_themes):
        self.selected_plugins = selected_plugins
        self.selected_themes = selected_themes
        self.populate_install_list()

    def populate_install_list(self):
        self.install_list.config(state=tk.NORMAL)
        self.install_list.delete(1.0, tk.END)
        self.install_list.insert(tk.END, "WordPress Core\n")
        for plugin in self.selected_plugins:
            self.install_list.insert(tk.END, f"{plugin} (Plugin)\n")
        for theme in self.selected_themes:
            self.install_list.insert(tk.END, f"{theme} (Theme)\n")
        self.install_list.config(state=tk.DISABLED)