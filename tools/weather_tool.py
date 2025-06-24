def get_weather(destination):
    # Mocked weather database
    fake_weather = {
        "Manali": "5°C, Snowy",
        "Goa": "30°C, Sunny",
        "Jaipur": "35°C, Dry and Sunny",
        "Rishikesh": "20°C, Pleasant",
        "Ladakh": "-2°C, Cold and Windy"
    }
    return fake_weather.get(destination, "Weather data not available")
