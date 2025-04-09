import tkinter as tk
from tkinter import ttk
import subprocess

class Step02(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f4f4f4")

        # Title
        title_label = tk.Label(self, text="Terms and Conditions", font=("Arial", 18, "bold"), bg="#f4f4f4")
        title_label.pack(pady=(20, 10))

        # Create a frame for the scrollable text area
        text_frame = tk.Frame(self, bg="white")
        text_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=False)
        text_frame.config(height=250)  # Reduce height by about 35%

        # Add a scrollable text area
        text_area = tk.Text(text_frame, wrap=tk.WORD, bg="white", font=("Arial", 12), height=20)
        scrollbar = tk.Scrollbar(text_frame, command=text_area.yview)
        text_area.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Insert placeholder Terms and Conditions text
        terms_text = (
            "By using this application, you acknowledge that you are solely responsible "
            "for any modifications made to your WordPress installation. This tool "
            "automates the download and installation of plugins and themes from "
            "WordPress.org, a trusted resource, but we cannot guarantee the safety "
            "or compatibility of any downloaded files.\n\n"
            "Use this tool with caution. If files are overwritten, it may lead to "
            "unexpected issues or the loss of existing configurations. We are not "
            "liable for any damage caused by using this application.\n\n"
            "Please make sure you have a backup of your website before proceeding."
        )
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, terms_text)
        text_area.config(state=tk.DISABLED)

        # Checkbox to agree to terms
        self.agree_var = tk.IntVar()
        agree_checkbox = tk.Checkbutton(self, text="I have read and agree to the above terms and conditions", 
                                        variable=self.agree_var, command=self.toggle_next_button, bg="#f4f4f4")
        agree_checkbox.pack(pady=10)

        # Button frame
        button_frame = tk.Frame(self, bg="#f4f4f4")
        button_frame.pack(pady=20)

        prev_button = ttk.Button(button_frame, text="< Prev", command=self.prev_window)
        prev_button.grid(row=0, column=0, padx=10)

        self.next_button = ttk.Button(button_frame, text="> Next", command=lambda: controller.show_frame("Step03"), state=tk.DISABLED)
        self.next_button.grid(row=0, column=1, padx=10)

    def toggle_next_button(self):
        if self.agree_var.get() == 1:
            self.next_button.config(state=tk.NORMAL)
        else:
            self.next_button.config(state=tk.DISABLED)

    def prev_window(self):
        subprocess.Popen(["python", "01.py"])
        self.controller.destroy()

    def next_window(self):
        subprocess.Popen(["python", "03.py"])
        self.controller.destroy()
