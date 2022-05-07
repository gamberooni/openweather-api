from openweather.models.onecall import OneCallAPI
from openweather.models.geocode import Geocode
from openweather.models.weather import CurrentWeatherData
from openweather.models.air_pollution import (
    CurrentAirPollutionData,
    FiveDayHourlyForecastedAirPollutionData,
)
import logging

logger = logging.getLogger(__name__)

geocoder = Geocode(city="Kuala Lumpur", country_code="MY")
geocode = geocoder.get()

current_weather_data = CurrentWeatherData(geocoder=geocode)
print(current_weather_data.get().stringify())

onecall_api = OneCallAPI(geocoder=geocode)
print(onecall_api.get_current().stringify())

current_air_pollution_data = CurrentAirPollutionData(geocoder=geocode)
print(current_air_pollution_data.get())

five_day_air_pollution_data = FiveDayHourlyForecastedAirPollutionData(geocoder=geocode)
print(five_day_air_pollution_data.get())
