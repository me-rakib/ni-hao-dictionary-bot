from typing import AnyStr
import discord
from discord.ext import tasks, commands
from googletrans import Translator
translator = Translator()

bot = commands.Bot(command_prefix='.')


def get_translation(str, dest='bn'):
    return translator.translate(str, dest).text


@bot.command()
async def translate(ctx, *, str):
    await ctx.reply(get_translation(str))


@bot.event
async def on_ready():
    send_msg.start()


@tasks.loop(seconds=20)
async def send_msg():
    channel = bot.get_channel(846353236863483917)
    print(bot.get_all_channels())
    await channel.send("HEllo")

bot.run('OTEwNjA0NjU1NzE1ODIzNjQ2.YZVQrA.wSbnmHpovBpvcM_nwbKsFb7oDPI')
