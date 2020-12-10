"""TODO: Write docstring
"""
import data_process
from entities import Station, Temperature, SeaLevel
from climate_sea_level_system import ClimateSeaLevelSystem


class EntityGenerator:
    """An abstract class that generate all entities."""

    def generate(self, system: ClimateSeaLevelSystem, entity=None) -> None:
        """Mutate the given food delivery system to process this event.
        """
        raise NotImplementedError


class GenerateTemperature(EntityGenerator):
    """A class that is responsible for generating temperatures."""

    def generate(self, system: ClimateSeaLevelSystem, entity=None) -> None:
        """Mutate system by generating temperatures.
        """
        lst_temp = data_process.process_temperature_data()
        for temp in lst_temp:
            new_temp = Temperature(temp[0], temp[1])
            system.add_temperature(new_temp)


class GenerateSeaLevel(EntityGenerator):
    """A class that is responsible for generating sea-level.
    """

    def generate(self, system: ClimateSeaLevelSystem, sea_level=None) -> None:
        """Mutate system by generating sea-levels.
        """
        new_measure = SeaLevel(sea_level.date, sea_level.height, sea_level.station)
        system.add_sea_level(new_measure)


class GenerateStation(EntityGenerator):
    """A class that is responsible for generating station.
    """

    def generate(self, system: ClimateSeaLevelSystem, entity=None) -> None:
        """Mutate system by generating stations.
        """
        station_list = data_process.processed_sea_level_data.keys()
        for station in station_list:
            new_station = Station(station, station_list[station][0], [])
            lst = data_process.process_sea_level_csv(station)
            for detail in lst:
                sea_level = SeaLevel(detail[0], detail[1], new_station)
                temp = GenerateSeaLevel()
                temp.generate(system, sea_level)
                new_station.sea_level.append(sea_level)
            system.add_station(new_station)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['dataclasses', 'datetime', 'python_ta.contracts', 'random',
                          'entities', 'food_delivery_system', 'generate_data'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'R0201']
    })
