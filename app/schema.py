from pydantic import BaseModel, Field
from typing import List

class WeatherDay(BaseModel):
    date: str = Field(description="Дата в формате ГГГГ-ММ-ДД")
    temp_day: float = Field(description="Дневная температура")
    temp_night: float = Field(description="Ночная температура")
    humidity: int = Field(description="Влажность, %")
    pressure: int = Field(description="Давление, гПа")
    wind_speed: float = Field(description="Скорость ветра, м/с")
    description: str = Field(description="Краткое описание погоды")

class WeatherResponse(BaseModel):
    city: str
    forecast: List[WeatherDay]