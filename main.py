import environment

# libraries imports
import requests
from bs4 import BeautifulSoup
import re
import os
import json
import time

PAGE_COUNT = environment.PAGE_COUNT
URL = environment.URL

def load_data(page):
    url = URL % (page)
    r = requests.get(url)
    return r.text


# loading files
page = 1
while page <= PAGE_COUNT:
    data = load_data(page)
    with open('./data_lists/page_%d.html' % (page), 'w') as output_file:
        output_file.write(data)
        page += 1


# parse data
data_table = []

for filename in os.listdir('./data_lists/'):
    print(filename)
    if filename.find('html') == -1:
        continue
    filepath = './data_lists/' + filename
    
    with open(filepath) as input_file:
        text = input_file.read()     
    
    soup = BeautifulSoup(text, "lxml")
    items = soup.find('table', {'class': 'table-hover'}).find('tbody').find_all('tr')

    for item in items:
        tmp_dict = {
            'name': item.find('a', {'class': 'player_name_players_table'}).text
        }
        data_table.append(tmp_dict)
    
print(data_table)