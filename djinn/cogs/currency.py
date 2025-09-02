
import discord
from discord.ext import commands
from discord import app_commands

class Currency(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="daily", description="Redeem your daily silvers")
    @app_commands.checks.cooldown(1, 86400)
    async def daily(self, interactions: discord.Interaction):
        await interactions.response.send_message(f"Your daily **100 Silvers** is redeemed!")

    @daily.error
    async def daily_error(
            self,
            interaction: discord.Interaction, 
            error: app_commands.AppCommandError
        ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                "You've already redeem your daily rewards. Please come back tomorrow!",
                ephemeral=True 
            )
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Currency(bot))
