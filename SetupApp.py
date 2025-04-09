import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
import json

# Import additional steps
from step02 import Step02
from step03 import Step03
from step04 import Step04
from step05 import Step05
from step06 import Step06

class SetupApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("WP Quickstart - quick WP installer")
        self.geometry("800x600")
        self.configure(bg="#f4f4f4")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close event

        self.selected_plugins = []  # Initialize selected_plugins as an empty list
        self.selected_themes = []  # Initialize selected_themes as an empty list

        self.frames = {}
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (StartPage, Step02, Step03, Step04, Step05, Step06):
            page_name = F.__name__
            if F == Step05:
                frame = F(parent=container, controller=self, selected_plugins=self.selected_plugins, selected_themes=self.selected_themes)
            else:
                frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        if page_name == "Step05":
            with open("selections.json", "r") as file:
                selections = json.load(file)
                self.selected_plugins = selections.get("plugins", [])
                self.selected_themes = selections.get("themes", [])
            frame = self.frames[page_name]
            frame.update_selections(self.selected_plugins, self.selected_themes)
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):
        if hasattr(self, 'installation_thread') and self.installation_thread.is_alive():
            self.installation_thread.stop()  # Stop the installation thread
        self.destroy()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f4f4f4")

        # Title
        title_label = tk.Label(self, text="Welcome to WP Quickstart", font=("Arial", 18, "bold"), bg="#f4f4f4")
        title_label.pack(pady=(20, 10))

        # Logo
        if getattr(sys, 'frozen', False):
            logo_path = os.path.join(sys._MEIPASS, "img/logo.png")
        else:
            logo_path = os.path.join(os.path.dirname(__file__), "img/logo.png")
        logo = tk.PhotoImage(file=logo_path)
        logo = logo.subsample(int(logo.width() / 200))  # Resize to 200px wide
        logo_label = tk.Label(self, image=logo, bg="#f4f4f4")
        logo_label.image = logo  # Keep a reference to avoid garbage collection
        logo_label.pack(pady=(30, 30))

        # Introduction text
        intro_text = (
            "This tool makes setting up a WordPress site easier than ever. "
            "Select the plugins and themes you need, and we will automatically "
            "download, unpack, and place them in the correct directories. "
            "Additionally, we will upload everything to your server via FTP, "
            "saving you time and effort."
        )
        intro_label = tk.Label(self, text=intro_text, wraplength=450, justify="left", bg="#f4f4f4")
        intro_label.pack(pady=(10, 20), padx=20)

        # What you will need section
        requirements_label = tk.Label(self, text="What you will need", font=("Arial", 12, "bold"), bg="#f4f4f4")
        requirements_label.pack(pady=(10, 5))

        requirements_text = (
            "- A working internet connection\n"
            "- A web host that supports WordPress\n"
            "- FTP login credentials for your web host"
        )
        requirements_content = tk.Label(self, text=requirements_text, justify="left", bg="#f4f4f4")
        requirements_content.pack(pady=(0, 20), padx=20)

        # Next button
        next_button = ttk.Button(self, text="Next", command=lambda: controller.show_frame("Step02"))
        next_button.pack(pady=10)

if __name__ == "__main__":
    app = SetupApp()
    app.mainloop()
