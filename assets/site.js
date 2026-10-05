'use strict';
// Downloads work without JavaScript. Animation never gates a download or navigation.
const variants = {
  universal: { size: 11463583, file: 'BeamAndroid-0.3.0-universal.apk' },
  arm64: { size: 6081206, file: 'BeamAndroid-0.3.0-arm64.apk' },
  arm32: { size: 5356216, file: 'BeamAndroid-0.3.0-arm32.apk' },
  x86_64: { size: 5749427, file: 'BeamAndroid-0.3.0-x86_64.apk' },
  x86: { size: 5556912, file: 'BeamAndroid-0.3.0-x86.apk' },
};
const picker = document.getElementById('android-variant');
const androidLink = document.querySelector('[data-download="android"]');
const androidSize = document.querySelector('[data-size="android"]');
function updateVariant() {
  const variant = variants[picker.value] || variants.universal;
  androidLink.href = `https://github.com/JughoDorf/beam-site/releases/download/android-v0.3.0/${variant.file}`;
  androidSize.textContent = `${new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(variant.size / 1000000)} МБ`;
  androidLink.setAttribute('aria-label', `Скачать Beam Android 0.3.0, ${picker.options[picker.selectedIndex].text}`);
}
if (picker && androidLink && androidSize) {
  picker.addEventListener('change', updateVariant);
  updateVariant();
}

const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
if (!motionPreference.matches && 'IntersectionObserver' in window) {
  const blocks = document.querySelectorAll('.feature, .download-card, .setup-grid li, .closing');
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.remove('reveal-pending');
      entry.target.classList.add('reveal-visible');
      observer.unobserve(entry.target);
    }
  }, { rootMargin: '0px 0px 40px 0px', threshold: 0.08 });
  for (const block of blocks) {
    if (block.getBoundingClientRect().top < window.innerHeight) continue;
    block.classList.add('reveal-pending');
    observer.observe(block);
    block.addEventListener('animationend', () => block.classList.remove('reveal-visible'), { once: true });
  }
  // Reveal keyboard-focused controls immediately.
  document.addEventListener('focusin', event => {
    const block = event.target.closest('.reveal-pending');
    if (!block) return;
    block.classList.remove('reveal-pending');
    observer.unobserve(block);
  });
  const stopMotion = () => {
    if (!motionPreference.matches) return;
    observer.disconnect();
    for (const block of blocks) block.classList.remove('reveal-pending', 'reveal-visible');
  };
  if (motionPreference.addEventListener) motionPreference.addEventListener('change', stopMotion);
  else motionPreference.addListener(stopMotion);
}
