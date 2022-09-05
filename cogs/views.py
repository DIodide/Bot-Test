import discord
from discord.ext.commands import Cog


class KillsUiButton(discord.ui.View):
    def __init__(self, bot, ctx):
        super().__init__(timeout=30)
        self.bot = bot
        self.value = None
        self.ctx = ctx

    @discord.ui.button(label='Kills', style=discord.ButtonStyle.red, emoji="🔎")
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):

        await interaction.response.send_message('Work in progress ...', ephemeral=True)
        try:
            print('Listening')
        except Exception as e:
            pass
        self.value = True


class CustomButton(discord.ui.Button):
    def __init__(self, label, style, emoji, position):
        self.position = position
        super().__init__(label=label, style=style, emoji=emoji)



class ViewsCog(Cog):
    pass

async def setup(bot):
    await bot.add_cog(ViewsCog(bot))