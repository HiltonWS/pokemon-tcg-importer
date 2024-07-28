from drive_service import download_from_google_drive

from flask import Flask, jsonify
from database import connection

app = Flask(__name__)


@app.route('/<set_id>/cards', methods=['GET'])
def get_cards_by_set(set_id):
    conn = connection()
    query = '''
            SELECT card.*, "set".name as set_name, "set".series as set_series
            FROM card
            JOIN "set" ON card.set_id = "set".id
            WHERE card.set_id = ?
            '''
    cards = conn.execute(query, (set_id,)).fetchall()
    conn.close()
    cards_list = []
    for card in cards:
        card_dict = dict(card)
        card_dict['set'] = {
            'id': card_dict['set_id'],
            'name': card_dict['set_name'],
            'series': card_dict['set_series']
        }
        cards_list.append(card_dict)
    return jsonify(cards_list)


@app.route('/sets', methods=['GET'])
def get_sets():
    conn = connection()
    sets = conn.execute('SELECT * FROM "set"').fetchall()
    sets_list = [dict(ix) for ix in sets]
    conn.close()
    return jsonify(sets_list)


@app.route('/load_data', methods=['GET'])
def load_data():
    download_from_google_drive()
    return 'loaded'


if __name__ == '__main__':
    app.run(debug=True)
