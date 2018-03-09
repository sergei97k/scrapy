import environment
import requests

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
    with open('./page_%d.html' % (page), 'w') as output_file:
        output_file.write(data)
        page += 1
