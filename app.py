from drive_service import download_from_google_drive
from card_service import collected

from flask import Flask, jsonify, request
from database import connection

app = Flask(__name__)


@app.route('/<set_id>/cards', methods=['GET'])
def get_cards_by_set(set_id):
    conn = connection()
    query = '''
            SELECT card.*, "set".name as set_name, "set".series as set_series,
            "set".image_logo as set_logo, "set".image_symbol as set_symbol
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
            'series': card_dict['set_series'],
            'image': {
                'logo': card_dict['set_logo'],
                'symbol': card_dict['set_symbol']
            }
        }
        del card_dict['set_id']
        del card_dict['set_name']
        del card_dict['set_series']
        del card_dict['set_logo']
        del card_dict['set_symbol']
        cards_list.append(card_dict)
    return jsonify(cards_list)


@app.route('/sets', methods=['GET'])
def get_sets():
    conn = connection()
    sets = conn.execute('SELECT * FROM "set"').fetchall()
    sets_list = [dict(ix) for ix in sets]
    conn.close()
    return jsonify(sets_list)


# id, collected true/false
@app.route('/collect_card/', methods=['POST'])
def update_card():
    print(request)
    collected(request.json)
    return jsonify(request.json)


@app.route('/load_data', methods=['GET'])
def load_data():
    download_from_google_drive()
    return 'loaded'


if __name__ == '__main__':
    app.run(debug=True)
