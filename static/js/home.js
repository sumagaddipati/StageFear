// ============================================
// NO AUTHENTICATION REQUIRED
// ============================================

// All users can access this page directly

// ============================================
// 30 MOTIVATIONAL QUOTES
// ============================================

const quotes = [
    '"Your voice matters."',
    '"Confidence comes from practice."',
    '"Speak even if your voice shakes."',
    '"Start before you\'re ready."',
    '"Fear fades with action."',
    '"Every expert was once a beginner."',
    '"Progress over perfection."',
    '"Your story deserves to be told."',
    '"Clarity beats perfection."',
    '"Confidence is built, not born."',
    '"Speak slowly, think clearly."',
    '"You have something valuable to say."',
    '"Growth comes from discomfort."',
    '"Practice is the path to confidence."',
    '"Your words have power."',
    '"Silence is a choice; speak with purpose."',
    '"Be heard. Be bold. Be you."',
    '"Small steps lead to big changes."',
    '"Consistency is your superpower."',
    '"Your voice is your strength."',
    '"Fear is temporary; impact is lasting."',
    '"Speak from the heart."',
    '"Confidence is a skill, not a gift."',
    '"Every mistake is a lesson."',
    '"You are ready. Start now."',
    '"Speaking well is speaking often."',
    '"Embrace the nervousness; it means you care."',
    '"Your potential is limitless."',
    '"Transform fear into fuel."',
    '"Today is your day to shine."'
];

// ============================================
// TOPICS FOR THE DAY
// ============================================

const dailyTopics = [
    "The impact of artificial intelligence on society",
    "What does success mean to you?",
    "Is social media beneficial or harmful?",
    "The importance of continuous learning",
    "How to overcome self-doubt",
    "The future of remote work",
    "Why communication skills matter in your career",
    "The role of failure in personal growth",
    "Building meaningful relationships",
    "How to lead effectively in uncertain times",
    "The power of storytelling in business",
    "Why mental health should be a priority",
    "The impact of technology on human connection",
    "How to stay motivated through challenges",
    "The importance of diversity and inclusion",
    "Ways to develop emotional intelligence",
    "The art of active listening",
    "How to present ideas with confidence",
    "The benefits of public speaking practice",
    "Building a personal brand in the digital age",
    "The role of creativity in problem-solving",
    "How to handle criticism constructively",
    "The importance of time management",
    "Building trust in professional relationships",
    "The power of positive thinking",
    "How to overcome imposter syndrome",
    "The art of negotiation",
    "The importance of work-life balance",
    "How to inspire and motivate others",
    "The journey of personal transformation"
];

// ============================================
// FUNCTIONS
// ============================================

/**
 * Initialize page on load
 */
function initializePage() {
    loadTopicOfTheDay();
    loadNewQuote();
}

/**
 * Load Topic of the Day based on current date
 */
function loadTopicOfTheDay() {
    const dayOfMonth = new Date().getDate();
    const topicIndex = dayOfMonth % dailyTopics.length;
    const topic = dailyTopics[topicIndex];
    
    const topicElement = document.getElementById('topicContent');
    if (topicElement) {
        topicElement.innerText = topic;
    }
}

/**
 * Load random quote
 */
function loadNewQuote() {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    const quote = quotes[randomIndex];
    
    const quoteElement = document.getElementById('quoteText');
    if (quoteElement) {
        quoteElement.innerText = quote;
        // Add subtle animation on load
        quoteElement.style.opacity = '0.7';
        setTimeout(() => {
            quoteElement.style.opacity = '1';
        }, 100);
    }
}

/**
 * Navigate to specified page
 */
function navigateTo(path) {
    window.location.href = path;
}

/**
 * Logout user
 */
function logout() {
  // No authentication to clear - just redirect home
  window.location.href = '/home';
}

// ============================================
// INITIALIZE ON PAGE LOAD
// ============================================

document.addEventListener('DOMContentLoaded', initializePage);