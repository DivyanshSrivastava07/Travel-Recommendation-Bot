import json
import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from datetime import datetime

class SeasonalityToolInput(BaseModel):
    location: str = Field(..., description="Travel destination")
    date: str = Field(..., description="Travel date in YYYY-MM-DD format")
    preferences: str = Field(..., description="User travel preferences")

class SeasonalityTool(BaseTool):
    name: str = "seasonality_analysis"
    description: str = "Analyze destination seasonality and crowd levels"
    args_schema: Type[BaseModel] = SeasonalityToolInput

    def _run(self, location: str, date: str, preferences: str) -> str:
        # Parse date and determine season
        travel_date = datetime.strptime(date, "%Y-%m-%d")
        month = travel_date.month

        seasons = {
            "spring": [3, 4, 5],
            "summer": [6, 7, 8],
            "autumn": [9, 10, 11],
            "winter": [12, 1, 2]
        }

        current_season = next(season for season, months in seasons.items() if month in months)

        # Basic seasonality analysis based on preferences
        if "beach" in preferences.lower() or "sun" in preferences.lower():
            crowd_level = "high" if current_season == "summer" else "low"
            weather_suitability = "excellent" if current_season == "summer" else "poor"
            peak_activities = ["beach", "water sports"] if current_season == "summer" else []
        elif "skiing" in preferences.lower() or "snow" in preferences.lower():
            crowd_level = "high" if current_season == "winter" else "low"
            weather_suitability = "excellent" if current_season == "winter" else "poor"
            peak_activities = ["skiing", "winter sports"] if current_season == "winter" else []
        else:
            crowd_level = "moderate"
            weather_suitability = "good" if current_season in ["spring", "autumn"] else "fair"
            peak_activities = ["sightseeing", "cultural activities"]

        preference_match = "High" if any(pref in preferences.lower() for pref in peak_activities) else "Moderate"

        return f"Seasonality analysis for {location} in {current_season}: Crowd level: {crowd_level}, Weather suitability: {weather_suitability}, Peak activities: {', '.join(peak_activities) if peak_activities else 'General tourism'}, Preference match: {preference_match}"

    async def _arun(self, location: str, date: str, preferences: str) -> str:
        return self._run(location, date, preferences)
