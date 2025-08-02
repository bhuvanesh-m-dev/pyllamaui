# PyllamaUI for VS Code 🧠🦙

A lightweight **offline AI assistant inside VS Code** powered by Python + Ollama.  
Access local LLMs directly from your editor — no cloud, no telemetry, no internet required.

![VS Code](https://img.shields.io/badge/Built%20for-VSCode-blue)
![MIT License](https://img.shields.io/badge/License-MIT-green)
![Ollama](https://img.shields.io/badge/Powered%20by-Ollama-yellow)
![Python](https://img.shields.io/badge/Backend-Python%203.10%2B-blue)

---

## 🌟 About

**PyllamaUI (VS Code Edition)** is a [VS Code extension](https://marketplace.visualstudio.com/) that lets you chat with **locally hosted LLMs** using Python as the backend and [Ollama](https://ollama.com) as the model runner.

It's fully offline, privacy-friendly, and designed for low-resource Linux systems.

---

## ✨ Features

- 💬 Chat UI inside a VS Code panel
- 🧠 Interact with local Ollama models (`llama3`, `mistral`, etc.)
- 🐍 Python-powered backend (via `run_prompt.py`)
- 🔌 Uses VS Code’s WebView for integrated GUI
- 🚫 Works without internet – offline-first mindset
- 📁 All user data processed locally

---

## 🛠️ Requirements

### 💻 System
- **VS Code 1.75+**
- **Python 3.10+**

### 📦 Python Libraries
Your backend should have the following installed (via `requirements.txt` or manually):

```bash
pip install requests customtkinter markdown2
