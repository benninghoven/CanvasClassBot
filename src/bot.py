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


def simple_embed(title_text):
    """Returns Discord embed and sets title_text as embed title"""

    embed = discord.Embed(title=title_text, color=0x00000)
    embed.set_author(
        name=client.user.display_name, icon_url=client.user.avatar)
    embed.set_footer(
        text="Use .help for the complete commands list!")

    return embed


@client.event
async def on_ready():
    print(f"{client.user} bot is online")

    con = sqlite3.connect("bot.db")
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS keys(guild_id int UNIQUE, api_key string, class_name string)")
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
            await message.channel.send(embed=simple_embed("No API key inputted, try again!"))
            return

        try:
            test_key(api_key)
        except canvasapi.exceptions.InvalidAccessToken:
            await message.channel.send(embed=simple_embed("Invalid API key!"))
            return

        # Insert key into DB
        con = sqlite3.connect("bot.db")
        with con:
            cur = con.cursor()
            cur.execute(f"REPLACE "
                        f"INTO keys (guild_id, api_key) "
                        f"VALUES (({message.guild.id}), (\"{api_key}\"))")

        con.close()
        await message.channel.send(embed=simple_embed("API key registered!"))

    # List assignments
    if user_message.lower() == ".assignments":
        api_key = get_api_key(message.guild.id)

        if api_key == "401":
            await message.channel.send(embed=simple_embed("No API key found!"))
            return

        try:
            test_key(api_key)
        except canvasapi.exceptions.InvalidAccessToken:
            await message.channel.send(embed=simple_embed("Invalid API key!"))
            return

        # Get course from DB
        con = sqlite3.connect("bot.db")
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT class_name FROM keys WHERE guild_id = {message.guild.id}")
            course_name = cur.fetchone()[0]
        con.close()

        course = search_course(api_key, course_name)[0]
        assignments = list_assignments(course)

        assignment_message = "**Assignments**\n"
        for assignment in assignments:
            assignment_message += (assignment + "\n\n")

        await message.channel.send(assignment_message)

    # Courses (list courses)
    if user_message.lower() == ".courses":
        api_key = get_api_key(message.guild.id)

        if api_key == "401":
            await message.channel.send(embed=simple_embed("No API key found!"))
            return

        try:
            test_key(api_key)
        except canvasapi.exceptions.InvalidAccessToken:
            await message.channel.send(embed=simple_embed("Invalid API key!"))
            return

        course_list = list_courses(api_key)
        await message.channel.send("**Course List:**")
        for courses in course_list:
            await message.channel.send(courses)

    # Set course
    if user_message.lower().startswith(".setcourse"):
        query = user_message
        query = query[10::].strip()

        api_key = get_api_key(message.guild.id)

        if api_key == "401":
            await message.channel.send(embed=simple_embed("No API key found!"))
            return

        try:
            test_key(api_key)
        except canvasapi.exceptions.InvalidAccessToken:
            await message.channel.send(embed=simple_embed("Invalid API key!"))
            return

        courses = search_course(api_key, query)
        if len(courses) == 0:
            await message.channel.send(embed=simple_embed(f"No courses found for: **{query}**"))
            return

        # Set course
        course = courses[0].name

        con = sqlite3.connect("bot.db")
        with con:
            cur = con.cursor()
            cur.execute(f"REPLACE "
                        f"INTO keys (guild_id, api_key, class_name) "
                        f"VALUES (({message.guild.id}), (\"{api_key}\"), (\"{course}\"))")
        con.close()

        await message.channel.send(embed=simple_embed(f"Course set as {course}"))

    # Search (returns matching course name)
    if user_message.lower().startswith(".search"):
        query = user_message
        query = query[7::].strip()

        api_key = get_api_key(message.guild.id)

        if api_key == "401":
            await message.channel.send(embed=simple_embed("No API key found!"))
            return

        try:
            test_key(api_key)
        except canvasapi.exceptions.InvalidAccessToken:
            await message.channel.send(embed=simple_embed("Invalid API key!"))
            return

        if query == "":
            await message.channel.send(embed=simple_embed("Invalid query, try again!"))
            return

        courses = search_course(api_key, query)
        await message.channel.send(f"Found `{len(courses)}` courses containing: **{query}**")
        for course in courses:
            await message.channel.send(course)

    # Help (returns list of commands)
    if user_message.lower() == ".help":
        embed = discord.Embed(title="Commands List", color=0x00000)
        embed.set_author(name=client.user.display_name, icon_url=client.user.avatar)
        embed.description = ("`.register (api_key)` This command registers your Canvas API key with the bot."
                             " This step is required for the bot to function.\n\n"
                             "`.courses` This command is intended for use during setup to list all possible "
                             "Canvas courses for the bot to pair with.\n\n"
                             "`.search (query)` This command is intended for use during setup to search for a "
                             "Canvas course to pair the bot pair with.")

        await message.channel.send(embed=embed)


client.run(token)
