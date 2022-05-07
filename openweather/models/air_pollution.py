from __future__ import annotations
from dataclasses import dataclass
from typing import List
from openweather.models.base import Base
from openweather.models.geocode import Geocode
import requests
import logging

logger = logging.getLogger(__name__)


@dataclass
class AirPollutionData:

    geocoder: Geocode = None
    datetime: int = None
    air_quality_index: int = None
    carbon_monoxide: float = None
    nitrogen_monoxide: float = None
    nitrogen_dioxide: float = None
    ozone: float = None
    sulphur_dioxide: float = None
    fine_particles_matter: float = None
    coarse_particulate_matter: float = None
    ammonia: float = None


@dataclass
class CurrentAirPollutionData(AirPollutionData, Base):
    def __post_init__(self):
        self.endpoint = (
            f"{self._base_url}/data/2.5/air_pollution?lat={self.geocoder.latitude}"
            f"&lon={self.geocoder.longitude}&appid={self._api_key}"
        )

    def get(self) -> CurrentAirPollutionData:
        logger.debug(
            "Calling current air pollution data endpoint to get weather data of latitude:"
            f" {self.geocoder.latitude} and longitude: {self.geocoder.longitude}"
        )
        response = requests.get(self.endpoint).json()
        air_pollution_data = response["list"][0]
        return CurrentAirPollutionData(
            geocoder=self.geocoder,
            datetime=air_pollution_data["dt"],
            air_quality_index=air_pollution_data["main"]["aqi"],
            carbon_monoxide=air_pollution_data["components"]["co"],
            nitrogen_monoxide=air_pollution_data["components"]["no"],
            nitrogen_dioxide=air_pollution_data["components"]["no2"],
            ozone=air_pollution_data["components"]["o3"],
            sulphur_dioxide=air_pollution_data["components"]["so2"],
            fine_particles_matter=air_pollution_data["components"]["pm2_5"],
            coarse_particulate_matter=air_pollution_data["components"]["pm10"],
            ammonia=air_pollution_data["components"]["nh3"],
        )


@dataclass
class FiveDayHourlyForecastedAirPollutionData(AirPollutionData, Base):
    def __post_init__(self):
        self.endpoint = (
            f"{self._base_url}/data/2.5/air_pollution/forecast?lat={self.geocoder.latitude}"
            f"&lon={self.geocoder.longitude}&appid={self._api_key}"
        )

    def get(self) -> List[AirPollutionData]:
        logger.debug(
            "Calling 5-day forecasted air pollution data endpoint to get weather data of latitude:"
            f" {self.geocoder.latitude} and longitude: {self.geocoder.longitude}"
        )
        response = requests.get(self.endpoint).json()
        five_day_air_pollution_data_list = response["list"]
        return list(map(self._parse_hourly, five_day_air_pollution_data_list))

    def _parse_hourly(
        self, air_pollution_data_dict
    ) -> FiveDayHourlyForecastedAirPollutionData:
        return FiveDayHourlyForecastedAirPollutionData(
            geocoder=self.geocoder,
            datetime=air_pollution_data_dict["dt"],
            air_quality_index=air_pollution_data_dict["main"]["aqi"],
            carbon_monoxide=air_pollution_data_dict["components"]["co"],
            nitrogen_monoxide=air_pollution_data_dict["components"]["no"],
            nitrogen_dioxide=air_pollution_data_dict["components"]["no2"],
            ozone=air_pollution_data_dict["components"]["o3"],
            sulphur_dioxide=air_pollution_data_dict["components"]["so2"],
            fine_particles_matter=air_pollution_data_dict["components"]["pm2_5"],
            coarse_particulate_matter=air_pollution_data_dict["components"]["pm10"],
            ammonia=air_pollution_data_dict["components"]["nh3"],
        )
