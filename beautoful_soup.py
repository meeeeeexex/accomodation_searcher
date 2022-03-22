import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta


def db_create():
    con = sqlite3.connect('flats.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE flets
                   (house_title text, price text, description text, date text)''')
    con.commit()
    return con, cur


def db_conect():
    con = sqlite3.connect('flats.db')
    cur = con.cursor()
    return con, cur


con, cur = db_conect()
base_url = 'https://dom.ria.com/'
res = requests.get('https://dom.ria.com/uk/arenda-kvartir/ivano-frankovsk/')
soup = BeautifulSoup(res.text, 'html.parser')

all_house = soup.find_all("div", {"class": "wrap_desc"})
all_price = soup.find_all("div", {"class": "flex f-center"})
all_desc = soup.find_all("div", {"class": "mt-15 text pointer desc-hidden"})

prices_storage, houses_storage, descriptions_storage, dates_storage = [], [], [], []
for price in all_price:
    # print(price.b.text)
    prices_storage.append(price.b.text)

for house in all_house:
    post_date = house.time.text.lower().strip()
    # print(post_date)
    if 'вчора' in post_date:
        post_date = datetime.now().date() - timedelta(days=1)
        # print(post_date)
    elif 'сьогодні' in post_date:
        post_date = datetime.now().date()
    dates_storage.append(post_date)
    houses_storage.append(house.h2.a['title'])
    # print(f_house.h2.a['href'])

for description in all_desc:
    # print(description.text)
    descriptions_storage.append(description.text)

all_storage = []
for (house, price, description, dates) in zip(houses_storage, prices_storage, descriptions_storage, dates_storage):
    all_storage.append((house, price, description, dates))
cur.executemany(f"INSERT OR IGNORE INTO flets VALUES (?,?,?,?)", all_storage)

con.commit()
con.close()
