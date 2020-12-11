"""TODO: Write docstring"""

import data_process
from data_process import processed_sea_level_data, process_single_sea_level
from climate_sea_level_system import ClimateSeaLevelSystem
from entities import Station, Temperature, SeaLevel


class EntityGenerator:
    """An abstract class that generate all entities."""

    def generate(self, system: ClimateSeaLevelSystem, entity=None) -> None:
        """generating new entities based on the data collected.
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
        print("All temperatures are added")


class GenerateStationAndSeaLevel(EntityGenerator):
    """A class that is responsible for generating station.
    """

    def generate_all(self, system: ClimateSeaLevelSystem) -> None:
        """Mutate system by generating stations.
        """
        station_list = processed_sea_level_data.keys()
        for station in station_list:
            if len(system.get_station()) >= 20:
                break
            location = processed_sea_level_data[station][0]
            sea_level = process_single_sea_level(station)
            new_station = Station(station, location, sea_level)
            system.add_station(new_station)
            print(f'{station} is added. Please be patient')
            print(f'{50 - len(system.get_station())} is left')

    def generate(self, system: ClimateSeaLevelSystem, entity=None) -> None:
        """Mutate system by generating stations.
        """
        location = processed_sea_level_data[entity][0]
        sea_level = process_single_sea_level(entity)
        new_station = Station(entity, location, sea_level)
        system.add_station(new_station)
        print(f'{entity} is added')
