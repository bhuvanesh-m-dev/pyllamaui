# ui_components.py
# Defines GUI components for PyLlamaUI with live typing, Markdown support, and agentic mode

import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext
import markdown2
import threading
import time
from settings import SettingsDialog

class ChatApp:
    def __init__(self, root, api, agent=None):
        """Initialize the chat application GUI with Markdown and agentic support."""
        self.root = root
        self.api = api
        self.agent = agent  # AgenticWorkflow instance, optional
        self.root.title("PyLlamaUI")
        self.root.geometry("600x400")

        # For streaming cancellation
        self._stop_stream = threading.Event()
        self._streaming = False

        # Undo/redo stacks for normal mode
        self.prompt_stack = []
        self.undo_stack = []

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

        # Mode selection (Normal or Agentic)
        self.mode_var = tk.StringVar(value="Normal")
        self.mode_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.mode_frame.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.normal_radio = ctk.CTkRadioButton(
            self.mode_frame, text="Normal", variable=self.mode_var, value="Normal"
        )
        self.normal_radio.grid(row=0, column=0, padx=(0, 5))
        self.agentic_radio = ctk.CTkRadioButton(
            self.mode_frame, text="Agentic", variable=self.mode_var, value="Agentic"
        )
        self.agentic_radio.grid(row=0, column=1, padx=(0, 5))

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

        # Frame for settings, model, send, and other buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.button_frame.grid_columnconfigure(0, weight=0)
        self.button_frame.grid_columnconfigure(1, weight=0)
        self.button_frame.grid_columnconfigure(2, weight=0)
        self.button_frame.grid_columnconfigure(3, weight=0)
        self.button_frame.grid_columnconfigure(4, weight=0)
        self.button_frame.grid_columnconfigure(5, weight=0)

        # Settings button
        self.settings_button = ctk.CTkButton(
            self.button_frame,
            text="⚙️",
            width=40,
            command=self.open_settings
        )
        self.settings_button.grid(row=0, column=0, padx=(0,5))

        # Model selection button
        self.model_button = ctk.CTkButton(
            self.button_frame,
            text=self.api.model,
            width=80,
            command=self.show_model_menu
        )
        self.model_button.grid(row=0, column=1, padx=(0,5))

        # Send/Agent button (context-dependent)
        self.send_button = ctk.CTkButton(
            self.button_frame,
            text="Send",
            command=self.send_or_stop
        )
        self.send_button.grid(row=0, column=2, padx=(0,5))

        # Undo button (for normal mode)
        self.undo_button = ctk.CTkButton(
            self.button_frame, text="Undo", width=80, command=self.undo
        )
        self.undo_button.grid(row=0, column=3, padx=(0,5))

        # Redo button (for normal mode)
        self.redo_button = ctk.CTkButton(
            self.button_frame, text="Redo", width=80, command=self.redo
        )
        self.redo_button.grid(row=0, column=4, padx=(0,5))

        # Bind Enter key to send message or run agent
        self.prompt_entry.bind("<Return>", lambda event: self.send_or_stop())

    def open_settings(self):
        SettingsDialog(self.root)

    def show_model_menu(self):
        """Show a dropdown menu to select the model from Ollama."""
        models = self.api.get_available_models()
        if isinstance(models, dict) and "error" in models:
            self._show_popup("Model Error", models["error"])
            return
        model_names = [m["name"] if isinstance(m, dict) and "name" in m else str(m) for m in models]
        if not model_names:
            self._show_popup("Model Error", "No models found from Ollama.")
            return

        menu = tk.Menu(self.root, tearoff=0)
        for name in model_names:
            menu.add_command(label=name, command=lambda n=name: self.set_model(n))
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

    def send_or_stop(self):
        """Handle sending prompt or running agent based on mode, or stopping streaming."""
        if self._streaming:
            self.stop_streaming()
        else:
            if self.mode_var.get() == "Normal":
                self.send_message()
            else:
                self.run_agent()

    def send_message(self):
        """Handle sending the prompt and displaying the streamed response (Normal mode)."""
        prompt = self.prompt_entry.get()
        if not prompt.strip():
            return

        # Display user prompt (right-aligned)
        user_message = f"You: {prompt}\n"
        self._display_message(user_message, align="right")
        self.prompt_stack.append((prompt, ""))  # Store prompt, response added later
        self.undo_stack.clear()  # Clear redo stack

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
        """Stream and display the Ollama response with a typing effect (Normal mode)."""
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
            self.prompt_stack[-1] = (prompt, response_text)  # Update with full response

        # Re-enable input and reset button
        def reset():
            self.prompt_entry.configure(state="normal")
            self.send_button.configure(text="Send", state="normal")
            self._streaming = False
        self.root.after(0, reset)

    def run_agent(self):
        """Run an agentic workflow based on the prompt (Agentic mode)."""
        if not self.agent:
            self._show_popup("Error", "Agent not initialized")
            return

        prompt = self.prompt_entry.get()
        if not prompt.strip():
            return

        # Display user prompt (right-aligned)
        user_message = f"You: {prompt}\n"
        self._display_message(user_message, align="right")

        # Clear input
        self.prompt_entry.delete(0, tk.END)

        # Prepare for agentic streaming
        self.prompt_entry.configure(state="disabled")
        self._stop_stream.clear()
        self._streaming = True
        self.send_button.configure(text="Stop", state="normal")

        # Start agent tasks in a separate thread
        threading.Thread(target=self._run_agent_tasks, args=(prompt,), daemon=True).start()

    def _run_agent_tasks(self, prompt):
        """Execute agentic tasks and display results."""
        # Single task to process the user request via the Offline System Agent
        self.agent.add_task("process", prompt)

        for result in self.agent.run_tasks():
            if self._stop_stream.is_set():
                break
            self._display_message(result + "\n", align="left")

        # Re-enable input and reset button
        def reset():
            self.prompt_entry.configure(state="normal")
            self.send_button.configure(text="Send", state="normal")
            self._streaming = False
        self.root.after(0, reset)

    def undo(self):
        """Undo the last prompt and response in Normal mode."""
        if self.prompt_stack:
            prompt, response = self.prompt_stack.pop()
            self.undo_stack.append((prompt, response))
            self.chat_display.configure(state="normal")
            self.chat_display.delete("end-2l", tk.END)  # Remove AI message
            self.chat_display.delete("end-2l", tk.END)  # Remove user message
            self.chat_display.configure(state="disabled")

    def redo(self):
        """Redo the last undone prompt and response in Normal mode."""
        if self.undo_stack:
            prompt, response = self.undo_stack.pop()
            self.prompt_stack.append((prompt, response))
            self._display_message(f"You: {prompt}\n", align="right")
            self._display_message(f"PyLlamaUI: {response}\n", align="left")

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
