from __future__ import annotations
from dataclasses import dataclass
from openweather.models.base import Base
from openweather.models.geocode import Geocode
import requests
import logging

logger = logging.getLogger(__name__)


@dataclass
class WeatherData:

    geocoder: Geocode = None
    datetime: int = None
    sunrise: int = None
    sunset: int = None
    temperature: float = None
    feels_like_temperature: float = None
    pressure_hpa: int = None
    humidity: int = None
    wind_speed: int = None
    wind_degree: int = None
    cloudiness_pct: int = None
    weather_description: str = None


@dataclass
class CurrentWeatherData(WeatherData, Base):

    min_current_temperature: float = None
    max_current_temperature: float = None

    def __post_init__(self):
        self.endpoint = (
            f"{self._base_url}/data/2.5/weather?lat={self.geocoder.latitude}"
            f"&lon={self.geocoder.longitude}&appid={self._api_key}&units=metric"
        )

    def get(self) -> CurrentWeatherData:
        logger.debug(
            "Calling current weather data endpoint to get weather data of latitude:"
            f" {self.geocoder.latitude} and longitude: {self.geocoder.longitude}"
        )
        response = requests.get(self.endpoint).json()
        return CurrentWeatherData(
            geocoder=self.geocoder,
            datetime=response["dt"],
            sunrise=response["sys"]["sunrise"],
            sunset=response["sys"]["sunset"],
            temperature=response["main"]["temp"],
            feels_like_temperature=response["main"]["feels_like"],
            min_current_temperature=response["main"]["temp_min"],
            max_current_temperature=response["main"]["temp_max"],
            pressure_hpa=response["main"]["pressure"],
            humidity=response["main"]["humidity"],
            wind_speed=response["wind"]["speed"],
            wind_degree=response["wind"]["deg"],
            cloudiness_pct=response["clouds"]["all"],
            weather_description=response["weather"][0]["description"],
        )


@dataclass
class ForecastWeatherData(WeatherData):

    probability_of_precipitation: float = None
    rain_volume: float = None
    uv_index: float = None


@dataclass
class HourlyForecastWeatherData(ForecastWeatherData):

    """
    Hourly forecast WeatherData object
    """


@dataclass
class DailyTemperature:

    morning_temp: float
    day_temp: float
    evening_temp: float
    night_temp: float


@dataclass
class DailyForecastWeatherData(ForecastWeatherData):

    """
    Daily forecast WeatherData object
    """

    temperature: DailyTemperature = None
    min_daily_temperature: float = None
    max_daily_temperature: float = None
    feels_like_temperature: DailyTemperature = None
