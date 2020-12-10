"""CSC110 Fall 2020: Food Delivery System Entities

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 David Liu and Mario Badr.
"""
from __future__ import annotations

from dataclasses import dataclass
import datetime
from typing import Dict, Tuple, Optional


@dataclass
class Restaurant:
    """A place that serves food.

    Instance Attributes:
      - name: the name of the restaurant
      - address: the address of the restaurant
      - menu: the menu of the restaurant with the name of the dish mapping to
        the price
      - location: the location of the restaurant as (latitude, longitude)

    Representation Invariants:
      - self.name != ''
      - self.address != ''
      - all(self.menu[item] >= 0 for item in self.menu)
      - -90 <= self.location[0] <= 90
      - -180 <= self.location[1] <= 180

    Sample Usage:
    >>> mcdonalds = Restaurant(name='McDonalds', address='160 Spadina Ave',\
                               menu={'fries': 4.5}, location=(43.649, -79.397))
    """
    name: str
    address: str
    menu: Dict[str, float]
    location: Tuple[float, float]


@dataclass
class Customer:
    """A person who orders food.

    Instance Attributes:
      - name: the name of the customer
      - location: the location of the customer as (latitude, longitude)

    Representation Invariants:
      - self.name != ''
      - -90 <= self.location[0] <= 90
      - -180 <= self.location[1] <= 180

    Sample Usage:

    >>> david = Customer('David', (44.649, -79.115))
    """
    name: str
    location: Tuple[float, float]


@dataclass
class Order:
    """A food order from a customer.

    Instance Attributes:
      - customer: the customer who placed this order
      - restaurant: the restaurant the order is placed for
      - food_items: a mapping from names of food to the quantity being ordered
      - start_time: the time the order was placed
      - courier: the courier assigned to this order (initially None)
      - end_time: the time the order was completed by the courier (initially None)

    Representation Invariants:
      - self.food_items != {}
      - all(self.food_items[item] > 0 for item in self.food_items)

    Sample Usage:

    >>> david = Customer('David', (43.671, -79.413))
    >>> mcdonalds = Restaurant(name='McDonalds', address='160 Spadina Ave',\
                               menu={'fries': 4.5}, location=(43.649, -79.397))
    >>> order = Order(customer=david, restaurant=mcdonalds,\
                      food_items={'fries': 10},\
                      start_time=datetime.datetime(2020, 11, 5, 11, 30))
    >>> order.courier is None  # Illustrating default values
    True
    >>> order.end_time is None
    True
    """
    customer: Customer
    restaurant: Restaurant
    food_items: Dict[str, int]
    start_time: datetime.datetime
    courier: Optional[Courier] = None
    end_time: Optional[datetime.datetime] = None


###############################################################################
# Exercise 1: Designing a `Courier` data class
###############################################################################
@dataclass
class Courier:
    """A person who delivers food orders from restaurants to customers.
    """


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod(verbose=True)

    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['dataclasses', 'datetime', 'python_ta.contracts'],
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    # })
