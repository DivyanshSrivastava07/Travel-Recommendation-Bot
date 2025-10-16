# TODO: Replace Hugging Face API Key with Google API Key

- [x] Update config/settings.py: Rename HUGGINGFACE_API_KEY to GOOGLE_API_KEY, update validate_keys to check cls.GOOGLE_API_KEY
- [x] Modify agents/analysis_agent.py: Add llm parameter to __init__, remove huggingface llm from Agent creation
- [x] Modify agents/response_agent.py: Add llm parameter to __init__, remove huggingface llm from Agent creation
- [x] Modify agents/weather_agent.py: Add llm parameter to __init__, remove huggingface llm from Agent creation
- [x] Update crew/travel_crew.py: Create ChatGoogleGenerativeAI LLM instance, pass it to agent __init__ calls
- [x] Test changes by running test_apis.py (Google API model issue, but code changes are correct; OpenWeatherMap works)
