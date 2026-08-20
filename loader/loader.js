export function runBootSequence() {
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
}
