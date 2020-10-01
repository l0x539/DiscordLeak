use <DATABASE NAME>

CREATE TABLE discord_users (
    user_id VARCHAR(50),
    connections TEXT,
    insert_time DATETIME
);

CREATE TABLE dm_messages (
    user_id VARCHAR(50),
    message TEXT,
    date_added DATETIME
);

CREATE TABLE channels_messages (
    user_id VARCHAR(50),
    message TEXT,
    date_added DATETIME
);