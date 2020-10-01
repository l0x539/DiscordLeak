from advertise_discord.mysqldb import *

from enum_client_reached_users import *
from advertise_message import *

from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

db = DB(host=config.get('database', 'host'), user=config.get('database', 'user'), password=config.get('database', 'password'), db=config.get('database', 'db'))

def get_tokens():
    return [c['token'] for c in db.execute("SELECT * FROM tokens")]


if __name__ == "__main__":
    for token in get_tokens():
        try:
            enumerate(token)
        except Exception as e:
            print(e)
        try:
            advertize(token)
        except Exception as e:
            print(e)
    