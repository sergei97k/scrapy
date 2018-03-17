import environment

# libraries imports
import requests
from bs4 import BeautifulSoup
import re
import os
import json
import time
import pandas as pd
from collections import OrderedDict
import pymongo
from pymongo import MongoClient

#connect to db
client = MongoClient()

PAGE_COUNT = environment.PAGE_COUNT
URL = environment.URL
LIMIT_GAMES = environment.LIMIT_GAMES

data_table = []

def load_data(page):
    url = URL % (page)
    r = requests.get(url)
    return r.text


# loading files
def loadFiles():
    page = 1
    while page <= PAGE_COUNT:
        data = load_data(page)
        with open('./data_lists/page_%d.html' % (page), 'w') as output_file:
            output_file.write(data)
            print(page)
            page += 1


# parse data
## get files
def getFilesData():
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
            count_games = int(item.find('td', {'class': 'num_td'}).text.replace(',', ''))

            if count_games >= LIMIT_GAMES:
                main = item.find('a', {'class': 'player_name_players_table'}).text
                info = item.find('span', {'class': 'players_club_nation'})
                main_img = item.find('img', {'class': 'player_img'})['src']
                person_info = item.find('a', {'class': 'player_name_players_table'})['href']

                version_info = item.find('span', {'class': 'rating'})['class'][2:-1]
                version_info.reverse()

                club_info = info.select('a')[0]
                nation_info = info.select('a')[1]
                league_info = info.select('a')[2]

                tmp_dict = OrderedDict([
                    ('player_id', int(re.findall('\d+', person_info)[1])),
                    ('name', main[0 : main.find(' (')]),
                    ('position', main[main.find('(') + 1 : main.find(' )')]),
                    ('rating', int(item.find('span', {'class': 'rating'}).text)),
                    ('person_page', person_info),
                    ('img', main_img),
                    ('games', count_games),
                    ('club_id', int(re.findall('\d+', club_info['href'])[2])),
                    ('club_name', club_info['data-original-title']),
                    ('club_img', club_info.find('img')['src']),
                    ('nation_id', int(re.findall('\d+', nation_info['href'])[2])),
                    ('nation_name', nation_info['data-original-title']),
                    ('nation_img', nation_info.find('img')['src']),
                    ('league_id', int(re.findall('\d+', league_info['href'])[2])),
                    ('league_name', league_info['data-original-title']),
                    ('league_img', league_info.find('img')['src']),
                    ('version_quality', version_info[1]),
                    ('version_type', version_info[0]),
                    ('version_special', version_info[len(version_info) - 1] if len(version_info) == 3 else 'null'),
                    ('price_ps4', item.find('span', {'class': 'ps4_color'}).text),
                    ('price_xb1', item.find('span', {'class': 'xb1_color'}).text)
                ])

                data_table.append(tmp_dict)
            else:
                break

# saving data to CSV format
def saveToCsv():
    df = pd.DataFrame(data_table)
    df.to_csv('data.csv', encoding = 'utf-8', index=False)

if __name__ == '__main__':
    loadFiles()
    getFilesData()
    saveToCsv()

    db = client.test;
    print(db);