import os
import json
import base64
import requests
import sqlite3

from pokemontcgsdk import RestClient

from pokemontcgsdk import Card

API_KEY = os.getenv("API_KEY")
COLLECTION_SETS = json.loads(os.getenv("COLLECTION_SETS"))

RestClient.configure(API_KEY)
conn = sqlite3.connect('pokemon_cards.db')
cursor = conn.cursor()

def urlContentToBase64(url):
        return base64.b64encode(requests.get(url).content)

def updateDatabase(data):
     with open('db/tables.sql', 'r') as sql_file:
        sqlScript = sql_file.read()
        conn.executescript(sqlScript)
        conn.commit()
     with open('db/insertSet.sql', 'r') as sql_file:
        sqlScript = sql_file.read()
        conn.execute(sqlScript, (
            data['set']['id'],
            data['set']['name'],
            data['set']['series']
            ))
        conn.commit()
     with open('db/insertCard.sql', 'r') as sql_file:
        sqlScript = sql_file.read()
        conn.execute(sqlScript, (
            data['id'], 
            data['number'], 
            data['name'], 
            data['image'], 
            data['rarity'],
            data['euPrice'],
            data['set']['id']
            ))
        conn.commit()
    


for set in COLLECTION_SETS:
    cards = Card.where(q="set.id:" + set, orderBy="number")
    for cardData in cards:
        cardData: Card = cardData
        card = {}
        card['id'] = cardData.id
        card['number'] = cardData.number
        card['name'] = cardData.name
        cardImageUrl = cardData.images.large
        card['image'] = urlContentToBase64(cardImageUrl)
        card['rarity'] = cardData.rarity
        card['set'] = {}
        card['set']['id'] = cardData.set.id
        card['set']['name'] = cardData.set.name
        card['set']['series'] = cardData.set.series
        card['euPrice'] = cardData.cardmarket.prices.averageSellPrice
        updateDatabase(card)

conn.close()

