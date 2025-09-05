import discord
from discord import app_commands
from discord.ext import commands

from djinn.bot import Djinn


class Event(commands.Cog):
    def __init__(self, bot: Djinn):
        self.bot = bot

    @app_commands.command(name="test", description="Send reply test")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello World")

async def setup(bot: Djinn):
    await bot.add_cog(Event(bot))
