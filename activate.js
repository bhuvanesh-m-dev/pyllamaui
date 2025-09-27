const vscode = require('vscode');
const { getWebviewContent } = require('./webviewContent');
const http = require('http');

function activate(context) {
    let currentRequest = null;

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
                async message => {
                    if (message.command === 'getModelList') {
                        // Fetch models from Ollama API
                        http.get('http://localhost:11434/api/tags', res => {
                            let data = '';
                            res.on('data', chunk => data += chunk);
                            res.on('end', () => {
                                try {
                                    const tags = JSON.parse(data);
                                    const models = tags.models ? tags.models.map(m => m.name) : [];
                                    panel.webview.postMessage({ command: 'modelList', models });
                                } catch (e) {
                                    panel.webview.postMessage({ command: 'modelList', models: [] });
                                }
                            });
                        }).on('error', () => {
                            panel.webview.postMessage({ command: 'modelList', models: [] });
                        });
                    }

                    if (message.command === 'sendPrompt') {
                        // Abort previous request if any
                        if (currentRequest && currentRequest.abort) currentRequest.abort();

                        const model = message.model || 'llama2';
                        const prompt = message.text;
                        const options = {
                            hostname: 'localhost',
                            port: 11434,
                            path: '/api/generate',
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' }
                        };

                        let botReply = '';
                        currentRequest = http.request(options, res => {
                            res.on('data', chunk => {
                                // Ollama streams JSON lines
                                const lines = chunk.toString().split('\n').filter(Boolean);
                                for (const line of lines) {
                                    try {
                                        const obj = JSON.parse(line);
                                        if (obj.response) {
                                            botReply += obj.response;
                                            panel.webview.postMessage({ command: 'responseChunk', text: botReply });
                                        }
                                        if (obj.done) {
                                            panel.webview.postMessage({ command: 'responseDone' });
                                            currentRequest = null;
                                        }
                                    } catch {}
                                }
                            });
                        });

                        currentRequest.on('error', () => {
                            panel.webview.postMessage({ command: 'responseDone' });
                            currentRequest = null;
                        });

                        currentRequest.write(JSON.stringify({ model, prompt, stream: true }));
                        currentRequest.end();
                    }

                    if (message.command === 'stopPrompt') {
                        if (currentRequest && currentRequest.abort) {
                            currentRequest.abort();
                            panel.webview.postMessage({ command: 'responseDone' });
                            currentRequest = null;
                        }
                    }

                    if (message.command === 'setModel') {
                        panel.webview.postMessage({ command: 'setModel', model: message.model });
                    }

                    if (message.command === 'setTheme') {
                        panel.webview.postMessage({ command: 'setTheme', theme: message.theme });
                    }
                },
                undefined,
                context.subscriptions
            );
        })
    );
}

module.exports = { activate };
