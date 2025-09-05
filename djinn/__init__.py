

import discord
from discord.ext import tasks, commands
from loguru import logger

from djinn.constants import GUILD

from .cog_loader import load_cogs
from .bot import Djinn

intents = discord.Intents.default()
intents.presences = True
intents.messages = True
intents.members = True

djinn = Djinn(intents=intents, command_prefix="!")


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
    logger.info(f"Logged in as : {djinn.user}")
    
    try:
        dbs = await djinn.db.motor.list_database_names()
        logger.success(f"Connected! Databases: {dbs}")
    except Exception as e:
        logger.error(f"Connection failed: {e}")

    await load_cogs(djinn, "djinn/cogs")
    await djinn.tree.sync(guild=GUILD)
    
    update_member_count_status.start()
   
    
