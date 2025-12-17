// Client-side Script for Guy Heart Photography Chat

const STORAGE_KEY = 'guyheart_chat_history';

// Initialize Lucide icons
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    // Load previous chat history
    loadChatHistory();
    // Focus input on load
    document.getElementById('user-input').focus();
});

let chatHistory = [];
const chatContainer = document.getElementById('chat-container'); // Scrollable area
const messagesArea = document.getElementById('messages-area'); // Message list

// Configure Marked.js
marked.setOptions({
    breaks: true,
    gfm: true
});

// ========== LOCALSTORAGE FUNCTIONS ==========

function saveChatHistory() {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(chatHistory));
    } catch (e) {
        console.warn('Failed to save chat history:', e);
    }
}

function loadChatHistory() {
    try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            chatHistory = JSON.parse(saved);
            // Re-render all messages
            chatHistory.forEach(entry => {
                const role = entry.role === 'client' ? 'user' : 'ai';
                appendMessage(role, entry.message, false); // false = don't save again
            });
        }
    } catch (e) {
        console.warn('Failed to load chat history:', e);
        chatHistory = [];
    }
}

function clearChatHistory() {
    if (confirm('Clear all chat history?')) {
        chatHistory = [];
        localStorage.removeItem(STORAGE_KEY);
        messagesArea.innerHTML = '';
    }
}

// ========== CHAT FUNCTIONS ==========

async function handleSend(e) {
    e.preventDefault();
    const input = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const message = input.value.trim();

    if (!message) return;

    // Disable input while processing
    input.value = '';
    input.disabled = true;
    sendBtn.disabled = true;

    // 1. Add User Message
    appendMessage('user', message);

    // 2. Add Loading Indicator
    const loadingId = appendLoading();

    try {
        // 3. Fetch Response
        const response = await fetch('/generate-reply', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                clientSequence: message,
                chatHistory: chatHistory
            })
        });

        const data = await response.json();
        
        // Remove Loading Indicator
        removeLoading(loadingId);

        if (data.aiReply) {
            // 4. Add AI Message
            appendMessage('ai', data.aiReply);
            
            // Update History
            chatHistory.push({ role: 'client', message: message });
            chatHistory.push({ role: 'consultant', message: data.aiReply });
            
            // Save to localStorage
            saveChatHistory();
        } else {
            appendMessage('ai', "I'm having a bit of trouble connecting right now. Please try again in a moment.");
            console.error(data);
        }

    } catch (err) {
        removeLoading(loadingId);
        appendMessage('ai', "Sorry, I seem to be offline. Please check your internet connection.");
        console.error(err);
    } finally {
        // Re-enable input
        input.disabled = false;
        sendBtn.disabled = false;
        input.focus();
    }
}

function appendMessage(role, text, shouldSave = true) {
    const templateId = role === 'user' ? 'template-user' : 'template-ai';
    const template = document.getElementById(templateId);
    const clone = template.content.cloneNode(true);
    
    // Select the container div
    const messageDiv = clone.querySelector('div');

    // Find the inner content div (it's the second child in correct structure usually, or just finding the one with content)
    // For user: it's the only child of the wrapper. For AI: it's the second child (after avatar).
    let contentDiv;
    if (role === 'user') {
        contentDiv = messageDiv.children[0];
        contentDiv.innerText = text; // User text is plain text usually
    } else {
        contentDiv = messageDiv.children[1];
        contentDiv.innerHTML = marked.parse(text); // AI text is markdown
        
        // Post-process table styling if marked generates tables
        // We can add classes to tables here if needed, or rely on Tailwind Typography (prose)
    }

    messagesArea.appendChild(clone);
    scrollToBottom();
    
    // Re-init icons for new content if any (though marked usually doesn't output lucide tags unless we custom render)
    lucide.createIcons();
}

function appendLoading() {
    const template = document.getElementById('template-loading');
    const clone = template.content.cloneNode(true);
    const id = 'loading-' + Date.now();
    clone.firstElementChild.id = id;
    messagesArea.appendChild(clone);
    scrollToBottom();
    return id;
}

function removeLoading(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
