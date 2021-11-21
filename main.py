import discord
from discord import message
from discord.ext import commands, tasks
import json
from difflib import get_close_matches
from deep_translator import GoogleTranslator
from nltk.corpus import wordnet
from dotenv import load_dotenv
from os import getenv
import random
import asyncio
load_dotenv()

# loading data
data = json.load(open("data.json"))
keys = data.keys()

# bot status
status_games = ['Scrabble', 'Hangman', 'Wordplay: Exercise your brain',
                'TypeShift', 'Words of Wonders: Crossword to Connect Vocabulary']
status_listen = ['Podcast', 'BBC News']

# period as prefix to call bot command
bot = commands.Bot(command_prefix='.')


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
def get_translation(str, dest='en'):
    return GoogleTranslator(source='auto', target=dest).translate(str)


# fetch synonyms
def get_synonym(word):
    word_list = []
    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
            word_list.append(lm.name())
    return word_list


# fetch antonyms
def get_antonym(word):
    word_list = []
    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
            if lm.antonyms():
                word_list.append(lm.antonyms()[0].name())
    return word_list


# print synonyms or antonyms
def print_list(list_contain, word, word_list):
    if len(word_list) == 0:
        return 'My bad! I haven\'t found anything'
    else:
        return f'{list_contain} words of \'{word}\': {str(word_list).replace("]", "").replace("[", "")} etc.'


# replacing ' and " from string
def replace_quote(str):
    return str.replace("'", '').replace('"', '')


# change bot status after one hour
async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(name=random.choice(status_games)))
        await asyncio.sleep(3550)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=random.choice(status_listen)))
        await asyncio.sleep(3550)


# bot commands
# get help
@bot.command()
async def helpme(ctx):
    await ctx.reply('''Hi! Nǐn hǎo here. How can I be your friend?
    .meaning word - for meaning
    .synonym word - for synonyms
    .antonym word - for antonyms
    .translate text - for English translation
    .TTH text - for Hindi translation
    .TTB text - for Bangla translation''')


# get meaning
@bot.command()
async def meaning(ctx, *, txt):
    temp = get_meaning(replace_quote(txt).lower())
    await ctx.reply(get_random_meaning(temp))


# get english translations
@bot.command()
async def translate(ctx, *, txt):
    await ctx.reply(get_translation(replace_quote(txt)))


# get hindi translation
@bot.command()
async def TTH(ctx, *, txt):
    await ctx.reply(get_translation(replace_quote(txt), 'hi'))


# get bangla translation
@bot.command()
async def TTB(ctx, *, txt):
    await ctx.reply(get_translation(replace_quote(txt), 'bn'))


# get synonyms
@bot.command()
async def synonym(ctx, txt):
    await ctx.reply(print_list('Similar', txt, get_synonym(txt)[:5]))


# get antonym
@bot.command()
async def antonym(ctx, txt):
    await ctx.reply(print_list('Opposite', txt, get_antonym(txt)[:5]))

# events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} #{bot.user.id}")
    daily_word.start()
    bot.loop.create_task(status_task())


# send daily word
@tasks.loop(hours=23.9)
async def daily_word():
    word = get_random_key()
    temp = get_meaning(word)
    channel = bot.get_channel(911305088964898876)
    await channel.send(f"Today's word: '{word}' which means '{get_random_meaning(temp)}'")


bot.run(getenv('TOKEN'))
