import sys
import traceback
from discord.ext.commands import Cog
from discord.ext import tasks
from deepdiff import DeepDiff
from classes.match import Match, Agent, MatchCache



class EventsCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.general = self.bot.get_channel(850107194639777802)
        self.presence_channel = self.bot.get_channel(1009939955407147048)
        self.get_last_five_val_matches = {
            'revenantcheerio': "https://api.henrikdev.xyz/valorant/v3/matches/na/revenantcheerio/NAA",
            'anger bird playr': "https://api.henrikdev.xyz/valorant/v3/matches/na/anger%20bird%20playr/9433",
            'StickyFishLips69': "https://api.henrikdev.xyz/valorant/v3/matches/na/StickyFishLips69/7928",
            'padoru': "https://api.henrikdev.xyz/valorant/v3/matches/na/padoru/0001"}
        self.old_matches = []
        self.check_valorant_losses.start()

    def cog_unload(self):
        self.check_valorant_losses.cancel()
        self.old_matches = []


    @tasks.loop(minutes=1)
    async def check_valorant_losses(self):
        final_message = ""
        new_matches = []
        runs = 0
        if self.old_matches == []:
            for name, link in self.get_last_five_val_matches.items():
                content = await self.bot.session.get(link)
                result2 = await content.json()
                last_match = Match(result2, 0, name)
                self.old_matches.append(last_match)

        for index, (name, link) in enumerate(self.get_last_five_val_matches.items()):
            content = await self.bot.session.get(link)
            try:
                result = await content.json()
                last_match = Match(result, 0, name)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
                return "Error"

            # Dupe Checking
            new_matches.append(last_match)
            if last_match.__eq__(self.old_matches[index]):
                continue
                # continues to next loop if match is duplicate


            try:
                headshot_ratio = last_match.headshots / (last_match.bodyshots + last_match.legshots)
                headshot_ratio = "{:.0%}".format(headshot_ratio)
            except ZeroDivisionError:
                headshot_ratio = "100%"

            if last_match.mode != "Deathmatch":
                message = str(
                    f"**{last_match.map_name}** - {last_match.mode} - {last_match.server} **<t:{last_match.timestamp_start}:f>**\n"
                    f"**{str(name).upper()}** __{last_match.rank}__ has **{last_match.has_won}** on **{str(last_match.map_name).upper()}** with a team score of "
                    f"`{last_match.rounds_won}` / `{last_match.rounds_lost}`\n`K/D/A`: `{last_match.kills}`/`{last_match.deaths}`/`{last_match.assists}` "
                    f"- **Headshot Ratio:** `{headshot_ratio})`\n\n")
            else:
                message = str(
                    f"**{last_match.map_name}** - {last_match.mode} - {last_match.server} **<t:{last_match.timestamp_start}:f>**\n"
                    f"**{str(name).upper()}** __{last_match.rank}__ has **played Deathmatch** on **{str(last_match.map_name).upper()}** with a KDA of "
                    f"\n`K/D/A`: `{last_match.kills}`/`{last_match.deaths}`/`{last_match.assists}`"
                )

            if last_match.mode != "Deathmatch":
                agent = Agent(last_match.agent)
                message_two = str(f"```prolog\n"
                                  f"Abilities Used: ({last_match.agent})\n"
                                  f"    {agent.q[f'{last_match.agent}']} (Q): {last_match.q_cast}\n"
                                  f"    {agent.c[f'{last_match.agent}']} (C): {last_match.c_cast}\n"
                                  f"    {agent.e[f'{last_match.agent}']} (E): {last_match.e_cast}\n"
                                  f"    {agent.x[f'{last_match.agent}']} (Ult): {last_match.times_ulted}\n```"

                                  )
            else:
                message_two = ""
            message = message + message_two
            final_message = final_message + message + "\n-------------------------------------------------"

        for match, match2 in zip(self.old_matches, new_matches):
            runs += 1
            print(runs)
            print(len(list(zip(self.old_matches, new_matches))))
            print("Checking")
            print(match.__eq__(match2))
            if match.__eq__(match2):
                print("Finishing")
            else:
                runs -= 1

        print(final_message)
        if len(list(zip(self.old_matches, new_matches))) == runs:
            print("Not running")
            return True

        print("sending new")
        await self.presence_channel.send(final_message)
        self.old_matches = new_matches


        #
        # if result != old_content:
        #     changes = DeepDiff(result, old_content)
        #     print(changes)

    @Cog.listener()
    async def on_presence_update(self, before, after):
        pass
        # is_real = 0
        # before_message = f'**{after.name}:** '
        # after_message = f'**{after.name}:** '
        # print(before.activities)
        # print(after.activities)
        # for activity in before.activities:
        #     if activity.type == ActivityType.playing:
        #         print("HE S DOING THE DID")
        #         before_message = before_message + str(activity.name) + " + "
        #         is_real += 1
        # for activity in after.activities:
        #     if activity.type == ActivityType.playing:
        #         after_message = after_message + str(activity.name) + " + "
        #         is_real += 1
        # message = f"{before_message.rstrip('+ ')} ------> {after_message.rstrip('+ ')}"
        # if is_real:
        #     await self.presence_channel.send(message)







async def setup(bot):
    await bot.add_cog(EventsCog(bot))
