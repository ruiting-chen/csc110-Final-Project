"""TODO: write docstring"""
from typing import List, Any, Dict
from bs4 import BeautifulSoup
import requests
import datetime
from datapackage import Package
from entities import Station
from statistics import mean
import urllib.request
import csv


def get_sea_level_data() -> List[List[str]]:
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


def process_sea_level_data() -> dict:
    """Return a list of sea level data in the form that we are going to use"""
    all_data = get_sea_level_data()
    useful_data = {}
    for data in all_data:
        l = [(float(data[5]), float(data[4])), data[8]]
        useful_data[data[2]] = l
    return useful_data


processed_sea_level_data = process_sea_level_data()


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


def process_sea_level_csv(station: Station) -> List[List[Any]]:
    """This function will extract sea-level data from the internet.

    This function will promote the caller to type in a station that he want to check out.
    Base on the station the user typed in, this function will extract the corresponding
    sea-level data from the internet.

    If the input station is not among the ones promoted, an InvalidStationError will occur."""
    csv_web = processed_sea_level_data[station][1]
    csv_file = urllib.request.urlopen(csv_web)
    lst_line = [line.decode('utf-8') for line in csv_file.readlines()]
    read = csv.reader(lst_line)

    lst = []
    for row in read:
        if int(row[3]) > 0:
            date = datetime.date(int(row[0]), int(row[1]), int(row[2]))
            height = row[3]
            new_lst = [date, height]
            lst.append(new_lst)
    return lst


class InvalidStationError(Exception):
    """This exception will raise if the input station is not among the ones promoted."""

    def __str__(self):
        return 'The input station is not among the ones promoted.'