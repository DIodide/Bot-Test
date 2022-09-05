import asyncio
import os
import sys
from datetime import datetime
from traceback import print_exception
from aiohttp import ClientSession # web browser async version of import requests
from discord import Intents, Embed
from discord.ext import commands
from discord.utils import setup_logging
from discord.ext.commands import Bot
import discord
import traceback

owner_id = 377543612810133504
intents = Intents().all()

with open("PREFIX.txt", "r") as f: # r is read mode
    PREFIX = f.read()
PREFIX = PREFIX + " "


class MyBot(Bot):
    async def setup_hook(self):
        print(f"Logging in as: {self.user}")
        # Initial Cog Load
        print("Attempting load cogs. . .")
        for filename in os.listdir("./cogs"):
            if filename.endswith('.py'):
                print(f"Attempting to load {filename}")
                await client.load_extension(f'cogs.{filename[:-3]}')
                print(f"Successfully loaded cogs.{filename}")

        print(f"\nYour Mom has finally loaded and is ready to use, use Your mom with the prefix {PREFIX}\n"
              f"------------------------------------------------------------------------\nnig\n"
              f"------------------------------------------------------------------------")

    async def start_bot(self):
        setup_logging()
        self.session = ClientSession()
        with open("TOKEN.txt", 'r') as f:
            TOKEN = f.read()
        await self.start(TOKEN)



client = MyBot(command_prefix=[PREFIX, 'ym'], intents=intents, slash_command_guilds=[850084933988646927])


@client.command(brief="reloads your momma", description="*Splendor*")
async def reload(ctx):
    # Unloads all extensions and discards error if no extensions are loaded.
    print("Attempting Reload. . .")
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            try:
                await client.unload_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print_exception(type(e), e, e.__traceback__, file=sys.stderr)
    message = ''
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            message = message + f"Successfully reloaded.. `{filename}`\n"
    await ctx.send(message)


async def cmd_help(ctx, cmd):
    now = datetime.utcnow()
    embed = Embed(title=f"Help Command: {cmd}",
                  description=f"{help_syntax(cmd)}",
                  colour=ctx.author.colour)
    embed.add_field(name="Command Usage", value=cmd.description or "No description")
    embed.add_field(name='\u200B', value='\u200B')
    await ctx.send(embed=embed)


def help_syntax(cmd):
    cmd_and_aliases = "|".join([str(cmd), *cmd.aliases])
    params = []

    for key, value in cmd.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)

    return f"`{PREFIX}{cmd_and_aliases} {params}`"

# Error Handler
@client.event
async def on_command_error(ctx, error):
    error = getattr(error, 'original', error)
    if isinstance(error, commands.MissingRequiredArgument):
        await cmd_help(ctx, ctx.command)
    elif isinstance(error, discord.errors.HTTPException):
        await ctx.send(str(error) + f" <@{owner_id}>")
        print("DISCORD HTTPEXCEPTION")
        print(error)
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    elif isinstance(error, discord.ext.commands.CommandNotFound):
        await ctx.reply("No command found with that name " + str(error) )
    elif isinstance(error, discord.ext.commands.MaxConcurrencyReached):
        await ctx.reply(str(error) + " Try again later.")
    else:
        await ctx.send(str(error) + f" <@{owner_id}>")
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


# Start Bot
asyncio.run(client.start_bot())







