from advertise_discord.mysqldb import DB

import json
import time

class Save:
    def __init__(self, db: DB):
        self.db = db
        pass

    def save_user_connections(self, user_id: int, connections: list):
        if not self.check_user_exist(user_id): self.save_user_init(user_id)

        self.db.execute("UPDATE discord_users SET connections=%s, insert_time=%s WHERE user_id=%s", (json.dumps(connections), time.strftime('%Y-%m-%d %H:%M:%S'), user_id))

    
    def check_user_exist(self, user_id: int):
        c = self.db.execute("SELECT * FROM discord_users WHERE user_id=%s", (user_id,))

        for cursor in c:
            return cursor
        
        return False

    def save_user_init(self, user_id: int):
        if not self.check_user_exist(user_id): self.db.execute("INSERT INTO discord_users  (user_id, insert_time) VALUES(%s, %s)", (user_id, time.strftime('%Y-%m-%d %H:%M:%S')))

    def get_user(self, user_id: int):
        return self.db.execute("SELECT * FROM discord_users WHERE user_id=%s", (user_id,))
    
    def get_all_users(self):
        return self.db.execute("SELECT * FROM discord_users")
    
    def save_dm_message(self, user_id: int, message: dict):
        self.db.execute("INSERT INTO dm_messages (user_id, message, date_added) VALUES (%s, %s, %s)", (user_id, json.dumps(message), time.strftime('%Y-%m-%d %H:%M:%S')))
    
    def save_channel_message(self, message: dict):
        self.db.execute("INSERT INTO channels_messages (channel_id, message, date_added) VALUES (%s, %s)", (message['channel_id'], json.dumps(message), time.strftime('%Y-%m-%d %H:%M:%S')))
    
    def get_dm_messages(self, user_id:int):
        return self.db.execute("SELECT * FROM dm_messages WHERE user_id=%s", (user_id, ))
    
    def get_channel_messages(self, channel_id:int):
        return self.db.execute("SELECT * FROM channels_messages WHERE channel_id=%s", (channel_id, ))

    def add_sent(self, receipent_id:int):
        return self.db.execute("INSERT INTO messages_sent (receipent_id, date_added) VALUES (%s, %s)", (receipent_id, time.strftime('%Y-%m-%d %H:%M:%S')))
    
    def check_sent(self, receipent_id:int):
        c = self.db.execute("SELECT * FROM messages_sent WHERE receipent_id=%s", (receipent_id, ))

        for cursor in c:
            return cursor
        
        return False