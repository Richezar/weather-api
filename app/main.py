from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .service import get_weekly_forecast
from .schema import WeatherResponse
from .exceptions import WeatherServiceError

app = FastAPI(
    title="Weather API",
    description="API для получения прогноза погоды на 5 дней"
)

class WeatherRequest(BaseModel):
    city: str
    token: str

@app.post("/weather/", response_model=WeatherResponse)
async def post_weather(request: WeatherRequest):
    """Получить прогноз погоды на 5 дней"""
    try:
        return await get_weekly_forecast(request.city)
    except WeatherServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера" )

@app.get("/")
async def root():
    return {"message": "API прогноза погоды. Используйте /weather/ для получения прогноза."}