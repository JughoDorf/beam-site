'use strict';
// Core downloads and navigation work without JavaScript. Only the APK variant changes here.
const variants = {
  universal: { size: 11451239, file: 'BeamAndroid-0.2.0-universal.apk' },
  arm64: { size: 6068862, file: 'BeamAndroid-0.2.0-arm64.apk' },
  arm32: { size: 5343872, file: 'BeamAndroid-0.2.0-arm32.apk' },
  x86_64: { size: 5737083, file: 'BeamAndroid-0.2.0-x86_64.apk' },
  x86: { size: 5544568, file: 'BeamAndroid-0.2.0-x86.apk' },
};
const picker = document.getElementById('android-variant');
const androidLink = document.querySelector('[data-download="android"]');
const androidSize = document.querySelector('[data-size="android"]');
function updateVariant() {
  const variant = variants[picker.value] || variants.universal;
  androidLink.href = `https://github.com/JughoDorf/beam-site/releases/download/android-v0.2.0/${variant.file}`;
  androidSize.textContent = `${new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(variant.size / 1000000)} МБ`;
  androidLink.setAttribute('aria-label', `Скачать Beam Android 0.2.0, ${picker.options[picker.selectedIndex].text}`);
}
if (picker && androidLink && androidSize) {
  picker.addEventListener('change', updateVariant);
  updateVariant();
}
