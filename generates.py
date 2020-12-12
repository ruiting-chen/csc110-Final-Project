"""TODO: Write docstring"""

import data_process
from data_process import processed_sea_level_data, process_single_sea_level
from climate_sea_level_system import ClimateSeaLevelSystem
from entities import Station, Temperature


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
        print("All temperatures are added")


class GenerateStationAndSeaLevel(EntityGenerator):
    """A class that is responsible for generating station.
    """

    def generate(self, system: ClimateSeaLevelSystem) -> None:
        """Mutate system by generating stations.
        """
        station_dict = processed_sea_level_data.keys()
        for station in station_dict:
            if len(system.get_station()) >= 2:
                break
            location = processed_sea_level_data[station][0]
            sea_level = process_single_sea_level(station)
            min_height = min(sea_level[0][data] for data in sea_level[0])
            max_height = max(sea_level[0][data] for data in sea_level[0])
            new_station = Station(station, location, sea_level[0], min_height, max_height)
            system.add_station(new_station)
            system.add_sea_level_date(sea_level[1])
            print(f'{station} is added. Please be patient')
            print(f'{50 - len(system.get_station())} is left')

    def generate_one(self, system: ClimateSeaLevelSystem, station: str) -> None:
        """Mutate system by generating stations.
        """
        location = processed_sea_level_data[station][0]
        sea_level = process_single_sea_level(station)
        min_height = min(sea_level[0][data] for data in sea_level[0])
        max_height = max(sea_level[0][data] for data in sea_level[0])
        new_station = Station(station, location, sea_level[0], min_height, max_height)
        system.add_station(new_station)
        system.add_sea_level_date(sea_level[1])
        print(f'{station} is added')
