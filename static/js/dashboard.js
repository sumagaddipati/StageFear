/* dashboard.js */

const API = '';
const token = localStorage.getItem('sf_token');
if (!token) window.location.href = '/';

const headers = { 'Authorization': 'Bearer ' + token };

// Apply theme
const savedTheme = localStorage.getItem('sf_theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);
if (savedTheme === 'light') {
  document.getElementById('icon-moon').classList.add('hidden');
  document.getElementById('icon-sun').classList.remove('hidden');
}

function toggleTheme() {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
  localStorage.setItem('sf_theme', isDark ? 'light' : 'dark');
  document.getElementById('icon-moon').classList.toggle('hidden', !isDark);
  document.getElementById('icon-sun').classList.toggle('hidden', isDark);
  if (window._chart) {
    updateChartTheme();
  }
}

function logout() {
  localStorage.removeItem('sf_token');
  localStorage.removeItem('sf_username');
  window.location.href = '/';
}

function greeting() {
  const h = new Date().getHours();
  if (h < 12) return 'Good morning,';
  if (h < 17) return 'Good afternoon,';
  return 'Good evening,';
}

// ── Init ──────────────────────────────────────────────────────
async function init() {
  const username = localStorage.getItem('sf_username') || 'Speaker';
  document.getElementById('greeting').textContent = greeting();
  document.getElementById('username-display').textContent = username;

  // Load topic of day
  try {
    const res = await fetch(API + '/api/topics/today');
    const data = await res.json();
    document.getElementById('tod-text').textContent = data.text;
  } catch { document.getElementById('tod-text').textContent = 'Could not load'; }

  // Load stats and sessions in parallel
  const [statsRes, sessionsRes] = await Promise.all([
    fetch(API + '/api/stats', { headers }),
    fetch(API + '/api/sessions?limit=10', { headers }),
  ]);

  if (!statsRes.ok || !sessionsRes.ok) {
    if (statsRes.status === 401) { logout(); return; }
  }

  const stats = await statsRes.json();
  const sessions = await sessionsRes.json();

  renderStats(stats);
  renderChart(stats.score_trend || []);
  renderWeaknesses(stats.weaknesses || []);
  renderCategoryBars(stats.category_avg || {});
  renderSessions(sessions);
}

function renderStats(stats) {
  animateCount('stat-total', stats.total);
  animateCount('stat-avg', stats.avg_score);
  animateCount('stat-best', stats.best_score);
  animateCount('stat-wpm', stats.avg_wpm);
}

function animateCount(id, target) {
  const el = document.getElementById(id);
  if (!el) return;
  let current = 0;
  const step = target / 30;
  const interval = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = Math.round(current);
    if (current >= target) clearInterval(interval);
  }, 30);
}

let chartInstance = null;
function renderChart(trend) {
  const canvas = document.getElementById('progress-chart');
  const emptyEl = document.getElementById('empty-chart');

  if (!trend || trend.length === 0) {
    canvas.classList.add('hidden');
    emptyEl.classList.remove('hidden');
    return;
  }

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';
  const textColor = isDark ? '#615c72' : '#9994a6';

  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(canvas, {
    type: 'line',
    data: {
      labels: trend.map(t => t.date),
      datasets: [
        {
          label: 'Score',
          data: trend.map(t => t.score),
          borderColor: '#f0a500',
          backgroundColor: 'rgba(240,165,0,0.08)',
          borderWidth: 2.5,
          pointBackgroundColor: '#f0a500',
          pointRadius: 4,
          pointHoverRadius: 6,
          tension: 0.4,
          fill: true,
        },
        {
          label: 'WPM',
          data: trend.map(t => t.wpm),
          borderColor: '#60a5fa',
          backgroundColor: 'rgba(96,165,250,0.05)',
          borderWidth: 2,
          pointBackgroundColor: '#60a5fa',
          pointRadius: 3,
          pointHoverRadius: 5,
          tension: 0.4,
          fill: false,
          yAxisID: 'y1',
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { mode: 'index', intersect: false } },
      scales: {
        x: { grid: { color: gridColor }, ticks: { color: textColor, font: { size: 11 } } },
        y: {
          min: 0, max: 100,
          grid: { color: gridColor },
          ticks: { color: textColor, font: { size: 11 } },
        },
        y1: {
          position: 'right',
          grid: { display: false },
          ticks: { color: textColor, font: { size: 11 } },
        },
      },
    },
  });
  window._chart = chartInstance;
}

function updateChartTheme() {
  if (!chartInstance) return;
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';
  const textColor = isDark ? '#615c72' : '#9994a6';
  chartInstance.options.scales.x.grid.color = gridColor;
  chartInstance.options.scales.x.ticks.color = textColor;
  chartInstance.options.scales.y.grid.color = gridColor;
  chartInstance.options.scales.y.ticks.color = textColor;
  chartInstance.options.scales.y1.ticks.color = textColor;
  chartInstance.update();
}

function renderWeaknesses(weaknesses) {
  const container = document.getElementById('weaknesses-list');
  if (!weaknesses.length) {
    container.innerHTML = '<div class="empty-state" style="padding:20px"><p>Complete a few sessions to see your weak areas.</p></div>';
    return;
  }
  container.innerHTML = weaknesses.map(w => `
    <div class="weakness-item">
      <span class="weakness-label">${w.label}</span>
      <span class="weakness-score">${w.score}</span>
      <span class="weakness-tip">${w.tip}</span>
    </div>
  `).join('');
}

function renderCategoryBars(catAvg) {
  const container = document.getElementById('category-bars');
  if (!Object.keys(catAvg).length) {
    container.innerHTML = '<div class="empty-state" style="padding:20px"><p>No category data yet.</p></div>';
    return;
  }
  container.innerHTML = Object.entries(catAvg).map(([cat, score]) => `
    <div class="cat-bar-item">
      <div class="cat-bar-header">
        <span>${cat}</span>
        <span>${score}</span>
      </div>
      <div class="cat-bar">
        <div class="cat-bar-fill" style="width:${score}%"></div>
      </div>
    </div>
  `).join('');
}

function renderSessions(sessions) {
  const container = document.getElementById('sessions-list');
  if (!sessions.length) {
    container.innerHTML = `
      <div class="empty-state">
        <p>No sessions yet. Start your first practice!</p>
        <button class="btn-primary" onclick="window.location.href='/session'">Start Session</button>
      </div>`;
    return;
  }

  const CAT_ICONS = { Tech: '💻', Lifestyle: '🌿', Interview: '💼', Fun: '🎲', Abstract: '🔮' };

  container.innerHTML = sessions.map(s => {
    const scoreClass = s.overall_score >= 75 ? 'score-good' : s.overall_score >= 50 ? 'score-mid' : 'score-bad';
    const date = new Date(s.created_at).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' });
    return `
      <div class="session-row">
        <div>
          <div class="session-topic">${escapeHtml(s.topic)}</div>
          <div class="session-meta">${s.word_count} words · ${s.wpm} WPM · ${s.filler_count} fillers</div>
        </div>
        <div class="session-cat">${CAT_ICONS[s.category] || '📌'} ${s.category}</div>
        <div class="session-cat">${s.difficulty}</div>
        <div class="session-score ${scoreClass}">${Math.round(s.overall_score)}</div>
        <div class="session-date">${date}</div>
      </div>
    `;
  }).join('');
}

function escapeHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

init();