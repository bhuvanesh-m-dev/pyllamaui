const vscode = acquireVsCodeApi();
const md = window.marked;
let waitingForResponse = false;
let currentBotMsgDiv = null;
let currentBotMessageContent = '';
let currentModel = '';
let models = [];

function addMessage(text, sender, streaming = false) {
    const chat = document.getElementById('chat');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message';
    const bubble = document.createElement('div');
    bubble.className = sender === 'user' ? 'user' : 'bot';
    if (sender === 'bot') {
        bubble.innerHTML = md(text); // Render Markdown for bot
    } else {
        bubble.textContent = text;
    }
    msgDiv.appendChild(bubble);
    chat.appendChild(msgDiv);
    chat.scrollTop = chat.scrollHeight;
    if (sender === 'bot' && streaming) {
        currentBotMsgDiv = bubble;
        currentBotMessageContent = text; // Initialize with current text
    }
}

function updateBotMessage(textChunk) {
    if (currentBotMsgDiv) {
        currentBotMessageContent += textChunk;
        currentBotMsgDiv.innerHTML = md(currentBotMessageContent); // live markdown rendering
        document.getElementById('chat').scrollTop = document.getElementById('chat').scrollHeight;
    }
}

function send() {
    if (waitingForResponse) {
        vscode.postMessage({
            command: 'stopPrompt'
        });
        waitingForResponse = false;
        setSendBtnState();
        document.getElementById('input').disabled = false;
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
    vscode.postMessage({
        command: 'sendPrompt',
        text: prompt,
        model: currentModel
    });
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
    switch (message.command) {
        case 'responseChunk':
            updateBotMessage(message.text);
            break;
        case 'responseDone':
            waitingForResponse = false;
            setSendBtnState();
            document.getElementById('input').disabled = false;
            currentBotMsgDiv = null;
            break;
        case 'modelList':
            models = message.models;
            const select = document.getElementById('modelSelect');
            select.innerHTML = '';
            models.forEach(m => {
                const opt = document.createElement('option');
                opt.value = m;
                opt.textContent = m;
                select.appendChild(opt);
            });
            if (currentModel && models.includes(currentModel)) {
                select.value = currentModel;
            } else if (models.length > 0) {
                currentModel = models[0];
                select.value = currentModel;
            }
            updateModelIndicator();
            break;
        case 'setModel':
            currentModel = message.model;
            updateModelIndicator();
            break;
        case 'setTheme':
            setTheme(message.theme);
            break;
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
    vscode.postMessage({
        command: 'setModel',
        model: currentModel
    });
};

function setTheme(theme) {
    document.body.className = theme;
    vscode.postMessage({
        command: 'setTheme',
        theme
    });
}

// Initial request for models and settings
vscode.postMessage({ command: 'getModelList' });

// Restore state
const lastState = vscode.getState();
if (lastState) {
    currentModel = lastState.model;
    setTheme(lastState.theme);
    document.getElementById('chat').innerHTML = lastState.chatHistory;
}

// Save state
window.addEventListener('beforeunload', () => {
    vscode.setState({
        model: currentModel,
        theme: document.body.className,
        chatHistory: document.getElementById('chat').innerHTML
    });
});

setSendBtnState();