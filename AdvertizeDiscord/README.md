# Discord Advertize

## Discord API

### API ENDPOINTS Reversing

Append header:

```curl
-H "authorization: TOKEN"
```

on `POST`:

```curl
-H "Content-Type: application/json"
```

Route:

`https://discord.com`

* `/api/v8/users/@me` Method: `GET` :

    Get user info.

* `/api/v8/users/@me/affinities/guilds` Method: `GET` :

    Get user guilds.

* `/api/v8/guilds/{guild_id}/channels` Method: `GET` :

    GET guild channels

* `/api/v8/channels/{channel_id}/messages?limit=100` Method: `GET` :

    Get channel Messages.
    - Options:
        - `limit` how many messages, max `100`.
        - `before` load messages before `<message id>`.
    - response:
        - list:
            1. `author`.`id`

* `/api/v8/users/@me/channels` Method: `GET` :
    Get user DMs.

* `/api/v8/users/@me/channels` Method: `POST` :

    Open DM:
    - options:
        - `recipient_id` user/receipent `id`.
    - response:
        - `id` the DM channel `id` (needed to send message).

 - example:
```curl
curl "https://discord.com/api/v8/users/@me/channels" -H "authorization: TOKEN" -H "Content-Type: application/json" -X POST -d '{"recipient_id":224493476249600000}'
output: 
{"id": "760933438143463504", "type": 1, "last_message_id": null, "recipients": [{"id": "224493476249600000", "username": "bennes", "avatar": null, "discriminator": "1738", "public_flags": 0}]}
```

* `/api/v8/channels/{channel_id}/messages` Method: `POST` :
    Send Message.
    - options:
        - `content` Message content.

## Coding:

This code is not multi threaded for a personal use reason, contact me if you wanna work on an asynchronous upgrade.

### FrameWork:

* `User` class:
    - snippet from library:
```python
class User:
    def __init__(self, token: str, route="https://discord.com", api_version=8, init=False):
        ...
```
    - how to use it:
```python
user = User("TOKEN")
```

### Listing Guilds:
    - snippet from library
* getting possible guilds:

```python
    def get_possible_guilds(self):
        r = requests.get(self.route + self.api + "users/@me/affinities/guilds", headers=self.headers)

        if 'message' in json.loads(r.content):
                raise Exception(json.loads(r.content)['message'])

        return list(set([int(x["guild_id"]) for x in json.loads(r.content)['guild_affinities']]))  # list of ints
```
    - how to use it:
```python
guilds = user.get_possible_guilds()
```

### Open Dms:

* open user dm:
    - snippet from library:
```python
    def open_dm(self, user_id: int):
        r = requests.post(self.route + self.api + "users/@me/channels", headers=self.headers, json={
            "recipient_id": user_id
        })
        if 'message' in json.loads(r.content):
            raise Exception(json.loads(r.content)['message'])

        return int(int(json.loads(r.content)['id']))         # dm id
```
    - how to use it:
```python
user_id = 443548921357139969
opened_dm = user.open_dm(user_id)
```

### Listing possible DMs:

* getting already opened DMs:
    - snippet from library:
```python
    def get_all_dms(self):
        r = requests.get(self.route + self.api + "users/@me/channels", headers=self.headers)

        if 'message' in json.loads(r.content):
                raise Exception(json.loads(r.content)['message'])
        
        return json.loads(r.content)           # list of dicts opened dms
```
    - how to use it:
```python
dms = user.get_all_dms()
```

### Sending Message:

* send simple message to an opened dm id:
    - snippet from library:
```python
    def send_message(self, user_id: int, content: str, channel_id=None):
        if channel_id:
            self.opened_dm = channel_id
        else:
            self.opened_dm = self.open_dm(user_id)
        
        r = requests.post(self.route + self.api + f"channels/{self.opened_dm}/messages", headers=self.headers, json={
            "content": content
        })

        if 'message' in json.loads(r.content):
            raise Exception(json.loads(r.content)['message'])

        return json.loads(r.content)            # dict message
```

    - how to use it:
```python
user_id = 443548921357139969
message = user.send_message(user_id)
```

### Get all possible users:

* Get possible users that current user can interact with:
    - snippet from library:
```python
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
```
    - how to use it:
```python
users = user.get_all_users()
```

* Note:
if you used `init=True` better use `reached_users`:
```python
user = User("TOKEN", init=True)
users = user.reached_users
```

### Database interaction: