import discord
from discord.ext import commands
import json
from difflib import get_close_matches
from googletrans import Translator
from dotenv import load_dotenv
from os import getenv
load_dotenv()

# loading data
data = json.load(open("data.json"))

# period as prefix to call bot command
bot = commands.Bot(command_prefix='.')

# creating an instance of translator
translator = Translator()


# find word meaning
def get_meaning(w):
    keys = data.keys()
    close_match = get_close_matches(w, keys)
    if w in keys:
        return data[w]
    elif w.title() in keys:
        return data[w.tit.le()]
    elif w.upper() in keys:
        return data[w.upper()]
    elif len(close_match) >= 1:
        return f"Maybe you meant '{close_match[0]}' which means '{data[close_match[0]][0]}'"
    else:
        return "My bad! This might be a new word!"


# translation
def get_translation(str, dest='en'):
    return translator.translate(str, dest).text


# replacing ' and " from string
def replace_quote(str):
    return str.replace("'", '').replace('"', '')

# bot commands


@bot.command()
async def helpme(ctx):
    await ctx.reply('''Hi! Nǐn hǎo here. How can I be your friend?
    .meaning yourword - to find the meaning.
    .translate yoursentence - for English translation
    .TTH yoursentence - for Hindi translation
    .TTB yoursentence - for Bangla translation''')


# get meaning
@bot.command()
async def meaning(ctx, *, str):
    temp = get_meaning(replace_quote(str).lower())
    output = ''
    if type(temp) == list:
        output = temp[0]
    else:
        output = temp
    await ctx.reply(output)


# get english translations
@bot.command()
async def translate(ctx, *, str):
    await ctx.reply(get_translation(replace_quote(str)))


# get hindi translation
@bot.command()
async def TTH(ctx, *, str):
    await ctx.reply(get_translation(replace_quote(str), 'hi'))

# get bangla translation


@bot.command()
async def TTB(ctx, *, str):
    await ctx.reply(get_translation(replace_quote(str), 'bn'))

bot.run(getenv('TOKEN'))
