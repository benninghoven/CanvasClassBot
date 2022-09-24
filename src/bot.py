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

intents=discord.Intents.default()

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

	# TODO: Add handling for null API_KEY

	# Register (register API key)
	if user_message.startswith(".register"):
		api_key = user_message.split(".register")[1].strip()

		set_api_key(message.guild.id, api_key)

		await message.channel.send("API key registered!")

	# Courses (list courses)
	if user_message.startswith(".courses"):
		guild_id = message.guild.id
		api_key = guild_keys[guild_id]
		course_list = list_courses(api_key)

		await message.channel.send("Course List: ")
		for courses in course_list:
			await message.channel.send(courses)

	# Search (returns matching course name)
	if user_message.startswith(".search"):
		query = user_message.split(".search")[1]
		guild_id = message.guild.id
		api_key = guild_keys[guild_id]

		await message.channel.send(find_course(api_key,query).name)

	# Misc
	if channel == "general":
		if user_message.lower() == "canvas":
			await message.channel.send("Enter the course: ")
			return
		elif user_message.lower() == "help" or user_message.lower() == "commands":
			# list the commands that users can type
			return

client.run(token)