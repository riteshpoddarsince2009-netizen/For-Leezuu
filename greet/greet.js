export async function openGreetModal() {
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
}
