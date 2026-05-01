/* auth.js — Login / Signup logic */

const API = '';

// Check if already logged in
if (localStorage.getItem('sf_token')) {
  window.location.href = '/home';
}

function switchTab(tab) {
  document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
  document.getElementById('tab-' + tab).classList.add('active');
  document.getElementById(tab + '-form').classList.add('active');
}

async function handleLogin(e) {
  e.preventDefault();
  const btn = document.getElementById('login-btn');
  const errEl = document.getElementById('login-error');
  errEl.classList.add('hidden');

  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value;

  btn.disabled = true;
  btn.querySelector('span').textContent = 'Signing in...';

  try {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const res = await fetch(API + '/api/auth/login', { method: 'POST', body: formData });
    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || 'Login failed');

    localStorage.setItem('sf_token', data.access_token);
    localStorage.setItem('sf_username', data.username);
    window.location.href = '/home';
  } catch (err) {
    errEl.textContent = err.message;
    errEl.classList.remove('hidden');
    btn.disabled = false;
    btn.querySelector('span').textContent = 'Sign In';
  }
}

async function handleSignup(e) {
  e.preventDefault();
  const btn = document.getElementById('signup-btn');
  const errEl = document.getElementById('signup-error');
  errEl.classList.add('hidden');

  const payload = {
    username: document.getElementById('signup-username').value.trim(),
    email: document.getElementById('signup-email').value.trim(),
    password: document.getElementById('signup-password').value,
  };

  if (payload.password.length < 8) {
    errEl.textContent = 'Password must be at least 8 characters';
    errEl.classList.remove('hidden');
    return;
  }

  btn.disabled = true;
  btn.querySelector('span').textContent = 'Creating account...';

  try {
    const res = await fetch(API + '/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Signup failed');

    localStorage.setItem('sf_token', data.access_token);
    localStorage.setItem('sf_username', data.username);
    window.location.href = '/home';
  } catch (err) {
    errEl.textContent = err.message;
    errEl.classList.remove('hidden');
    btn.disabled = false;
    btn.querySelector('span').textContent = 'Create Account';
  }
}

function togglePw(id, btn) {
  const input = document.getElementById(id);
  input.type = input.type === 'password' ? 'text' : 'password';
}

function toggleTheme() {
  const html = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  html.setAttribute('data-theme', isDark ? 'light' : 'dark');
  localStorage.setItem('sf_theme', isDark ? 'light' : 'dark');
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