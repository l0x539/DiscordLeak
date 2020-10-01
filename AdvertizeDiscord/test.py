from advertise_discord.mysqldb import *
from advertise_discord.user import *
from advertise_discord.save_core import *

if __name__ == "__main__":

    from configparser import ConfigParser

    config = ConfigParser()
    config.read('config.ini')

    db = DB(host=config.get('database', 'host'), user=config.get('database', 'user'), password=config.get('database', 'password'), db=config.get('database', 'db'))

    save = Save(db)

    user = User(sys.argv[1], proxies={
        'http':'socks5h://localhost:9050',
        'https':'socks5h://localhost:9050'
    })

    user_info = user.get_user_infos()

    connections = user.get_all_users()

    if config.getboolean('Unit', 'init'): save.save_user_connections(user_info['id'], connections)
    else:
        for c in save.get_user(user_info['id']):
            for connection in json.loads(c['connections']):
                user.send_message(int(connection), sys.argv[2])