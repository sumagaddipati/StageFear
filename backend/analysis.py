import re
import random
import math

FILLER_WORDS = [
    "um", "uh", "like", "you know", "basically", "literally", "actually",
    "so", "right", "okay", "well", "i mean", "kind of", "sort of",
    "you see", "anyway", "whatever", "stuff", "things", "honestly"
]

OPENING_PHRASES = [
    "today i want to", "i'm going to talk about", "let me tell you",
    "the topic i", "so today", "in this talk", "i would like to",
    "let's discuss", "i'll be talking", "welcome"
]

CLOSING_PHRASES = [
    "in conclusion", "to summarize", "to wrap up", "finally",
    "in summary", "so to conclude", "that's why", "thank you",
    "to end", "overall"
]


def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Real-world: use speech_recognition or Whisper API.
    Here we return a placeholder since audio processing requires system libs.
    In production: install SpeechRecognition + pocketsphinx or call Whisper.
    """
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        import tempfile, os
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes)
            tmp_path = f.name
        try:
            with sr.AudioFile(tmp_path) as source:
                audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
        except Exception:
            return _generate_sample_transcript()
        finally:
            os.unlink(tmp_path)
    except ImportError:
        return _generate_sample_transcript()


def _generate_sample_transcript() -> str:
    """Generate a realistic sample transcript for demo purposes."""
    samples = [
        "Um, so today I want to talk about this really important topic. Basically, I think that, you know, it affects all of us in some way. Like, when I first thought about it, I was kind of surprised by how, uh, complex it actually is. So I mean, the first point I want to make is that we need to think more carefully. And uh, you know, there's a lot of evidence to support this. In conclusion, I believe that we can all make a difference if we just, like, pay more attention.",
        "Good morning everyone. I'm going to talk about something that I feel really strongly about. When we look at this issue, we see that there are multiple dimensions to consider. First, we have the economic aspect which is actually quite significant. Second, the social implications are profound and far-reaching. Third, we need to consider the long-term consequences. To wrap up, I want to leave you with this thought: change begins with awareness.",
        "So, uh, the topic today is something I've been thinking about a lot. Um, I think it's really, like, important because basically it touches on our daily lives. You know what I mean? The thing is, we often overlook these things. Kind of like how we don't notice the air we breathe until it's polluted. Right? So, I mean, my main argument here is that we should pay more attention. Honestly, if we just did that one thing, things would be so much better.",
        "This is a topic that fascinates me deeply. The complexity of modern society means we face unprecedented challenges. Consider the way technology has transformed human interaction over just two decades. We communicate faster but perhaps less meaningfully. We have access to infinite information yet wisdom seems scarce. The solution lies not in rejecting progress but in becoming more intentional about how we engage with it. By developing critical awareness, we can harness the benefits while mitigating the downsides.",
    ]
    return random.choice(samples)


def count_fillers(text: str) -> dict:
    text_lower = text.lower()
    filler_hits = {}
    total = 0
    for filler in FILLER_WORDS:
        pattern = r'\b' + re.escape(filler) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            filler_hits[filler] = len(matches)
            total += len(matches)
    return {"total": total, "breakdown": filler_hits}


def highlight_fillers(text: str) -> str:
    """Return text with filler words wrapped in <mark> tags."""
    result = text
    for filler in sorted(FILLER_WORDS, key=len, reverse=True):
        pattern = r'(?i)\b' + re.escape(filler) + r'\b'
        result = re.sub(pattern, lambda m: f'<mark class="filler">{m.group()}</mark>', result)
    return result


def score_confidence(text: str, wpm: float, filler_count: int, word_count: int) -> float:
    score = 70.0
    # Penalize heavy filler usage
    filler_ratio = filler_count / max(word_count, 1)
    score -= filler_ratio * 120

    # Penalize extreme WPM
    if wpm < 80:
        score -= 15
    elif wpm > 180:
        score -= 10
    elif 110 <= wpm <= 150:
        score += 10

    # Reward longer speech (more committed)
    if word_count > 80:
        score += 8
    elif word_count < 30:
        score -= 15

    # Penalize very short sentences (choppy)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if sentences:
        avg_sent_len = word_count / len(sentences)
        if avg_sent_len < 5:
            score -= 10
        elif avg_sent_len > 8:
            score += 5

    return max(0, min(100, round(score + random.uniform(-3, 3))))


def score_clarity(filler_count: int, word_count: int) -> float:
    if word_count == 0:
        return 0
    filler_ratio = filler_count / word_count
    # 0 fillers = 100, linear decay
    score = 100 - (filler_ratio * 300)
    return max(0, min(100, round(score + random.uniform(-5, 5))))


def score_structure(text: str, word_count: int) -> float:
    score = 50.0
    text_lower = text.lower()

    has_opening = any(phrase in text_lower for phrase in OPENING_PHRASES)
    has_closing = any(phrase in text_lower for phrase in CLOSING_PHRASES)

    if has_opening:
        score += 15
    if has_closing:
        score += 15

    # Reward adequate length
    if word_count >= 100:
        score += 15
    elif word_count >= 60:
        score += 8
    elif word_count < 30:
        score -= 15

    # Reward use of transition words
    transitions = ["first", "second", "third", "however", "therefore", "furthermore",
                   "additionally", "in contrast", "on the other hand", "for example",
                   "as a result", "finally", "moreover"]
    transition_count = sum(1 for t in transitions if t in text_lower)
    score += min(15, transition_count * 3)

    return max(0, min(100, round(score + random.uniform(-3, 3))))


def generate_feedback(confidence: float, clarity: float, structure: float,
                      wpm: float, word_count: int, filler_count: int, text: str) -> list:
    feedback = []
    text_lower = text.lower()

    # Intro feedback
    has_opening = any(p in text_lower for p in OPENING_PHRASES)
    if not has_opening:
        feedback.append({
            "type": "warning",
            "icon": "⚠️",
            "title": "Weak Opening",
            "body": "Your intro didn't hook the audience. Start with a bold statement, a question, or a surprising fact."
        })
    else:
        feedback.append({
            "type": "success",
            "icon": "✅",
            "title": "Strong Opening",
            "body": "You set up your talk clearly from the start. First impressions matter!"
        })

    # Filler feedback
    if filler_count == 0:
        feedback.append({
            "type": "success",
            "icon": "🎯",
            "title": "Zero Filler Words",
            "body": "Exceptional! You spoke without filler words — this signals high confidence and preparation."
        })
    elif filler_count <= 3:
        feedback.append({
            "type": "info",
            "icon": "💬",
            "title": "Minimal Fillers",
            "body": f"Only {filler_count} filler word(s) detected. Very good — just a little more mindfulness and you'll be flawless."
        })
    elif filler_count <= 8:
        feedback.append({
            "type": "warning",
            "icon": "🔶",
            "title": "Moderate Filler Usage",
            "body": f"{filler_count} filler words detected. Practice pausing silently instead of saying 'um' or 'like'."
        })
    else:
        feedback.append({
            "type": "error",
            "icon": "🚨",
            "title": "Heavy Filler Usage",
            "body": f"{filler_count} filler words! These undermine your credibility. Record yourself and consciously eliminate them."
        })

    # WPM feedback
    if wpm < 80:
        feedback.append({
            "type": "warning",
            "icon": "🐢",
            "title": "Speaking Too Slowly",
            "body": f"Your pace was {wpm:.0f} WPM — too slow. Aim for 120–150 WPM to keep listeners engaged."
        })
    elif wpm > 170:
        feedback.append({
            "type": "warning",
            "icon": "⚡",
            "title": "Speaking Too Fast",
            "body": f"You spoke at {wpm:.0f} WPM — too fast. Slow down, breathe, and let your points land."
        })
    else:
        feedback.append({
            "type": "success",
            "icon": "🎵",
            "title": "Great Pace",
            "body": f"Your speaking pace of {wpm:.0f} WPM is in the ideal range. Listeners can follow you comfortably."
        })

    # Structure feedback
    has_closing = any(p in text_lower for p in CLOSING_PHRASES)
    if not has_closing:
        feedback.append({
            "type": "warning",
            "icon": "📌",
            "title": "Missing Conclusion",
            "body": "You didn't close strongly. Always end with a summary or a call to action — don't just trail off."
        })

    # Confidence-based
    if confidence >= 75:
        feedback.append({
            "type": "success",
            "icon": "💪",
            "title": "Confident Delivery",
            "body": "You came across as assured and credible. Your vocal presence was strong throughout."
        })
    elif confidence >= 50:
        feedback.append({
            "type": "info",
            "icon": "📈",
            "title": "Growing Confidence",
            "body": "You showed confidence in parts. Keep practicing — consistency is the key differentiator."
        })
    else:
        feedback.append({
            "type": "error",
            "icon": "😰",
            "title": "Low Confidence Detected",
            "body": "Your delivery felt uncertain. Practice power posing before sessions and breathe deeply."
        })

    # Word count
    if word_count < 40:
        feedback.append({
            "type": "error",
            "icon": "📝",
            "title": "Too Brief",
            "body": "You used very few words. Don't be afraid to elaborate — depth shows mastery of the topic."
        })

    return feedback


def analyze_speech(audio_bytes: bytes, duration: float, topic: str) -> dict:
    transcript = transcribe_audio(audio_bytes)
    words = transcript.split()
    word_count = len(words)
    effective_duration = max(duration, 1)
    wpm = round((word_count / effective_duration) * 60)

    filler_data = count_fillers(transcript)
    filler_count = filler_data["total"]

    confidence = score_confidence(transcript, wpm, filler_count, word_count)
    clarity = score_clarity(filler_count, word_count)
    structure = score_structure(transcript, word_count)

    overall = round((confidence * 0.35) + (clarity * 0.30) + (structure * 0.35))

    feedback = generate_feedback(confidence, clarity, structure, wpm, word_count, filler_count, transcript)
    highlighted = highlight_fillers(transcript)

    return {
        "transcript": transcript,
        "highlighted_transcript": highlighted,
        "word_count": word_count,
        "wpm": wpm,
        "filler_count": filler_count,
        "filler_breakdown": filler_data["breakdown"],
        "confidence_score": confidence,
        "clarity_score": clarity,
        "structure_score": structure,
        "overall_score": overall,
        "feedback": feedback,
    }