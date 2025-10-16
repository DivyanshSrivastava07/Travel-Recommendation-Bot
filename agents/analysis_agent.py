from crewai import Agent
from tools.seasonality_tool import SeasonalityTool

class AnalysisAgent:
    def __init__(self, llm):
        self.agent = Agent(
            role="Travel Analysis Expert",
            goal="Analyze travel suitability comprehensively",
            backstory="Seasoned travel consultant with global destination expertise",
            tools=[SeasonalityTool()],
            llm=llm,
            verbose=True,
            allow_delegation=False,
            max_iter=10
        )

    def get_agent(self):
        return self.agent
