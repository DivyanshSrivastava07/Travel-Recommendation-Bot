import gradio as gr
from crew.travel_crew import TravelRecommendationCrew
from datetime import datetime, timedelta

class TravelRecommendationUI:
    def __init__(self):
        self.crew = TravelRecommendationCrew()

    def get_recommendation(self, destination, travel_date, preferences):
        try:
            if not destination or not travel_date or not preferences:
                return " Please fill in all fields."

            # Parse the date string to datetime object
            date_obj = datetime.strptime(travel_date, "%Y-%m-%d")
            date_str = date_obj.strftime("%Y-%m-%d")
            result = self.crew.get_recommendation(destination, date_str, preferences)

            return f" **Travel Recommendation for {destination}**\n\n{result}"

        except Exception as e:
            return f" Error generating recommendation: {str(e)}"

    def create_interface(self):
        destination_input = gr.Textbox(
            label=" Destination",
            placeholder="e.g., Paris, France or Tokyo, Japan",
            info="Enter the city and country you want to visit"
        )

        date_input = gr.Textbox(
            label=" Travel Date",
            placeholder="YYYY-MM-DD",
            info="Enter your planned travel date (e.g., 2025-07-15)",
            value=(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        )

        preferences_input = gr.CheckboxGroup(
            label=" Your Interests",
            choices=[
                "Sightseeing", "Museums & Culture", "Food & Dining",
                "Adventure & Hiking", "Beach & Water Sports", "Nightlife",
                "Shopping", "Nature & Wildlife", "Photography",
                "History & Architecture", "Relaxation & Spa", "Festivals & Events"
            ],
            info="Select activities you enjoy (multiple selections allowed)"
        )

        recommendation_output = gr.Markdown(label=" AI Travel Recommendation")

        interface = gr.Interface(
            fn=lambda dest, date, prefs: self.get_recommendation(dest, date, ", ".join(prefs)),
            inputs=[destination_input, date_input, preferences_input],
            outputs=recommendation_output,
            title=" AI Travel Recommendation Bot",
            description="Get personalized travel recommendations based on weather forecasts, seasonality, and your interests.",
            theme=gr.themes.Soft(),
            examples=[
                ["Kyoto, Japan", datetime(2025, 11, 10), ["Museums & Culture", "Photography"]],
                ["Santorini, Greece", datetime(2025, 7, 15), ["Beach & Water Sports", "Photography"]],
                ["Reykjavik, Iceland", datetime(2025, 12, 20), ["Nature & Wildlife", "Adventure & Hiking"]]
            ]
        )

        return interface

def launch_app():
    app = TravelRecommendationUI()
    interface = app.create_interface()
    interface.launch(server_name="127.0.0.1", server_port=7860, share=False)
