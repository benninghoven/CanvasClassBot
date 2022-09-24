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

token = 'MTAyMzE0MTMzNTA1NTczNjg0Mg.GwhJrV.70XYk5LkrM5ULbjwqK9bLKNjoBixf_NV8X0s_U'

api_key = 0

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

	# TODO: Enable only when from guild
	# TODO: Add handling for null API_KEY

	# Register (register API key)
	if user_message.startswith(".register"):
		global api_key
		api_key = user_message.split(".register")[1].strip()
		set_api_key(api_key)

		await message.channel.send("API key registered!")
		print("API Key: " + api_key)

	# Courses (list courses)
	if user_message.startswith(".courses"):
		course_list = list_courses()

		await message.channel.send("Course List: ")

		for courses in course_list:
			await message.channel.send(courses)

	# Search (returns matching course name)
	if user_message.startswith(".search"):
		query = user_message.split(".search")[1]
		await message.channel.send(find_course(query).name)

	# Misc
	if channel == "general":
		if user_message.lower() == "canvas":
			await message.channel.send("Enter the course: ")
			return
		elif user_message.lower() == "help" or user_message.lower() == "commands":
			# list the commands that users can type
			return

client.run(token)