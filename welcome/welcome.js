export function initWelcome() {
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
}
