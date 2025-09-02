

import discord
from discord import app_commands
from discord.ext import tasks
from .constants import GUILD
from loguru import logger

class Djinn(discord.Client):

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)


    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)
    

intents = discord.Intents.default()
intents.presences = True
intents.messages = True

djinn = Djinn(intents=intents)

@tasks.loop(minutes=5) # Update status every 5 minutes
async def update_member_count_status():
    total_member_count = 0
    for guild in djinn.guilds:
        total_member_count += guild.member_count

    await djinn.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{total_member_count} komays"
        )
    )


@djinn.event
async def on_ready():
    logger.info(f"Logged in as : {djinn.user} (ID: {djinn.user.id})")
    update_member_count_status.start()
   
    
