import random
from datetime import datetime, date

TOPICS_DB = {
    "Tech": {
        "Easy": [
            {"id": "T-E-001", "text": "How has your smartphone changed your daily life?"},
            {"id": "T-E-002", "text": "What is the internet and why does it matter?"},
            {"id": "T-E-003", "text": "Describe a technology you couldn't live without"},
            {"id": "T-E-004", "text": "How do social media apps affect our attention spans?"},
            {"id": "T-E-005", "text": "Should kids learn coding in elementary school?"},
            {"id": "T-E-006", "text": "What is your favorite app and why?"},
            {"id": "T-E-007", "text": "How has video calling changed remote work?"},
            {"id": "T-E-008", "text": "What makes a website easy to use?"},
            {"id": "T-E-009", "text": "How do search engines find information?"},
            {"id": "T-E-010", "text": "What is cloud storage and why should you use it?"},
        ],
        "Medium": [
            {"id": "T-M-001", "text": "How is artificial intelligence reshaping the job market?"},
            {"id": "T-M-002", "text": "Are we becoming too dependent on technology?"},
            {"id": "T-M-003", "text": "Should social media companies be held responsible for misinformation?"},
            {"id": "T-M-004", "text": "How does machine learning differ from traditional programming?"},
            {"id": "T-M-005", "text": "What role should government play in regulating big tech?"},
            {"id": "T-M-006", "text": "How is blockchain technology beyond just cryptocurrency?"},
            {"id": "T-M-007", "text": "The impact of 5G on everyday life"},
            {"id": "T-M-008", "text": "How does open source software benefit society?"},
            {"id": "T-M-009", "text": "Should autonomous vehicles be allowed on public roads?"},
            {"id": "T-M-010", "text": "What are the biggest cybersecurity threats today?"},
            {"id": "T-M-011", "text": "How AR and VR are transforming education"},
            {"id": "T-M-012", "text": "Is remote work technology enabling or isolating us?"},
        ],
        "Hard": [
            {"id": "T-H-001", "text": "Argue for or against AGI being achievable within 20 years"},
            {"id": "T-H-002", "text": "The ethical implications of neural interfaces like Neuralink"},
            {"id": "T-H-003", "text": "How quantum computing will disrupt current encryption standards"},
            {"id": "T-H-004", "text": "Should AI systems have legal personhood?"},
            {"id": "T-H-005", "text": "The geopolitical implications of semiconductor supply chains"},
            {"id": "T-H-006", "text": "How does algorithmic bias perpetuate systemic inequality?"},
            {"id": "T-H-007", "text": "The case for and against techno-solutionism"},
            {"id": "T-H-008", "text": "How surveillance capitalism undermines democratic institutions"},
            {"id": "T-H-009", "text": "Comparing federated learning vs centralized AI training models"},
            {"id": "T-H-010", "text": "The societal cost of planned obsolescence in consumer electronics"},
        ],
    },
    "Lifestyle": {
        "Easy": [
            {"id": "L-E-001", "text": "What is your morning routine and why does it matter?"},
            {"id": "L-E-002", "text": "How do you stay motivated when working from home?"},
            {"id": "L-E-003", "text": "Describe your ideal vacation and why"},
            {"id": "L-E-004", "text": "What hobby have you picked up recently?"},
            {"id": "L-E-005", "text": "How important is sleep for your daily performance?"},
            {"id": "L-E-006", "text": "What does a healthy breakfast look like to you?"},
            {"id": "L-E-007", "text": "How do you unplug from screens after work?"},
            {"id": "L-E-008", "text": "What book recently changed your perspective?"},
            {"id": "L-E-009", "text": "How do you practice gratitude daily?"},
            {"id": "L-E-010", "text": "Describe a simple habit that made a big difference in your life"},
        ],
        "Medium": [
            {"id": "L-M-001", "text": "How do you balance ambition and contentment?"},
            {"id": "L-M-002", "text": "What does minimalism mean to you?"},
            {"id": "L-M-003", "text": "How does environment affect your productivity?"},
            {"id": "L-M-004", "text": "The relationship between physical health and mental clarity"},
            {"id": "L-M-005", "text": "How has social comparison culture affected mental health?"},
            {"id": "L-M-006", "text": "Is hustle culture sustainable or harmful?"},
            {"id": "L-M-007", "text": "What is the role of community in personal wellbeing?"},
            {"id": "L-M-008", "text": "How do you define success beyond money?"},
            {"id": "L-M-009", "text": "The impact of food choices on cognitive performance"},
            {"id": "L-M-010", "text": "How do you cope with uncertainty and change?"},
            {"id": "L-M-011", "text": "Digital detox: necessary or overrated?"},
            {"id": "L-M-012", "text": "How journaling can accelerate personal growth"},
        ],
        "Hard": [
            {"id": "L-H-001", "text": "Is the pursuit of happiness a flawed life goal?"},
            {"id": "L-H-002", "text": "How do cultural norms shape our concept of self?"},
            {"id": "L-H-003", "text": "The paradox of choice in modern consumer lifestyle"},
            {"id": "L-H-004", "text": "How do we separate identity from productivity?"},
            {"id": "L-H-005", "text": "Is radical authenticity possible in a social media world?"},
            {"id": "L-H-006", "text": "The philosophy of slow living vs the efficiency imperative"},
            {"id": "L-H-007", "text": "How does consumerism fill an existential void?"},
            {"id": "L-H-008", "text": "What does it mean to live a meaningful life in the 21st century?"},
        ],
    },
    "Interview": {
        "Easy": [
            {"id": "I-E-001", "text": "Tell me about yourself in 60 seconds"},
            {"id": "I-E-002", "text": "What are your top 3 strengths?"},
            {"id": "I-E-003", "text": "Why are you interested in this role?"},
            {"id": "I-E-004", "text": "Where do you see yourself in 5 years?"},
            {"id": "I-E-005", "text": "Describe a challenge you overcame at work"},
            {"id": "I-E-006", "text": "What motivates you professionally?"},
            {"id": "I-E-007", "text": "How do you handle constructive criticism?"},
            {"id": "I-E-008", "text": "Tell me about a time you worked in a team"},
            {"id": "I-E-009", "text": "What is your greatest professional achievement?"},
            {"id": "I-E-010", "text": "Why are you leaving your current position?"},
        ],
        "Medium": [
            {"id": "I-M-001", "text": "Describe a situation where you had to lead without authority"},
            {"id": "I-M-002", "text": "Tell me about a time you failed and what you learned"},
            {"id": "I-M-003", "text": "How do you prioritize tasks when everything is urgent?"},
            {"id": "I-M-004", "text": "Describe a time you disagreed with your manager"},
            {"id": "I-M-005", "text": "How do you handle ambiguity in a project?"},
            {"id": "I-M-006", "text": "What is your approach to building relationships with stakeholders?"},
            {"id": "I-M-007", "text": "Tell me about a time you had to learn something quickly"},
            {"id": "I-M-008", "text": "How do you measure success in your work?"},
            {"id": "I-M-009", "text": "Describe your problem-solving process with a real example"},
            {"id": "I-M-010", "text": "How do you give feedback to peers who are underperforming?"},
        ],
        "Hard": [
            {"id": "I-H-001", "text": "Pitch yourself in 90 seconds for a role you've never done"},
            {"id": "I-H-002", "text": "If you were CEO for a day, what would you change about this company?"},
            {"id": "I-H-003", "text": "How would you turn around a failing team?"},
            {"id": "I-H-004", "text": "Describe the biggest strategic mistake you've ever made"},
            {"id": "I-H-005", "text": "How do you navigate politics in large organizations?"},
            {"id": "I-H-006", "text": "What would you do in your first 90 days to prove your value?"},
            {"id": "I-H-007", "text": "How do you lead through a crisis when the path is unclear?"},
            {"id": "I-H-008", "text": "Make the case for a controversial decision you've had to defend"},
        ],
    },
    "Fun": [
        {"id": "F-001", "text": "If you could have dinner with any historical figure, who and why?"},
        {"id": "F-002", "text": "What superpower would you choose and how would you use it?"},
        {"id": "F-003", "text": "Design your perfect day from start to finish"},
        {"id": "F-004", "text": "If you could live in any TV show universe, which would it be?"},
        {"id": "F-005", "text": "What would you do if you won 100 crores tomorrow?"},
        {"id": "F-006", "text": "If animals could talk, which would be the rudest?"},
        {"id": "F-007", "text": "What's the most underrated food and why?"},
        {"id": "F-008", "text": "If you could time travel, where and when would you go?"},
        {"id": "F-009", "text": "Design a new Olympic sport and explain the rules"},
        {"id": "F-010", "text": "What would your autobiography title be?"},
        {"id": "F-011", "text": "If you could swap lives with any celebrity for a week, who?"},
        {"id": "F-012", "text": "What is the most useful skill no one teaches in school?"},
        {"id": "F-013", "text": "If Earth had a second moon, how would life be different?"},
        {"id": "F-014", "text": "What would you invent to solve your biggest daily annoyance?"},
        {"id": "F-015", "text": "If you were a character in a video game, what would your stats be?"},
        {"id": "F-016", "text": "Explain the plot of your favorite movie as if it were a business pitch"},
        {"id": "F-017", "text": "What is the most important thing you own and why?"},
        {"id": "F-018", "text": "If you could add one rule to society, what would it be?"},
        {"id": "F-019", "text": "Describe the best meal you ever had"},
        {"id": "F-020", "text": "What would the world look like if everyone told the truth?"},
    ],
    "Abstract": [
        {"id": "A-001", "text": "Is free will real or an illusion we need to function?"},
        {"id": "A-002", "text": "What does justice truly mean?"},
        {"id": "A-003", "text": "Can something be beautiful without being seen?"},
        {"id": "A-004", "text": "Is boredom a problem or a gift?"},
        {"id": "A-005", "text": "What is the relationship between language and thought?"},
        {"id": "A-006", "text": "Does art have inherent meaning or is it audience-defined?"},
        {"id": "A-007", "text": "Is it possible to be truly objective?"},
        {"id": "A-008", "text": "What makes a life well-lived?"},
        {"id": "A-009", "text": "Is progress inevitable or just a narrative we tell ourselves?"},
        {"id": "A-010", "text": "What would it mean for humanity to 'succeed'?"},
        {"id": "A-011", "text": "Can you be loyal to someone you deeply disagree with?"},
        {"id": "A-012", "text": "Is silence a form of communication?"},
        {"id": "A-013", "text": "What is the difference between knowledge and wisdom?"},
        {"id": "A-014", "text": "Is change always growth?"},
        {"id": "A-015", "text": "What does it mean to belong somewhere?"},
        {"id": "A-016", "text": "Can we ever truly understand another person's experience?"},
        {"id": "A-017", "text": "What is the cost of certainty?"},
        {"id": "A-018", "text": "Is hope rational?"},
        {"id": "A-019", "text": "What would a truly fair society look like?"},
        {"id": "A-020", "text": "Can creativity be taught, or only cultivated?"},
    ],
}

DYNAMIC_TEMPLATES = {
    "Tech": [
        "Discuss the impact of {tech} on {domain}",
        "Should {tech} be regulated by governments?",
        "How will {tech} change {domain} in the next decade?",
        "The ethical dilemmas of {tech}",
        "Why {tech} is both a solution and a problem",
    ],
    "Lifestyle": [
        "How {habit} affects your {outcome}",
        "The hidden cost of {lifestyle_choice}",
        "Why {lifestyle_value} matters more than ever",
        "Redefining {concept} in the modern world",
    ],
    "Interview": [
        "Describe a time you used {skill} to solve a {challenge}",
        "How would you approach {scenario} in your first week?",
        "What does {quality} mean to you professionally?",
    ],
    "Abstract": [
        "Is {concept} a human invention or a discovery?",
        "What would the world look like without {concept}?",
        "Can {concept} and {concept2} coexist?",
        "The paradox of {concept}",
    ],
    "Fun": [
        "If {silly_thing} were a sport, what would the rules be?",
        "Design the perfect {thing}",
        "What if {hypothetical}?",
    ],
}

FILL_VALUES = {
    "tech": ["AI", "blockchain", "quantum computing", "AR/VR", "5G", "biometrics", "robotics", "IoT", "edge computing", "generative AI"],
    "domain": ["healthcare", "education", "finance", "agriculture", "transportation", "entertainment", "governance"],
    "habit": ["meditation", "journaling", "cold showers", "intermittent fasting", "daily exercise", "reading 30 minutes"],
    "outcome": ["mental clarity", "productivity", "creativity", "relationships", "career growth"],
    "lifestyle_choice": ["remote work", "minimalism", "veganism", "constant connectivity", "hustle culture"],
    "lifestyle_value": ["solitude", "community", "rest", "curiosity", "vulnerability"],
    "concept": ["time", "freedom", "identity", "truth", "power", "beauty", "memory", "fairness", "love", "success"],
    "concept2": ["order", "chaos", "tradition", "progress", "individualism", "collectivism"],
    "skill": ["data analysis", "communication", "critical thinking", "empathy", "negotiation", "storytelling"],
    "challenge": ["conflict", "tight deadline", "budget cut", "team misalignment", "technical failure"],
    "quality": ["leadership", "integrity", "resilience", "adaptability", "ownership"],
    "scenario": ["a legacy system migration", "a team in conflict", "an unclear product brief", "a client emergency"],
    "silly_thing": ["procrastination", "overthinking", "scrolling social media", "napping", "making excuses"],
    "thing": ["city", "school day", "workweek", "meeting", "social network"],
    "hypothetical": ["gravity worked sideways", "everyone could read minds", "money didn't exist", "sleep was optional"],
}


def _generate_dynamic_topic(category: str, difficulty: str) -> dict:
    templates = DYNAMIC_TEMPLATES.get(category, DYNAMIC_TEMPLATES["Abstract"])
    template = random.choice(templates)

    result = template
    for key, values in FILL_VALUES.items():
        if "{" + key + "}" in result:
            result = result.replace("{" + key + "}", random.choice(values))

    # Fill any remaining placeholders
    import re
    leftovers = re.findall(r"\{(\w+)\}", result)
    for lo in leftovers:
        result = result.replace("{" + lo + "}", random.choice(["innovation", "change", "growth"]))

    topic_id = f"DYN-{category[:2]}-{random.randint(10000, 99999)}"
    return {"id": topic_id, "text": result, "category": category, "difficulty": difficulty, "generated": True}


def get_topic(category: str, difficulty: str, used_ids: list) -> dict:
    use_dynamic = random.random() < 0.30  # 30% dynamic

    # Special handling for Fun/Abstract (no difficulty sub-keys)
    if category in ("Fun", "Abstract"):
        pool = TOPICS_DB.get(category, [])
        available = [t for t in pool if t["id"] not in used_ids]
        if not available or use_dynamic:
            return _generate_dynamic_topic(category, difficulty)
        topic = random.choice(available)
        return {**topic, "category": category, "difficulty": difficulty, "generated": False}

    pool_by_diff = TOPICS_DB.get(category, {}).get(difficulty, [])
    available = [t for t in pool_by_diff if t["id"] not in used_ids]

    if not available or use_dynamic:
        return _generate_dynamic_topic(category, difficulty)

    topic = random.choice(available)
    return {**topic, "category": category, "difficulty": difficulty, "generated": False}


def get_topic_of_day() -> dict:
    today = date.today()
    seed = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    all_topics = []
    for cat, val in TOPICS_DB.items():
        if isinstance(val, list):
            all_topics.extend(val)
        else:
            for diff, topics in val.items():
                all_topics.extend(topics)
    topic = random.choice(all_topics)
    random.seed()  # reset seed
    return {**topic, "category": "Mixed", "difficulty": "Mixed", "is_daily": True}