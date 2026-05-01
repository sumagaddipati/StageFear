/* auth.js — FINAL WORKING VERSION */

const API = '';

function switchTab(tab) {
document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
document.getElementById('tab-' + tab).classList.add('active');
document.getElementById(tab + '-form').classList.add('active');
}

// ---------------- LOGIN ----------------
async function handleLogin(e) {
e.preventDefault();

const btn = document.getElementById('login-btn');
const errEl = document.getElementById('login-error');

errEl.classList.add('hidden');

const username = document.getElementById('login-username').value.trim();
const password = document.getElementById('login-password').value;

btn.disabled = true;
btn.innerText = 'Signing in...';

try {
const formData = new FormData();
formData.append('username', username);
formData.append('password', password);

```
const res = await fetch(API + '/api/auth/login', {
  method: 'POST',
  body: formData
});

const data = await res.json();

if (!res.ok) throw new Error(data.detail || 'Login failed');

localStorage.setItem('sf_token', data.access_token);
localStorage.setItem('sf_username', data.username);

window.location.href = '/home';
```

} catch (err) {
errEl.innerText = err.message;
errEl.classList.remove('hidden');

```
btn.disabled = false;
btn.innerText = 'Sign In';
```

}
}

// ---------------- SIGNUP ----------------
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
errEl.innerText = 'Password must be at least 8 characters';
errEl.classList.remove('hidden');
return;
}

btn.disabled = true;
btn.innerText = 'Creating account...';

try {
const res = await fetch(API + '/api/auth/signup', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify(payload),
});

```
const data = await res.json();

if (!res.ok) throw new Error(data.detail || 'Signup failed');

localStorage.setItem('sf_token', data.access_token);
localStorage.setItem('sf_username', data.username);

window.location.href = '/home';
```

} catch (err) {
errEl.innerText = err.message;
errEl.classList.remove('hidden');

```
btn.disabled = false;
btn.innerText = 'Create Account';
```

}
}

// ---------------- PASSWORD TOGGLE ----------------
function togglePw(id) {
const input = document.getElementById(id);
input.type = input.type === 'password' ? 'text' : 'password';
}
