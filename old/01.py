import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os

class SetupApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("WP Quickstart - quick WP installer")
        self.geometry("800x600")
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
        next_button = ttk.Button(self, text="Next", command=self.next_step)
        next_button.pack(pady=10)

    def next_step(self):
        print("Proceeding to the next step...")
        subprocess.Popen(["python", "02.py"])
        self.destroy()

if __name__ == "__main__":
    app = SetupApp()
    app.mainloop()
