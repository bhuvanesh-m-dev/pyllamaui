# PyllamaUI for VS Code 🧠🦙

A lightweight **offline AI assistant inside VS Code** powered by Python + Ollama.  
Access local LLMs directly from your editor — no cloud, no telemetry, no internet required.

![VS Code](https://img.shields.io/badge/Built%20for-VSCode-blue)
![MIT License](https://img.shields.io/badge/License-MIT-green)
![Ollama](https://img.shields.io/badge/Powered%20by-Ollama-yellow)
![Python](https://img.shields.io/badge/Backend-Python%203.10%2B-blue)

---

## 🌟 About

**PyllamaUI (VS Code Edition)** is a [VS Code extension](https://marketplace.visualstudio.com/items?itemName=bhuvanesh-m-dev.pyllamaui) that lets you chat with **locally hosted LLMs** using Python as the backend and [Ollama](https://ollama.com) as the model runner.

It's fully offline, privacy-friendly, and designed for low-resource systems.


## ✨ Features

- 💬 Chat UI inside a VS Code panel
- 🧠 Interact with local Ollama models (`llama3`, `mistral`, etc.)
- 📝 **Full Markdown support** with **bold text**, *italics*, headers, lists, and blockquotes
- 🎨 **Syntax highlighting** for code blocks (Python, JavaScript, JSON, Bash, and more)
- 📋 **One-click copy buttons** for all code blocks with proper indentation
- 🔌 Uses VS Code's WebView for integrated GUI
- 🚫 **Fully offline** – no internet required, all dependencies bundled
- 📁 All user data processed locally
- ⚡ Real-time markdown rendering as responses stream in

---

## 🛠️ Requirements

{{ ... }}
- **VS Code 1.75+**
- **Python 3.10+**
- **ollama**
---  
✅ **Model Recommendations**

| Use Case        | Model Name       | Approx. Size | Description                                  |
|-----------------|------------------|--------------|----------------------------------------------|
| 📝 Text Chat    | `tinyllama`      | ~600 MB      | Lightweight text model                       |
| 💻 Coding Help  | `deepseek-coder` | ~700 MB      | Designed for code generation                 |
| ⚡ All-in-One    | `gemma:3b` (aka `gemma3n`) | ~5.5 GB  | Great for both chat & coding (Google DeepMind) |

✅ **If unsure, just install `gemma3n` for the best all-around experience.**

---

To run a model:  
`ollama run gemma3n`  
`ollama run tinyllama`  
`ollama run deepseek-coder`

📌 *Special thanks to [Ollama](https://ollama.com/download) for making local LLMs accessible to all.*

---

## 🎨 Markdown Features

PyLlamaUI now supports full markdown rendering with:

### Text Formatting
- **Bold text** using `**text**`
- *Italic text* using `*text*`
- Headers using `# ## ###`
- Blockquotes using `>`
- Lists (ordered and unordered)

### Code Support
- Inline code using backticks: `console.log("hello")`
- Code blocks with syntax highlighting:

```python
def example():
    print("This code has syntax highlighting!")
    return True
```

### Copy Functionality
- Every code block includes a **Copy** button
- Preserves proper indentation and formatting
- Works with all supported languages: Python, JavaScript, JSON, Bash, and more
- Fully offline - no external dependencies required

### Real-time Rendering
- Markdown is rendered as the AI response streams in
- Smooth, responsive interface
- All processing happens locally in VS Code
