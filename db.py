import sqlite3
import channels

# Define connection and cursor
connection = sqlite3.connect('discord_record.db')
cursor = connection.cursor()

# Create stores table
createMessages = """CREATE TABLE IF NOT EXISTS
messages(message_id INTEGER PRIMARY KEY, guild_id INTEGER, channel_id INTEGER, 
author_id Integer, time_created TEXT, content TEXT)"""
cursor.execute(createMessages)

# create purchase table
createPrivacy = """CREATE TABLE IF NOT EXISTS
privacy(id INTEGER PRIMARY KEY, id_type TEXT, time_called TEXT)"""
cursor.execute(createPrivacy)

# save the setup
connection.commit()


# Methods
def log_message(message):
    cursor.execute(f"INSERT OR REPLACE INTO messages VALUES ({int(message.id)}"
                   f", {int(message.guild.id)}, {int(message.channel.id)}, {int(message.author.id)}"
                   f", '{str(message.created_at)}', '{str(message.content)}')")
    connection.commit()


def log_privacy(id: int, id_type: str, time: str):
    cursor.execute(f"INSERT OR REPLACE INTO privacy VALUES ({id}, {id_type}, {time})")
    connection.commit()
