const fs = require('fs');
const path = require('path');

function getWebviewContent(extensionPath) {
    const htmlPath = path.join(extensionPath, 'webview', 'index.html');
    const cssPath = path.join(extensionPath, 'webview', 'styles.css');
    const jsPath = path.join(extensionPath, 'webview', 'main.js');
    const markedPath = path.join(extensionPath, 'webview', 'marked.min.js');

    const html = fs.readFileSync(htmlPath, 'utf-8');
    const css = fs.readFileSync(cssPath, 'utf-8');
    const js = fs.readFileSync(jsPath, 'utf-8');
    const marked = fs.readFileSync(markedPath, 'utf-8');

    return html.replace('<link rel="stylesheet" href="styles.css">', `<style>${css}</style>`)
               .replace('<script src="main.js"></script>', `<script>${js}</script>`)
               .replace('<script src="marked.min.js"></script>', `<script>${marked}</script>`);
}

module.exports = { getWebviewContent };