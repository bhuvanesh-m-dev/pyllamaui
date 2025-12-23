# main.py
# Entry point for PyLlamaUI, initializes the GUI and connects components

import tkinter as tk
from ui_components import ChatApp
from api import OllamaAPI
from agentic import AgenticWorkflow

def main():
    # Initialize the main Tkinter window
    root = tk.Tk()
    
    # Create Ollama API instance
    api = OllamaAPI(base_url="http://localhost:11434")
    
    # Create agentic workflow instance
    agent = AgenticWorkflow(api)
    
    # Create and start the chat application with agent support
    app = ChatApp(root, api, agent)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
