
from .. import djinn
from discord import app_commands
import discord

@djinn.tree.command()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")
