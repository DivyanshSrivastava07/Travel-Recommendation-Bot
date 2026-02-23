import requests
import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class WeatherToolInput(BaseModel):
    location: str = Field(..., description="City and country for weather forecast")
    date: str = Field(..., description="Date in YYYY-MM-DD format")

class WeatherTool(BaseTool):
    name: str = "weather_forecast"
    description: str = "Get weather forecast for a specific location and date"
    args_schema: Type[BaseModel] = WeatherToolInput

    def _run(self, location: str, date: str) -> str:
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")

        
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if not geo_data:
            return f"Could not find location: {location}"

        lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]

        
        weather_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        
        target_date = date
        forecasts = []

        for item in weather_data.get("list", []):
            if target_date in item["dt_txt"]:
                forecasts.append({
                    "datetime": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "humidity": item["main"]["humidity"],
                    "description": item["weather"][0]["description"],
                    "rain": item.get("rain", {}).get("3h", 0)
                })

        if not forecasts:
            return f"No weather forecast available for {location} on {date}"

        
        avg_temp = sum(f["temperature"] for f in forecasts) / len(forecasts)
        rain_total = sum(f["rain"] for f in forecasts)
        conditions = list(set(f["description"] for f in forecasts))

        suitability = "Good" if avg_temp > 15 and rain_total < 5 else "Fair" if avg_temp > 10 else "Poor"

        return f"Weather forecast for {location} on {date}: Avg temp {avg_temp:.1f}°C, Conditions: {', '.join(conditions)}, Rain: {rain_total:.1f}mm, Suitability: {suitability}"

    async def _arun(self, location: str, date: str) -> str:
        return self._run(location, date)
