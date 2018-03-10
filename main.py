import environment

# libraries imports
import requests
from bs4 import BeautifulSoup
import re
import os
import json
import time
import pandas as pd

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
        person_info = item.find('a', {'class': 'player_name_players_table'})['href']

        version_info = item.find('span', {'class': 'rating'})['class'][2:-1]
        version_info.reverse()

        club_info = info.select('a')[0]
        nation_info = info.select('a')[1]
        league_info = info.select('a')[2]

        count_games = int(item.find('td', {'class': 'num_td'}).text.replace(',', ''))

        tmp_dict = {
            'player_id': int(re.findall('\d+', person_info)[1]),
            'name': main[0 : main.find(' (')],
            'position': main[main.find('(') + 1 : main.find(' )')],
            'rating': int(item.find('span', {'class': 'rating'}).text),
            'person_page': person_info,
            'img': main_img,
            'games': count_games,
            'club': {
                'id': int(re.findall('\d+', club_info['href'])[2]),
                'name': club_info['data-original-title'],
                'img': club_info.find('img')['src']
            },
            'nation': {
                'id': int(re.findall('\d+', nation_info['href'])[2]),
                'name': nation_info['data-original-title'],
                'img': nation_info.find('img')['src']
            },
            'league': {
                'id': int(re.findall('\d+', league_info['href'])[2]),
                'name': league_info['data-original-title'],
                'img': league_info.find('img')['src']
            },
            'version': {
                'quality': version_info[1],
                'type': version_info[0],
                'special': version_info[len(version_info) - 1] if len(version_info) == 3 else 'null'
            },
            'price': {
                'ps4': item.find('span', {'class': 'ps4_color'}).text,
                'xb1': item.find('span', {'class': 'xb1_color'}).text
            }
        }

        data_table.append(tmp_dict)

# saving data to CSV format
df = pd.DataFrame(data_table)
df.to_csv('data.csv', encoding = 'utf-8')    