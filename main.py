import os
from dotenv import load_dotenv
from ui.gradio_app import launch_app

def main():
    load_dotenv()

    required_keys = ["GOOGLE_API_KEY", "OPENWEATHERMAP_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]

    if missing_keys:
        print(f" Missing required environment variables: {', '.join(missing_keys)}")
        return

    print(" Starting Travel Recommendation Bot...")
    launch_app()

if __name__ == "__main__":
    main()
