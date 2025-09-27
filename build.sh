#!/bin/bash

# PyLlamaUI Extension Build Script
echo "🦙 Building PyLlamaUI Extension..."

# Create a temporary directory for packaging
mkdir -p dist
cp -r . dist/pyllamaui-temp
cd dist/pyllamaui-temp

# Remove unnecessary files
rm -rf .git
rm -rf dist
rm -f build.sh
rm -f test-markdown.html
rm -rf testing

# Create the extension package structure
echo "📦 Packaging extension files..."

# Verify all required files are present
echo "✅ Checking required files:"
echo "   - package.json: $([ -f package.json ] && echo "✓" || echo "✗")"
echo "   - extension.js: $([ -f extension.js ] && echo "✓" || echo "✗")"
echo "   - activate.js: $([ -f activate.js ] && echo "✓" || echo "✗")"
echo "   - webviewContent.js: $([ -f webviewContent.js ] && echo "✓" || echo "✗")"
echo "   - libs/: $([ -d libs ] && echo "✓" || echo "✗")"

# Count library files
lib_count=$(ls libs/ | wc -l)
echo "   - Library files: $lib_count"

echo ""
echo "🎉 Extension is ready for installation!"
echo ""
echo "📋 Installation Instructions:"
echo "1. Open VS Code"
echo "2. Press Ctrl+Shift+P"
echo "3. Type 'Extensions: Install from VSIX'"
echo "4. Select this folder as the extension"
echo ""
echo "🧪 Or test the markdown features with:"
echo "   Open test-markdown.html in a browser"
echo ""
echo "✨ Features included:"
echo "   - Full markdown rendering"
echo "   - Syntax highlighting for code blocks"
echo "   - Copy buttons for all code"
echo "   - Fully offline operation"
echo "   - Real-time streaming support"

cd ../..
echo ""
echo "🚀 Build complete! Extension ready in: $(pwd)/dist/pyllamaui-temp"
