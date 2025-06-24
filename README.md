# 🧭 Travel Planner AI Agent

This is a simple AI-based travel planner project. It helps users plan trips by understanding their preferences like budget, duration, and interests. It gives destination suggestions, weather, attractions, and a full itinerary — and answers follow-up questions too.

✅ **No API key needed**.  
✅ **Fully offline** using local models and tools.  
✅ **Deployed on Hugging Face Spaces**.

## 📦 What This Project Does

- Takes natural language input like:
  > "I want to travel for 5 days on a low budget. I love mountains and trekking."
- Extracts:
  - Budget → low
  - Duration → 5 days
  - Interests → mountains, trekking
- Recommends suitable Indian destinations
- Shows weather + tourist places (offline tool calling)
- Gives a day-by-day travel plan
- Lets you ask questions like:
  > "What is special about Pangong Lake?"

---

## 🧰 Tech Used

- Python
- Gradio (for UI)
- Sentence Transformers (for embedding)
- FAISS (for vector search)
- Custom tools for weather & attractions
- No external API used

---

## 💻 How to Run Locally

```bash
# 1. Clone the project
git clone https://github.com/your-username/travel-planner-ai
cd travel-planner-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
