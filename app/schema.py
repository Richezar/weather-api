from pydantic import BaseModel
from typing import List

class WeatherDay(BaseModel):
    date: str
    temp_day: float
    temp_night: float
    humidity: int
    pressure: int
    wind_speed: float
    description: str

class WeatherResponse(BaseModel):
    city: str
    forecast: List[WeatherDay]