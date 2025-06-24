from tools.weather_tool import get_weather
from tools.attractions_tool import get_attractions
from preference_extractor import extract_preferences
from destination_recommender import load_destinations, create_faiss_index, recommend_destinations
from tools.weather_tool import get_weather
from tools.attractions_tool import get_attractions
from itinerary_generator import generate_itinerary
from rag_answering import load_docs, build_rag_index, answer_question



if __name__ == "__main__":
    user_input = input("Enter your travel preferences:\n> ")

    # Step 1
    prefs = extract_preferences(user_input)
    print("\nExtracted Preferences:")
    print("Budget   :", prefs['budget'])
    print("Duration :", prefs['duration'], "days")
    print("Interests:", ', '.join(prefs['interests']))

    # Step 2
    destinations = load_destinations()
    index, _, texts = create_faiss_index(destinations)
    recommended = recommend_destinations(prefs['interests'], destinations, index, texts)

    print("\nRecommended Destinations:")
    for place in recommended:
        print("-", place)

    # Step 3: Tool Calls
    print("\nDetails for Top Destination:")
    top_dest = recommended[0]  # just use the first for now

    weather = get_weather(top_dest)
    attractions = get_attractions(top_dest)

    print(f"\nWeather in {top_dest}: {weather}")
    print(f"Top attractions in {top_dest}:")
    for spot in attractions:
        print("-", spot)
    # Step 4: Generate itinerary
    print(f"\n🗺️ Suggested {prefs['duration']}-Day Itinerary for {top_dest}:")
    itinerary = generate_itinerary(top_dest, prefs['duration'], prefs['interests'])
    print(itinerary)

        # Step 5: Follow-up questions using RAG
    docs = load_docs()
    rag_index, _ = build_rag_index(docs)

    print("\nAsk a follow-up question about your destination (or type 'exit'):")
    while True:
        q = input("> ")
        if q.lower() == 'exit':
            break
        answer = answer_question(q, docs, rag_index)
        print("Answer:", answer)


