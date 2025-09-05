import os
from dotenv import load_dotenv; load_dotenv()
import discord
from motor.motor_asyncio import AsyncIOMotorClient

TOKEN = os.getenv("TOKEN")
GUILD = discord.Object(id=1409368851589763195)
MONGO_DB = os.getenv("MONGODB")

MOTOR = AsyncIOMotorClient(MONGO_DB) 
