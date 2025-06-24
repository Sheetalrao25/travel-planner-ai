import gradio as gr
from preference_extractor import extract_preferences
from destination_recommender import load_destinations, create_faiss_index, recommend_destinations
from itinerary_generator import generate_itinerary
from tools.weather_tool import get_weather
from tools.attractions_tool import get_attractions
from rag_answering import load_docs, build_rag_index, answer_question

# Load everything once
destinations = load_destinations()
index, _ = create_faiss_index(destinations)
docs = load_docs()
rag_index, _ = build_rag_index(docs)

def full_planner(user_input, follow_up=""):
    prefs = extract_preferences(user_input)

    results = [f"**Extracted Preferences:**\n- Budget: {prefs['budget']}\n- Duration: {prefs['duration']} days\n- Interests: {', '.join(prefs['interests']) or 'None'}\n"]

    recommended = recommend_destinations(prefs, destinations, index)
    results.append("**Recommended Destinations:**\n- " + "\n- ".join(recommended))

    top_dest = recommended[0] if recommended else "Unknown"
    weather = get_weather(top_dest)
    attractions = get_attractions(top_dest)
    results.append(f"**Details for {top_dest}:**\n- Weather: {weather}\n- Attractions: " + ", ".join(attractions))

    itinerary = generate_itinerary(top_dest, prefs["duration"], prefs["interests"])
    results.append(f"**🗺️ Suggested Itinerary:**\n{itinerary}")

    final_output = "\n\n".join(results)

    # Follow-up question via RAG
    rag_answer = answer_question(follow_up, docs, rag_index) if follow_up else "Ask a follow-up question below."

    return final_output, rag_answer
iface = gr.Interface(
    fn=full_planner,
    inputs=[
        gr.Textbox(label="Enter your travel preferences", placeholder="I want to travel for 5 days on a low budget. I enjoy trekking."),
        gr.Textbox(label="Ask a follow-up question (optional)", placeholder="What’s special about Pangong Lake?")
    ],
    outputs=[
        gr.Markdown(label="Travel Plan"),
        gr.Markdown(label="Answer")
    ],
    title="AI Travel Planner Agent",
    description="An offline AI travel assistant using LangGraph-like logic, local LLM, and RAG. No APIs needed."
)

iface.launch()
