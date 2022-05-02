from openweather.models.onecall import OneCallAPI
from openweather.models.geocode import Geocode
from openweather.models.weather import CurrentWeatherData
import logging

logger = logging.getLogger(__name__)

geocoder = Geocode(city="Kuala Lumpur", country_code="MY")
geocode = geocoder.get()
current_weather_data = CurrentWeatherData(geocoder=geocode)
print(current_weather_data.get().stringify())
onecall_api = OneCallAPI(geocoder=geocode)
print(onecall_api.get_current().stringify())
