function getWebviewContent() {
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: var(--bg, #181818);
                color: var(--fg, #fff);
                margin: 0;
                padding: 0;
                height: 100vh;
                box-sizing: border-box;
            }
            h3 {
                margin: 0;
                padding: 16px;
                background: var(--header-bg, #222);
                border-bottom: 1px solid #333;
                font-size: 1.2em;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            #model-indicator {
                font-size: 0.9em;
                color: var(--accent, #7c3aed);
                margin-left: 10px;
            }
            #settingsBtn {
                background: none;
                border: none;
                color: var(--fg, #fff);
                font-size: 1.3em;
                cursor: pointer;
                margin-left: 10px;
            }
            #settingsMenu {
                display: none;
                position: absolute;
                top: 56px;
                right: 16px;
                background: var(--header-bg, #222);
                border: 1px solid #333;
                border-radius: 8px;
                padding: 16px;
                z-index: 10;
                min-width: 220px;
            }
            #settingsMenu label {
                display: block;
                margin-bottom: 8px;
                font-size: 1em;
            }
            #settingsMenu select {
                width: 100%;
                margin-bottom: 12px;
                padding: 6px;
                border-radius: 6px;
                border: none;
                background: var(--bg, #181818);
                color: var(--fg, #fff);
            }
            #settingsMenu .theme-btn {
                display: inline-block;
                margin-right: 8px;
                margin-bottom: 8px;
                padding: 6px 14px;
                border-radius: 6px;
                border: none;
                background: #7c3aed;
                color: #fff;
                cursor: pointer;
                font-size: 0.95em;
            }
            #chat {
                display: flex;
                flex-direction: column;
                gap: 10px;
                padding: 16px;
                height: calc(100vh - 120px);
                min-height: 300px;
                overflow-y: auto;
                background: var(--chat-bg, #222);
                border-bottom: 1px solid #333;
            }
            .message {
                display: flex;
                width: 100%;
            }
            .user {
                margin-left: auto;
                background: #7c3aed;
                color: #fff;
                padding: 10px 18px;
                border-radius: 18px 0 18px 18px;
                max-width: 70%;
                word-break: break-word;
                font-size: 1em;
                box-shadow: 0 2px 8px #7c3aed33;
                align-self: flex-end;
            }
            .bot {
                margin-right: auto;
                background: #111;
                color: #fff;
                padding: 10px 18px;
                border-radius: 0 18px 18px 18px;
                max-width: 70%;
                word-break: break-word;
                font-size: 1em;
                box-shadow: 0 2px 8px #00000033;
                align-self: flex-start;
            }
            #inputRow {
                display: flex;
                align-items: center;
                padding: 16px;
                background: var(--bg, #181818);
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100vw;
                gap: 10px;
                z-index: 5;
            }
            #input {
                flex: 1;
                padding: 10px;
                border-radius: 8px;
                border: none;
                background: var(--chat-bg, #222);
                color: var(--fg, #fff);
                font-size: 1em;
            }
            #input:focus {
                outline: 2px solid #7c3aed;
            }
            #sendBtn {
                padding: 10px 20px;
                background: #7c3aed;
                color: #fff;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                cursor: pointer;
                transition: background 0.2s;
            }
            #sendBtn:disabled {
                background: #444;
                cursor: not-allowed;
            }
            #sendBtn.stop {
                background: #ef4444;
            }
            #sendBtn.stop:hover {
                background: #b91c1c;
            }
        </style>
    </head>
    <body>
        <h3>
            🦙 PyllamaUI Chat
            <span id="model-indicator"></span>
            <button id="settingsBtn" title="Settings">&#9881;</button>
        </h3>
        <div id="settingsMenu">
            <label for="modelSelect">Model:</label>
            <select id="modelSelect"></select>
            <label>Theme:</label>
            <button class="theme-btn" onclick="setTheme('dark')">Dark</button>
            <button class="theme-btn" onclick="setTheme('light')">Light</button>
        </div>
        <div id="chat"></div>
        <div id="inputRow">
            <input id="input" type="text" placeholder="Type your prompt..." autocomplete="off" />
            <button id="sendBtn" onclick="send()">Send</button>
        </div>
        <script>
            const vscode = acquireVsCodeApi();
            let waitingForResponse = false;
            let currentBotMsgDiv = null;
            let currentModel = '';
            let models = [];

            function addMessage(text, sender, streaming=false) {
                const chat = document.getElementById('chat');
                const msgDiv = document.createElement('div');
                msgDiv.className = 'message';
                const bubble = document.createElement('div');
                bubble.className = sender === 'user' ? 'user' : 'bot';
                bubble.textContent = text;
                msgDiv.appendChild(bubble);
                chat.appendChild(msgDiv);
                chat.scrollTop = chat.scrollHeight;
                if (sender === 'bot' && streaming) {
                    currentBotMsgDiv = bubble;
                }
            }

            function updateBotMessage(text) {
                if (currentBotMsgDiv) {
                    currentBotMsgDiv.textContent = text;
                    document.getElementById('chat').scrollTop = document.getElementById('chat').scrollHeight;
                }
            }

            function send() {
                if (waitingForResponse) {
                    vscode.postMessage({ command: 'stopPrompt' });
                    return;
                }
                const input = document.getElementById('input');
                const prompt = input.value.trim();
                if (!prompt) return;
                addMessage(prompt, 'user');
                waitingForResponse = true;
                setSendBtnState();
                input.value = '';
                input.disabled = true;
                addMessage('', 'bot', true); // Start bot bubble for streaming
                vscode.postMessage({ command: 'sendPrompt', text: prompt, model: currentModel });
            }

            function setSendBtnState() {
                const btn = document.getElementById('sendBtn');
                if (waitingForResponse) {
                    btn.textContent = 'Stop';
                    btn.classList.add('stop');
                } else {
                    btn.textContent = 'Send';
                    btn.classList.remove('stop');
                }
                btn.disabled = false;
            }

            window.addEventListener('message', event => {
                const message = event.data;
                if (message.command === 'responseChunk') {
                    updateBotMessage(message.text);
                }
                if (message.command === 'responseDone') {
                    waitingForResponse = false;
                    setSendBtnState();
                    document.getElementById('input').disabled = false;
                    currentBotMsgDiv = null;
                }
                if (message.command === 'modelList') {
                    models = message.models;
                    const select = document.getElementById('modelSelect');
                    select.innerHTML = '';
                    models.forEach(m => {
                        const opt = document.createElement('option');
                        opt.value = m;
                        opt.textContent = m;
                        select.appendChild(opt);
                    });
                    if (!currentModel && models.length) {
                        currentModel = models[0];
                        select.value = currentModel;
                        updateModelIndicator();
                    }
                }
                if (message.command === 'setModel') {
                    currentModel = message.model;
                    updateModelIndicator();
                }
                if (message.command === 'setTheme') {
                    setTheme(message.theme);
                }
            });

            function updateModelIndicator() {
                document.getElementById('model-indicator').textContent = currentModel ? '– ' + currentModel : '';
            }

            document.getElementById('input').addEventListener('keydown', function(e) {
                if (e.key === 'Enter') send();
            });

            document.getElementById('settingsBtn').onclick = function() {
                const menu = document.getElementById('settingsMenu');
                menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
            };

            document.getElementById('modelSelect').onchange = function(e) {
                currentModel = e.target.value;
                updateModelIndicator();
                vscode.postMessage({ command: 'setModel', model: currentModel });
            };

            function setTheme(theme) {
                if (theme === 'light') {
                    document.body.style.setProperty('--bg', '#f5f5f5');
                    document.body.style.setProperty('--fg', '#222');
                    document.body.style.setProperty('--header-bg', '#e5e5e5');
                    document.body.style.setProperty('--chat-bg', '#fff');
                    document.body.style.setProperty('--accent', '#7c3aed');
                } else {
                    document.body.style.setProperty('--bg', '#181818');
                    document.body.style.setProperty('--fg', '#fff');
                    document.body.style.setProperty('--header-bg', '#222');
                    document.body.style.setProperty('--chat-bg', '#222');
                    document.body.style.setProperty('--accent', '#7c3aed');
                }
                vscode.postMessage({ command: 'setTheme', theme });
            }

            // Initial request for models
            vscode.postMessage({ command: 'getModelList' });

            setSendBtnState();
        </script>
    </body>
    </html>`;
}

module.exports = { getWebviewContent };
