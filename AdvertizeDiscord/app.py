from advertise_discord.mysqldb import *
from advertise_discord.user import *
from advertise_discord.save_core import *

if __name__ == "__main__":

    from configparser import ConfigParser

    config = ConfigParser()
    config.read('config.ini')

    db = DB(host=config.get('database', 'host'), user=config.get('database', 'user'), password=config.get('database', 'password'), db=config.get('database', 'db'))

    save = Save(db)

    user = User(sys.argv[1])

    user_info = user.get_user_infos()

    connections = user.get_all_users()

    if config.getboolean('Unit', 'init'): save.save_user_connections(user_info['id'], connections)
    else:
        user_users = save.get_user(user_info['id'])
        if not user:
            print("make sure you switch init to true first, run program, then switch it back.")
        for c in user_users:
            for connection in json.loads(c['connections']):
                user.send_message(int(connection), sys.argv[2])

