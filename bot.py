import discord
import os
import random
from dotenv import load_dotenv
from dotenv import dotenv_values
from discord.ext import context
from discord.ext import commands

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


	print(f'Message {user_message} by {username} on {channel}')

	if message.author == client.user:
		return

	if channel == "general":
		if user_message.lower() == "hello" or user_message.lower() == "hi" or user_message.lower() == "greetings":
			await message.channel.send(f'Hello {username}')
			return
		elif user_message.lower() == "bye":
			await message.channel.send(f'Bye {username}')
			return
		elif user_message.lower() == "canvas":
			await message.channel.send("Enter the course: ")
			return
		elif user_message.lower() == "help" or user_message.lower() == "commands":
			# list the commands that users can type
			return

client.run(token)