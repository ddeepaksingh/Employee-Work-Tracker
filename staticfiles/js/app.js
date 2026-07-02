/**
 * Employee Report System — Main JavaScript
 */

// ── Theme / Dark Mode ─────────────────────────────────────────────────────────
(function () {
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
})();

document.addEventListener('DOMContentLoaded', function () {

  // ── Apply saved theme to <html> ──────────────────────────────────────────
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  syncThemeIcon(savedTheme);

  // ── Theme toggle button ──────────────────────────────────────────────────
  const themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const next = current === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      syncThemeIcon(next);
    });
  }

  function syncThemeIcon(theme) {
    const icon = document.getElementById('theme-icon');
    if (icon) {
      icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
    }
  }

  // ── Sidebar Mobile Toggle ─────────────────────────────────────────────────
  const sidebarToggle = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');

  function openSidebar() {
    sidebar && sidebar.classList.add('open');
    overlay && overlay.classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar && sidebar.classList.remove('open');
    overlay && overlay.classList.remove('show');
    document.body.style.overflow = '';
  }

  if (sidebarToggle) sidebarToggle.addEventListener('click', openSidebar);
  if (overlay) overlay.addEventListener('click', closeSidebar);

  // ── Auto-dismiss Django messages as Bootstrap Toasts ──────────────────────
  const toastElems = document.querySelectorAll('.auto-toast');
  toastElems.forEach(function (el) {
    const t = new bootstrap.Toast(el, { delay: 5000 });
    t.show();
  });

  // ── Character Counter for Report Textarea ─────────────────────────────────
  const textarea = document.getElementById('id_report_text');
  const counter = document.getElementById('char-counter');
  if (textarea && counter) {
    const MIN = parseInt(textarea.getAttribute('minlength') || 50);
    const MAX = parseInt(textarea.getAttribute('maxlength') || 5000);

    function updateCounter() {
      const len = textarea.value.length;
      counter.textContent = `${len} / ${MAX} characters (min: ${MIN})`;
      counter.className = 'char-counter';
      if (len > MAX * 0.9) counter.classList.add('error');
      else if (len > MAX * 0.75) counter.classList.add('warn');
    }

    textarea.addEventListener('input', updateCounter);
    updateCounter();
  }

  // ── Live Clock ────────────────────────────────────────────────────────────
  const clockEl = document.getElementById('live-clock');
  if (clockEl) {
    function tick() {
      const now = new Date();
      clockEl.textContent = now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }
    tick();
    setInterval(tick, 1000);
  }

  // ── Confirm Modals for Delete Buttons ────────────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (!confirm(el.dataset.confirm)) e.preventDefault();
    });
  });

  // ── Loading overlay on form submit ────────────────────────────────────────
  document.querySelectorAll('form[data-loading]').forEach(function (form) {
    form.addEventListener('submit', function () {
      const overlay = document.getElementById('loading-overlay');
      if (overlay) overlay.classList.add('show');
    });
  });

  // ── Department → Designation dynamic filter ───────────────────────────────
  const deptSelect = document.getElementById('id_emp_dept');
  const desigSelect = document.getElementById('id_emp_desig');
  if (deptSelect && desigSelect) {
    const allOptions = Array.from(desigSelect.options);
    deptSelect.addEventListener('change', function () {
      const deptId = this.value;
      desigSelect.innerHTML = '<option value="">---------</option>';
      allOptions.forEach(function (opt) {
        if (!deptId || opt.dataset.dept === deptId || opt.value === '') {
          desigSelect.appendChild(opt.cloneNode(true));
        }
      });
    });
  }

  // ── Notification mark-read via AJAX ──────────────────────────────────────
  document.querySelectorAll('.mark-read-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const pk = btn.dataset.pk;
      fetch(`/notifications/${pk}/read/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json',
        },
      }).then(function () {
        const item = document.getElementById(`notif-${pk}`);
        if (item) {
          item.classList.remove('unread');
          btn.remove();
        }
        const badge = document.getElementById('notif-badge');
        if (badge) {
          const count = parseInt(badge.textContent) - 1;
          if (count <= 0) badge.style.display = 'none';
          else badge.textContent = count;
        }
      });
    });
  });

  // ── Date range filter: show/hide custom date inputs ───────────────────────
  const rangeSelect = document.getElementById('id_filter_range');
  const customRange = document.getElementById('custom-date-range');
  if (rangeSelect && customRange) {
    function toggleCustomRange() {
      customRange.style.display = rangeSelect.value === 'custom' ? 'flex' : 'none';
    }
    rangeSelect.addEventListener('change', toggleCustomRange);
    toggleCustomRange();
  }

  // ── Tooltip initialization ────────────────────────────────────────────────
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

  // ── Helper: get cookie value ──────────────────────────────────────────────
  function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
      c = c.trim();
      if (c.startsWith(name + '=')) return decodeURIComponent(c.slice(name.length + 1));
    }
    return '';
  }

});
