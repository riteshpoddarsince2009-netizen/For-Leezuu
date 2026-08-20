export async function initHome() {
  updateClock();
  setInterval(updateClock, 1000);

  await loadDailyWidgetMessage();

  const openGreetBtn = document.getElementById('openGreetModalBtn');
  const openChatBtn = document.getElementById('openChatBtn');

  openGreetBtn.addEventListener('click', async () => {
    const modalContainer = document.getElementById('greet-modal-container');
    modalContainer.classList.remove('hidden');
    const { openGreetModal } = await import('../greet/greet.js');
    openGreetModal();
  });

  openChatBtn.addEventListener('click', async () => {
    document.getElementById('home-container').classList.add('hidden');
    const chatContainer = document.getElementById('chat-container');
    chatContainer.classList.remove('hidden');
    const { initChat } = await import('../chat/chat.js');
    initChat();
  });
}

function updateClock() {
  const clockEl = document.getElementById('liveClock');
  if (!clockEl) return;
  const now = new Date();
  clockEl.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

async function loadDailyWidgetMessage() {
  const titleEl = document.getElementById('widgetTitle');
  const msgEl = document.getElementById('widgetMessage');
  const iconEl = document.getElementById('widgetIcon');

  try {
    const res = await fetch('home/daily-messages.json');
    const data = await res.json();

    const hour = new Date().getHours();
    let slot = 'morning';
    let title = 'Good Morning ☀️';
    let icon = '☀️';

    if (hour >= 5 && hour < 11) {
      slot = 'morning';
      title = 'Good Morning ☀️';
      icon = '☀️';
    } else if (hour >= 11 && hour < 17) {
      slot = 'afternoon';
      title = 'Aaj ka Note ✨';
      icon = '✨';
    } else if (hour >= 17 && hour < 21) {
      slot = 'evening';
      title = 'Evening Note 🌅';
      icon = '🌅';
    } else {
      slot = 'night';
      title = 'Good Night 🌙';
      icon = '🌙';
    }

    const messages = data[slot];
    const selectedMsg = messages[Math.floor(Math.random() * messages.length)];

    titleEl.innerText = title;
    iconEl.innerText = icon;
    msgEl.innerText = selectedMsg;
  } catch (err) {
    console.error("Daily messages load error:", err);
  }
}
