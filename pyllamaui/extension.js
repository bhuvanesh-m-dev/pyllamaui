const vscode = require('vscode');
const path = require('path');
const cp = require('child_process');

function activate(context) {
    context.subscriptions.push(
        vscode.commands.registerCommand('pyllamaui.chat', () => {
            const panel = vscode.window.createWebviewPanel(
                'pyllamauiChat',
                'PyllamaUI Chat',
                vscode.ViewColumn.One,
                { enableScripts: true }
            );

            panel.webview.html = getWebviewContent();

            panel.webview.onDidReceiveMessage(
                message => {
                    if (message.command === 'sendPrompt') {
                        const script = path.join(context.extensionPath, 'py', 'run_prompt.py');
                        const python = process.platform === 'win32' ? 'python' : 'python3';
                        const prompt = message.text;

                        cp.execFile(python, [script, prompt], (err, stdout, stderr) => {
                            if (err || stderr) {
                                panel.webview.postMessage({ command: 'response', text: "Error: " + (stderr || err.message) });
                                return;
                            }

                            try {
                                const parsed = JSON.parse(stdout);
                                panel.webview.postMessage({ command: 'response', text: parsed.response });
                            } catch (e) {
                                panel.webview.postMessage({ command: 'response', text: "Invalid response from backend." });
                            }
                        });
                    }
                },
                undefined,
                context.subscriptions
            );
        })
    );
}

function getWebviewContent() {
    return `
    <!DOCTYPE html>
    <html>
    <body style="font-family: sans-serif; background: #1e1e1e; color: white; padding: 10px;">
        <h3>🦙 PyllamaUI Chat</h3>
        <div id="chat" style="white-space: pre-wrap; border: 1px solid #555; padding: 10px; height: 250px; overflow-y: auto;"></div>
        <input id="input" type="text" style="width: 80%; padding: 5px;" placeholder="Type your prompt..." />
        <button onclick="send()" style="padding: 5px 10px;">Send</button>

        <script>
            const vscode = acquireVsCodeApi();
            function send() {
                const input = document.getElementById('input');
                const chat = document.getElementById('chat');
                const prompt = input.value;
                chat.innerHTML += "\\nYou: " + prompt;
                vscode.postMessage({ command: 'sendPrompt', text: prompt });
                input.value = '';
            }

            window.addEventListener('message', event => {
                const message = event.data;
                if (message.command === 'response') {
                    document.getElementById('chat').innerHTML += "\\nPyllamaUI: " + message.text;
                }
            });
        </script>
    </body>
    </html>`;
}

function deactivate() {}

module.exports = { activate, deactivate };
