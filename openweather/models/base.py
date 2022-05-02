from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod
import os


@dataclass
class Base(ABC):

    _base_url: str = field(default="https://api.openweathermap.org", repr=False)
    _api_key: str = field(default=os.getenv("API_KEY"), repr=False)

    @abstractmethod
    def get(self):
        pass

    def stringify(self):
        return asdict(self, dict_factory=self._dataclass_dict_factory)

    def _dataclass_dict_factory(self, data: dict) -> dict:

        """
        Dict factory method for dataclasses asdict() to filter out sensitive fields
        """
        return {x[0]: x[1] for x in data if x[0] not in ("_base_url", "_api_key")}
