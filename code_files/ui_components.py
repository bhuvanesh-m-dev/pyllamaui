# ui_components.py
# Defines GUI components for PyLlamaUI with live typing and Markdown support

import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext
import markdown2
import threading
import time
from settings import SettingsDialog

class ChatApp:
    def __init__(self, root, api):
        """Initialize the chat application GUI with Markdown support."""
        self.root = root
        self.api = api
        self.root.title("PyLlamaUI")
        self.root.geometry("600x400")

        # For streaming cancellation
        self._stop_stream = threading.Event()
        self._streaming = False

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

        # Chat display (scrollable text area with Markdown rendering)
        self.chat_display = scrolledtext.ScrolledText(
            self.main_frame,
            height=15,
            width=50,
            wrap=tk.WORD,
            state="disabled",
            font=("Arial", 11),
            bg="#2b2b2b",
            fg="#ffffff"
        )
        self.chat_display.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Prompt input
        self.prompt_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter your prompt here...",
            height=40
        )
        self.prompt_entry.grid(row=2, column=0, sticky="ew", padx=5, pady=5)



        # Frame for settings, model, send, and theme buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.button_frame.grid_columnconfigure(0, weight=0)
        self.button_frame.grid_columnconfigure(1, weight=0)
        self.button_frame.grid_columnconfigure(2, weight=0)
        self.button_frame.grid_columnconfigure(3, weight=0)

        # Settings button (leftmost)
        self.settings_button = ctk.CTkButton(
            self.button_frame,
            text="⚙️",
            width=40,
            command=self.open_settings
        )
        self.settings_button.grid(row=0, column=0, padx=(0,5))

        # Model selection button (left of send button)
        self.model_button = ctk.CTkButton(
            self.button_frame,
            text=self.api.model,
            width=80,
            command=self.show_model_menu
        )
        self.model_button.grid(row=0, column=1, padx=(0,5))

        # Send button (center)
        self.send_button = ctk.CTkButton(
            self.button_frame,
            text="Send",
            command=self.send_or_stop
        )
        self.send_button.grid(row=0, column=2)
    def open_settings(self):
        SettingsDialog(self.root)

    def show_model_menu(self):
        """Show a dropdown menu to select the model from Ollama."""
        # Fetch models from Ollama
        models = self.api.get_available_models()
        if isinstance(models, dict) and "error" in models:
            # Show error popup
            self._show_popup("Model Error", models["error"])
            return
        model_names = [m["name"] if isinstance(m, dict) and "name" in m else str(m) for m in models]
        if not model_names:
            self._show_popup("Model Error", "No models found from Ollama.")
            return

        # Create a popup menu
        menu = tk.Menu(self.root, tearoff=0)
        for name in model_names:
            menu.add_command(label=name, command=lambda n=name: self.set_model(n))
        # Place the menu below the model button
        x = self.model_button.winfo_rootx()
        y = self.model_button.winfo_rooty() + self.model_button.winfo_height()
        menu.tk_popup(x, y)

    def set_model(self, model_name):
        """Set the selected model for the API and update UI label/button."""
        self.api.model = model_name
        self.model_label.configure(text=f"Model: {model_name}")
        self.model_button.configure(text=model_name)

    def _show_popup(self, title, message):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("350x120")
        label = tk.Label(popup, text=message, wraplength=320)
        label.pack(pady=20)
        btn = tk.Button(popup, text="OK", command=popup.destroy)
        btn.pack(pady=5)

        # Bind Enter key to send message
        self.prompt_entry.bind("<Return>", lambda event: self.send_or_stop())

    def send_or_stop(self):
        if self._streaming:
            self.stop_streaming()
        else:
            self.send_message()

    def send_message(self):
        """Handle sending the prompt and displaying the streamed response."""
        prompt = self.prompt_entry.get()
        if not prompt.strip():
            return

        # Display user prompt (right-aligned)
        user_message = f"You: {prompt}\n"
        self._display_message(user_message, align="right")

        # Clear input
        self.prompt_entry.delete(0, tk.END)

        # Prepare for streaming
        self.prompt_entry.configure(state="disabled")
        self._stop_stream.clear()
        self._streaming = True
        self.send_button.configure(text="Stop", state="normal")

        # Start streaming response in a separate thread
        threading.Thread(target=self._stream_response, args=(prompt,), daemon=True).start()

    def stop_streaming(self):
        """Signal the streaming thread to stop."""
        self._stop_stream.set()
        self.send_button.configure(state="disabled")

    def _stream_response(self, prompt):
        """Stream and display the Ollama response with a typing effect. Supports cancellation."""
        response_text = ""
        self._display_message("PyLlamaUI: ", align="left")  # Start AI message

        for chunk in self.api.send_prompt(prompt, stream=True):
            if self._stop_stream.is_set():
                break
            response_text += chunk
            self._display_message(chunk, align="left", append=True)
            time.sleep(0.05)  # Simulate typing effect

        # Finalize message with newline if not stopped
        if not self._stop_stream.is_set():
            self._display_message("\n", align="left", append=True)

        # Re-enable input and reset button
        def reset():
            self.prompt_entry.configure(state="normal")
            self.send_button.configure(text="Send", state="normal")
            self._streaming = False
        self.root.after(0, reset)

    def _display_message(self, message, align="left", append=False):
        """Display a message in the chat window with Markdown and alignment."""
        self.chat_display.configure(state="normal")
        
        if not append:
            # Convert Markdown to HTML-like formatting for basic styling
            html_message = markdown2.markdown(message, extras=["fenced-code-blocks"])
            # Simplify to basic Tkinter text formatting
            formatted_message = message  # Tkinter ScrolledText doesn't support full HTML
            if align == "right":
                formatted_message = " " * 20 + formatted_message  # Simple right-align hack
        else:
            formatted_message = message

        if append:
            self.chat_display.insert(tk.END, formatted_message)
        else:
            self.chat_display.insert(tk.END, formatted_message)
        
        self.chat_display.see(tk.END)
        self.chat_display.configure(state="disabled")

