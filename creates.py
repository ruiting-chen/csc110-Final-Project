"""TODO: Write docstring
"""
from entities import Station, Temperature, SeaLevel
from climate_sea_level_system import ClimateSeaLevelSystem
import datetime
from typing import List, Tuple


class CreateEntity:
    """An abstract class that create all entities."""

    def create(self, system: ClimateSeaLevelSystem) -> None:
        """Mutate the given ClimateSeaLevelSystem to create new entities.
        """
        raise NotImplementedError


class CreateStation(CreateEntity):
    """A class that is responsible for creating station.
    """
    # Private Attribute:
    #    - _name: name of a station
    #    - _location: location represented in (longitude, latitude)
    #    - _sea_level: a list containing all its sea-level data at different time.
    _name: str
    _location: Tuple[float, float]
    _sea_level: List[SeaLevel]

    def __init__(self, name: str, location: Tuple[float, float], sea_level: List[SeaLevel]):
        self._name = name
        self._location = location
        self._sea_level = sea_level

    def create(self, system: ClimateSeaLevelSystem) -> None:
        """Mutate system by creating stations.
        """
        new_station = Station(self._name, self._location, self._sea_level)
        system.add_station(new_station)


class CreateMeasurement(CreateEntity):
    """An abstract class that create all measurements."""

    # Private Attribute:
    #   - _date: The date when a certain measurement is made.
    #   _ _measurement: The measurement made at the date.
    _date: datetime.date
    _measurement: float

    def __init__(self, date: datetime.date, measurement: float):
        self._date = date
        self._measurement = measurement

    def create(self, system: ClimateSeaLevelSystem) -> None:
        """Mutate the given ClimateSeaLevelSystem to create new measurements.
       """
        raise NotImplementedError


class CreateTemperature(CreateMeasurement):
    """A class that is responsible for creating temperatures."""

    def create(self, system: ClimateSeaLevelSystem) -> None:
        """Mutate system by creating temperatures.
        """
        new_temperature = Temperature(self._date, self._measurement)
        system.add_temperature(new_temperature)


class CreateSeaLevel(CreateMeasurement):
    """A class that is responsible for creating sea-level.
    """
    # Private Attribute:
    #   - _station: The name of the station at where a certain measurement is made.
    _station: str

    def __init__(self, date: datetime.date, measurement: float, station: str):
        CreateMeasurement.__init__(self, date, measurement)
        self._station = station

    def create(self, system: ClimateSeaLevelSystem) -> SeaLevel:
        """Mutate system by creating sea-levels.

        Return the created sea-level to be used in GenerateStation
        """
        new_measure = SeaLevel(self._date, self._measurement, self._station)
        system.add_sea_level(new_measure)
        return new_measure


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['dataclasses', 'datetime', 'python_ta.contracts', 'random',
                          'entities', 'food_delivery_system', 'generate_data'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'R0201']
    })
