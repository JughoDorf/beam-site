'use strict';
// Existing Beam bookmarks and updater links keep their exact destination after the brand split.
const beamSections = new Set(['#beam-installer', '#easytier', '#downloads', '#client-update', '#easytier-setup', '#separate-installers', '#setup', '#features', '#faq']);
function openLegacyBeamSection() {
  if (!beamSections.has(location.hash)) return;
  const target = new URL('beam.html', location.href);
  target.search = location.search;
  target.hash = location.hash;
  location.replace(target.href);
}
openLegacyBeamSection();
window.addEventListener('hashchange', openLegacyBeamSection);
