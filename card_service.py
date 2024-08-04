from database import connection
from file_service import read_file


def collected(card):
    con = connection()
    con.execute(read_file('db/update_card_collected.sql'), (
        card['collected'],
        card['id'],
        ))
    con.commit()
    con.close()