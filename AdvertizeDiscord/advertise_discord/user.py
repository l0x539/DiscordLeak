import requests
import json
import sys
from time import sleep

class User:
    def __init__(self, token: str, route="https://discord.com", api_version=8, init=False, proxies:dict=None):
        self.token = token
        self.route = route
        self.api = f"/api/v{api_version}/"
        self.opened_dm = None
        self.headers = {
            "authorization": token,
            "Content-Type": "application/json"
            }
        self.proxies = proxies
        self.guilds = []
        self.reached_users = []
        self.channels = []
        self.get_user_infos()
        if init:
            self.get_all_users()
    
    def get_user_infos(self):
        r = requests.get(self.route + self.api + "users/@me", headers=self.headers, proxies=self.proxies)

        if 'message' in json.loads(r.content):
            raise Exception(json.loads(r.content)['message'])
        
        return json.loads(r.content)                        # dict

    def open_dm(self, user_id: int):
        r = requests.post(self.route + self.api + "users/@me/channels", headers=self.headers, json={
            "recipient_id": user_id
        }, proxies=self.proxies)
        if 'message' in json.loads(r.content):
            raise Exception(json.loads(r.content)['message'])

        return int(int(json.loads(r.content)['id']))         # dm id

    def send_message(self, user_id: int, content: str, channel_id=None):
        if channel_id:
            self.opened_dm = channel_id
        else:
            self.opened_dm = self.open_dm(user_id)
        
        r = requests.post(self.route + self.api + f"channels/{self.opened_dm}/messages", headers=self.headers, json={
            "content": content
        }, proxies=self.proxies)

        if 'message' in json.loads(r.content):
            raise Exception(json.loads(r.content)['message'])

        return json.loads(r.content)            # dict message

    def get_all_dms(self):
        r = requests.get(self.route + self.api + "users/@me/channels", headers=self.headers, proxies=self.proxies)

        if 'message' in json.loads(r.content):
                raise Exception(json.loads(r.content)['message'])
        
        return json.loads(r.content)           # list of dicts opened dms
    
    def get_channel_messages(self, channel_id: int, limit=50, before=None):
        messages = []
        last_message_id = before
        for _ in range((limit//100)+1):
            r = requests.get(self.route + self.api + f"channels/{channel_id}/messages?limit={limit%100}" + (f"&before={last_message_id}" if last_message_id else ""), headers=self.headers, proxies=self.proxies)

            if 'message' in json.loads(r.content):
                if json.loads(r.content)['message'] == 'Missing Access':
                    continue
                elif 'You are being rate limited' in json.loads(r.content)['message']:
                    sleep(5)
                    continue
                else:
                    raise Exception(json.loads(r.content)['message'])

            messages += json.loads(r.content)
            if len(messages) > 1:
                last_message_id = messages[-1]['id']
            else:
                break
        
        return messages         # list of dicts messages

    def get_guild_channels(self, guild_id):
        r = requests.get(self.route + self.api + f"guilds/{guild_id}/channels", headers=self.headers, proxies=self.proxies)
        channels = []
        for channel in json.loads(r.content):
            if channel['type'] == 0:
                channels.append(int(channel['id']))
        
        return list(set(channels))            # list of channels id

    def get_possible_guilds(self):
        r = requests.get(self.route + self.api + "users/@me/affinities/guilds", headers=self.headers, proxies=self.proxies)

        if 'message' in json.loads(r.content):
                raise Exception(json.loads(r.content)['message'])

        return list(set([int(x["guild_id"]) for x in json.loads(r.content)['guild_affinities']]))  # list of ints

    def get_all_channel_messages(self, channel_id, Max=1000):
        l = 50
        b = None
        messages = []
        received = 0
        while (len(m := self.get_channel_messages(channel_id, limit=l, before=b)) == 50) and (received < Max):
            b = m[-1]['id']
            messages += m
            received += l
        return messages


    def get_all_users(self):
        users = []
        for x in self.get_all_dms():
            for Id in x['recipients']:
                users.append(int(Id['id']))
        for guild_id in self.get_possible_guilds():
            self.guilds.append(int(guild_id))
            for channel_id in self.get_guild_channels(guild_id):
                self.channels.append(int(channel_id))
                for message in self.get_all_channel_messages(channel_id, Max=50):
                    if int(message['author']['id']) not in users:
                        users.append(int(message['author']['id']))
                print(channel_id)
        users = list(set(users))
        self.reached_users = users
        return users


if __name__ == "__main__":
    user = User(sys.argv[1], init=True)
    print(user.reached_users)