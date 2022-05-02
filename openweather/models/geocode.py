from __future__ import annotations
from openweather.models.base import Base
from dataclasses import dataclass
import logging
import requests

logger = logging.getLogger(__name__)


@dataclass
class Geocode(Base):

    city: str = None
    country_code: str = None
    latitude: float = None
    longitude: float = None

    def __post_init__(self):
        self.endpoint = (
            f"{self._base_url}/geo/1.0/direct?q={self.city},"
            f" {self.country_code}&appid={self._api_key}"
        )

    def get(self) -> Geocode:
        logger.debug(
            f"Calling geocoding endpoint of city: {self.city} and country_code:"
            f" {self.country_code}"
        )
        response = requests.get(self.endpoint).json()[0]
        return Geocode(
            city=response["name"],
            country_code=response["country"],
            latitude=response["lat"],
            longitude=response["lon"],
        )
