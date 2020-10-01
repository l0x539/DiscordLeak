from advertise_discord.mysqldb import *
from advertise_discord.user import *
from advertise_discord.save_core import *

from configparser import ConfigParser
import json

config = ConfigParser()
config.read('config.ini')

save = Save(DB(host=config.get('database', 'host'), user=config.get('database', 'user'), password=config.get('database', 'password'), db=config.get('database', 'db')))

def send_message(user, user_id, content):
    
    if not save.check_sent(user_id):
        user.send_message(user_id, content)
        save.add_sent(user_id)
        return 1
    return 0

def advertize(token):
    user = User(token, proxies={
        'http':'socks5h://localhost:9050',
        'https':'socks5h://localhost:9050'
    })
    current_user = user.get_user_infos()
    for c in save.get_user(current_user['id']):
        for user_id in json.loads(c['connections']):
            send_message(user, user_id, "**CHEAP**CHEAP YouTube Views, Facebook, Instagram, Twitter Likes & Much more! https://social-celebrity.com/\nhttps://m.youtube.com/watch?feature=emb_title&v=jF69mebpeCc")

def main():
    advertize(sys.argv[1])

if __name__ == "__main__":
    main()
