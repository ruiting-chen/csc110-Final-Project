import datetime
from typing import Dict

# This is the Python module containing the individual entity data classes.
from entities import Temperature, Station, SeaLevel


class ClimateSeaLevelSystem:
    """A system that maintains all entities (temperature, station, and sea-level).

    Representation Invariants:
        - all(name == self._stations[name].name for name in self._stations)
    """
    # Private Instance Attributes:
    #   - _temperatures: a mapping from the date when a measure of the global
    #       temperature is made to the measurement.
    #       This represents all the temperatures in the system.
    #   - _sea_levels: a mapping from the date when a measure of the sea_level
    #       of a certain station is made to SeaLevel object.
    #       This represents all the sea-levels in the system.
    #   - _stations: a mapping from station name to Station object.
    #       This represents all the stations in the system.

    _temperatures: Dict[datetime.date, Temperature]
    _sea_levels: Dict[(datetime.date, Station), SeaLevel]
    _stations: Dict[str, Station]

    def __init__(self) -> None:
        """Initialize a new food delivery system.

        The system starts with no entities.
        """
        self._temperatures = {}
        self._sea_levels = {}
        self._stations = {}

    def add_temperature(self, temperature: Temperature) -> bool:
        """Add the given temperature to this system.

        Do NOT add the temperature if one with the same date already exists.

        Return whether the temperature was successfully added to this system.
        """
        identifier = temperature.date
        if identifier in self._temperatures:
            return False
        self._temperatures[identifier] = temperature
        return True

    def add_sea_level(self, sea_level: SeaLevel) -> bool:
        """Add the given SeaLevel to this system.

        Do NOT add the sea_level if one with the same date and station already exists.

        Return whether the SeaLevel was successfully added to this system.
        """
        identifier = (sea_level.date, sea_level.station)
        if identifier in self._sea_levels:
            return False
        self._sea_levels[identifier] = sea_level
        return True

    def add_station(self, station: Station) -> bool:
        """Add the given station to this system.

        Do NOT add the station if one with the same name already exists.

        Return whether the station was successfully added to this system.
        """
        identifier = station.name
        if identifier in self._stations:
            return False
        self._stations[identifier] = station
        return True


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod(verbose=True)

    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['dataclasses', 'datetime', 'python_ta.contracts', 'math', 'entities'],
    #     'allowed-io': ['run_example'],
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200', 'R0201']
    # })
