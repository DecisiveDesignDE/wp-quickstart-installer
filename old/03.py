import tkinter as tk
from tkinter import ttk
import subprocess
from PIL import Image, ImageTk
import os
import json

class PluginThemeSelection(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("WP Quickstart - quick WP installer")
        self.geometry("800x600")
        self.configure(bg="#f4f4f4")

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(self, bg="#f4f4f4")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas, bg="#f4f4f4")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        # Headline
        title_label = tk.Label(scrollable_frame, text="Select Plugins and Themes", font=("Arial", 18, "bold"), bg="#f4f4f4")
        title_label.pack(pady=(20, 10))

        # Function to create checkboxes with icons and tooltips
        def create_checkbox_with_icon(parent, name, var, row, column, icon_path):
            frame = tk.Frame(parent, bg="#f4f4f4")
            frame.grid(row=row, column=column, padx=10, pady=5, sticky=tk.W)
            
            img = Image.open(icon_path).resize((30, 30))
            icon = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=icon, bg="#f4f4f4")
            img_label.image = icon
            img_label.pack(side=tk.LEFT, padx=5)
            
            checkbox = tk.Checkbutton(frame, text=name, variable=var, bg="#f4f4f4")
            checkbox.pack(side=tk.LEFT)
            
            info_img = Image.open("img/question.png").resize((15, 15))
            info_icon = ImageTk.PhotoImage(info_img)
            info_label = tk.Label(frame, image=info_icon, bg="#f4f4f4", cursor="question_arrow")
            info_label.image = info_icon
            info_label.pack(side=tk.LEFT, padx=5)
            
            def show_tooltip(event, text=name + " - Additional info here."):
                tooltip = tk.Toplevel(frame)
                tooltip.wm_overrideredirect(True)
                tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
                tk.Label(tooltip, text=text, bg="white", relief="solid", borderwidth=1).pack()
                frame.tooltip = tooltip
            
            def hide_tooltip(event):
                if hasattr(frame, "tooltip"):
                    frame.tooltip.destroy()
            
            info_label.bind("<Enter>", lambda e: show_tooltip(e))
            info_label.bind("<Leave>", hide_tooltip)

        # Plugins
        subheadline_plugins = tk.Label(scrollable_frame, text="Plugins", font=("Arial", 14, "bold"), bg="#f4f4f4")
        subheadline_plugins.pack(pady=10)
        plugins_frame = tk.Frame(scrollable_frame, bg="#f4f4f4")
        plugins_frame.pack(pady=10)

        plugin_names = ["Elementor", "Contact Form 7", "Yoast SEO", "WooCommerce", "LiteSpeed Cache", "Really Simple SSL", "Yoast Duplicate Post", "WP Mail SMTP", "Autoptimize", "Duplicator", "WP Fastest Cache"]
        self.plugin_vars = {name: tk.IntVar() for name in plugin_names}
        
        plugin_icons = {
            "Elementor": "img/elementor.jpg",
            "Contact Form 7": "img/contact_form_7.jpg",
            "Yoast SEO": "img/yoast_seo.jpg",
            "WooCommerce": "img/woocommerce.jpg",
            "LiteSpeed Cache": "img/litespeed_cache.jpg",
            "Really Simple SSL": "img/really_simple_ssl.jpg",
            "Yoast Duplicate Post": "img/yoast_duplicate_post.jpg",
            "WP Mail SMTP": "img/wp_mail_smtp.jpg",
            "Autoptimize": "img/autoptimize.jpg",
            "Duplicator": "img/duplicator.jpg",
            "WP Fastest Cache": "img/wp_fastest_cache.jpg"
        }
        
        for idx, name in enumerate(plugin_names):
            create_checkbox_with_icon(plugins_frame, name, self.plugin_vars[name], idx // 3, idx % 3, plugin_icons[name])
        
        # Themes
        subheadline_themes = tk.Label(scrollable_frame, text="Themes", font=("Arial", 14, "bold"), bg="#f4f4f4")
        subheadline_themes.pack(pady=10)
        themes_frame = tk.Frame(scrollable_frame, bg="#f4f4f4")
        themes_frame.pack(pady=10)
        
        theme_names = ["Hello Elementor", "Astra", "Kadence", "GeneratePress", "Storefront", "Hello Biz"]
        self.theme_vars = {name: tk.IntVar() for name in theme_names}
        
        theme_icons = {
            "Hello Elementor": "img/hello.jpg",
            "Astra": "img/astra.jpg",
            "Kadence": "img/kadence.jpg",
            "GeneratePress": "img/generatepress.jpg",
            "Storefront": "img/storefront.jpg",
            "Hello Biz": "img/hello_biz.jpg"
        }
        
        for idx, name in enumerate(theme_names):
            create_checkbox_with_icon(themes_frame, name, self.theme_vars[name], idx // 2, idx % 2, theme_icons[name])
        
        # Button frame
        button_frame = tk.Frame(scrollable_frame, bg="#f4f4f4")
        button_frame.pack(pady=20)

        prev_button = ttk.Button(button_frame, text="< Prev", command=self.prev_window)
        prev_button.grid(row=0, column=0, padx=10)

        next_button = ttk.Button(button_frame, text="> Next", command=self.next_window)
        next_button.grid(row=0, column=1, padx=10)

    def prev_window(self):
        subprocess.Popen(["python", "02.py"])
        self.destroy()

    def next_window(self):
        selected_plugins = [name for name, var in self.plugin_vars.items() if var.get() == 1]
        selected_themes = [name for name, var in self.theme_vars.items() if var.get() == 1]
        
        # Save selections to a file
        selections = {
            "plugins": selected_plugins,
            "themes": selected_themes
        }
        with open("selections.json", "w") as file:
            json.dump(selections, file)
        
        subprocess.Popen(["python", "04.py"])
        self.destroy()

if __name__ == "__main__":
    app = PluginThemeSelection()
    app.mainloop()
