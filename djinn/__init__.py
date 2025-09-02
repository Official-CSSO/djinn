

import discord
from discord import app_commands
from discord.ext import tasks, commands
from .constants import GUILD
from loguru import logger

from .cog_loader import load_cogs

class Djinn(discord.Client):

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)


    async def setup_hook(self) -> None:
        logger.success("Slash commands hook succesfully installed")
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)
    

intents = discord.Intents.default()
intents.presences = True
intents.messages = True
intents.members = True

djinn = commands.Bot(intents=intents, command_prefix="ff ")


@tasks.loop(minutes=5)
async def update_member_count_status():
    total_members = 0

    for guild in djinn.guilds:
  
        if not guild.chunked:
            await guild.chunk(cache=True)
 
        total_members += sum(1 for member in guild.members if not member.bot)

    print(total_members)
    await djinn.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{total_members} komsays"
        )
    )
@djinn.event
async def on_ready():
    logger.info(f"Logged in as : {djinn.user} (ID: {djinn.user.id})")
    
    await load_cogs(djinn, "djinn/cogs")

    await djinn.tree.sync()
    
    update_member_count_status.start()
   
    
