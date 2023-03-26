from time import sleep
import random
import discord
from secrets import token
from enum import Enum
import db
import channels

# This will load the permissions the bot has been granted in the previous configuration
intents = discord.Intents.default()
intents.message_content = True


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False  # added to make sure that the command tree will be synced only once
        self.added = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # check if slash commands have been synced
            await tree.sync(guild=discord.Object(
                '895359434539302953'))  # guild specific: you can leave sync() blank to make it global. But it can
            # take up to 24 hours, so test it in a specific guild.
            self.synced = True
        if not self.added:
            self.added = True
        print(f"{self.user} is online")


client = aclient()
tree = discord.app_commands.CommandTree(client)


@tree.command(description='Respond hello to you.', guild=discord.Object('895359434539302953'))
async def greet(interaction: discord.Interaction):
    await interaction.response.send_message('Hello!')


GreetingTime = Enum(value='GreetingTime', names=['MORNING', 'AFTERNOON', 'EVENING', 'NIGHT'])

'''
@tree.command(description='Respond according to the period of the day.', guild=discord.Object('895359434539302953'))
@discord.app_commands.describe(period='Period of the day')
async def greet_time_of_day(interaction: discord.Interaction, period: GreetingTime):
    user = interaction.user.id
    if period.name == 'MORNING':
        await interaction.response.send_message(f'Good Morning, <@{user}>!')
        return
    if period.name == 'AFTERNOON':
        await interaction.response.send_message(f'Good Afternoon, <@{user}>!')
        return
    if period.name == 'EVENING':
        await interaction.response.send_message(f'Good Evening, <@{user}>!')
        return
    if period.name == 'NIGHT':
        await interaction.response.send_message(f'Have a good night, <@{user}>!')
        return
'''


@client.event
async def on_message(message):
    # Records the inbound message
    db.log_message(message)

    # This checks if the message is not from the bot itself. If it is, it'll ignore the message.
    if message.author == client.user:
        return

    # Do stuff


# add the token of your bot
client.run(token)
