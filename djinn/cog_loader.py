import os
from discord.ext import commands
from loguru import logger

async def load_cogs(bot: commands.Bot, path: str):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                path = os.path.join(root, file).replace("/", ".").replace("\\", ".")
                module = path[:-3]  # remove .py
                try:
                    await bot.load_extension(module)
                    logger.success(f"Loaded: {module}")
                except Exception as e:
                    logger.error(f"Error loading {module}: {e}")
