/* session.js — Full practice session controller */

const API = '';

// No authentication required - app is fully public
const AUTH = {};

// Apply theme
const savedTheme = localStorage.getItem('sf_theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);
if (savedTheme === 'light') {
  document.getElementById('icon-moon').classList.add('hidden');
  document.getElementById('icon-sun').classList.remove('hidden');
}

// ── State ─────────────────────────────────────────────────────
let state = {
  category: 'Tech',
  difficulty: 'Easy',
  topic: null,
  usedTopicIds: JSON.parse(localStorage.getItem('sf_used_topics') || '[]'),
  phase: 'topic', // topic | prep | speak | results
  prepTimer: null,
  speakTimer: null,
  prepRemaining: 60,
  speakRemaining: 60,
  paused: false,
  mediaRecorder: null,
  audioChunks: [],
  audioBlob: null,
  audioURL: null,
  analyzerNode: null,
  animFrame: null,
  silenceTimer: null,
  silenceThreshold: 20,
  speakDuration: 0,
};

// ── Utilities ─────────────────────────────────────────────────
function toggleTheme() {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
  localStorage.setItem('sf_theme', isDark ? 'light' : 'dark');
  document.getElementById('icon-moon').classList.toggle('hidden', !isDark);
  document.getElementById('icon-sun').classList.toggle('hidden', isDark);
}

function setPhase(name) {
  document.querySelectorAll('.phase').forEach(p => p.classList.remove('active'));
  document.getElementById('phase-' + name).classList.add('active');
  state.phase = name;
  updateSteps();
}

function updateSteps() {
  const phaseOrder = ['topic', 'prep', 'speak', 'results'];
  const idx = phaseOrder.indexOf(state.phase);
  for (let i = 1; i <= 4; i++) {
    const el = document.getElementById('step-' + i);
    el.classList.remove('active', 'done');
    if (i - 1 < idx) el.classList.add('done');
    else if (i - 1 === idx) el.classList.add('active');
  }
}

function selectChip(btn, type) {
  const parent = btn.closest('.chip-grid');
  parent.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  btn.classList.add('active');
  state[type] = btn.dataset.value;
}

// ── Topic Generation ──────────────────────────────────────────
async function generateTopic() {
  const btn = event.target.closest('button');
  btn.disabled = true;
  btn.textContent = '⏳ Generating...';

  try {
    const res = await fetch(API + '/api/topics/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        category: state.category,
        difficulty: state.difficulty,
        used_topic_ids: state.usedTopicIds,
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail);
    showTopic(data);
  } catch (err) {
    alert('Failed to generate topic: ' + err.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v1m0 16v1M4.22 4.22l.707.707m14.142 14.142.707.707M3 12h1m16 0h1M4.22 19.78l.707-.707M18.364 5.636l.707-.707"/><circle cx="12" cy="12" r="4"/></svg> Generate Topic`;
  }
}

async function surpriseTopic() {
  try {
    const res = await fetch(API + '/api/topics/surprise');
    const data = await res.json();
    // Update chips to match
    selectChipByValue('category', data.category);
    selectChipByValue('difficulty', data.difficulty);
    showTopic(data);
  } catch { alert('Failed to get surprise topic'); }
}

function selectChipByValue(type, value) {
  const grids = { category: 'category-chips', difficulty: 'difficulty-chips' };
  const parent = document.getElementById(grids[type]);
  if (!parent) return;
  parent.querySelectorAll('.chip').forEach(c => {
    c.classList.remove('active');
    if (c.dataset.value === value) { c.classList.add('active'); state[type] = value; }
  });
}

async function loadDailyTopic() {
  try {
    const res = await fetch(API + '/api/topics/today');
    const data = await res.json();
    document.getElementById('daily-text').textContent = data.text;
    window._dailyTopic = data;
  } catch { document.getElementById('daily-text').textContent = 'Could not load'; }
}

function useDailyTopic() {
  if (window._dailyTopic) showTopic(window._dailyTopic);
}

function showTopic(data) {
  state.topic = data;
  document.getElementById('topic-empty').classList.add('hidden');
  document.getElementById('topic-content').classList.remove('hidden');

  const ICONS = { Tech: '💻', Lifestyle: '🌿', Interview: '💼', Fun: '🎲', Abstract: '🔮', Mixed: '🌐' };
  document.getElementById('topic-meta').innerHTML = `
    <span>${ICONS[data.category] || '📌'} ${data.category}</span>
    <span>·</span>
    <span>${data.difficulty}</span>
  `;
  document.getElementById('topic-text').textContent = data.text;
  document.getElementById('topic-generated-tag').textContent = data.generated ? '⚡ AI Generated' : '📚 Curated Topic';

  // Animate card
  const card = document.getElementById('topic-card');
  card.style.animation = 'none';
  card.offsetHeight;
  card.style.animation = 'fadeSlide 0.4s ease';
}

// ── Prep Phase ────────────────────────────────────────────────
function startPrepPhase() {
  if (!state.topic) return;
  setPhase('prep');

  document.getElementById('prep-topic-banner').textContent = state.topic.text;

  // Add to used topics
  state.usedTopicIds.push(state.topic.id);
  localStorage.setItem('sf_used_topics', JSON.stringify(state.usedTopicIds.slice(-50)));

  state.prepRemaining = 60;
  updatePrepTimer();

  state.prepTimer = setInterval(() => {
    state.prepRemaining--;
    updatePrepTimer();
    if (state.prepRemaining <= 0) {
      clearInterval(state.prepTimer);
      startSpeakPhase();
    }
  }, 1000);
}

function updatePrepTimer() {
  document.getElementById('prep-count').textContent = state.prepRemaining;
  const circumference = 553;
  const offset = circumference - (circumference * (60 - state.prepRemaining) / 60);
  document.getElementById('prep-ring').style.strokeDashoffset = offset;
}

function skipPrep() {
  clearInterval(state.prepTimer);
  startSpeakPhase();
}

// ── Speaking Phase ────────────────────────────────────────────
async function startSpeakPhase() {
  setPhase('speak');
  document.getElementById('speak-topic-banner').textContent = state.topic.text;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    setupVisualizer(stream);
    startRecording(stream);
    startSpeakTimer();
  } catch (err) {
    alert('Microphone access denied. Please allow microphone access to record.');
    setPhase('topic');
  }
}

function setupVisualizer(stream) {
  const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  const source = audioCtx.createMediaStreamSource(stream);
  const analyser = audioCtx.createAnalyser();
  analyser.fftSize = 256;
  source.connect(analyser);
  state.analyzerNode = analyser;
  drawVisualizer();
  detectSilence();
}

function drawVisualizer() {
  const canvas = document.getElementById('audio-visualizer');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const analyser = state.analyzerNode;
  if (!analyser) return;

  const bufferLength = analyser.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

  function draw() {
    state.animFrame = requestAnimationFrame(draw);
    analyser.getByteFrequencyData(dataArray);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const barWidth = (canvas.width / bufferLength) * 2.5;
    let x = 0;
    for (let i = 0; i < bufferLength; i++) {
      const barHeight = (dataArray[i] / 255) * canvas.height;
      const alpha = 0.3 + (dataArray[i] / 255) * 0.7;
      ctx.fillStyle = `rgba(240, 165, 0, ${alpha})`;
      ctx.fillRect(x, canvas.height - barHeight, barWidth - 1, barHeight);
      x += barWidth + 1;
    }
  }
  draw();
}

function detectSilence() {
  const analyser = state.analyzerNode;
  if (!analyser) return;
  const dataArray = new Uint8Array(analyser.frequencyBinCount);
  let silentFrames = 0;

  const check = setInterval(() => {
    if (state.paused || !state.mediaRecorder) return;
    analyser.getByteFrequencyData(dataArray);
    const avg = dataArray.reduce((a, b) => a + b, 0) / dataArray.length;
    if (avg < state.silenceThreshold) {
      silentFrames++;
      if (silentFrames > 5) {
        document.getElementById('speak-silence-alert').classList.remove('hidden');
      }
    } else {
      silentFrames = 0;
      document.getElementById('speak-silence-alert').classList.add('hidden');
    }
  }, 1000);
  state.silenceTimer = check;
}

function startRecording(stream) {
  state.audioChunks = [];
  const options = { mimeType: 'audio/webm;codecs=opus' };
  try {
    state.mediaRecorder = new MediaRecorder(stream, options);
  } catch {
    state.mediaRecorder = new MediaRecorder(stream);
  }

  state.mediaRecorder.ondataavailable = e => {
    if (e.data.size > 0) state.audioChunks.push(e.data);
  };

  state.mediaRecorder.onstop = () => {
    const blob = new Blob(state.audioChunks, { type: 'audio/webm' });
    state.audioBlob = blob;
    state.audioURL = URL.createObjectURL(blob);
    stream.getTracks().forEach(t => t.stop());
    cancelAnimationFrame(state.animFrame);
    clearInterval(state.silenceTimer);
    analyzeRecording();
  };

  state.mediaRecorder.start(250);
}

function startSpeakTimer() {
  state.speakRemaining = 60;
  state.speakDuration = 0;
  updateSpeakTimer();

  state.speakTimer = setInterval(() => {
    if (state.paused) return;
    state.speakRemaining--;
    state.speakDuration++;
    updateSpeakTimer();
    if (state.speakRemaining <= 0) {
      clearInterval(state.speakTimer);
      stopRecording();
    }
  }, 1000);
}

function updateSpeakTimer() {
  document.getElementById('speak-count').textContent = state.speakRemaining;
  const circumference = 553;
  const offset = circumference * (1 - (60 - state.speakRemaining) / 60);
  document.getElementById('speak-ring').style.strokeDashoffset = offset;
}

function togglePause() {
  state.paused = !state.paused;
  const label = document.getElementById('pause-label');
  const pauseIcon = document.getElementById('pause-icon');
  const resumeIcon = document.getElementById('resume-icon');

  if (state.paused) {
    state.mediaRecorder?.pause();
    label.textContent = 'Resume';
    pauseIcon.classList.add('hidden');
    resumeIcon.classList.remove('hidden');
    document.getElementById('speak-label').textContent = 'PAUSED';
  } else {
    state.mediaRecorder?.resume();
    label.textContent = 'Pause';
    pauseIcon.classList.remove('hidden');
    resumeIcon.classList.add('hidden');
    document.getElementById('speak-label').textContent = 'REC';
  }
}

function stopRecording() {
  clearInterval(state.speakTimer);
  clearInterval(state.silenceTimer);
  if (state.mediaRecorder && state.mediaRecorder.state !== 'inactive') {
    state.mediaRecorder.stop();
  }
  setPhase('results');
}

// ── Analysis ──────────────────────────────────────────────────
const ANALYZING_STEPS = [
  'Transcribing audio...',
  'Counting filler words...',
  'Computing WPM...',
  'Scoring clarity & structure...',
  'Generating AI feedback...',
];

async function analyzeRecording() {
  document.getElementById('analyzing-overlay').style.display = 'flex';
  document.getElementById('results-content').classList.add('hidden');

  // Animate steps
  let stepIdx = 0;
  const stepInterval = setInterval(() => {
    document.getElementById('analyzing-step').textContent = ANALYZING_STEPS[Math.min(stepIdx++, ANALYZING_STEPS.length - 1)];
  }, 800);

  try {
    const formData = new FormData();
    formData.append('audio', state.audioBlob, 'recording.webm');
    formData.append('topic', state.topic.text);
    formData.append('category', state.topic.category || state.category);
    formData.append('difficulty', state.topic.difficulty || state.difficulty);
    formData.append('duration', String(state.speakDuration || 30));

    const res = await fetch(API + '/api/sessions/analyze', {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    clearInterval(stepInterval);

    if (!res.ok) throw new Error(data.detail || 'Analysis failed');

    window._lastResult = data;
    renderResults(data);
  } catch (err) {
    clearInterval(stepInterval);
    document.getElementById('analyzing-step').textContent = 'Error: ' + err.message;
    setTimeout(() => {
      document.getElementById('analyzing-overlay').style.display = 'none';
      document.getElementById('results-content').classList.remove('hidden');
    }, 2000);
  }
}

function renderResults(data) {
  document.getElementById('analyzing-overlay').style.display = 'none';
  document.getElementById('results-content').classList.remove('hidden');

  // Overall score ring
  const circumference = 327;
  const offset = circumference - (circumference * data.overall_score / 100);
  setTimeout(() => {
    document.getElementById('overall-ring').style.strokeDashoffset = offset;
  }, 100);
  document.getElementById('overall-score-num').textContent = Math.round(data.overall_score);

  // Grade
  const grade = data.overall_score >= 85 ? 'Excellent 🏆' :
    data.overall_score >= 70 ? 'Great 🎯' :
    data.overall_score >= 55 ? 'Good 📈' :
    data.overall_score >= 40 ? 'Fair 🔶' : 'Needs Work 💪';
  document.getElementById('score-grade').textContent = grade;

  // Sub scores
  setTimeout(() => {
    document.getElementById('conf-val').textContent = Math.round(data.confidence_score);
    document.getElementById('clar-val').textContent = Math.round(data.clarity_score);
    document.getElementById('struct-val').textContent = Math.round(data.structure_score);
    document.getElementById('conf-bar').style.width = data.confidence_score + '%';
    document.getElementById('clar-bar').style.width = data.clarity_score + '%';
    document.getElementById('struct-bar').style.width = data.structure_score + '%';
  }, 200);

  // Quick stats
  document.getElementById('stat-words').textContent = data.word_count;
  document.getElementById('stat-wpm-result').textContent = data.wpm;
  document.getElementById('stat-fillers').textContent = data.filler_count;

  // Transcript with highlights
  document.getElementById('transcript-body').innerHTML = data.highlighted_transcript || data.transcript || '(No transcript available)';

  // Audio playback
  if (state.audioURL) {
    const audio = document.getElementById('result-audio');
    audio.src = state.audioURL;
    document.getElementById('audio-playback').style.display = 'block';
  }

  // Feedback
  const feedbackList = document.getElementById('feedback-list');
  feedbackList.innerHTML = '';
  (data.feedback || []).forEach((item, i) => {
    const div = document.createElement('div');
    div.className = `feedback-item ${item.type}`;
    div.style.animationDelay = (i * 0.1) + 's';
    div.innerHTML = `
      <div class="feedback-title">${item.icon} ${item.title}</div>
      <div class="feedback-body">${item.body}</div>
    `;
    feedbackList.appendChild(div);
  });
}

// ── Export PDF ────────────────────────────────────────────────
function exportReport() {
  const data = window._lastResult;
  if (!data) return;

  const html = `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>StageFear Breaker — Session Report</title>
<style>
  body { font-family: Georgia, serif; max-width: 700px; margin: 40px auto; color: #1a1a1a; }
  h1 { font-size: 2rem; border-bottom: 3px solid #f0a500; padding-bottom: 12px; }
  h2 { font-size: 1.2rem; color: #555; margin-top: 28px; }
  .score-row { display: flex; gap: 24px; margin: 20px 0; }
  .score-box { background: #f8f7fb; border-radius: 8px; padding: 16px 24px; text-align: center; flex: 1; }
  .score-box .val { font-size: 2rem; font-weight: bold; color: #f0a500; }
  .score-box .lbl { font-size: 0.8rem; color: #888; }
  .feedback-item { margin: 10px 0; padding: 12px; background: #f8f7fb; border-left: 3px solid #f0a500; }
  .feedback-title { font-weight: bold; }
  .transcript { background: #f8f7fb; padding: 20px; border-radius: 8px; line-height: 1.8; }
  mark { background: #fff3cd; padding: 1px 3px; }
  footer { margin-top: 40px; color: #888; font-size: 0.8rem; text-align: center; }
</style>
</head><body>
<h1>🎤 StageFear Breaker — Session Report</h1>
<p><strong>Topic:</strong> ${escapeHtmlStr(state.topic?.text || '')}</p>
<p><strong>Category:</strong> ${state.topic?.category} · <strong>Difficulty:</strong> ${state.topic?.difficulty}</p>
<p><strong>Date:</strong> ${new Date().toLocaleDateString()}</p>

<div class="score-row">
  <div class="score-box"><div class="val">${Math.round(data.overall_score)}</div><div class="lbl">Overall Score</div></div>
  <div class="score-box"><div class="val">${Math.round(data.confidence_score)}</div><div class="lbl">Confidence</div></div>
  <div class="score-box"><div class="val">${Math.round(data.clarity_score)}</div><div class="lbl">Clarity</div></div>
  <div class="score-box"><div class="val">${Math.round(data.structure_score)}</div><div class="lbl">Structure</div></div>
</div>

<div class="score-row">
  <div class="score-box"><div class="val">${data.word_count}</div><div class="lbl">Words</div></div>
  <div class="score-box"><div class="val">${data.wpm}</div><div class="lbl">WPM</div></div>
  <div class="score-box"><div class="val">${data.filler_count}</div><div class="lbl">Filler Words</div></div>
</div>

<h2>📝 Transcript</h2>
<div class="transcript">${data.highlighted_transcript || data.transcript}</div>

<h2>🧠 AI Coach Feedback</h2>
${(data.feedback || []).map(f => `
  <div class="feedback-item">
    <div class="feedback-title">${f.icon} ${f.title}</div>
    <div>${f.body}</div>
  </div>
`).join('')}

<footer>Generated by StageFear Breaker · ${new Date().toISOString()}</footer>
</body></html>`;

  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'stagefear-report-' + Date.now() + '.html';
  a.click();
  URL.revokeObjectURL(url);
}

function escapeHtmlStr(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

function startNewSession() {
  // Reset state
  state.topic = null;
  state.audioBlob = null;
  state.audioURL = null;
  state.paused = false;
  document.getElementById('topic-empty').classList.remove('hidden');
  document.getElementById('topic-content').classList.add('hidden');
  setPhase('topic');
}

// ── Init ──────────────────────────────────────────────────────
loadDailyTopic();
setPhase('topic');