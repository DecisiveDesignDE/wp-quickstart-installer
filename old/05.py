import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import winsound  # Add this import
import json

class InstallationScreen(tk.Tk):
    def __init__(self, selected_plugins, selected_themes):
        super().__init__()
        
        self.title("WP Quickstart - quick WP installer")
        self.geometry("800x600")
        self.configure(bg="#f4f4f4")

        # Headline
        title_label = tk.Label(self, text="Installation", font=("Arial", 18, "bold"), bg="#f4f4f4")
        title_label.pack(pady=(20, 10))

        # Installation Notice
        notice_text = (
            "We will now install WordPress, the selected Plugin(s) and Theme(s) to your server. "
            "Again, please make sure to backup your files if the folder is not empty."
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

        install_list = tk.Text(install_list_frame, wrap=tk.WORD, height=4, font=("Arial", 12), bg="white", state=tk.DISABLED, yscrollcommand=install_list_scrollbar.set)
        install_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        install_list_scrollbar.config(command=install_list.yview)

        # Populate install list
        install_list.config(state=tk.NORMAL)
        install_list.insert(tk.END, "WordPress Core\n")
        for plugin in selected_plugins:
            install_list.insert(tk.END, f"{plugin} (Plugin)\n")
        for theme in selected_themes:
            install_list.insert(tk.END, f"{theme} (Theme)\n")
        install_list.config(state=tk.DISABLED)

        # Confirmation Notice
        confirm_label = tk.Label(self, text="Only if the previous is correct, start by clicking the button", font=("Arial", 12), bg="#f4f4f4")
        confirm_label.pack(pady=10)

        # Start Button
        start_button = ttk.Button(self, text="START", command=self.start_installation, style="Bold.TButton")
        start_button.pack(pady=10)

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

        prev_button = ttk.Button(button_frame, text="< Prev", command=self.prev_window)
        prev_button.grid(row=0, column=0, padx=10)

        self.next_button = ttk.Button(button_frame, text="> Next", command=self.next_window, state=tk.DISABLED)
        self.next_button.grid(row=0, column=1, padx=10)

        # Styling
        style = ttk.Style()
        style.configure("Bold.TButton", font=("Arial", 12, "bold"), padding=10)

        # Create Step05 frame
        self.step05_frame = Step05(self, self, selected_plugins, selected_themes)
        self.step05_frame.pack(fill=tk.BOTH, expand=True)

    def start_installation(self):
        self.status_list.config(state=tk.NORMAL)
        self.status_list.insert(tk.END, "Starting installation...\nPlease wait as this may take a few minutes.\n")
        self.status_list.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)

        def run_installation():
            process = subprocess.Popen(["python", "install.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in iter(process.stdout.readline, ''):
                self.status_list.config(state=tk.NORMAL)
                self.status_list.insert(tk.END, line)
                self.status_list.config(state=tk.DISABLED)
                self.status_list.see(tk.END)  # Auto-scroll to the end
                if "SCRIPT_DONE" in line:
                    self.next_button.config(state=tk.NORMAL)
                    self.show_success_message()
                elif "FTP_CONNECTION_OPENED" in line:
                    self.status_list.config(state=tk.NORMAL)
                    self.status_list.insert(tk.END, "FTP connection opened.\n")
                    self.status_list.config(state=tk.DISABLED)
                elif "UPLOADING_FILES" in line:
                    self.status_list.config(state=tk.NORMAL)
                    self.status_list.insert(tk.END, "Uploading files...\n")
                    self.status_list.config(state=tk.DISABLED)
                elif "ALL_FILES_UPLOADED" in line:
                    self.status_list.config(state=tk.NORMAL)
                    self.status_list.insert(tk.END, "All files uploaded.\n")
                    self.status_list.config(state=tk.DISABLED)
            process.stdout.close()
            process.wait()

        threading.Thread(target=run_installation).start()

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

    def prev_window(self):
        subprocess.Popen(["python", "04.py"])
        self.destroy()

    def next_window(self):
        subprocess.Popen(["python", "06.py"])
        self.destroy()

if __name__ == "__main__":
    # Read selected options from file
    with open("selections.json", "r") as file:
        selections = json.load(file)
    
    selected_plugins = selections.get("plugins", [])
    selected_themes = selections.get("themes", [])
    
    app = InstallationScreen(selected_plugins, selected_themes)
    app.mainloop()