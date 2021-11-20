import discord
from discord.ext import commands, tasks
import json
from difflib import get_close_matches
# from googletrans import Translator
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from os import getenv
import random
load_dotenv()

# loading data
data = json.load(open("data.json"))
keys = data.keys()

# period as prefix to call bot command
bot = commands.Bot(command_prefix='.')

# creating an instance of translator
# translator = Translator()


# find word meaning
def get_meaning(w):
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


# get a random key for gerenating daily word meaning
def get_random_key():
    return random.choice(list(keys))


# get one random meaning from meaning list
def get_random_meaning(meaning_list):
    output = ''
    if type(meaning_list) == list:
        output = random.choice(meaning_list)
    else:
        output = meaning_list
    return output


# translation
# def get_translation(str, dest='en'):
#     return translator.translate(str, dest).text

def get_translation(str, dest='en'):
    return GoogleTranslator(source='auto', target=dest).translate(str)


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
    await ctx.reply(get_random_meaning(temp))


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


@bot.event
async def on_ready():
    daily_word.start()


@tasks.loop(hours=24)
async def daily_word():
    word = get_random_key()
    temp = get_meaning(word)
    channel = bot.get_channel(911305088964898876)
    await channel.send(f"Today's word: '{word}' which means '{get_random_meaning(temp)}'")


bot.run(getenv('TOKEN'))
