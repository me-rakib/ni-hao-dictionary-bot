import discord
from discord.ext import commands
import json
from difflib import get_close_matches

data = json.load(open("data.json"))


def get_meaning(w):
    keys = data.keys()
    close_match = get_close_matches(w, keys)
    if w in keys:
        return data[w]
    elif w.title() in keys:
        return data[w.title()]
    elif w.upper() in keys:
        return data[w.upper()]
    elif len(close_match) >= 1:
        return f"Maybe you meant '{close_match[0]}' which means '{data[close_match[0]][0]}'"
    else:
        return "My bad! This might be a new word!"


bot = commands.Bot(command_prefix='.')


@bot.command()
async def meaning(ctx, word):
    temp = get_meaning(word.lower())
    output = ''
    if type(temp) == list:
        output = temp[0]
    else:
        output = temp

    await ctx.reply(output)

bot.run('OTEwNjA0NjU1NzE1ODIzNjQ2.YZVQrA.wSbnmHpovBpvcM_nwbKsFb7oDPI')
