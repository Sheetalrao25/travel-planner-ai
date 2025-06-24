import gradio as gr
from weather_tool import get_weather
from attractions_tool import get_attractions
from preference_extractor import extract_preferences
from destination_recommender import load_destinations, create_faiss_index, recommend_destinations
from itinerary_generator import generate_itinerary
from rag_answering import load_docs, build_rag_index, answer_question

# Load data once
destinations = load_destinations()
index, _, texts = create_faiss_index(destinations)
docs = load_docs()
rag_index, _ = build_rag_index(docs)

# Store global state (last destination)
last_top_destination = {"name": ""}

def plan_trip(user_input):
    prefs = extract_preferences(user_input)

    result = f"### ✅ Extracted Preferences\n"
    result += f"- **Budget**: {prefs['budget'] or 'Not specified'}\n"
    result += f"- **Duration**: {prefs['duration']} days\n"
    result += f"- **Interests**: {', '.join(prefs['interests']) or 'None'}\n"

    recommended = recommend_destinations(prefs['interests'], destinations, index, texts)
    if not recommended:
        return result + "\n❌ No destinations found.", ""

    top_dest = recommended[0]
    last_top_destination["name"] = top_dest  # Save for follow-up tab

    result += f"\n### 🌍 Recommended Destinations:\n" + "\n".join([f"- {r}" for r in recommended])

    weather = get_weather(top_dest)
    attractions = get_attractions(top_dest)

    result += f"\n\n### ☁️ Weather in {top_dest}:\n{weather}"
    result += f"\n\n### 📍 Top Attractions in {top_dest}:\n" + "\n".join([f"- {a}" for a in attractions])

    itinerary = generate_itinerary(top_dest, prefs['duration'], prefs['interests'])
    # Split by sentence and reformat nicely
    days = itinerary.split(". ")
    formatted_itinerary = "\n".join([f"- {day.strip()}" for day in days if day.strip()])
    result += f"\n\n### 🗺️ Suggested Itinerary:\n{formatted_itinerary}"


    return result, f"You can now ask questions about {top_dest} in the next tab ⬇️"

def ask_follow_up(question):
    if not question.strip():
        return "Please enter a question."

    return answer_question(question, docs, rag_index)

# Gradio UI with two tabs
with gr.Blocks() as demo:
    gr.Markdown("## 🧭 AI Travel Planner – No API Key Needed")

    with gr.Tab("Plan Trip"):
        with gr.Row():
            user_input = gr.Textbox(label="Enter your travel preferences", lines=3, placeholder="I want to travel for 5 days, low budget, love beaches.")
        plan_btn = gr.Button("Plan My Trip")
        trip_output = gr.Markdown()
        note = gr.Markdown()

    with gr.Tab("Follow-up Question"):
        follow_input = gr.Textbox(label="Ask about destination", lines=2)
        follow_btn = gr.Button("Ask")
        follow_output = gr.Markdown()

    # Bind logic
    plan_btn.click(plan_trip, inputs=user_input, outputs=[trip_output, note])
    follow_btn.click(ask_follow_up, inputs=follow_input, outputs=follow_output)

demo.launch()
