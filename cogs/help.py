from discord.ext.commands import Cog, bot, hybrid_command
from discord import Embed
from discord.ext.menus import MenuPages
from cogs.menus import HelpMenu
from typing import Optional
from discord.utils import get
import datetime


class HelpCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("PREFIX.txt", "r") as f:
            PREFIX = f.read()
        self.PREFIX = PREFIX

    async def cmd_help(self, ctx, cmd):
        now = datetime.datetime.utcnow()
        embed = Embed(title=f"Help with `{cmd}`",
                      description=f"{self.help_syntax(cmd)}",
                      colour=ctx.author.colour)
        embed.add_field(name="Command description", value=cmd.description or "No description")
        embed.add_field(name='\u200B', value='\u200B')
        embed.set_footer(text=now.strftime("%d, %A %Y %I:%M:%S"), icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    @hybrid_command(name="help", hidden=True)
    async def show_help(self, ctx, cmd: Optional[str]):
        """Shows this message."""
        if cmd is None:
            menu = MenuPages(source=HelpMenu(ctx, [c for c in list(self.bot.commands) if not c.hidden]),
                             delete_message_after=False,
                             timeout=180.0)
            await menu.start(ctx)

        else:
            if command := get(self.bot.commands, name=cmd):
                print(command)
                await self.cmd_help(ctx, command)

            else:
                await ctx.reply("That command does not exist...")

    def help_syntax(self, cmd):
        cmd_and_aliases = "|".join([str(cmd), *cmd.aliases])

        params = []

        for key, value in cmd.params.items():
            if key not in ("self", "ctx"):
                params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

        params = " ".join(params)
        return f"`{self.PREFIX}{cmd_and_aliases} {params}`"


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
