from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import os


@dataclass
class Base(ABC):

    base_url: str = field(default="https://api.openweathermap.org", repr=False)
    api_key: str = field(default=os.getenv("API_KEY"), repr=False)

    @abstractmethod
    def get(self):
        pass