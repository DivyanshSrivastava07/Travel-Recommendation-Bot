import sys
sys.path.append('.')
import gradio as gr
from crew.travel_crew import TravelRecommendationCrew
from datetime import datetime, timedelta
import random
import re
import csv
import os

class TravelRecommendationUI:
    def __init__(self):
        self.crew = TravelRecommendationCrew()
        self.conversation_history = []  

    def validate_date(self, date_str):
        formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"]
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                if date_obj.date() < datetime.now().date():
                    return None, "Travel date must be in the future."
                return date_obj, None
            except ValueError:
                continue
        return None, "Invalid date format. Please use YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY, or YYYY/MM/DD."

    def log_to_csv(self, destination, travel_date, preferences, recommendation, flag=False, username="anonymous"):
        log_file = "flagged/log.csv"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_exists = os.path.isfile(log_file)
        with open(log_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Destination", "Travel Date", "Your Interests", "AI Travel Recommendation", "flag", "username", "timestamp"])
            writer.writerow([destination, travel_date, preferences, recommendation, flag, username, datetime.now().isoformat()])

    def get_recommendation(self, destination, travel_date, preferences, flag=False, follow_up_question=""):
        try:
            if follow_up_question:

                if not self.conversation_history:
                    return " No previous recommendations found. Please generate a new recommendation first."

                last_recommendation = self.conversation_history[-1]["recommendation"]
                result = self.crew.get_follow_up_recommendation(last_recommendation, follow_up_question)
                full_result = f" **Follow-up on Previous Recommendation**\n\n{result}"
                self.conversation_history.append({"type": "follow_up", "question": follow_up_question, "recommendation": full_result})
                
                self.log_to_csv("", "", f"Follow-up: {follow_up_question}", full_result, flag=False)
                return full_result

            if not destination or not travel_date or not preferences:
                return " Please fill in all fields."

            
            date_obj, error_msg = self.validate_date(travel_date)
            if error_msg:
                self.log_to_csv(destination, travel_date, preferences, error_msg, flag=True)
                return f" {error_msg}"

            date_str = date_obj.strftime("%Y-%m-%d")
            result = self.crew.get_recommendation(destination, date_str, preferences)

            full_result = f" **Travel Recommendation for {destination}**\n\n{result}"
            self.log_to_csv(destination, travel_date, preferences, full_result, flag=flag)
            self.conversation_history.append({"type": "initial", "destination": destination, "date": travel_date, "preferences": preferences, "recommendation": full_result})

            return full_result

        except Exception as e:
            error_msg = f" Error generating recommendation: {str(e)}"
            self.log_to_csv(destination, travel_date, preferences, error_msg, flag=True)
            return error_msg

    def get_history_display(self):
        if not self.conversation_history:
            return "No conversation history yet."
        history_lines = []
        for i, item in enumerate(self.conversation_history, 1):
            if item["type"] == "initial":
                history_lines.append(f"**{i}. Initial Recommendation for {item['destination']} on {item['date']}**\nPreferences: {item['preferences']}\n")
            elif item["type"] == "follow_up":
                history_lines.append(f"**{i}. Follow-up Question:** {item['question']}\n")
        return "\n".join(history_lines)

    def load_past_recommendations(self, date_offset=None, selected_date=None):
        log_file = "flagged/log.csv"
        if not os.path.isfile(log_file):
            return "No past recommendations found."

        recommendations = []
        try:
            with open(log_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if selected_date:
                        
                        if row.get('Travel Date') == selected_date:
                            recommendations.append(row)
                    else:
                        
                        timestamp = datetime.fromisoformat(row['timestamp'])
                        target_date = (datetime.now() - timedelta(days=date_offset)).date()
                        if timestamp.date() == target_date:
                            recommendations.append(row)
        except Exception as e:
            return f"Error loading past recommendations: {str(e)}"

        if not recommendations:
            filter_desc = f"travel date {selected_date}" if selected_date else f"generation date {(datetime.now() - timedelta(days=date_offset)).date().strftime('%Y-%m-%d')}"
            return f"No recommendations found for {filter_desc}."

        display_lines = []
        for i, rec in enumerate(recommendations, 1):
            dest = rec.get('Destination', 'N/A')
            date = rec.get('Travel Date', 'N/A')
            prefs = rec.get('Your Interests', 'N/A')
            recom = rec.get('AI Travel Recommendation', 'N/A')
            display_lines.append(f"**{i}. Recommendation for {dest} on {date}**\nPreferences: {prefs}\nRecommendation: {recom}\n")
        return "\n".join(display_lines)

    def create_interface(self):
        custom_css = """
        .gradio-container {
            background-color: #e8f5e8 !important; /* Light green background */
        }
        .gr-button {
            background: linear-gradient(45deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3) !important; /* Rainbow gradient background */
            color: white !important;
            border-radius: 35px !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1), 0 0 20px rgba(255, 0, 0, 0.5) !important; /* Added glow effect */
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 10px 20px !important;
            background-size: 200% 200% !important;
            animation: rainbow 3s ease infinite !important;
        }
        .gr-button:hover {
            background: linear-gradient(45deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3) !important; /* Rainbow gradient on hover */
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15), 0 0 30px rgba(255, 0, 0, 0.7) !important; /* Enhanced glow on hover */
            animation: rainbow 1.5s ease infinite !important;
        }
        @keyframes rainbow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .gr-textbox, .gr-checkbox-group, .gr-markdown {
            border-radius: 35px !important;
            border: 2px solid #4caf50 !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
            background-color: #ffffff !important;
        }
        .gr-textbox:focus, .gr-checkbox-group:focus {
            border-color: #388e3c !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
        }
        .gr-checkbox-group input[type="checkbox"]:checked + label {
            color: #4caf50 !important; /* Green color for selected preferences */
            font-weight: bold !important;
        }
        .gr-markdown {
            border: 2px solid #4caf50 !important;
            border-radius: 35px !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
            background-color: #f9f9f9 !important;
            padding: 10px !important;
        }
        .gr-label {
            font-weight: bold !important;
            color: #b71c1c !important; /* Light maroon for labels */
        }
        .gr-group:first-child {
            background-image: url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80'), url('https://images.unsplash.com/photo-1472214103451-9374bd1c798e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80') !important; /* Eye-relaxing travel background image and sunset image */
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            padding: 20px !important;
            border-radius: 35px !important;
            position: relative !important;
        }
        .gr-group:first-child::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            background-color: rgba(255, 255, 255, 0.8) !important; /* Semi-transparent overlay for readability */
            border-radius: 35px !important;
            z-index: 1 !important;
        }
        .gr-group:first-child > * {
            position: relative !important;
            z-index: 2 !important;
        }
        """

        with gr.Blocks(title="Travel Recommendation", theme=gr.themes.Soft(), css=custom_css) as interface:
            gr.Markdown("# Travel Recommendation")

            with gr.Group():
                gr.Markdown("## Input Section")
                with gr.Row():
                    destination_input = gr.Textbox(
                        label=" Place",
                        placeholder="New Delhi, London etc",
                        info="Enter the destination"
                    )

                    date_input = gr.Textbox(
                        label=" Travel Date",
                        placeholder="YYYY-MM-DD",
                        info="Enter date",
                        value=(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                    )

                preferences_list = [
                    "Sightseeing", "Museums & Culture", "Food & Dining",
                    "Adventure & Hiking", "Beach & Water Sports", "Nightlife",
                    "Shopping", "Nature & Wildlife", "Photography",
                    "History & Architecture", "Relaxation & Spa", "Festivals & Events"
                ]
                random.shuffle(preferences_list)

                preferences_input = gr.CheckboxGroup(
                    label=" Preference(s)",
                    choices=preferences_list,
                    info="Activities(multiple selection)"
                )

                flag_checkbox = gr.Checkbox(
                    label="Flag this recommendation",
                    value=False
                )

                submit_btn = gr.Button("SUBMIT")

            follow_up_group = gr.Group(visible=False)
            with follow_up_group:
                gr.Markdown("## Follow-up Section")
                follow_up_input = gr.Textbox(
                    label=" Follow-up Question",
                    placeholder="Ask a question about the previous recommendation...",
                    info="Optional: Ask follow-up questions based on prior recommendations"
                )
                follow_up_btn = gr.Button("ASK FOLLOW-UP")

            with gr.Group():
                gr.Markdown("## Conversation History")
                history_output = gr.Markdown(label=" Previous Recommendations", value=self.get_history_display())

            with gr.Group():
                gr.Markdown("## Past Recommendations")
                past_date_dropdown = gr.Dropdown(
                    label="Select Date",
                    choices=["Today", "Yesterday", "2 days ago", "3 days ago", "4 days ago", "5 days ago", "6 days ago", "7 days ago"],
                    value="Today",
                    info="Select a past date to view recommendations"
                )
                past_output = gr.Markdown(label=" Past Recommendations")

                load_past_btn = gr.Button("Load Past Recommendations for Selected Date")

            with gr.Group():
                gr.Markdown("## Output Section")
                recommendation_output = gr.Markdown(label=" AI Travel Recommendation")

            submit_btn.click(
                fn=lambda dest, date, prefs, flag: (self.get_recommendation(dest, date, ", ".join(prefs), flag), self.get_history_display(), gr.update(visible=True)),
                inputs=[destination_input, date_input, preferences_input, flag_checkbox],
                outputs=[recommendation_output, history_output, follow_up_group]
            )

            follow_up_btn.click(
                fn=lambda question: (self.get_recommendation("", "", "", False, question), self.get_history_display(), gr.update(visible=True)),
                inputs=[follow_up_input],
                outputs=[recommendation_output, history_output, follow_up_group]
            )

            past_date_dropdown.change(
                fn=lambda date_str: self.load_past_recommendations({"Today": 0, "Yesterday": 1, "2 days ago": 2, "3 days ago": 3, "4 days ago": 4, "5 days ago": 5, "6 days ago": 6, "7 days ago": 7}[date_str]),
                inputs=[past_date_dropdown],
                outputs=[past_output]
            )

            load_past_btn.click(
                fn=lambda date: self.load_past_recommendations(selected_date=date),
                inputs=[date_input],
                outputs=[past_output]
            )



        return interface

def launch_app():
    app = TravelRecommendationUI()
    interface = app.create_interface()
    interface.launch(server_name="127.0.0.1", server_port=7864, share=False)
