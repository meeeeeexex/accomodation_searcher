import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
import argparse

parser = argparse.ArgumentParser()
cities = ['uzhgorod/', 'lvov/', 'chernovtsy/' 'ivano-frankovsk/']


def db_conect(arg):
    con = sqlite3.connect('flats.db')
    cur = con.cursor()
    if arg == True:
        cur.execute('''CREATE TABLE flets
                       (house_title text, price text, description text, link text, date text, PRIMARY KEY (link))''')
        con.commit()

    return con, cur


def main():
    base_url = 'https://dom.ria.com/'
    for city_name in cities:
        res = requests.get('https://dom.ria.com/uk/arenda-kvartir/' + city_name)
        soup = BeautifulSoup(res.text, 'html.parser')

        all_house = soup.find_all("div", {"class": "wrap_desc"})
        all_price = soup.find_all("div", {"class": "flex f-center"})
        all_desc = soup.find_all("div", {"class": "mt-15 text pointer desc-hidden"})

        all_storage = []

        for (price, house, description) in zip(all_price, all_house, all_desc):
            link = base_url + house.h2.a['href']
            post_date = house.time.text.lower().strip()
            if 'вчора' in post_date:
                post_date = datetime.now().date() - timedelta(days=1)
            elif 'сьогодні' in post_date:
                post_date = datetime.now().date()
            all_storage.append((house.h2.a['title'], description.text.strip(), price.b.text, link, post_date))

        cur.executemany(f"INSERT OR IGNORE INTO flets VALUES (?,?,?,?,?)", all_storage)
        cur.execute('''select count(*) from flets;''')
    final_length = cur.fetchall()[0][0]
    if current_length != final_length:
        print('message')
    con.commit()
    con.close()


if __name__ == '__main__':
    parser.add_argument("-v", "--verbose", help="if you are running for the first time",
                        action="store_true")
    args = parser.parse_args()
    con, cur = db_conect(arg=args.verbose)
    cur.execute('''select count(*) from flets;''')
    current_length = cur.fetchall()[0][0]
    main()
