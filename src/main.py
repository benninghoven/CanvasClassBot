import os
import json
import bot
from database import *

def Main():
    with open("data/config.json") as file:
        data = json.load(file)
    try:
        token = data["token"]
    except KeyError:
        print("error could not find file app/data/config.json")
    print("starting bot")
    bot.client.run(token)
    exit()


@bot.client.event #FIXME add guild to database
async def on_guild_join(guild):
    print(f"joined {guild}")

# guild is either deleted or bot has been kicked
#FIXME remove guild from database,
@bot.client.event 
async def on_guild_remove(guild):
    # check if guild is registered before
    print(f"guild {guild} purged, remove it from the database")

async def RegisterUser(userID, canvasKey):
    if SearchOwner(userID):
        await user.send("INVALID API KEY")
        return
    database.AddOwnerIDApiKey(userID, canvasKey)
    await user.send("register complete")
    

async def setup_guild(guild):
    # we got the thumbs up, send it!
    ownerID = guild.owner.id
    if not SearchOwner(ownerID):
        await guild.owner.send("You are not in the database yet!")
        await guild.owner.send("please register a valid api key")
        await guild.owner.send("register APIKEY")
        return
    print(f"setting up {guild} for {ownerID}")
    await guild.owner.send("hello owner")
    # CHECK IF THEY ARE ALREADY IN THE DATABASE
    # ASK FOR API KEY
    # IF ALREADY HAVE API KEY, GO STRAIGHT TO CLASSES
    # PRESENT LIST OF CLASSES
    # REACT TO CHOOSE CLASS
    # ARE YOU SURE YOU WANT TO TURN X GUILD INTO IT?
    return


@bot.client.event
async def on_message(message):
    if message.author == bot.client.user:
        return
    #if message.guild is None: # DMS?
    #    return
    if message.content == "setup":
        await setup_guild(message.guild)
    #FIXME 
    if "register" in message.content and message.guild is None:
        messageLst = message.content.split()
        if len(messageLst) == 2:
            apiKey = messageLst[-1]
            await message.author.send(f"registering key:{apiKey}") #VERIFY KEY
            await RegisterUser(message.author.id,apiKey)
            # ADD TO DATABASE

        else:
            await message.authore.send(f"invalid key")

Main()




