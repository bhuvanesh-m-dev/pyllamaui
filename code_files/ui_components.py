# ui_components.py
# Defines GUI components for PyLlamaUI using customtkinter

import tkinter as tk
from tkinter import scrolledtext
import customtkinter as ctk

class ChatApp:
    def __init__(self, root, api):
        """Initialize the chat application GUI."""
        self.root = root
        self.api = api
        self.root.title("PyLlamaUI")
        self.root.geometry("600x400")
        
        # Set customtkinter theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Model name label
        self.model_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Model: {self.api.model}",
            font=("Arial", 12)
        )
        self.model_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Chat display (scrollable text area)
        self.chat_display = scrolledtext.ScrolledText(
            self.main_frame,
            height=15,
            width=50,
            wrap=tk.WORD,
            state="disabled",
            font=("Arial", 11)
        )
        self.chat_display.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Prompt input
        self.prompt_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter your prompt here...",
            height=40
        )
        self.prompt_entry.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # Send button
        self.send_button = ctk.CTkButton(
            self.main_frame,
            text="Send",
            command=self.send_message
        )
        self.send_button.grid(row=3, column=0, sticky="e", padx=5, pady=5)

        # Bind Enter key to send message
        self.prompt_entry.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        """Handle sending the prompt and displaying the response."""
        prompt = self.prompt_entry.get()
        if not prompt.strip():
            return

        # Display user prompt
        self._display_message(f"You: {prompt}\n")

        # Get response from API
        response = self.api.send_prompt(prompt)

        # Display response
        self._display_message(f"AI: {response}\n")

        # Clear input
        self.prompt_entry.delete(0, tk.END)

    def _display_message(self, message):
        """Display a message in the chat window."""
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, message)
        self.chat_display.see(tk.END)
        self.chat_display.configure(state="disabled")
