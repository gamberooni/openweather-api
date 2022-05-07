from openweather.models.geocode import Geocode
from openweather.models.weather import CurrentWeatherData
from openweather.models.air_pollution import CurrentAirPollutionData
from openweather.utils.utils import fetch_data_and_write_to_db
from sqlalchemy import create_engine
import schedule
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    # get current weather and air pollution data once every 1 minute and write into sqlite3

    geocoder = Geocode(city="Kuala Lumpur", country_code="MY")
    geocode = geocoder.get()
    current_weather = CurrentWeatherData(geocoder=geocode)
    current_air_pollution = CurrentAirPollutionData(geocoder=geocode)
    engine = create_engine("sqlite:///openweather.db")

    schedule.every(1).minutes.do(
        fetch_data_and_write_to_db,
        model_instance=current_weather,
        table_name="current_weather",
        engine=engine,
    )
    schedule.every(1).minutes.do(
        fetch_data_and_write_to_db,
        model_instance=current_air_pollution,
        table_name="current_air_pollution",
        engine=engine,
    )

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
