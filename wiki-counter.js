(function () {
  const STORAGE_PREFIX = 'views:';
  const CHANNEL_NAME = 'views';

  function normalizeFileKey(fileKey) {
    return String(fileKey || '').replace(/^\/+/, '').replace(/\\/g, '/');
  }

  function getLocalCount(fileKey) {
    const key = STORAGE_PREFIX + normalizeFileKey(fileKey);
    return Number(parseInt(localStorage.getItem(key) || '0', 10) || 0);
  }

  function setLocalCount(fileKey, count) {
    const key = STORAGE_PREFIX + normalizeFileKey(fileKey);
    localStorage.setItem(key, String(Number(count || 0)));
  }

  function renderCount(node, count) {
    if (!node) return;
    node.textContent = `Nombre de lectures : ${Number(count || 0)}`;
  }

  async function fetchCount(fileKey) {
    const key = normalizeFileKey(fileKey);
    const response = await fetch(`/api/views?file=${encodeURIComponent(key)}`, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('API unavailable');
    }
    const data = await response.json();
    return Number(data.count || 0);
  }

  async function refreshCountNode(node, fileKey) {
    const key = normalizeFileKey(fileKey);
    const fallback = getLocalCount(key);
    renderCount(node, fallback);

    try {
      const count = await fetchCount(key);
      renderCount(node, count);
      setLocalCount(key, count);
      return count;
    } catch (error) {
      renderCount(node, fallback);
      return fallback;
    }
  }

  function notify(fileKey, count) {
    try {
      const channel = new BroadcastChannel(CHANNEL_NAME);
      channel.postMessage({ file: normalizeFileKey(fileKey), count: Number(count || 0) });
    } catch (error) {
      // Browsers without BroadcastChannel can ignore this safely.
    }
  }

  function bindLiveUpdates() {
    try {
      const channel = new BroadcastChannel(CHANNEL_NAME);
      channel.onmessage = (event) => {
        try {
          const file = normalizeFileKey(event?.data?.file);
          const count = Number(event?.data?.count || 0);
          if (!file) return;

          document.querySelectorAll(`[data-file="${file}"]`).forEach((link) => {
            const span = link.querySelector('.viewcount') || link.parentElement?.querySelector('.viewcount');
            if (span) {
              renderCount(span, count);
            }
          });

          document.querySelectorAll('.viewcount').forEach((node) => {
            if (node.dataset.file === file) {
              renderCount(node, count);
            }
          });
        } catch (error) {
          // no-op: updates should never break the page
        }
      };
    } catch (error) {
      // no-op: BroadcastChannel is optional
    }
  }

  window.WikiCounter = {
    normalizeFileKey,
    getLocalCount,
    setLocalCount,
    renderCount,
    fetchCount,
    refreshCountNode,
    notify,
    bindLiveUpdates,
  };
})();
