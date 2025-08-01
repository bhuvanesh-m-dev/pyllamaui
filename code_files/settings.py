# settings.py
# Settings dialog for PyLlamaUI

import tkinter as tk

class SettingsDialog:
    def __init__(self, root):
        self.root = root
        self.dialog = tk.Toplevel(root)
        self.dialog.title("Settings")
        self.dialog.geometry("350x200")
        self.dialog.resizable(False, False)

        about_label = tk.Label(self.dialog, text="About", font=("Arial", 14, "bold"))
        about_label.pack(pady=(20, 5))
        info_label = tk.Label(
            self.dialog,
            text="PyLlamaUI\nDeveloped by: BHUVANESH M\nVersion: 0.0.1\nLicense: MIT",
            font=("Arial", 11),
            justify="center"
        )
        info_label.pack(pady=(0, 20))

        close_btn = tk.Button(self.dialog, text="Close", command=self.dialog.destroy)
        close_btn.pack(pady=10)
