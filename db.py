import sqlite3
import channels

# Define connection and cursor
connection = sqlite3.connect('~/myPrograms/TheMessageKeeper/discord_record1.db')
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


def log_privacy(the_id: int, id_type: str, time: str):
    cursor.execute(f"INSERT OR REPLACE INTO privacy VALUES ({the_id}, '{id_type}', '{time}')")
    connection.commit()


def undo_privacy(the_id: int, id_type: str):
    cursor.execute(f"DELETE FROM privacy WHERE id={the_id} AND id_type='{id_type}'")
    connection.commit()


def in_privacy(user_id: int, channel_id: int) -> bool:
    cursor.execute("SELECT * FROM privacy")
    results = cursor.fetchall()

    for i in results:
        if (i[1] == 'user' and i[0] == user_id) or (i[1] == 'channel' and i[0] == channel_id):
            return True

    return False
