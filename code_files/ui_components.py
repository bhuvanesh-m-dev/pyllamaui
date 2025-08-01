# ui_components.py
# Defines GUI components for PyLlamaUI with live typing and Markdown support

import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext
import markdown2
import threading
import time

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

        # Send button

        self.send_button = ctk.CTkButton(
            self.main_frame,
            text="Send",
            command=self.send_or_stop
        )
        self.send_button.grid(row=3, column=0, sticky="e", padx=5, pady=5)

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
