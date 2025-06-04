from fastapi import FastAPI, HTTPException
from .service import get_weekly_forecast
from .schema import WeatherResponse
from .exceptions import WeatherServiceError

app = FastAPI(
    title="Weather API",
    description="API для получения прогноза погоды на 5 дней"
)

@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    """Получить прогноз погоды на 5 дней"""
    try:
        return await get_weekly_forecast(city)
    except WeatherServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@app.get("/")
async def root():
    return {"message": "API прогноза погоды. Используйте /weather/{город} для получения прогноза."}