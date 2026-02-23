from crewai import Crew, Task, Process, LLM
from agents.weather_agent import WeatherAgent
from agents.analysis_agent import AnalysisAgent
from agents.response_agent import ResponseAgent
import os

class TravelRecommendationCrew:
    def __init__(self):
        llm = LLM(model="gemini/gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY"))
        self.weather_agent = WeatherAgent(llm).get_agent()
        self.analysis_agent = AnalysisAgent(llm).get_agent()
        self.response_agent = ResponseAgent(llm).get_agent()

    def create_tasks(self, destination: str, travel_date: str, preferences: str):
    
        weather_task = Task(
            description=f"Get detailed weather forecast for {destination} on {travel_date}. Focus on temperature, precipitation, and conditions affecting travel.",
            agent=self.weather_agent,
            expected_output="Detailed weather forecast with suitability assessment"
        )

        
        analysis_task = Task(
            description=f"Analyze travel suitability for {destination} on {travel_date} considering preferences: {preferences}. Use weather data and seasonality information.",
            agent=self.analysis_agent,
            expected_output="Comprehensive analysis of travel suitability with reasoning",
            context=[weather_task]
        )

        
        response_task = Task(
            description=f"Provide clear recommendation for visiting {destination} on {travel_date} with preferences: {preferences}. Include: 1) Go/Avoid/Consider recommendation, 2) Weather-based reasoning, 3) Tips or alternatives, 4) Suitability score (1-10)",
            agent=self.response_agent,
            expected_output="Clear, actionable travel recommendation with justification",
            context=[weather_task, analysis_task]
        )

        return [weather_task, analysis_task, response_task]

    def get_recommendation(self, destination: str, travel_date: str, preferences: str):
        tasks = self.create_tasks(destination, travel_date, preferences)

        crew = Crew(
            agents=[self.weather_agent, self.analysis_agent, self.response_agent],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result

    def get_follow_up_recommendation(self, previous_recommendation: str, follow_up_question: str):
        from crewai import Task
        follow_up_task = Task(
            description=f"Answer the follow-up question based on the previous recommendation: {previous_recommendation}. Question: {follow_up_question}",
            agent=self.response_agent,
            expected_output="Clear, concise answer to the follow-up question based on prior context"
        )

        crew = Crew(
            agents=[self.response_agent],
            tasks=[follow_up_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result
