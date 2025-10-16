from crewai import Agent

class ResponseAgent:
    def __init__(self, llm):
        self.agent = Agent(
            role="Travel Recommendation Specialist",
            goal="Generate clear, actionable travel recommendations",
            backstory="Friendly travel advisor who synthesizes complex data into clear suggestions",
            tools=[],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

    def get_agent(self):
        return self.agent
