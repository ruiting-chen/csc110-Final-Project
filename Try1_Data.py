from typing import Any, List
from bs4 import BeautifulSoup
import requests


url = 'http://uhslc.soest.hawaii.edu/data/fd.html'


def get_sea_level_info(link: str) -> List[List[str]]:
    """Return a list of sea level information extracted from the given html"""
    r = requests.get(link).text
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
