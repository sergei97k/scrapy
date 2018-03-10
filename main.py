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

## get files
lst = os.listdir('./data_lists/')
lst.sort()

for filename in lst:
    if filename.find('html') == -1:
        continue
    filepath = './data_lists/' + filename
    
    with open(filepath) as input_file:
        text = input_file.read()     
    
    soup = BeautifulSoup(text, "lxml")
    items = soup.find('table', {'class': 'table-hover'}).find('tbody').find_all('tr')

    for item in items:
        main = item.find('a', {'class': 'player_name_players_table'}).text
        info = item.find('span', {'class': 'players_club_nation'})
        main_img = item.find('img', {'class': 'player_img'})['src']
        version_info = item.find('span', {'class': 'rating'})['class'][2:-1]
        version_info.reverse()

        tmp_dict = {
            'name': main[0 : main.find(' (')],
            'position': main[main.find('(') + 1 : main.find(' )')],
            'club': {
                'name': info.select('a')[0]['data-original-title'],
                'img': info.select('a')[0].find('img')['src']
            },
            'nation': {
                'name': info.select('a')[1]['data-original-title'],
                'img': info.select('a')[1].find('img')['src']
            },
            'league': {
                'name': info.select('a')[2]['data-original-title'],
                'img': info.select('a')[2].find('img')['src']
            },
            'img': main_img,
            'version': {
                'quality': version_info[1],
                'type': version_info[0],
                'special': version_info[len(version_info) - 1] if len(version_info) == 3 else 'null'
            },
            'rating': int(item.find('span', {'class': 'rating'}).text)
        }

        data_table.append(tmp_dict)
        print(tmp_dict)
    
# print(data_table)