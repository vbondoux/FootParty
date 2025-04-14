const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const userMessage = input.value.trim();
  if (!userMessage) return;

  appendMessage('user', userMessage);
  input.value = '';

  appendMessage('bot', '⏳ Réponse en cours...');

  try {
    const response = await fetch('https://footparty-production.up.railway.app/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userMessage })
    });

    const data = await response.json();
    removeLastBotMessage();
    appendMessage('bot', data.response || "Erreur dans la réponse");
  } catch (err) {
    removeLastBotMessage();
    appendMessage('bot', "❌ Erreur de connexion au serveur.");
    console.error(err);
  }
});

function appendMessage(sender, text) {
  const div = document.createElement('div');
  div.classList.add('message', sender);
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLastBotMessage() {
  const messages = document.querySelectorAll('.bot');
  if (messages.length) {
    chatBox.removeChild(messages[messages.length - 1]);
  }
}
