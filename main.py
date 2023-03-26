from time import sleep
import random
import discord
from secrets import token
from enum import Enum
import db
import channels
import asyncio
import os

# This will load the permissions the bot has been granted in the previous configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
servers_synced = {}


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False  # added to make sure that the command tree will be synced only once
        self.added = False

    async def on_ready(self):
        await client.wait_until_ready()

        async for i in client.fetch_guilds():
            servers_synced[i.id] = False

        print(f"{self.user} is online")


client = aclient()
tree = discord.app_commands.CommandTree(client)

@tree.command(description='Sends my invite link')
async def invite(interaction: discord.Interaction):
    await interaction.response.send_message(
        'https://discord.com/api/oauth2/authorize?client_id=1089259451002916935&permissions=2148076608&scope=bot')


@tree.command(description='Tells me to stop watching your messages')
async def opt_out(interaction: discord.Interaction):
    db.log_privacy(interaction.user.id, "user", str(interaction.created_at))
    await interaction.response.send_message('You have opted-out successfully')


@tree.command(description='Tells me to start watching your messages')
async def opt_in(interaction: discord.Interaction):
    db.undo_privacy(interaction.user.id, "user")
    await interaction.response.send_message('You have opted-in successfully')


@tree.command(description='Tells me to stop watching a channels messages')
async def opt_out_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    if interaction.user.guild_permissions.administrator:
        db.log_privacy(channel.id, "channel", str(interaction.created_at))
        await interaction.response.send_message(f'You have opted-out the channel {channel.name} successfully')
    else:
        await interaction.response.send_message(f'You do not have permission to use this command')


@tree.command(description='Tells me to start watching a channels messages')
async def opt_in_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    if interaction.user.guild_permissions.administrator:
        db.undo_privacy(channel.id, "channel")
        await interaction.response.send_message(f'You have opted-in the channel {channel.name} successfully')
    else:
        await interaction.response.send_message(f'You do not have permission to use this command')


@client.event
async def on_message(message):
    # Syncs to server
    if message.guild and not servers_synced[message.guild.id]:
        await tree.sync()
        servers_synced[message.guild.id] = True
        print(f"synced to server: {message.guild.name}")

    # This checks if the message is not from the bot itself. If it is, it'll ignore the message.
    if message.author == client.user:
        return

    # Records the inbound message
    if not db.in_privacy(message.author.id, message.channel.id):
        db.log_message(message)

    # Do stuff
    if message.content.lower() == "reboot":
        os.system("reboot")
    if message.content.lower() == "quit":
        quit()


# add the token of your bot
client.run(token)
