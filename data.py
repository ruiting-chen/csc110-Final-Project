import csv, urllib.request
from typing import Any, List
from bs4 import BeautifulSoup
import requests

# The filepath of the 'data.csv' file
filepath = 'data.csv'

# The dictionary that contains all the stations and its
# corresponding portion of url.
dic = {}


def read_data_file() -> None:
    """Read the 'data.csv' file, and process the data contained inside.

    This function will mutate the dic so that it contain the station name as key
    and its corresponding portion of url as its value.

    Precondition:
        - the 'data.csv' and 'data.py' must be stored under the SAME directory.
    """
    with open(filepath) as file:
        reader = csv.reader(file)
        for row in reader:
            lst = row[0].split()
            if len(lst) > 2:
                dic[lst[2]] = f'd{lst[0]}'


# url = 'http://uhslc.soest.hawaii.edu/data/fd.html'


def get_sea_level_info() -> List[List[str]]:
    """Return a list of sea level information extracted from the website we found"""
    r = requests.get('http://uhslc.soest.hawaii.edu/data/fd.html').text
    soup = BeautifulSoup(r, features="html.parser")

    # get all the useful information(for example: city, country, location, .csv data link)
    # from the html code. information is stored in a list where every 12 element is a line
    # on the original website(excluding the header line)
    info = soup.find_all('td')

    # store the information from the website as a list
    info_lst = []
    for i in range(len(info) // 12):
        lst = []
        for j in range(0, 8):
            lst.append(info[i * 12 + j].text)
        lst.append(info[i * 12 + 9].find_all('a')[0].get('href'))
        info_lst.append(lst)
    return info_lst


def process_data() -> None:
    """This function will extract sea-level data from the internet.

    This function will promot the caller to type in a station that he want to check out.
    Base on the station the user typed in, this function will extract the corresponding
    sea-level data from the internet.

    If the input station is not among the ones promoted, an InvalidStationError will occur."""
    station = input(f'Which station do you want to see? Choose from {list(dic.keys())}')

    if station not in dic:
        raise InvalidStationError

    csv_web = f'http://uhslc.soest.hawaii.edu/data/csv/fast/daily/{dic[station]}.csv'
    csv_file = urllib.request.urlopen(csv_web)
    lst_line = [line.decode('utf-8') for line in csv_file.readlines()]
    read = csv.reader(lst_line)

    for row in read:
        print(row)


class InvalidStationError(Exception):
    """This exception will raise if the input station is not among the ones promoted."""

    def __str__(self):
        return 'The input station is not among the ones promoted.'


def have_fun() -> None:
    """This function integrate the previous two functions in a user-friendly way.

    Precondition:
        - the 'data.csv' and 'data.py' must be stored under the SAME directory.
    """
    read_data_file()
    process_data()
