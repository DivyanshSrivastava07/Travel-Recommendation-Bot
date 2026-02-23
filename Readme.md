🌍 AI Multi-Agent Travel Recommendation System

An intelligent, AI-powered Travel Recommendation System built using a multi-agent orchestration architecture.
This system analyzes user travel preferences, fetches seasonal and weather intelligence, and generates contextual travel recommendations using modular AI agents and tools.

🚀 Project Overview

This project implements a Crew-based multi-agent architecture where specialized AI agents collaborate to generate personalized travel recommendations.

Instead of using simple filtering logic, the system:

Understands user intent

Analyzes seasonal travel data

Fetches weather intelligence

Synthesizes responses using AI reasoning

Returns context-aware recommendations via an interactive UI

🏗 Architecture
User Input (Gradio UI)
        ↓
Travel Crew (Orchestrator)
        ↓
 ┌───────────────────────────┐
 │  Analysis Agent           │ → Understands user preferences
 │  Weather Agent            │ → Fetches weather insights
 │  Response Agent           │ → Generates final recommendation
 └───────────────────────────┘
        ↓
Tools Layer (Weather + Seasonality)
        ↓
Structured Data / APIs
        ↓
Final Response to UI



🧠 Key Features

🤖 Multi-Agent AI Architecture

🔎 Intelligent user preference analysis

🌦 Weather-aware travel suggestions

📅 Seasonal recommendation intelligence

🧩 Modular agent-tool design

🎛 Crew-based orchestration layer

🖥 Interactive Gradio UI

📊 Structured JSON-based seasonal dataset

🛠 Tech Stack
Backend

Python

CrewAI-style multi-agent orchestration

OpenAI / LLM integration

Tools & Data

Weather API integration

JSON-based seasonality dataset

UI

Gradio

📂 Project Structure
Travel_recommendation_Final/
│
├── agents/
│   ├── analysis_agent.py
│   ├── weather_agent.py
│   └── response_agent.py
│
├── tools/
│   ├── seasonality_tool.py
│   └── weather_tool.py
│
├── crew/
│   └── travel_crew.py
│
├── config/
│   └── settings.py
│
├── data/
│   └── seasonality_data.json
│
├── ui/
│   └── gradio_app.py
│
├── main.py
├── test_apis.py
└── README.md


⚙️ Installation & Setup
1️⃣ Clone the Repository
cd Travel_recommendation_Final
2️⃣ Create Virtual Environment
python -m venv venv

Activate:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Configure Environment Variables

Create a .env file (if required):

OPENAI_API_KEY=your_api_key
WEATHER_API_KEY=your_api_key
5️⃣ Run the Application
python main.py

Or run UI directly:

python ui/gradio_app.py

The app will launch in your browser via Gradio.

🧩 How It Works

User provides travel preferences (budget, interests, duration, location).

The Analysis Agent extracts intent and constraints.

The Weather Agent retrieves climate intelligence.

The Seasonality Tool checks optimal travel time.

The Response Agent synthesizes all insights.

The final recommendation is displayed in the UI.

🎯 Design Principles

Single Responsibility per Agent

Clear separation between reasoning and data access

Tool-based data abstraction

Scalable architecture for adding more agents

Modular configuration management

📈 Future Enhancements

✈ Flight price integration

🏨 Hotel recommendation engine

📊 Vector embeddings for destination similarity

🧑‍💼 User authentication & travel history

🐳 Dockerization

☁ Cloud deployment (AWS / Render / GCP)

🔄 CI/CD pipeline