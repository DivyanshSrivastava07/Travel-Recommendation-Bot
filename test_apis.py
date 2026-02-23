import os
from dotenv import load_dotenv
import requests
from langchain_google_genai import GoogleGenerativeAI
import google.generativeai as genai

def test_google_gemini_api():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print(" GOOGLE_API_KEY not found in .env")
        return False

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content("Hello, how are you?")
        print(" Google Gemini API test successful")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f" Google Gemini API test failed: {str(e)}")
        return False

def test_openweathermap_api():
    load_dotenv()
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        print(" OPENWEATHERMAP_API_KEY not found in .env")
        return False

    try:
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(" OpenWeatherMap API test successful")
            print(f"Weather in London: {data['weather'][0]['description']}, Temp: {data['main']['temp']}°C")
            return True
        else:
            print(f" OpenWeatherMap API test failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f" OpenWeatherMap API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing APIs...")
    hf_success = test_google_gemini_api()
    owm_success = test_openweathermap_api()

    if hf_success and owm_success:
        print("\n All API tests passed!")
    else:
        print("\n  Some API tests failed. Please check your API keys in .env file.")
