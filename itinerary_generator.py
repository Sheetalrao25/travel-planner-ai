from transformers import pipeline

# Load the local T5 model for generation
itinerary_pipe = pipeline("text2text-generation", model="google/flan-t5-base")

def generate_itinerary(destination, duration, interests):
    base_plan = {
        "Ladakh": [
            "Arrive in Leh and rest for acclimatization.",
            "Visit Magnetic Hill and nearby monasteries.",
            "Travel to Nubra Valley and enjoy sand dunes.",
            "Explore Pangong Lake and camp overnight.",
            "Return to Leh and shop for local crafts."
        ],
        "Manali": [
            "Arrive and explore Manali Mall Road.",
            "Visit Solang Valley for snow and activities.",
            "Trek to Jogini Falls.",
            "Explore Rohtang Pass and take photos.",
            "Visit Hadimba Temple and relax."
        ],
        "Goa": [
            "Arrive and relax on Baga Beach.",
            "Visit Fort Aguada and nearby markets.",
            "Try water sports at Calangute.",
            "Explore Dudhsagar Falls.",
            "Enjoy nightlife and return."
        ]
    }

    steps = base_plan.get(destination, [f"Explore {destination} and enjoy your trip."])
    
    # Adjust to number of days
    if duration and duration <= len(steps):
        steps = steps[:duration]
    elif duration and duration > len(steps):
        steps += [f"Free exploration day in {destination}."] * (duration - len(steps))

    # Format into itinerary
    return "\n".join([f"Day {i+1}: {activity}" for i, activity in enumerate(steps)])
