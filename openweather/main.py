from openweather.models.models import Geocode, CurrentWeatherData
import logging

logger = logging.getLogger(__name__)

geocoder = Geocode()
geocode = geocoder.get("Kuala Lumpur", "MY")
current_weather_data = CurrentWeatherData()
print(current_weather_data.get(geocode.latitude, geocode.longitude))
