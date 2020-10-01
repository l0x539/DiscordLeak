from advertise_discord.mysqldb import *
from advertise_discord.user import *
from advertise_discord.save_core import *

from configparser import ConfigParser
import json

import random

config = ConfigParser()
config.read('config.ini')

save = Save(DB(host=config.get('database', 'host'), user=config.get('database', 'user'), password=config.get('database', 'password'), db=config.get('database', 'db')))

def send_message(user, user_id, content):
    
    if not save.check_sent(user_id):
        user.send_message(user_id, content)
        save.add_sent(user_id)
        return 1
    return 0

def generate_message():
    Zero = [
        "**CHEAP**",
        "**Legendary Pricess**",
        "**SO CHEAP**"
    ]

    One = ["Youtube Views,",
    "Facebook Likes,",
    "Instagram Hearts,",
    "Twitter Likes,"]

    Two = ["Youtube,",
    "Facebook,",
    "Instagram,",
    "Twitter,"]

    Three = ["& Much more!",
    "and Much mooore at",
    "and More, check it at"]

    Four = ["Website: https://social-celebrity.com/ \n Youtube: https://m.youtube.com/watch?feature=emb_title&v=jF69mebpeCc",
    "https://social-celebrity.com/ \n https://m.youtube.com/watch?feature=emb_title&v=jF69mebpeCc"]

    choices = [0, 1, 2, 3]


    rone = random.choice(choices)
    choices.remove(rone)

    rtwo = random.choice(choices)
    choices.remove(rtwo)

    rthree = random.choice(choices)
    choices.remove(rthree)

    rfour = choices[-1]

    return f"{random.choice(Zero)} {One[rone]} {Two[rtwo]} {Two[rthree]} {One[rfour][:-1]} {random.choice(Three)} {random.choice(Four)}"

def advertize(token):
    user = User(token, proxies={
        'http':'socks5h://localhost:9050',
        'https':'socks5h://localhost:9050'
    })
    current_user = user.get_user_infos()
    for c in save.get_user(current_user['id']):
        for user_id in json.loads(c['connections']):
            send_message(user, user_id, generate_message())
            sent = True
            break
        if sent: break

def main():
    #advertize(sys.argv[1])
    print(generate_message())


if __name__ == "__main__":
    main()
