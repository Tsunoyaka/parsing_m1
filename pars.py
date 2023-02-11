import requests
from bs4 import BeautifulSoup, Tag, ResultSet
from db import Hotel


def get_html(url: str, headers: dict='', params: str=''):
    html = requests.get(
        url,
        headers=headers,
        params=params,
        verify=False
    )
    return html.text


def get_cards_from_html(html: str) -> ResultSet:
    soup = BeautifulSoup(html, 'lxml')
    cards: ResultSet = soup.find_all('div', class_="search-item")
    return cards


def get_card(cards: list) -> list:
    list_ = []
    for card in cards:
        clearfix = card.find('div', class_='clearfix')
        title = clearfix.find('div', class_='title').text.strip()
        try:
            image = clearfix.find('div', class_='left-col').find('picture').find('img').get('data-src')
        except AttributeError:
            image = None
        try:
            price = int(clearfix.find('div', class_='price').text.strip().strip('$').replace(',', '')[:-3])
        except ValueError:
            price = None
        date = clearfix.find('div', class_='location').find('span', class_='date-posted').text.strip('< ')
        obj = {
        'title': title,
        'image': image,
        'price': price,
        'date': date
        }
        list_.append(obj)
    return list_


def pagination_pars() -> list:
    list_ = []
    for i in range(100):
        HOST = f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{i+1}/c37l1700273?ad=offering'
        HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
        html = get_html(HOST, HEADERS)
        cards = get_cards_from_html(html)
        db = get_card(cards)
        list_.extend(db)
    return list_


def create_hotel_in_db():
    pag_par = pagination_pars()
    for hotel in pag_par:
        hotel_db = Hotel.create(title=hotel['title'], image=hotel['image'], price=hotel['price'], date_=hotel['date'])
    print('Ваша БД заполнена!')

if __name__ == '__main__':
    create_hotel_in_db()
    