import canvasapi.exceptions
import discord
import os
import random
import sqlite3
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


def get_api_key(guild_id):
    """Returns Canvas API key"""

    con = sqlite3.connect("bot.db")

    try:
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT api_key FROM keys WHERE guild_id = {guild_id}")

        return cur.fetchone()[0]
    except (AttributeError, TypeError):
        return "401"
    finally:
        con.close()


@client.event
async def on_ready():
    print(f"{client.user} bot is online")

    con = sqlite3.connect("bot.db")
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS keys(guild_id int, api_key string)")
    con.close()


@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    if message.author == client.user:
        return
    if message.guild is None:
        return

    # Register (register API key)
    if user_message.lower().startswith(".register"):
        api_key = user_message
        api_key = api_key[9::].strip()

        if api_key == "":
            await message.channel.send("No API key inputted, try again!")
            return

        try:
            test_key(api_key)
        except canvasapi.exceptions.InvalidAccessToken:
            await message.channel.send("Invalid API key!")
            return

        # Insert key into DB
        con = sqlite3.connect("bot.db")
        con.execute(f"REPLACE INTO keys (guild_id, api_key) VALUES (({message.guild.id}), (\"{api_key}\"))")
        con.commit()

        await message.channel.send("API key registered!")

    # Courses (list courses)
    if user_message.lower() == ".courses":
        api_key = get_api_key(message.guild.id)

        if api_key == "401":
            await message.channel.send("No API key found!")
            return

        try:
            course_list = list_courses(api_key)
        except canvasapi.exceptions.InvalidAccessToken:
            await message.channel.send("Invalid API key!")
            return

        await message.channel.send("**Course List:**")
        for courses in course_list:
            await message.channel.send(courses)

    # Search (returns matching course name)
    if user_message.lower().startswith(".search"):
        query = user_message
        query = query[7::].strip()

        if query == "":
            await message.channel.send("Invalid query, try again!")
            return

        api_key = get_api_key(message.guild.id)

        if api_key == "401":
            await message.channel.send("No API key found!")
            return

        try:
            courses = search_course(api_key, query)
        except canvasapi.exceptions.InvalidAccessToken:
            await message.channel.send("Invalid API key!")
            return

        await message.channel.send(f"Found `{len(courses)}` courses containing: **{query}**")
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
