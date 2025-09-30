import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

logging.basicConfig(
    level=logging.DEBUG,
    filename="discord.log",
    encoding="utf-8",
    filemode="w",
    format="%(asctime)s:%(levelname)s:%(name)s: %(message)s"
)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user.name} is here to help!")

async def main():
    async with bot:
        await bot.load_extension("cogs.commands")
        await bot.start(token)

asyncio.run(main())