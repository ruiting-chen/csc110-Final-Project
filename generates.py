"""TODO: Write docstring"""

import data_process
from data_process import processed_sea_level_data, process_single_sea_level
from climate_sea_level_system import ClimateSeaLevelSystem
# from creates import CreateStation, CreateTemperature, CreateSeaLevel
from entities import Station, Temperature, SeaLevel


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
            new_temp = Temperature(temp[0], temp[1])
            system.add_temperature(new_temp)


class GenerateStationAndSeaLevel(EntityGenerator):
    """A class that is responsible for generating station.
    """

    def generate(self, system: ClimateSeaLevelSystem) -> None:
        """Mutate system by generating stations.
        """
        station_list = processed_sea_level_data.keys()
        for station in station_list:
            location = processed_sea_level_data[station][0]
            sea_level = process_single_sea_level(station)
            lst_sea_level = []
            for detail in sea_level:
                sea_level_obj = SeaLevel(detail[0], detail[1])
                system.add_sea_level(sea_level_obj)
                lst_sea_level.append(sea_level_obj)
            new_station = Station(station, location, lst_sea_level)
            system.add_station(new_station)