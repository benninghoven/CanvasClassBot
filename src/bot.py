import discord
import os
import random
from dotenv import load_dotenv
from dotenv import dotenv_values
from discord.ext import context
from discord.ext import commands
from canvas import *

# Libraries I installed:
# pip install -U discord.py
# pip install python-dotenv
# pip install discord.ext.context <- haven't used this library

load_dotenv()

intents = discord.Intents.default()

client = discord.Client(intents=intents)
intents.message_content = True

token = os.environ['TOKEN']


@client.event
async def on_ready():
    print("{0.user}".format(client) + " bot is online.")


@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    if message.author == client.user:
        return
    if message.guild is None:
        return

    # TODO: Add handling for invalid API_KEY

    # Register (register API key)
    if user_message.lower().startswith(".register"):
        api_key = user_message.split(" ")[1]

        if api_key == "":
            return

        set_api_key(message.guild.id, api_key)

        await message.channel.send("API key registered!")

    # Courses (list courses)
    if user_message.lower() == ".courses":
        api_key = guild_keys[message.guild.id]

        if api_key == "":
            return

        course_list = list_courses(api_key)

        await message.channel.send("**Course List:**")
        for courses in course_list:
            await message.channel.send(courses)

    # Search (returns matching course name)
    if user_message.lower().startswith(".search"):
        query = user_message.split(" ")[1]
        api_key = guild_keys[message.guild.id]

        if query == "" or api_key == "":
            return

        await message.channel.send(find_course(api_key, query).name)

    # Help (returns list of commands)
    if user_message.lower() == ".help":
        await message.channel.send("**Commands**\n\n"
                                   "`.register (api_key)` This command registers your Canvas API key with the bot."
                                   "This step is required for the bot to function.\n"
                                   "`.courses` This command is intended for use during setup to list all possible "
                                   "Canvas courses for the bot to pair with.\n"
                                   "`.search (query)` This command is intended for use during setup to search for a "
                                   "Canvas course for the bot to pair with.")


client.run(token)
