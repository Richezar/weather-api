import httpx
from datetime import datetime
from .config import settings
from typing import Dict, Any
from .exceptions import WeatherServiceError
from .schema import WeatherResponse, WeatherDay


async def get_weekly_forecast(city: str):
    """
    Получает прогноз погоды на 5 дней для указанного города
    """
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    try:
        async with httpx.AsyncClient() as client:
            params = {
                'q': city.strip(),
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric',
                'lang': 'ru',
                'cnt': 40
            }
            response = await client.get(base_url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            daily_data = process_weather_data(data)
            return generate_weekly_forecast(daily_data, data['city']['name'])

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise WeatherServiceError("Город не найден")
        raise WeatherServiceError(f"Ошибка API погоды: {str(e)}")
    except Exception as e:
        raise WeatherServiceError(f"Внутренняя ошибка: {str(e)}")


def process_weather_data(data: Dict[str, Any]):
    """Обрабатывает сырые данные погоды и группирует по дням"""
    daily_data = {}
    for item in data.get('list', []):
        date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
        if date not in daily_data:
            daily_data[date] = {
                'temps': [],
                'humidity': [],
                'pressure': [],
                'wind_speed': [],
                'descriptions': []
            }

        main = item.get('main', {})
        wind = item.get('wind', {})
        weather = item.get('weather', [{}])[0]

        daily_data[date]['temps'].append(main.get('temp', 0))
        daily_data[date]['humidity'].append(main.get('humidity', 0))
        daily_data[date]['pressure'].append(main.get('pressure', 0))
        daily_data[date]['wind_speed'].append(wind.get('speed', 0))
        daily_data[date]['descriptions'].append(weather.get('description', ''))

    return daily_data


def generate_weekly_forecast(daily_data: Dict[str, Dict[str, list]], city: str):
    forecast = []
    for date, values in sorted(daily_data.items())[:6]:
        if not values['temps']:
            continue

        rain_keywords = ['дождь', 'ливень', 'грозa', 'морось']
        description = max(set(values['descriptions']), key=values['descriptions'].count)
        for desc in values['descriptions']:
            if any(keyword in desc.lower() for keyword in rain_keywords):
                description = desc
                break

        forecast.append(WeatherDay(
            date=date,
            temp_day=max(values['temps']),
            temp_night=min(values['temps']),
            humidity=round(sum(values['humidity']) / len(values['humidity'])),
            pressure=round(sum(values['pressure']) / len(values['pressure'])),
            wind_speed=round(sum(values['wind_speed']) / len(values['wind_speed']), 1),
            description=description
        ))

    return WeatherResponse(city=city, forecast=forecast)