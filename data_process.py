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
        if int(data[6][:4]) < 1990:
            l = [data[6], data[7], (float(data[5]), float(data[4])), data[8]]
            useful_data[data[2]] = l
    return useful_data


processed_sea_level_data = process_sea_level_data()


def process_temperature_data() -> List[List[Any]]:
    """Return a list of Global component of Climate at a Glance (GCAG) data
    extracted from the website we found.
    The url of the website is https://datahub.io/core/global-temp/datapackage.json"""
    package = Package('https://datahub.io/core/global-temp/datapackage.json')
    temp_lst = []

    # get monthly temperature csv data
    for resource in package.resources:
        if resource.descriptor['name'] == 'monthly_csv':
            temp_raw_lst = resource.read()
            temp_lst = [temp_raw_lst[i][1:] for i in range(0, len(temp_raw_lst)) if i % 2 == 0]

    # change the temperature in temp_lst to float type
    for data in temp_lst:
        data[1] = float(data[1])

    return temp_lst


def average(lst: List[List[Any]]) -> dict:
    """Return a dictionary containing each month of each year that have valid measurements and
             the average of all measurements during that month."""
    average_dict = {}
    for measure in lst:
        year_month = datetime.date(measure[0].year, measure[0].month, 6)
        if year_month not in average_dict:
            average_dict[year_month] = [measure[1]]
        else:
            average_dict[year_month].append(measure[1])

    for month in average_dict:
        average_dict[month] = mean(average_dict[month])

    return average_dict


def process_single_sea_level(station: Station) -> dict:
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
        if int(row[3]) >= 0:
            date = datetime.date(int(row[0]), int(row[1]), int(row[2]))
            height = int(row[3])
            new_lst = [date, height]
            lst.append(new_lst)

    return average(lst)
