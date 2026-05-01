/* auth.js — REDIRECTS TO HOME (No auth needed) */

const API = '';

// Redirect directly to home - no authentication needed
window.location.href = '/home';
  document.getElementById('icon-moon').classList.toggle('hidden', !isDark);
  document.getElementById('icon-sun').classList.toggle('hidden', isDark);
}

// Apply saved theme
const savedTheme = localStorage.getItem('sf_theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);
if (savedTheme === 'light') {
  document.getElementById('icon-moon')?.classList.add('hidden');
  document.getElementById('icon-sun')?.classList.remove('hidden');
}