from openweather.models.base import Base
from openweather.models.geocode import Geocode
from openweather.models.weather import CurrentWeatherData, DailyForecastWeatherData, DailyTemperature, HourlyForecastWeatherData
from dataclasses import dataclass
from typing import Dict, List
import requests
import logging

logger = logging.getLogger(__name__)


@dataclass
class OneCallAPI(Base):

    geocoder: Geocode = None

    def __post_init__(self):
        self.endpoint = f"{self.base_url}/data/2.5/onecall?lat={self.geocoder.latitude}&lon={self.geocoder.longitude}&appid={self.api_key}&units=metric&exclude=minutely"

    def get(self):
        logger.debug(f"Calling OneCallAPI endpoint to get weather data of latitude: {self.geocoder.latitude} and longitude: {self.geocoder.longitude}")
        response = requests.get(self.endpoint).json()
        return response

    def get_current(self) -> CurrentWeatherData:

        """
        Get current weather data -- same as CurrentWeatherData.get() but min and max temp will be None
        """

        response = self.get()["current"]
        return CurrentWeatherData(
            datetime=response["dt"],
            sunrise=response["sunrise"],
            sunset=response["sunset"],
            temperature=response["temp"],
            feels_like_temperature=response["feels_like"],
            pressure_hpa=response["pressure"],
            humidity=response["humidity"],
            wind_speed=response["wind_speed"],
            wind_degree=response["wind_deg"],
            cloudiness_pct=response["clouds"],
            weather_description=response["weather"][0]["description"]
        )

    def _parse_daily(self, weather_data_dict: Dict) -> DailyForecastWeatherData:
        return DailyForecastWeatherData(
            datetime=weather_data_dict["dt"],
            sunrise=weather_data_dict["sunrise"],
            sunset=weather_data_dict["sunset"],
            temperature=DailyTemperature(
                morning_temp=weather_data_dict["temp"]["morn"],
                day_temp=weather_data_dict["temp"]["day"],
                evening_temp=weather_data_dict["temp"]["eve"],
                night_temp=weather_data_dict["temp"]["night"]
            ),
            feels_like_temperature=DailyTemperature(
                morning_temp=weather_data_dict["feels_like"]["morn"],
                day_temp=weather_data_dict["feels_like"]["day"],
                evening_temp=weather_data_dict["feels_like"]["eve"],
                night_temp=weather_data_dict["feels_like"]["night"]
            ),
            min_daily_temperature=weather_data_dict["temp"]["min"],
            max_daily_temperature=weather_data_dict["temp"]["max"],
            pressure_hpa=weather_data_dict["pressure"],
            humidity=weather_data_dict["humidity"],
            wind_speed=weather_data_dict["wind_speed"],
            wind_degree=weather_data_dict["wind_deg"],
            cloudiness_pct=weather_data_dict["clouds"],
            weather_description=weather_data_dict["weather"][0]["description"],
            probability_of_precipitation=weather_data_dict["pop"],
            rain_volume=weather_data_dict["rain"],
            uv_index=weather_data_dict["uvi"]
        )

    def _parse_hourly(self, weather_data_dict: Dict) -> HourlyForecastWeatherData:
        rain = weather_data_dict.get("rain", None)
        rain_volume = rain["1h"] if rain else None
        return HourlyForecastWeatherData(
            datetime=weather_data_dict["dt"],
            temperature=weather_data_dict["temp"],
            feels_like_temperature=weather_data_dict["feels_like"],
            pressure_hpa=weather_data_dict["pressure"],
            humidity=weather_data_dict["humidity"],
            wind_speed=weather_data_dict["wind_speed"],
            wind_degree=weather_data_dict["wind_deg"],
            cloudiness_pct=weather_data_dict["clouds"],
            weather_description=weather_data_dict["weather"][0]["description"],
            probability_of_precipitation=weather_data_dict["pop"],
            rain_volume=rain_volume,
            uv_index=weather_data_dict["uvi"],
        )

    def get_daily(self) -> List[DailyForecastWeatherData]:

        """
        Get the next seven days of daily weather data
        """

        response = self.get()["daily"]  # a list of dicts containing weather params
        # map each elem in the list into a function that parses each of the kv pairs into a WeatherData object
        return list(map(self._parse_daily, response))

    def get_hourly(self) -> List[HourlyForecastWeatherData]:

        """
        Get the next two days of hourly weather data
        """

        response = self.get()["hourly"]
        return list(map(self._parse_hourly, response))
