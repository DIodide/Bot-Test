import os
import argostranslate.package, argostranslate.translate
import aiohttp
from discord.ext.commands import Cog, hybrid_command, command
from discord import TextChannel, ui, app_commands, Interaction
import discord
from io import BytesIO

from discord.ext.menus import MenuPages
from discord.ext.menus.views import ViewMenuPages

from classes.match import Match
from cogs.menus import ValMatchMenu, ValKillsMenu
from cogs.views import KillsUiButton, CustomButton
MAX = 100
def replaceSpaces(string):
    print(string)
    # Remove remove leading and trailing spaces
    string = string.strip()

    i = len(string)

    # count spaces and find current length
    space_count = string.count(' ')

    # Find new length.
    new_length = i + space_count * 2

    # New length must be smaller than length
    # of string provided.
    if new_length > MAX:
        return -1

    # Start filling character from end
    index = new_length - 1

    string = list(string)

    # Fill string array
    for f in range(i - 2, new_length - 2):
        string.append('0')

    # Fill rest of the string from end
    for j in range(i - 1, 0, -1):

        # inserts %20 in place of space
        if string[j] == ' ':
            string[index] = '0'
            string[index - 1] = '2'
            string[index - 2] = '%'
            index = index - 3
        else:
            string[index] = string[j]
            index -= 1

    return ''.join(string)

class CommandsCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        print("removing help")
        self.bot.remove_command("help")

    def cog_unload(self):
        print(f'Cog Unloaded')



    @command(name='eee', hidden=True)
    async def eee(self, ctx, id):
        vcchannel = self.bot.get_channel(int(id))
        await vcchannel.connect()
        print("e")

    @command(name="purge")
    async def purge(self, ctx):
        if ctx.author.id != self.bot.owner_id:
            return await ctx.send("redacted for git hub")
        await ctx.channel.purge()

    @command(name='sudo')
    async def sudo(self, ctx, channel: TextChannel, *args: str):
        print("Sudo ran")
        print(args)
        result = ' '.join(args)
        message = await channel.send(result, tts=True)


    @command(name='yag')
    async def yag(self, ctx):
        class IsYourMomGay(ui.View):
            def __init__(self, bot):
                super().__init__(timeout=90)
                self.bot = bot

        view = IsYourMomGay(self.bot)
        view.add_item(ui.Button(label="?", url="https://i.scdn.co/image/ab67616d0000b273fcf94951de12a7f89d370537"))
        view.add_item(ui.Button(label="?", url="https://ih1.redbubble.net/image.573981190.4977/farp,small,wall_texture,product,750x1000.u4.jpg"))
        view.add_item(ui.Button(label="?", url="https://ih1.redbubble.net/image.694222316.4835/fposter,small,wall_texture,product,750x1000.u2.jpg"))
        return await ctx.send(f"<:abdulChad:866380943375990824> Your mom ??? <:abdulChad:866380943375990824>", view=view)

    @command(name="where")
    async def iss(self, ctx, *args):
        print("Starting your mom is")
        async with aiohttp.ClientSession() as session:
            result = await session.get("https://picsum.photos/400")
            print("Result received")
            image = await result.read()
            print(image)
            await ctx.send("Your mom is at:", file=discord.File(BytesIO(image), "img.png"))

    @app_commands.command(name="group1")
    async def my_sub_command_1(self, interaction: discord.Interaction, member: discord.Member) -> None:
        await interaction.response.send_message(f"nig'd on {member.name}", ephemeral=True)

    @command(name="valstats")
    async def valstats(self, ctx, *username): # your mom valstats "bb bb cc"  [1, 2, 3, 4, 5]
        username = " ".join(username)
        matches = []
        # hard coded with tag for now
        get_last_five_val_matches = {
            'revenantcheerio': "https://api.henrikdev.xyz/valorant/v3/matches/na/revenantcheerio/NAA",
            'anger bird playr': "https://api.henrikdev.xyz/valorant/v3/matches/na/anger%20bird%20playr/9433",
            'StickyFishLips69': "https://api.henrikdev.xyz/valorant/v3/matches/na/StickyFishLips69/7928",
            'padoru': "https://api.henrikdev.xyz/valorant/v3/matches/na/padoru/0001"
        }

        data = await self.bot.session.get(get_last_five_val_matches[username])
        data = await data.json()

        for i in range(5):
            match = Match(data, i, username)
            matches.append(match)

        source = ValMatchMenu(self.bot, matches, ctx)
        menu = ViewMenuPages(
            source=source)
        await menu.start(ctx)

        class KillsUiButton(CustomButton):
            def __init__(self, label, style, emoji, position, bot):
                super().__init__(label, style, emoji, position)
                self.bot = bot

            async def callback(self, interaction: Interaction):
                # print(matches[self.bot.current_val_page].match_kills)
                kills_menu = ValKillsMenu(self.bot, matches[self.bot.current_val_page])
                menu = ViewMenuPages(
                    source=kills_menu)
                await menu.start(ctx)

        class RoundsUiButton(CustomButton):
            def __init__(self, label, style, emoji, position, bot):
                super().__init__(label, style, emoji, position)
                self.bot = bot

            async def callback(self, interaction: Interaction):
                await ctx.send("i dont do jack sh't")


        buttons = [KillsUiButton(label='Kills', style=discord.ButtonStyle.red, emoji="⚔", position=10, bot=self.bot),
                   RoundsUiButton(label='Rounds', style=discord.ButtonStyle.red, emoji="🔎", position=11, bot=self.bot)]
        # MENU HAS TO BE ALREADY STARTED
        # ADD NEW BUTTON HAS TO BE AWAITED

        # THIS WILL NOT WORK IF YOU DO NOT HAVE DISCORD.EXT.MENUS.VIEWS SPECIFICALLY MADE FOR THIS BOT
        await menu.add_new_button(buttons, react=True)




async def setup(bot):
    await bot.add_cog(CommandsCog(bot))