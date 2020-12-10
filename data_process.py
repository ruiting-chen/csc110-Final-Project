from typing import List, Any
from bs4 import BeautifulSoup
import requests
from datapackage import Package


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
