import sys
import requests
import csv
from bs4 import BeautifulSoup
from time import sleep

hashes = []


def request(link):
    try:
        req = requests.get(link)
        return req.text
    except requests.exceptions.RequestException:
        return


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    themes = soup.findAll('div', class_='structItem')
    for theme in themes:
        theme_author = theme.get('data-author')
        theme_link = theme.find('div', class_='structItem-title').find('a').get('href')
        theme_name = theme.find('div', class_='structItem-title').find('a').next
        last_update = theme.find('time', class_='structItem-latestDate u-dt').get('title')
        last_update_author = theme.find('div', class_='structItem-cell structItem-cell--latest').find('div', class_='structItem-minor').find('a').next
        yield (theme_name, theme_link, last_update, last_update_author, theme_author)


def write_csv(filename, rows):
    with open(filename, 'a') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(rows)


def main(filename, link):
    while True:
        html = request(link)
        data = []
        if html:
            generator = parse(html)
            for row in generator:
                if check(row):
                    data.append(row)
        write_csv(filename, data)
        sleep(10)


def get_hash(row):
    return hash(str(row[0]) + str(row[2]) + str(row[3]))


def check(row):
    global hashes
    hashed_row = get_hash(row)  # Функция для проверки темы, является ли она новой. Берем хэш и сохраняем в памяти
    if hashed_row in hashes:  # хэши постов, которые уже добавили
        return False
    hashes.append(hashed_row)
    return True


if __name__ == '__main__':
    filename = 'themes.csv'
    link = sys.argv[1] # Проверял для https://sharewood.pro/whats-new/

    main(filename, link)
