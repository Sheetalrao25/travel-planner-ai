import re

import re

def extract_preferences(text):
    text = text.lower()

    # Duration (in days)
    duration_match = re.search(r'(\d+)\s*(days|day)', text)
    duration = int(duration_match.group(1)) if duration_match else None

    # Budget
    budget = "unknown"
    if "low" in text:
        budget = "low"
    elif "average" in text or "medium" in text:
        budget = "average"
    elif "high" in text or "luxury" in text:
        budget = "high"

    # Interests — match from a known list
    known_interests = [
        "beach", "mountain", "trekking", "hiking", "nature", "temples", "shopping", "photography",
        "wildlife", "snow", "adventure", "yoga", "river rafting", "camping", "culture"
    ]
    interests = []
    for interest in known_interests:
        if interest in text:
            interests.append(interest)

    return {
        "duration": duration,
        "budget": budget,
        "interests": interests
    }
