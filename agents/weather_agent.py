from crewai import Agent
from tools.weather_tool import WeatherTool

class WeatherAgent:
    def __init__(self, llm):
        self.agent = Agent(
            role="Weather Data Specialist",
            goal="Fetch accurate weather forecasts for travel destinations",
            backstory="Expert meteorologist with access to real-time weather data",
            tools=[WeatherTool()],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

    def get_agent(self):
        return self.agent
