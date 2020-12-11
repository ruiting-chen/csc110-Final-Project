"""TODO: Write docstring"""

import data_process
from data_process import processed_sea_level_data, process_sea_level_csv
from climate_sea_level_system import ClimateSeaLevelSystem
from creates import CreateStation, CreateTemperature, CreateSeaLevel


class EntityGenerator:
    """An abstract class that generate all entities."""

    def generate(self, system: ClimateSeaLevelSystem) -> None:
        """generating new entities based on the data collected.
       """
        raise NotImplementedError


class GenerateTemperature(EntityGenerator):
    """A class that is responsible for generating temperatures."""

    def generate(self, system: ClimateSeaLevelSystem) -> None:
        """Mutate system by generating temperatures.
        """
        lst_temp = data_process.process_temperature_data()
        for temp in lst_temp:
            new_temp = CreateTemperature(temp[0], temp[1])
            new_temp.create(system)


class GenerateStationAndSeaLevel(EntityGenerator):
    """A class that is responsible for generating station.
    """

    def generate(self, system: ClimateSeaLevelSystem) -> None:
        """Mutate system by generating stations.
        """
        station_list = processed_sea_level_data.keys()
        for station in station_list:
            location = processed_sea_level_data[station][0]
            lst = process_sea_level_csv(station)
            lst_sea_level = []
            for detail in lst:
                creator = CreateSeaLevel(detail[0], detail[1], station)
                sea_level = creator.create(system)
                lst_sea_level.append(sea_level)
            create_station = CreateStation(station, location, lst_sea_level)
            create_station.create(system)
