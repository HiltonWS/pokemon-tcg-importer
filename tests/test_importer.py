import sys
import os
import base64
from unittest import mock
import pytest
import requests_mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # noqa E501

from importer import (__url_content_to_base64__, __update_database__, __get_cards__, __init_database__) # noqa E501, E402
from pokemontcgsdk import Card # noqa E402
from mock_db import get_mock_connection # noqa E402


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def mock_db(mocker):
    mock_conn = get_mock_connection()
    mocker.patch('importer.connection', return_value=mock_conn)
    return mock_conn


def test_url_content_to_base64(mock_requests):
    url = 'https://www.hiltonws.com/images/eu.png'
    mock_requests.get(url, content=b'image content')
    encoded = __url_content_to_base64__(url)
    assert encoded == base64.b64encode(b'image content').decode('utf-8')


def test_update_database(mock_db, mocker):
    mock_conn = mock_db
    mocker.patch('importer.read_file', return_value='SQL SCRIPT')
    data = {
        'set': {
            'id': 'set1',
            'name': 'Set Name',
            'series': 'Series Name',
            'images': {
                'logo': 'Logo URL',
                'symbol': 'Symbol URL'
                }
            },
        'id': 'card1',
        'number': '1',
        'name': 'Card Name',
        'image': 'image_url',
        'rarity': 'Common',
        'eu_price': 1.0
        }
    __update_database__(mock_conn, data)
    assert mock_conn.execute.call_count == 2
    mock_conn.commit.assert_called_once()


def test_get_cards(mock_db, mocker):
    mock_conn = mock_db
    mock_card = mock.create_autospec(Card)
    mock_card.id = 'card1'
    mock_card.number = '1'
    mock_card.name = 'Card Name'
    mock_card.images = mock.Mock(large='image_url')
    mock_card.rarity = 'Common'
    mock_card.set = mock.Mock(
        id='set1',
        name='Set Name',
        series='Series Name'
    )
    mock_card.cardmarket = mock.Mock(
        prices=mock.Mock(
            averageSellPrice=1.0
            )
        )

    mocker.patch('pokemontcgsdk.Card.where', return_value=[mock_card])

    __get_cards__(mock_conn)
    assert mock_conn.execute.call_count > 0
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_init_database(mock_db):
    mock_conn = mock_db
    __init_database__(mock_conn)
    assert mock_conn.executescript.call_count == 4


def test_get_cards_without_cardmarket(mock_db, mocker):
    mock_conn = mock_db
    mock_card = mock.create_autospec(Card)
    mock_card.id = 'card1'
    mock_card.number = '1'
    mock_card.name = 'Card Name'
    mock_card.images = mock.Mock(large='image_url')
    mock_card.rarity = 'Common'
    mock_card.set = mock.Mock(
        id='set1',
        name='Set Name',
        series='Series Name'
    )

    mocker.patch('pokemontcgsdk.Card.where', return_value=[mock_card])
    mock_card.cardmarket = None

    __get_cards__()
    assert mock_conn.execute.call_count > 0
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()
