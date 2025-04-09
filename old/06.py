import tkinter as tk
from tkinter import ttk

class SuccessScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("WP Quickstart - quick WP installer")
        self.geometry("800x600")
        self.configure(bg="#f4f4f4")

        # Headline
        title_label = tk.Label(self, text="Success", font=("Arial", 18, "bold"), bg="#f4f4f4")
        title_label.pack(pady=(20, 10))

        # Success Message
        success_message = (
            "Congratulations. It seems everything worked out successfully."
        )
        success_label = tk.Label(self, text=success_message, wraplength=750, justify="left", bg="#f4f4f4", font=("Arial", 12))
        success_label.pack(pady=(10, 20), padx=20)

        # Subheading
        subheading_label = tk.Label(self, text="Next steps:", font=("Arial", 12, "bold"), bg="#f4f4f4")
        subheading_label.pack(anchor="w", padx=20)

        # Steps List
        steps = [
            "Check the folder with an FTP Tool like FileZilla to make sure everything was uploaded to the right place",
            "Open your website. By simply inputting your domain WordPress should now open the installation setup for you. After the setup, all Plugins and Themes should be available.",
            "Activate the Plugins and your favorite Theme",
            "Check OUR WEBSITE (placeholder link) for any further questions."
        ]
        steps_frame = tk.Frame(self, bg="#f4f4f4")
        steps_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        for step in steps:
            step_label = tk.Label(steps_frame, text=f"- {step}", wraplength=750, justify="left", bg="#f4f4f4", font=("Arial", 12))
            step_label.pack(anchor="w", pady=2)

        # Thank You Message
        thank_you_label = tk.Label(self, text="Thanks for using PLACEHOLDER NAME", font=("Arial", 12, "bold"), bg="#f4f4f4")
        thank_you_label.pack(pady=(20, 10))

        # Close Button
        close_button = ttk.Button(self, text="CLOSE", command=self.destroy, style="Bold.TButton")
        close_button.pack(pady=20)

        # Styling
        style = ttk.Style()
        style.configure("Bold.TButton", font=("Arial", 12, "bold"), padding=10)

if __name__ == "__main__":
    app = SuccessScreen()
    app.mainloop()
