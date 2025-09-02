import os
from dotenv import load_dotenv; load_dotenv()
import discord

TOKEN = os.getenv("TOKEN")
GUILD = discord.Object(id=1409368851589763195)
