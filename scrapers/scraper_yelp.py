'''
@author Samantha Comeau
@email  sjcomeau@wpi.edu
'''

import requests
import json
from lxml import html

from activity import Activity

class Yelp:
    
    def __init__(self):
        pass 

    def build_url(self, city, state):
        return "https://yelp.com/search?find_desc=things%20to%20do&find_loc="+city+"%2C%20"+state 

    
