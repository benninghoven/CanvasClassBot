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

#token = os.environ['TOKEN']
token = "MTAyMzE0MTMzNTA1NTczNjg0Mg.GfYAsD.V6JPMnj-TD007zybrInVZymEkdZwfP90NvOMjM"


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
    # TODO: take entire string minus command name
    if user_message.lower().startswith(".search"):
        query = user_message.split(" ")[1]
        api_key = guild_keys[message.guild.id]

        if query == "" or api_key == "":
            return

        courses = search_course(api_key, query)

        await message.channel.send(f"Found ({len(courses)}) courses containing: **{query}**")
        for course in courses:
            await message.channel.send(course)

    # Help (returns list of commands)
    if user_message.lower() == ".help":
        await message.channel.send("**Commands**\n\n"
                                   "`.register (api_key)` This command registers your Canvas API key with the bot."
                                   " This step is required for the bot to function.\n\n"
                                   "`.courses` This command is intended for use during setup to list all possible "
                                   "Canvas courses for the bot to pair with.\n\n"
                                   "`.search (query)` This command is intended for use during setup to search for a "
                                   "Canvas course to pair the bot pair with.")


client.run(token)
