# main.py
# Entry point for PyLlamaUI, initializes the GUI and connects components

import tkinter as tk
from ui_components import ChatApp
from api import OllamaAPI

def main():
    # Initialize the main Tkinter window
    root = tk.Tk()
    
    # Create Ollama API instance
    api = OllamaAPI(base_url="http://localhost:11434")
    
    # Create and start the chat application
    app = ChatApp(root, api)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()

