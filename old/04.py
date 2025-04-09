import tkinter as tk
from tkinter import ttk
import subprocess
from ftplib import FTP
import paramiko
import json  # Add this import

class ConnectionSetup(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("WP Quickstart - quick WP installer")
        self.geometry("800x600")
        self.configure(bg="#f4f4f4")

        # Storage for connection data
        self.connection_data = {}

        # Headline
        title_label = tk.Label(self, text="Connection Data", font=("Arial", 18, "bold"), bg="#f4f4f4")
        title_label.pack(pady=(20, 10))

        # Dropdown for connection type
        connection_frame = tk.Frame(self, bg="#f4f4f4")
        connection_frame.pack(pady=5)
        tk.Label(connection_frame, text="FTP Connection:", font=("Arial", 12), bg="#f4f4f4").pack(side=tk.LEFT, padx=5)
        
        self.connection_type = tk.StringVar(value="FTP")
        connection_dropdown = ttk.Combobox(connection_frame, textvariable=self.connection_type, values=["FTP", "SFTP (Secure)"], state="readonly")
        connection_dropdown.pack(side=tk.LEFT)
        connection_dropdown.bind("<<ComboboxSelected>>", self.update_port)

        # Input Fields
        input_frame = tk.Frame(self, bg="#f4f4f4")
        input_frame.pack(pady=10)

        labels = ["Server:", "Username:", "Password:", "Port:"]
        self.entries = {}

        for idx, label in enumerate(labels):
            frame = tk.Frame(input_frame, bg="#f4f4f4")
            frame.pack(pady=5, fill=tk.X, padx=20)
            tk.Label(frame, text=label, font=("Arial", 12), bg="#f4f4f4", width=15, anchor="w").pack(side=tk.LEFT)
            entry = ttk.Entry(frame, width=30, show="*" if "Password" in label else "")
            entry.pack(side=tk.LEFT, padx=5)
            self.entries[label] = entry

        # Default port
        self.entries["Port:"].insert(0, "21")

        # Test Connection Button
        self.status_label = tk.Label(self, text="", font=("Arial", 12), bg="#f4f4f4")
        self.status_label.pack(pady=5)
        test_button = ttk.Button(self, text="Test Connection", command=self.test_connection)
        test_button.pack(pady=10)

        # Button Frame
        button_frame = tk.Frame(self, bg="#f4f4f4")
        button_frame.pack(pady=20)

        prev_button = ttk.Button(button_frame, text="< Prev", command=self.prev_window)
        prev_button.grid(row=0, column=0, padx=10)

        self.next_button = ttk.Button(button_frame, text="> Next", command=self.next_window, state=tk.DISABLED)
        self.next_button.grid(row=0, column=1, padx=10)

    def update_port(self, event):
        """Update the port field when switching between FTP and SFTP"""
        if self.connection_type.get() == "SFTP (Secure)":
            self.entries["Port:"].delete(0, tk.END)
            self.entries["Port:"].insert(0, "22")
        else:
            self.entries["Port:"].delete(0, tk.END)
            self.entries["Port:"].insert(0, "21")

    def test_connection(self):
        server = self.entries["Server:"].get()
        username = self.entries["Username:"].get()
        password = self.entries["Password:"].get()
        port = self.entries["Port:"].get()
        connection_type = self.connection_type.get()

        # Store the connection data
        self.connection_data = {
            "server": server,
            "username": username,
            "password": password,
            "port": port,
            "connection_type": connection_type
        }
        
        try:
            if connection_type == "FTP":
                ftp = FTP()
                ftp.connect(server, int(port))
                ftp.login(username, password)
                ftp.quit()
            else:
                transport = paramiko.Transport((server, int(port)))
                transport.connect(username=username, password=password)
                transport.close()
            
            self.status_label.config(text="Connection successful", fg="green")
            self.next_button.config(state=tk.NORMAL)
        except Exception as e:
            self.status_label.config(text="Connection failed. Please check your inputs", fg="red")
            self.next_button.config(state=tk.DISABLED)
            print(f"Error: {e}")
    
    def prev_window(self):
        subprocess.Popen(["python", "03.py"])
        self.destroy()

    def next_window(self):
        # Save connection data before proceeding
        with open("connection_data.json", "w") as f:  # Change to JSON format
            json.dump(self.connection_data, f)  # Save as JSON
        
        subprocess.Popen(["python", "05.py"])
        self.destroy()

if __name__ == "__main__":
    app = ConnectionSetup()
    app.mainloop()