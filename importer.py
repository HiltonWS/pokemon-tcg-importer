import base64
import requests

from pokemontcgsdk import RestClient, Card

from drive_service import upload_to_google_drive
from config import API_KEY, COLLECTION_SETS
from database import connection


RestClient.configure(API_KEY)


def __url_content_to_base64__(url):
    return base64.b64encode(requests.get(url).content).decode('utf-8')


def __read_file__(file_path):
    with open(file_path, 'r') as sql_file:
        return sql_file.read()


def __update_database__(data):
    con = connection()
    con.executescript(__read_file__('db/tables.sql'))
    con.execute(__read_file__('db/insert_set.sql'), (
        data['set']['id'],
        data['set']['name'],
        data['set']['series']
        ))
    con.execute(__read_file__('db/insert_card.sql'), (
        data['id'],
        data['number'],
        data['name'],
        data['image'],
        data['rarity'],
        data['eu_price'],
        data['set']['id']
        ))
    con.commit()
    con.close()


def __get_cards__():
    for set in COLLECTION_SETS:
        cards = Card.where(q="set.id:" + set, orderBy="number")
        for card_data in cards:
            card_data: Card = card_data
            card = {
                'id': card_data.id,
                'number': card_data.number,
                'name': card_data.name,
                'image': card_data.images.large,
                'rarity': card_data.rarity,
                'set': {
                    'id': card_data.set.id,
                    'name': card_data.set.name,
                    'series': card_data.set.series,
                },
                'eu_price': card_data.cardmarket.prices.averageSellPrice,
            }
            __update_database__(card)


if __name__ == "__main__":
    __get_cards__()
    upload_to_google_drive()
