from openweather.models.geocode import Geocode
from openweather.models.weather import CurrentWeatherData
from openweather.models.air_pollution import CurrentAirPollutionData
from openweather.utils.utils import fetch_data_and_write_to_db
from sqlalchemy import create_engine
import schedule
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    # get current weather and air pollution data once every 1 minute and write into sqlite3

    geocoders = [
        Geocode(city="Kuala Lumpur", country_code="MY"),
        Geocode(city="Seremban", country_code="MY"),
        Geocode(city="Ipoh", country_code="MY"),
        Geocode(city="Malacca", country_code="MY"),
        Geocode(city="Johor Bahru", country_code="MY"),
        Geocode(city="Kuala Perlis", country_code="MY"),
        Geocode(city="Kota Bharu", country_code="MY"),
        Geocode(city="Kuala Terengganu", country_code="MY"),
        Geocode(city="Kuantan", country_code="MY"),
        Geocode(city="Kota Tinggi", country_code="MY"),
        Geocode(city="Klang", country_code="MY"),
        Geocode(city="George Town", country_code="MY"),
        Geocode(city="Tanah Rata", country_code="MY"),
        Geocode(city="Mersing", country_code="MY"),
        Geocode(city="Bentong", country_code="MY"),
        Geocode(city="Singapore", country_code="SG"),
    ]
    engine = create_engine("sqlite:///openweather.db")
    minutes_per_call = 1

    # user define - geocodes, sqlalchemy engine and minutes per call
    # current data - weather and air pollution
    # one location = 2 API calls
    # cannot have more than 30 locations per minute
    # abstract away other stuffs so that user does not need to write these code

    # make all the API calls for all the locations in one go
    # store in temporary memory
    # bulk write into database
    # do multithreading when making API calls and writing into temp memory

    for geocoder in geocoders:
        geocode = geocoder.get()
        current_weather = CurrentWeatherData(geocoder=geocode)
        current_air_pollution = CurrentAirPollutionData(geocoder=geocode)

        schedule.every(minutes_per_call).minutes.do(
            fetch_data_and_write_to_db,
            model_instance=current_weather,
            table_name="current_weather",
            engine=engine,
        )
        logger.info(f"Added schedule for fetching current weather data for {geocode}")
        schedule.every(minutes_per_call).minutes.do(
            fetch_data_and_write_to_db,
            model_instance=current_air_pollution,
            table_name="current_air_pollution",
            engine=engine,
        )
        logger.info(f"Added schedule for fetching current air pollution data for {geocode}")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
