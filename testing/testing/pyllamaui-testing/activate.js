const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');
const { getWebviewContent } = require('./webviewContent');

function activate(context) {
    let panel = undefined;
    let pythonProcess = null;

    // Function to send a command to the Python process
    function sendToPython(command, args = []) {
        if (pythonProcess) {
            pythonProcess.stdin.write(JSON.stringify({ command, args }) + '\n');
        }
    }

    // Function to kill the Python process
    function stopPythonProcess() {
        if (pythonProcess) {
            pythonProcess.kill();
            pythonProcess = null;
        }
    }

    context.subscriptions.push(
        vscode.commands.registerCommand('pyllamaui.chat', function () {
            if (panel) {
                panel.reveal(vscode.ViewColumn.Two);
                return;
            }

            panel = vscode.window.createWebviewPanel(
                'pyllamaUi',
                'PyllamaUI',
                vscode.ViewColumn.Two,
                {
                    enableScripts: true,
                    localResourceRoots: [vscode.Uri.file(path.join(context.extensionPath, 'webview'))]
                }
            );

            panel.webview.html = getWebviewContent(context.extensionPath);

            // Start the Python backend
            const pythonPath = vscode.workspace.getConfiguration('pyllamaui').get('pythonPath') || 'python';
            const scriptPath = path.join(context.extensionPath, 'py', 'run_prompt.py');
            pythonProcess = spawn(pythonPath, [scriptPath]);

            // Handle Python process output
            pythonProcess.stdout.on('data', (data) => {
                const output = data.toString().trim();
                try {
                    const result = JSON.parse(output);
                    if (result.response) {
                        panel.webview.postMessage({ command: 'responseChunk', text: result.response });
                    } else if (result.models) {
                        panel.webview.postMessage({ command: 'modelList', models: result.models });
                    } else if (result.error) {
                        vscode.window.showErrorMessage(`PyllamaUI Error: ${result.error}`);
                    }
                } catch (e) {
                    // Not a JSON response, likely a partial stream
                    panel.webview.postMessage({ command: 'responseChunk', text: output });
                }
            });

            pythonProcess.stderr.on('data', (data) => {
                vscode.window.showErrorMessage(`PyllamaUI Error: ${data}`);
            });

            pythonProcess.on('close', (code) => {
                if (code !== 0) {
                    vscode.window.showInformationMessage('PyllamaUI backend stopped.');
                }
                panel.webview.postMessage({ command: 'responseDone' });
            });

            // Handle messages from the webview
            panel.webview.onDidReceiveMessage(
                message => {
                    switch (message.command) {
                        case 'sendPrompt':
                            const model = vscode.workspace.getConfiguration('pyllamaui').get('modelName');
                            sendToPython('sendPrompt', [message.text, `--model=${model}`, '--stream']);
                            return;
                        case 'stopPrompt':
                            stopPythonProcess();
                            // Restart for next prompt
                            const pythonPath = vscode.workspace.getConfiguration('pyllamaui').get('pythonPath') || 'python';
                            const scriptPath = path.join(context.extensionPath, 'py', 'run_prompt.py');
                            pythonProcess = spawn(pythonPath, [scriptPath]);
                            panel.webview.postMessage({ command: 'responseDone' });
                            return;
                        case 'getModelList':
                            sendToPython('getModelList');
                            return;
                        case 'setModel':
                            vscode.workspace.getConfiguration('pyllamaui').update('modelName', message.model, vscode.ConfigurationTarget.Global);
                            panel.webview.postMessage({ command: 'setModel', model: message.model });
                            return;
                        case 'setTheme':
                             vscode.workspace.getConfiguration('pyllamaui').update('theme', message.theme, vscode.ConfigurationTarget.Global);
                            return;
                    }
                },
                undefined,
                context.subscriptions
            );

            panel.onDidDispose(() => {
                stopPythonProcess();
                panel = undefined;
            }, null, context.subscriptions);

            // Initial setup
            const savedModel = vscode.workspace.getConfiguration('pyllamaui').get('modelName');
            if (savedModel) {
                panel.webview.postMessage({ command: 'setModel', model: savedModel });
            }
            const savedTheme = vscode.workspace.getConfiguration('pyllamaui').get('theme');
            if (savedTheme) {
                panel.webview.postMessage({ command: 'setTheme', theme: savedTheme });
            }

            // Get the model list on startup
            sendToPython('getModelList');
        })
    );
}

module.exports = { activate };
