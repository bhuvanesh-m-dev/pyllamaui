# PyLlamaUI Installation & Testing Guide

## 🚀 Quick Start

### 1. Install the Extension

1. Open VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Extensions: Install from VSIX"
4. Select the `pyllamaui-0.1.6.vsix` file
5. Reload VS Code when prompted

### 2. Set up Ollama

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Pull a recommended model
ollama pull gemma:3b
# OR for a smaller model
ollama pull tinyllama

# Start Ollama service
ollama serve
```

### 3. Test the Extension

1. Open VS Code
2. Press `Ctrl+Shift+P`
3. Type "Open PyllamaUI Chat"
4. The chat panel should open on the right side

## 🧪 Testing Markdown Features

Try these prompts to test the new markdown features:

### Test Bold and Italic Text
```
Please respond with some **bold text** and *italic text* to test formatting.
```

### Test Code Blocks
```
Show me a Python function that prints "Hello World" with proper syntax highlighting.
```

### Test Lists and Headers
```
Create a markdown list of the top 5 programming languages with a header.
```

### Test Copy Functionality
```
Write a JavaScript function that I can copy and paste into my code.
```

## 🔧 Troubleshooting

### Extension Not Loading
- Make sure VS Code version is 1.75 or higher
- Check that the extension is enabled in Extensions panel
- Try reloading VS Code window

### No Models Available
- Ensure Ollama is running: `ollama serve`
- Check available models: `ollama list`
- Pull a model if none available: `ollama pull tinyllama`

### Markdown Not Rendering
- The markdown libraries are bundled offline
- If issues persist, check VS Code Developer Console (Help → Toggle Developer Tools)

### Copy Button Not Working
- Modern browsers support clipboard API
- For older browsers, fallback copy method is included
- Ensure VS Code has clipboard permissions

## 📝 Features Checklist

Test these features to ensure everything works:

- [ ] Extension loads and chat panel opens
- [ ] Can select different Ollama models
- [ ] Messages send and receive responses
- [ ] **Bold text** renders correctly
- [ ] *Italic text* renders correctly
- [ ] Code blocks have syntax highlighting
- [ ] Copy buttons appear on code blocks
- [ ] Copy functionality works
- [ ] Inline `code` styling works
- [ ] Lists and headers render properly
- [ ] Blockquotes render with styling
- [ ] All features work offline

## 🎯 Example Prompts

Try these to showcase the extension's capabilities:

```
Write a Python class for a simple calculator with methods for basic operations. Include docstrings and type hints.
```

```
Explain the difference between **synchronous** and *asynchronous* programming in JavaScript with code examples.
```

```
Create a markdown guide for Git commands with:
# Git Basics
- Common commands
- Code examples
- Best practices
```

## 📦 Building from Source

If you want to build the extension yourself:

```bash
# Install dependencies (if needed)
npm install -g vsce

# Package the extension
vsce package

# This creates pyllamaui-0.1.6.vsix
```

## 🆘 Support

If you encounter issues:

1. Check the VS Code Developer Console for errors
2. Verify Ollama is running and accessible
3. Test with the included `test-markdown.html` file
4. Create an issue on the GitHub repository

---

**Enjoy your enhanced PyLlamaUI experience with full markdown support! 🦙✨**
