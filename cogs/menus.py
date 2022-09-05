from discord.ext.commands import Cog
from discord.ext.menus import ListPageSource
from discord import Embed
import datetime # this is a package
import discord

from classes.match import Agent
from cogs.views import KillsUiButton

class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx
        with open("PREFIX.txt", "r") as f:
            PREFIX = f.read()
        self.PREFIX = PREFIX
        print(data)
        super().__init__(data, per_page=4)

    async def write_page(self, menu, fields=[]):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(title="Help",
                      description="Help Page\n\nAliases are shortened or alternate versions of the command that you can use instead of the command itself.\nExample: `ym does the same thing as yourmom\nDo `yourmom help <command name>` for help on how to use the command",
                      colour=self.ctx.author.colour)
        embed.set_thumbnail(url=self.ctx.author.avatar.url)

        embed.set_footer(
            text=f"{offset:,} - {min(len_data, offset + self.per_page - 1):,} of {len_data:,} commands.")

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        fields = []

        for entry in entries:
            fields.append((entry.brief or "No description", self.help_syntax(entry)))

        return await self.write_page(menu, fields)

    def help_syntax(self, cmd):
        cmd_and_aliases = "|".join([str(cmd), *cmd.aliases])
        params = []

        for key, value in cmd.params.items():
            if key not in ("self", "ctx"):
                params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

        params = " ".join(params)

        return f"`{self.PREFIX} {cmd_and_aliases} {params}`"


class ValMatchMenu(ListPageSource):

    def __init__(self, bot, data, ctx): # data = [match1, match2, match3. . .]
        super().__init__(data, per_page=1)
        self.bot = bot
        self.data = data
        self.username = self.data[0].name
        self.ctx = ctx
        self.send_initial_message = None


    async def write_page(self, menu, fields=[]):
        current_data = self.data[menu.current_page]
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)
        if current_data.has_won_bool:
            color = discord.Colour.green()
        else:
            color = discord.Colour.red()

        embed = Embed(title=f"Valorant Match Overview for {self.username}",
                      description=f"**Match Overview:**\n**{current_data.server} - {current_data.map_name} - {current_data.mode}**\n"
                                  f"**<t:{current_data.timestamp_start}> - <t:{int(current_data.game_end.timestamp())}>**\n"
                                  f"**Lasted:** `{'{:.2f}'.format(current_data.game_length_in_sec/60)}m`\n",
                      colour=color)
        embed.set_thumbnail(url=current_data.agent_small_icon)
        embed.set_image(url=f"{current_data.wide_card}")
        embed.set_footer(
            text=f"{offset:,} - {min(len_data, offset + self.per_page - 1):,} of {len_data:,} matches.")

        for name, value in fields: # ("Match Stats", table)
            embed.add_field(name=name, value=value, inline=False)

        self.bot.current_val_page = menu.current_page
        return embed

    async def format_page(self, menu, entries):
        message_two = ''
        fields = []
        current_data = self.data[menu.current_page]
        try:
            headshot_ratio = current_data.headshots / (current_data.bodyshots + current_data.legshots)
            headshot_ratio = "{:.0%}".format(headshot_ratio)
        except ZeroDivisionError:
            headshot_ratio = "100%"

        table = f"**{current_data.agent} - {current_data.team.capitalize()} Team - Score: `{current_data.rounds_won}` **/** `{current_data.rounds_lost}` {current_data.has_won.upper()}**\n" \
                f"**K/D/A:** `{current_data.kills}`**/**`{current_data.deaths}`**/**`{current_data.assists}` **`Hs/Bs/Ls`**: `{current_data.headshots}`/`{current_data.bodyshots}`/`{current_data.legshots}`\n" \
                f"**Headshot Ratio:** `{headshot_ratio}`\n**Combat Score:** `{current_data.combat_score}`\n" \

        if current_data.mode != "Deathmatch":
            agent = Agent(current_data.agent)
            message_two = str(f"\n```prolog\n"
                              f"Abilities Used: ({current_data.agent})\n"
                              f"    {agent.q[f'{current_data.agent}']} (Q): {current_data.q_cast}\n"
                              f"    {agent.c[f'{current_data.agent}']} (C): {current_data.c_cast}\n"
                              f"    {agent.e[f'{current_data.agent}']} (E): {current_data.e_cast}\n"
                              f"    {agent.x[f'{current_data.agent}']} (Ult): {current_data.times_ulted}\n```"

                              )
        table = table + message_two
        print(table)
        fields.append(("Match Stats:", table)) # fields = [("Match Stats:", table)]
        return await self.write_page(menu, fields)


class ValKillsMenu(ListPageSource):
    def __init__(self, bot, data):
        self.data = data
        self.bot = bot
        self.username = self.data.name
        super().__init__(data.match_kills, per_page=1)
        self.send_initial_message = None

    async def send_initial_message(self, ctx, channel):
        """|coro|

        The not default implementation of :meth:`Menu.send_initial_message`
        for the interactive pagination session.

        This implementation shows the first page of the source.
        """

        view = KillsUiButton(self.bot, self.ctx)
        print('OVEIRNJNDGS')
        page = await self._source.get_page(0)
        kwargs = await self._get_kwargs_from_page(page)
        return await channel.send(**kwargs, view=view)

    async def write_page(self, menu, fields=[]):
        current_data = self.data
        current_kill = self.data.match_kills[menu.current_page]
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)
        if current_data.has_won_bool:
            color = discord.Colour.green()
        else:
            color = discord.Colour.red()

        embed = Embed(title=f"Kills Overview ({self.username})",
                      description=f"**Match Overview:**\n**{current_data.server} - {current_data.map_name} - {current_data.mode}**\n",
                      colour=color)
        embed.set_thumbnail(url=current_kill['damage_weapon_assets']['display_icon'])
        embed.set_image(url=f"{current_data.wide_card}")
        embed.set_footer(
            text=f"{offset:,} - {min(len_data, offset + self.per_page - 1):,} of {len_data:,} kills.")

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        self.bot.current_val_page = menu.current_page
        return embed

    async def format_page(self, menu, page):
        current_data = self.data
        current_kill = self.data.match_kills[menu.current_page]
        message_two = ''
        fields = []
        offset = (menu.current_page * self.per_page) + 1

        round_number = current_kill['round']
        round = self.data.data['rounds'][round_number]

        if current_kill['killer_puuid'] == current_data.puuid:
            # Killer
            for player in round['player_stats']:
                if player['player_puuid'] == current_data.puuid:
                    shields = player['economy']['armor']['name']
                    if shields == None:
                        shields = "No Shield"
                    weapon = current_kill['damage_weapon_name']
                    if weapon == None:
                        weapon = "Suicide"
                    for damage_event in player['damage_events']:
                        if damage_event['receiver_puuid'] == current_kill['victim_puuid']:
                            bodyshots = damage_event['bodyshots']
                            headshots = damage_event['headshots']
                            legshots = damage_event['legshots']
                            total_damage = damage_event['damage']
                            break
                if player['player_puuid'] == current_kill['victim_puuid']:
                    ene_shields = player['economy']['armor']['name']
                    ene_weapon = current_kill['damage_weapon_name']
                    # Get Player Loadout from round player

            table = f"{self.username} ({shields} & {weapon}) ⚔ {current_kill['victim_display_name']} ({ene_shields} & {ene_weapon})\n" \
                    f"Killed with {weapon}"
        else:
            # Victim
            for player in round['player_stats']:
                if player['player_puuid'] == current_kill['killer_puuid']:
                    shields = player['economy']['armor']['name']
                    if shields == None:
                        shields = "No Shield"
                    weapon = current_kill['damage_weapon_name']
                    if weapon == None:
                        weapon = "Suicide"
                    for damage_event in player['damage_events']:
                        if damage_event['receiver_puuid'] == current_data.puuid:
                            bodyshots = damage_event['bodyshots']
                            headshots = damage_event['headshots']
                            legshots = damage_event['legshots']
                            total_damage = damage_event['damage']
                            break
                if player['player_puuid'] == current_kill['victim_puuid']:
                    ene_shields = player['economy']['armor']['name']
                    ene_weapon = current_kill['damage_weapon_name']

            table = f"{current_kill['victim_display_name']} ({shields} & {weapon}) ⚔ {self.username} ({ene_shields} & {ene_weapon})\n" \
                    f"Killed with {weapon}\nHeadshots: {headshots}\nBodyshots: {bodyshots}\nLegshots: {legshots}\nTotal Damage: {total_damage}"

        fields.append(("Match Stats:", table))
        return await self.write_page(menu, fields)

class MenusCog(Cog):
    pass

async def setup(bot):
    await bot.add_cog(MenusCog(bot))




