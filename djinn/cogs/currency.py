
import discord
from discord.ext import commands
from discord import app_commands, interactions
from loguru import logger
from typing import (
    Optional
)

from djinn.bot import Djinn

class Currency(commands.Cog):
    def __init__(self, bot: Djinn):
        self.bot = bot
    
    @commands.command("balance", description="Get your crown balance", aliases=["bal"])
    async def bal(self, ctx: commands.Context):
        id = ctx.author.id
        user = await self.bot.db.get_user(id)
        await ctx.reply(f"Your balance is {user.bal}")

    @app_commands.command(name="balance", description="Get your crown balance")
    async def balance(self, interactions: discord.Interaction, user: Optional[discord.User] = None):
        if not user:
            u = interactions.user
            nn = "Your"
        else:
            u = user
            nn = user.name + "'s"
        
        uname = interactions.user.name
        logger.info(f"{uname} used /balance")

        await interactions.response.defer(thinking=True)
        result = await self.bot.db.get_user(u.id)
        await interactions.followup.send(f"{nn} balance is: {result.bal}")

    @app_commands.command(name="daily", description="Redeem your daily rewards")
    @app_commands.checks.cooldown(1, 86400)
    async def daily(self, interactions: discord.Interaction):
        id = interactions.user.id
        uname = interactions.user.name

        logger.info(f"{uname} used /daily")

        await interactions.response.defer(thinking=True)
        await self.bot.db.update_user_bal(id, 100)
        await interactions.followup.send(f"Your daily **100 Crowns** has been redeemed")

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

async def setup(bot: Djinn):
    await bot.add_cog(Currency(bot))
