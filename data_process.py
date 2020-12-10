"""TODO: write docstring"""
from typing import List, Any, Dict
from bs4 import BeautifulSoup
import requests
import datetime
from datapackage import Package
from entities import Station
from statistics import mean


def process_sea_level_info() -> List[List[str]]:
    """Return a list of sea level information extracted from the website we found.
    The url of the website is http://uhslc.soest.hawaii.edu/data/fd.html"""
    r = requests.get('http://uhslc.soest.hawaii.edu/data/fd.html').text
    soup = BeautifulSoup(r, features="html.parser")
    info = soup.find_all('td')
    info_lst = []
    for i in range(len(info) // 12):
        new_l = []
        for j in range(0, 8):
            new_l.append(info[i * 12 + j].text)
        new_l.append(info[i * 12 + 9].find_all('a')[0].get('href'))
        info_lst.append(new_l)
    return info_lst


def process_temperature_data() -> List[List[Any]]:
    """Return a list of Global component of Climate at a Glance (GCAG) data
    extracted from the website we found.
    The url of the website is 'http://uhslc.soest.hawaii.edu/data/fd.html'"""
    package = Package('https://datahub.io/core/global-temp/datapackage.json')

    # get monthly temperature csv data
    for resource in package.resources:
        if resource.descriptor['name'] == 'monthly_csv':
            temp_raw_lst = resource.read()
            return [temp_raw_lst[i][1:] for i in range(0, len(temp_raw_lst)) if i % 2 == 0]


def average(station: Station) -> Dict[datetime.date, int]:
    """Return a dictionary containing each month of each year that have valid measurements and
             the average of all measurements during that month."""
    average_dict = {}
    for measure in station.sea_level:
        year_month = datetime.date(measure.date.year, measure.date.month, 1)
        if year_month not in average:
            average_dict[year_month] = [measure.height]
        else:
            average_dict[year_month].append(measure.height)

    for month in average_dict:
        mean_height = mean(average_dict[month])
        average_dict[month] = mean_height

    return average_dict
