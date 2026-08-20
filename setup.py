import os
import shutil

# 1. Cleanup old greeting directory if present
if os.path.exists("greeting"):
    shutil.rmtree("greeting")
    print("🗑️ Removed old 'greeting/' folder")

# 2. Complete Project Files Directory
files = {
    # --- Root Configs ---
    "manifest.json": """{
  "short_name": "Leezuu",
  "name": "Leezuu Private Space",
  "icons": [
    {
      "src": "assets/icon.png",
      "type": "image/png",
      "sizes": "512x512"
    }
  ],
  "start_url": "./index.html",
  "background_color": "#0d0d1a",
  "theme_color": "#0d0d1a",
  "display": "standalone"
}""",

    "sw.js": """const CACHE_NAME = 'leezuu-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './loader/loader.css',
  './loader/loader.js',
  './welcome/welcome.css',
  './welcome/welcome.js',
  './home/home.css',
  './home/home.js',
  './greet/greet.css',
  './greet/greet.js',
  './chat/chat.css',
  './chat/chat.js'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => response || fetch(e.request))
  );
});""",

    "README.md": """# Leezuu 🌸 - Cinematic Private Space

PS5-inspired Web Application featuring:
- Time-aware daily messages
- On-demand romantic greeting modal
- Real-time private chat with Firebase integration
- Particle & Aurora visual backgrounds
""",

    "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Leezuu 🌸</title>
  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#0d0d1a">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  
  <!-- CSS Stylesheets -->
  <link rel="stylesheet" href="loader/loader.css">
  <link rel="stylesheet" href="welcome/welcome.css">
  <link rel="stylesheet" href="home/home.css">
  <link rel="stylesheet" href="greet/greet.css">
  <link rel="stylesheet" href="chat/chat.css">
  <link rel="stylesheet" href="chat/typing.css">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap">
</head>
<body>

  <!-- Background Canvas Effects -->
  <canvas id="auroraCanvas"></canvas>
  <canvas id="particleCanvas"></canvas>

  <!-- Modular View Containers -->
  <div id="loader-container"></div>
  <div id="welcome-container" class="hidden"></div>
  <div id="home-container" class="hidden"></div>
  <div id="greet-modal-container" class="hidden"></div>
  <div id="chat-container" class="hidden"></div>

  <!-- Main Orchestrator -->
  <script type="module">
    import { initAurora } from './effects/aurora.js';
    import { initParticles } from './effects/particles.js';
    import { loadModule } from './effects/loader-helper.js';

    window.addEventListener('DOMContentLoaded', async () => {
      // 1. Start background canvases
      initAurora('auroraCanvas');
      initParticles('particleCanvas');

      // 2. Load module HTML into placeholders
      await loadModule('loader/loader.html', 'loader-container');
      await loadModule('welcome/welcome.html', 'welcome-container');
      await loadModule('home/home.html', 'home-container');
      await loadModule('greet/greet.html', 'greet-modal-container');
      await loadModule('chat/chat.html', 'chat-container');

      // 3. Trigger PS5 Boot Sequence
      const { runBootSequence } = await import('./loader/loader.js');
      runBootSequence();
    });
  </script>

  <!-- Service Worker Registration -->
  <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
          .then(reg => console.log('Service Worker registered:', reg.scope))
          .catch(err => console.error('Service Worker registration error:', err));
      });
    }
  </script>
</body>
</html>""",

    # --- Loader ---
    "loader/loader.html": """<div class="ps5-boot-overlay" id="ps5BootOverlay">
  <div class="ps5-particle-burst" id="ps5ParticleBurst"></div>
  <div class="ps5-logo-wrapper">
    <div class="ps5-orb-glow"></div>
    <h1 class="ps5-title">Leezuu 🌸</h1>
    <p class="ps5-subtitle">Initializing your space…</p>
  </div>
</div>""",

    "loader/loader.css": """.ps5-boot-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: #05050a;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  transition: opacity 1s cubic-bezier(0.16, 1, 0.3, 1), transform 1s cubic-bezier(0.16, 1, 0.3, 1);
}

.ps5-boot-overlay.fade-out {
  opacity: 0;
  transform: scale(1.08);
  pointer-events: none;
}

.ps5-logo-wrapper {
  position: relative;
  text-align: center;
  z-index: 2;
  font-family: 'SF Pro Display', -apple-system, sans-serif;
}

.ps5-orb-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 140px;
  height: 140px;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle, rgba(0, 242, 254, 0.8) 0%, rgba(255, 0, 127, 0.4) 50%, rgba(0,0,0,0) 70%);
  border-radius: 50%;
  filter: blur(25px);
  animation: orbPulse 2.5s infinite alternate ease-in-out;
}

@keyframes orbPulse {
  0% { transform: translate(-50%, -50%) scale(0.8); opacity: 0.5; }
  100% { transform: translate(-50%, -50%) scale(1.4); opacity: 1; }
}

.ps5-title {
  color: #ffffff;
  font-size: 2.8rem;
  font-weight: 700;
  letter-spacing: -0.5px;
  text-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
  opacity: 0;
  transform: translateY(20px) scale(0.95);
  animation: ps5Reveal 1s forwards cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s;
}

.ps5-subtitle {
  color: rgba(255, 255, 255, 0.65);
  font-size: 0.95rem;
  margin-top: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  opacity: 0;
  animation: ps5Reveal 1s forwards cubic-bezier(0.34, 1.56, 0.64, 1) 0.6s;
}

@keyframes ps5Reveal {
  to { opacity: 1; transform: translateY(0) scale(1); }
}""",

    "loader/loader.js": """export function runBootSequence() {
  const bootOverlay = document.getElementById('ps5BootOverlay');
  const IS_FIRST_LAUNCH = !localStorage.getItem('leezuu_first_open');

  setTimeout(() => {
    if (bootOverlay) {
      bootOverlay.classList.add('fade-out');

      setTimeout(async () => {
        bootOverlay.style.display = 'none';

        if (IS_FIRST_LAUNCH) {
          const welcomeContainer = document.getElementById('welcome-container');
          welcomeContainer.classList.remove('hidden');
          const { initWelcome } = await import('../welcome/welcome.js');
          initWelcome();
        } else {
          const homeContainer = document.getElementById('home-container');
          homeContainer.classList.remove('hidden');
          const { initHome } = await import('../home/home.js');
          initHome();
        }
      }, 1000);
    }
  }, 2800);
}""",

    # --- Welcome ---
    "welcome/welcome.html": """<div class="welcome-overlay" id="welcomeOverlay">
  <div class="welcome-glass-card">
    <div class="welcome-header">
      <span class="welcome-badge">First Launch 🌸</span>
      <h2>Welcome to Leezuu</h2>
    </div>
    <div class="welcome-body">
      <p id="welcomeTypewriterText" class="welcome-text"></p>
    </div>
    <div class="welcome-actions">
      <button class="welcome-btn skip-btn" id="welcomeSkipBtn">Skip</button>
      <button class="welcome-btn enter-btn" id="welcomeEnterBtn">Enter Space ✨</button>
    </div>
  </div>
</div>""",

    "welcome/welcome.css": """.welcome-overlay {
  position: fixed;
  inset: 0;
  z-index: 8000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(5, 5, 10, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.welcome-glass-card {
  width: 100%;
  max-width: 400px;
  background: rgba(25, 25, 45, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 28px;
  padding: 30px;
  color: #fff;
  font-family: 'SF Pro Display', -apple-system, sans-serif;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6), 0 0 40px rgba(0, 242, 254, 0.2);
  animation: welcomeZoomIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes welcomeZoomIn {
  from { opacity: 0; transform: scale(0.85) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.welcome-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  background: rgba(0, 242, 254, 0.15);
  color: #00f2fe;
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.welcome-header h2 {
  font-size: 1.8rem;
  margin: 0;
  font-weight: 700;
}

.welcome-body {
  margin: 20px 0 30px 0;
  min-height: 80px;
}

.welcome-text {
  font-size: 1.05rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.85);
}

.welcome-actions {
  display: flex;
  gap: 12px;
}

.welcome-btn {
  height: 48px;
  border-radius: 16px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.welcome-btn:active { transform: scale(0.96); }

.skip-btn {
  width: 90px;
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.enter-btn {
  flex: 1;
  background: linear-gradient(135deg, #ff007f 0%, #7928ca 100%);
  color: #fff;
  box-shadow: 0 0 20px rgba(255, 0, 127, 0.4);
}""",

    "welcome/welcome.js": """export function initWelcome() {
  const textEl = document.getElementById('welcomeTypewriterText');
  const enterBtn = document.getElementById('welcomeEnterBtn');
  const skipBtn = document.getElementById('welcomeSkipBtn');
  const welcomeOverlay = document.getElementById('welcomeOverlay');

  const welcomeMessage = "Hey Leezuu! This is your quiet, private space built just for us. Everything here is instant, personal, and cinematic.";
  
  let i = 0;
  const timer = setInterval(() => {
    if (i < welcomeMessage.length) {
      textEl.innerText += welcomeMessage.charAt(i);
      i++;
    } else {
      clearInterval(timer);
    }
  }, 30);

  async function completeWelcome() {
    localStorage.setItem('leezuu_first_open', 'true');
    welcomeOverlay.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    welcomeOverlay.style.opacity = '0';
    welcomeOverlay.style.transform = 'scale(0.95)';

    setTimeout(async () => {
      document.getElementById('welcome-container').classList.add('hidden');
      const homeContainer = document.getElementById('home-container');
      homeContainer.classList.remove('hidden');
      const { initHome } = await import('../home/home.js');
      initHome();
    }, 500);
  }

  enterBtn.addEventListener('click', completeWelcome);
  skipBtn.addEventListener('click', completeWelcome);
}""",

    # --- Home ---
    "home/home.html": """<div class="home-screen-wrapper">
  <!-- Top Bar -->
  <header class="home-top-bar glass-bar">
    <div class="brand-title">Leezuu 🌸</div>
    <div class="top-bar-right">
      <span class="online-indicator"></span>
      <span class="live-clock" id="liveClock">00:00</span>
    </div>
  </header>

  <!-- Content Container -->
  <main class="home-main-content">
    <!-- Daily Greeting Card Widget -->
    <div class="daily-widget-card glass-card-widget">
      <div class="widget-header">
        <span class="widget-icon" id="widgetIcon">☀️</span>
        <h3 id="widgetTitle">Good Morning</h3>
      </div>
      <p class="widget-message" id="widgetMessage">Loading daily message...</p>
    </div>

    <!-- Navigation Hub -->
    <div class="home-actions-grid">
      <button class="action-card open-greet-btn" id="openGreetModalBtn">
        <div class="action-icon">✨</div>
        <div class="action-text">
          <h4>Open Greeting</h4>
          <p>Read romantic notes</p>
        </div>
      </button>

      <button class="action-card open-chat-btn" id="openChatBtn">
        <div class="action-icon">💬</div>
        <div class="action-text">
          <h4>Private Chat</h4>
          <p>Open messenger</p>
        </div>
      </button>
    </div>
  </main>
</div>""",

    "home/home.css": """.home-screen-wrapper {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'SF Pro Display', -apple-system, sans-serif;
  color: #fff;
}

.glass-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: rgba(15, 15, 25, 0.6);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.brand-title {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.online-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #34c759;
  box-shadow: 0 0 8px #34c759;
}

.live-clock {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.home-main-content {
  flex: 1;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 480px;
  margin: 0 auto;
  width: 100%;
}

.glass-card-widget {
  background: rgba(25, 25, 45, 0.55);
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.widget-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.widget-icon { font-size: 1.4rem; }

.widget-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #00f2fe;
}

.widget-message {
  margin: 0;
  font-size: 1rem;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.88);
}

.home-actions-grid {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.action-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 20px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  cursor: pointer;
  text-align: left;
  transition: transform 0.2s ease, background 0.2s ease;
}

.action-card:active { transform: scale(0.97); }

.open-greet-btn {
  background: linear-gradient(135deg, rgba(0, 242, 254, 0.15) 0%, rgba(79, 172, 254, 0.15) 100%);
  border-color: rgba(0, 242, 254, 0.3);
}

.open-chat-btn {
  background: linear-gradient(135deg, rgba(255, 0, 127, 0.15) 0%, rgba(121, 40, 202, 0.15) 100%);
  border-color: rgba(255, 0, 127, 0.3);
}

.action-icon {
  font-size: 1.8rem;
}

.action-text h4 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
}

.action-text p {
  margin: 2px 0 0 0;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
}""",

    "home/home.js": """export async function initHome() {
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
}""",

    "home/daily-messages.json": """{
  "morning": [
    "Aaj ka din smile se start karna 😊",
    "Good morning, sunshine ☀️",
    "Ek nayi subah, ek nayi vibe ✨"
  ],
  "afternoon": [
    "Thoda paani peena mat bhoolna 💧",
    "Aaj ka din kaafi productive ho sakta hai ✨",
    "Take a short break and relax 🌸"
  ],
  "evening": [
    "Aaj ka sunset kaafi khoobsurat tha 🌅",
    "Thoda aaram bhi kar lena ✨",
    "Hope your day went well 🌆"
  ],
  "night": [
    "Good night 🌙",
    "Sweet dreams 😌",
    "Sleep well and rest up 🌌"
  ]
}""",

    # --- Greet ---
    "greet/greet.html": """<div class="greet-modal-backdrop" id="greetModalBackdrop">
  <div class="greet-modal-wrapper">
    <button class="close-greet-btn" id="closeGreetBtn">✕</button>
    <div class="greet-glass-card" id="greetGlassCard">
      <div class="greet-progress-bar"><div class="greet-progress-fill" id="greetProgressFill"></div></div>
      <div class="greet-card-header">
        <span class="greet-theme-badge" id="greetThemeBadge">Theme</span>
        <h2 id="greetCardTitle">...</h2>
      </div>
      <div class="greet-card-body">
        <p id="greetCardMessage" class="greet-typewriter"></p>
      </div>
      <div class="greet-card-footer">
        <button class="greet-nav-btn" id="prevGreetCardBtn">‹</button>
        <button class="greet-primary-btn" id="nextGreetCardBtn">Next ✨</button>
      </div>
    </div>
  </div>
</div>""",

    "greet/greet.css": """.greet-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 9000;
  background: rgba(5, 5, 15, 0.75);
  backdrop-filter: blur(25px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.greet-modal-wrapper {
  position: relative;
  width: 100%;
  max-width: 420px;
}

.close-greet-btn {
  position: absolute;
  top: -48px;
  right: 0;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1rem;
}

.greet-glass-card {
  background: rgba(20, 20, 35, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 28px;
  padding: 28px;
  color: #fff;
  font-family: 'SF Pro Display', -apple-system, sans-serif;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.greet-glass-card.slide-up { animation: cardSlideUp 0.5s ease; }
.greet-glass-card.zoom { animation: cardZoom 0.5s ease; }

@keyframes cardSlideUp {
  from { transform: translateY(40px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes cardZoom {
  from { transform: scale(0.85); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.greet-progress-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  margin-bottom: 20px;
  overflow: hidden;
}

.greet-progress-fill {
  height: 100%;
  width: 0%;
  background: #00f2fe;
  transition: width 0.3s ease;
}

.greet-theme-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 10px;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 8px;
  background: rgba(255, 255, 255, 0.1);
}

.greet-card-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.greet-card-body {
  min-height: 100px;
  margin: 20px 0;
}

.greet-typewriter {
  font-size: 1.05rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.9);
}

.greet-card-footer {
  display: flex;
  gap: 12px;
}

.greet-nav-btn {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  font-size: 1.4rem;
  cursor: pointer;
}

.greet-primary-btn {
  flex: 1;
  height: 48px;
  border-radius: 16px;
  border: none;
  background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
  color: #000;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
}""",

    "greet/greet.js": """export async function openGreetModal() {
  try {
    const res = await fetch('greet/greet-config.json');
    const config = await res.json();

    let currentIndex = 0;
    const cardEl = document.getElementById('greetGlassCard');
    const titleEl = document.getElementById('greetCardTitle');
    const msgEl = document.getElementById('greetCardMessage');
    const badgeEl = document.getElementById('greetThemeBadge');
    const progressEl = document.getElementById('greetProgressFill');
    const nextBtn = document.getElementById('nextGreetCardBtn');
    const prevBtn = document.getElementById('prevGreetCardBtn');
    const closeBtn = document.getElementById('closeGreetBtn');

    function renderCard(index) {
      const cardData = config.cards[index];
      const themeData = config.themes[cardData.theme] || {};

      badgeEl.innerText = cardData.theme;
      badgeEl.style.color = themeData.accentColor || '#00f2fe';
      progressEl.style.background = themeData.accentColor || '#00f2fe';

      cardEl.className = `greet-glass-card ${cardData.animation || 'slide-up'}`;

      titleEl.innerText = cardData.title;
      msgEl.innerText = '';

      let i = 0;
      const timer = setInterval(() => {
        if (i < cardData.message.length) {
          msgEl.innerText += cardData.message.charAt(i);
          i++;
        } else {
          clearInterval(timer);
        }
      }, 30);

      progressEl.style.width = `${((index + 1) / config.cards.length) * 100}%`;
      nextBtn.innerText = index === config.cards.length - 1 ? "Done ✨" : "Next ✨";
    }

    nextBtn.onclick = () => {
      if (currentIndex < config.cards.length - 1) {
        currentIndex++;
        renderCard(currentIndex);
      } else {
        closeModal();
      }
    };

    prevBtn.onclick = () => {
      if (currentIndex > 0) {
        currentIndex--;
        renderCard(currentIndex);
      }
    };

    closeBtn.onclick = closeModal;

    function closeModal() {
      document.getElementById('greet-modal-container').classList.add('hidden');
    }

    renderCard(0);
  } catch (err) {
    console.error("Greet config load error:", err);
  }
}""",

    "greet/greet-config.json": """{
  "themes": {
    "soft-romantic": {
      "accentColor": "#ff007f",
      "glowIntensity": "medium"
    },
    "electric-aurora": {
      "accentColor": "#00f2fe",
      "glowIntensity": "high"
    }
  },
  "cards": [
    {
      "theme": "soft-romantic",
      "title": "A little note 💖",
      "message": "Kabhi kabhi kuch log bina reason ke yaad aa jaate hain…",
      "animation": "slide-up"
    },
    {
      "theme": "electric-aurora",
      "title": "Electric Mood ⚡",
      "message": "Tumhari wajah se kuch din aur ache lagte hain.",
      "animation": "zoom"
    }
  ]
}""",

    # --- Chat Modules ---
    "chat/chat.html": """<div class="chat-wrapper">
  <header class="chat-header">
    <button class="back-btn" id="chatBackBtn">‹</button>
    <h3>Private Chat 💬</h3>
  </header>
  <div class="messages-list" id="chatMessagesList"></div>
  <div class="chat-input-bar">
    <input type="text" id="chatInput" placeholder="Type a message..." />
    <button id="sendChatBtn">Send</button>
  </div>
</div>""",

    "chat/chat.css": """.chat-wrapper {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: rgba(10, 10, 20, 0.85);
  backdrop-filter: blur(20px);
}
.chat-header {
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
}
.back-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.8rem;
  cursor: pointer;
}
.messages-list {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}
.chat-input-bar {
  padding: 16px;
  display: flex;
  gap: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}
.chat-input-bar input {
  flex: 1;
  padding: 12px 16px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}
.chat-input-bar button {
  padding: 12px 20px;
  border-radius: 20px;
  border: none;
  background: #00f2fe;
  color: #000;
  font-weight: 600;
  cursor: pointer;
}""",

    "chat/chat.js": """export function initChat() {
  const backBtn = document.getElementById('chatBackBtn');
  backBtn.onclick = () => {
    document.getElementById('chat-container').classList.add('hidden');
    document.getElementById('home-container').classList.remove('hidden');
  };
}""",

    "chat/typing.css": """.typing-indicator { display: flex; gap: 4px; padding: 8px; }""",
    "chat/typing.js": """export function handleTyping() {}""",
    "chat/reactions.js": """export function addReaction() {}""",
    "chat/reply.js": """export function setupReply() {}""",
    "chat/dissolve.js": """export function dissolveMessage() {}""",

    # --- Effects ---
    "effects/aurora.js": """export function initAurora(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();
}""",

    "effects/particles.js": """export function initParticles(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();
}""",

    "effects/reaction-burst.js": """export function triggerBurst() {}""",

    "effects/loader-helper.js": """export async function loadModule(url, containerId) {
  try {
    const res = await fetch(url);
    const html = await res.text();
    document.getElementById(containerId).innerHTML = html;
  } catch (err) {
    console.error(`Error loading module ${url}:`, err);
  }
}""",

    # --- Firebase Stubs ---
    "firebase/firebase-config.js": """// Initialize Firebase here
export const firebaseConfig = {};""",
    "firebase/auth.js": """export function initAuth() {}""",
    "firebase/database.js": """export function initDB() {}""",
    "firebase/presence.js": """export function initPresence() {}""",
    "firebase/storage.js": """export function initStorage() {}"""
}

# 3. Create Files and Folders
print("🚀 Creating all project folders and files...")
for file_path, content in files.items():
    folder = os.path.dirname(file_path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"  ✓ Created: {file_path}")

print("\n✨ Setup completed successfully! All 25+ files and folders are ready.")
