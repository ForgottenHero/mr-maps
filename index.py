#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import codecs
import discord
import pprint
import sys
import getpass
from discord.ext import commands
from os.path import expanduser
sys.dont_write_bytecode = True

try:
    with open(expanduser('~/credentials/discordConfig2.json'), 'r',encoding='utf8') as f:
        data = json.load(f)
        token = data["token"]
        prefix = data["prefix"]
        status = data["playing"]
except Exception as loadingJSON:
    print(loadingJSON)

bot = commands.Bot(command_prefix=prefix, prefix=prefix, case_insensitive=True)
print("Loading cogs...")
try:
    for file in os.listdir(expanduser('~/trollbot/cogs')):
        if file.endswith("admin.py"):
            name = file[:-3]
            bot.load_extension(f"cogs.{name}")
except Exception as loadingCogs:
    print(loadingCogs)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(f'Logged in as: {bot.user.name} in {guild.name}. Version: {discord.__version__}')
    await bot.change_presence(status=status)

print("Starting bot...")
bot.run(token, bot=True, reconnect=True)
