import base64
import requests
import sqlite3

from pokemontcgsdk import RestClient, Card

from drive_service import upload_to_google_drive, download_from_google_drive
from config import API_KEY, COLLECTION_SETS
from database import connection
from file_service import read_file


RestClient.configure(API_KEY)


def __url_content_to_base64__(url):
    return base64.b64encode(requests.get(url).content).decode('utf-8')


def __execute_script__(con, file):
    try:
        con.executescript(read_file(file))
    except sqlite3.OperationalError as e:
        if 'duplicate column name: ' not in str(e):
            raise
        else:
            print(f"{e}")

def __init_database__(con):
    __execute_script__(con, "db/tables.sql")
    __execute_script__(con, "db/tables_1.sql")
    __execute_script__(con, "db/tables_2.sql")
    __execute_script__(con, "db/tables_3.sql")

def __update_database__(con, data):
    con.execute(read_file('db/insert_set.sql'), (
        data['set']['id'],
        data['set']['name'],
        data['set']['series'],
        data['set']['images']['symbol'],
        data['set']['images']['logo']
        ))
    con.execute(read_file('db/insert_card.sql'), (
        data['id'],
        data['number'],
        data['name'],
        data['image'],
        data['rarity'],
        data['eu_price'],
        data['set']['id']
        ))
    con.commit()


def __get_cards__(con):
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
                    'images': {
                        'symbol': card_data.set.images.symbol,
                        'logo': card_data.set.images.logo
                    }
                },
                'eu_price': card_data.cardmarket.prices.averageSellPrice,
            }
            __update_database__(con, card)


if __name__ == "__main__":
    download_from_google_drive()
    con = connection()
    __init_database__(con)
    __get_cards__(con)
    con.close()
    upload_to_google_drive()
