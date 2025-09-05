
from discord.ext import commands
from .constants import MOTOR
from .quen import Quen

class Djinn(commands.Bot):
    """
    Discord bot subclass with attached motor client
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = Quen(MOTOR)

