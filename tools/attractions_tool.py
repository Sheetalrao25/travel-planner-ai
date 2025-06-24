def get_attractions(destination):
    attractions_db = {
        "Manali": ["Solang Valley", "Rohtang Pass", "Hadimba Temple"],
        "Goa": ["Baga Beach", "Fort Aguada", "Dudhsagar Falls"],
        "Jaipur": ["Amber Fort", "Hawa Mahal", "City Palace"],
        "Rishikesh": ["Laxman Jhula", "Ganga Aarti", "Neer Waterfall"],
        "Ladakh": ["Pangong Lake", "Magnetic Hill", "Nubra Valley"]
    }
    return attractions_db.get(destination, ["No attractions found"])
