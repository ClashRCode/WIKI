(function () {
  // "Histoire/[HIST] Napoléon.html", même format que fileKey dans les pages de liste
  const id = decodeURIComponent(location.pathname)
    .split('/').filter(Boolean).slice(-2).join('/');
  const key = 'views:' + id;

  document.addEventListener('DOMContentLoaded', () => {
    let count = 0;
    try {
      count = parseInt(localStorage.getItem(key) || '0', 10) || 0;

      // une seule lecture comptée par session et par fiche (anti-rafraîchissement)
      if (!sessionStorage.getItem('seen:' + key)) {
        sessionStorage.setItem('seen:' + key, '1');
        count += 1;
        localStorage.setItem(key, String(count));
        try {
          new BroadcastChannel('views').postMessage({ file: id, count });
        } catch (e) {}
      }
    } catch (e) {}

    const el = document.getElementById('viewCount');
    if (el) el.textContent = 'Nombre de lectures : ' + count;
  });
})();