from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import requests
import logging
import os

logger = logging.getLogger(__name__)


@dataclass
class Base(ABC):
    
    """
    Constructs the API endpoints for different operations.
    """

    base_url: str = field(default="https://api.openweathermap.org", repr=False)
    api_key: str = field(default=os.getenv("API_KEY"), repr=False)

    @abstractmethod
    def endpoint(self):
        pass

    @abstractmethod
    def get(self):
        pass

@dataclass
class Geocode(Base):

    city: str = None
    country_code: str = None
    latitude: float = None
    longitude: float = None

    def endpoint(self, city: str, country_code: str) -> str:
        endpoint = f"{self.base_url}/geo/1.0/direct?q={city}, {country_code}&appid={self.api_key}"
        return endpoint

    def get(self, city: str, country_code: str = None) -> Geocode:
        endpoint = self.endpoint(city, country_code)
        logger.debug(f"Calling geocoding endpoint to get latitude and longitude of city: {city} and country_code: {country_code}")
        response = requests.get(endpoint).json()[0]
        resp_city = response["name"]
        resp_country_code = response["country"]
        resp_latitude = response["lat"]
        resp_longitude = response["lon"]
        return Geocode(city=resp_city, country_code=resp_country_code, latitude=resp_latitude, longitude=resp_longitude)


@dataclass
class CurrentWeatherData(Base):

    datetime: int = None
    city_name: str = None
    city_id: int = None
    country_code: str = None
    latitude: float = None
    longitude: float = None
    measured_temperature: float = None
    feels_like_temperature: float = None
    min_temperature: float = None
    max_temperature: float = None
    pressure_hpa: int = None
    humidity: int = None
    wind_speed: int = None
    wind_degree: int = None
    cloudiness_pct: int = None

    def endpoint(self, latitude, longitude) -> str:
        endpoint = f"{self.base_url}/data/2.5/weather?lat={latitude}&lon={longitude}&appid={self.api_key}&units=metric"
        return endpoint

    def get(self, latitude: float, longitude: float) -> CurrentWeatherData:
        endpoint = self.endpoint(latitude, longitude)
        logger.debug(f"Calling current weather data endpoint to get weather data of latitude: {latitude} and longitude: {longitude}")
        response = requests.get(endpoint).json()
        resp_datetime = response["dt"]
        resp_city_name = response["name"]
        resp_city_id = response["id"]
        resp_country_code = response["sys"]["country"]
        resp_latitude = response["coord"]["lat"]
        resp_longitude = response["coord"]["lon"]
        resp_measured_temperature = response["main"]["temp"]
        resp_feels_like_temperature = response["main"]["feels_like"]
        resp_min_temperature = response["main"]["temp_min"]
        resp_max_temperature = response["main"]["temp_max"]
        resp_pressure_hpa = response["main"]["pressure"]
        resp_humidity = response["main"]["humidity"]
        resp_wind_speed = response["wind"]["speed"]
        resp_wind_degree = response["wind"]["deg"]
        resp_cloudiness_pct = response["clouds"]["all"]
        return CurrentWeatherData(
            datetime=resp_datetime,
            city_name=resp_city_name,
            city_id=resp_city_id,
            country_code=resp_country_code,
            latitude=resp_latitude,
            longitude=resp_longitude,
            measured_temperature=resp_measured_temperature,
            feels_like_temperature=resp_feels_like_temperature,
            min_temperature=resp_min_temperature,
            max_temperature=resp_max_temperature,
            pressure_hpa=resp_pressure_hpa,
            humidity=resp_humidity,
            wind_speed=resp_wind_speed,
            wind_degree=resp_wind_degree,
            cloudiness_pct=resp_cloudiness_pct,
        )
