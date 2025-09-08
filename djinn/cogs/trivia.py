# Note(ryuu): the view & button class doesnt have a proper type annotations
# leading to several warnings. if u want to fix it urself, open up a pull request
# i aint gon fix it bro :) if it works, it works. i know its bad code thats why 
# u need to fix it not me--too much task for me to handle.


import time
from typing import Optional, Any
from discord.ext import commands
from discord import app_commands
from enum import Enum
from typing import List
import discord
import random

from djinn.bot import Djinn
from djinn.constants import GUILD, TRIVIA_URL
from djinn.quen import Quen
import aiohttp
import html

class Difficulty(Enum):
    Easy = "easy"
    Medium = "medium"
    Hard = "hard"
    Random = random.choices(["easy", "medium", "hard"])[0]

ACTIVE_TRIVIA: set[int] = set()

class TriviaView(discord.ui.View):
    correct_ans: str
    message: discord.WebhookMessage
    user_id : int
    def __init__(self, correct_ans: str, ans: List[str], user_id: int):
        super().__init__(timeout=8)
        self.correct_ans = correct_ans 
        self.user_id = user_id

        for a in ans:
            self.add_item(AnswerButton(a, correct_ans, user_id))
    
    async def on_timeout(self):

        for c in self.children:
            if c.label == self.correct_ans:
                c.style = discord.ButtonStyle.green
            c.disabled = True
        
        if hasattr(self, "message"):
            await self.message.edit(content="⏰ Time’s up! No more answers.", view=self)

        if self.user_id in ACTIVE_TRIVIA:
            ACTIVE_TRIVIA.remove(self.user_id)
    
class AnswerButton(discord.ui.Button):
    correct_ans : str
    user_id : int
    def __init__(self, label: str, correct_ans: str, user_id: int):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.correct_ans = correct_ans
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction) -> Any:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("🚫 This trivia is not for you!", ephemeral=True)
            return
        
        if self.label == self.correct_ans:
            await interaction.response.send_message(
                "Correct!", 
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"Wrong! The correct answer was **{self.correct_ans}**",
                ephemeral=True
            )

        for c in self.view.children:
            if c.label == self.correct_ans:
                c.style = discord.ButtonStyle.green
            elif self.label != self.correct_ans:
                self.style = discord.ButtonStyle.red

            c.disabled = True

        await interaction.message.edit(view=self.view)

        # unlock user after answering
        if self.user_id in ACTIVE_TRIVIA:
            ACTIVE_TRIVIA.remove(self.user_id)

class Trivia(commands.Cog):
    bot: Djinn
    db: Quen
    def __init__(self, bot: Djinn):
        self.bot = bot
        self.db = bot.db
    
    @app_commands.command(name="trivia", description="Generate QNA about computers")
    @app_commands.checks.cooldown(1, 8+5)
    async def trivia(
        self, 
        interactions: discord.Interaction, 
        difficulty: Optional[Difficulty] = Difficulty.Random
    ):
        user_id = interactions.user.id
        if user_id in ACTIVE_TRIVIA:
            await interactions.response.send_message(
                "⏳ You already have an active trivia game! Finish it before starting another.",
                ephemeral=True
            )
            return

        await interactions.response.defer(thinking=True)
        
        # OPENTB Request
        url = f"{TRIVIA_URL}?amount=1&category=18&difficulty={difficulty.value}&type=multiple"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                data = await res.json()
                result = data['results'][0]
                
        question = html.unescape(result['question'])
        correct_ans = html.unescape(result['correct_answer'])
        incorrect_ans = [html.unescape(ans) for ans in result["incorrect_answers"]]
        answers = incorrect_ans + [correct_ans]
        random.shuffle(answers)

        embed = discord.Embed(
            title="🎲 Trivia!",
            description=f"## {question}\n\nCategory: `Sciece : Computers`\nDifficulty: `{difficulty.value.capitalize()}`"
        )
        embed.set_footer(text="You only have 8 seconds to answer. Choose wisely...")
        view = TriviaView(correct_ans, answers, user_id)
        msg = await interactions.followup.send(embed=embed, view=view)
        view.message = msg

    @trivia.error
    async def trivia_error(
        self, 
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        
        if isinstance(error, app_commands.CommandOnCooldown):
            retry_after = int(time.time() + error.retry_after)
            await interaction.response.send_message(
                f"You're on cooldown! Try again <t:{retry_after}:R>",
                ephemeral=True 
            )
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot: Djinn):
    await bot.add_cog(Trivia(bot), guild=GUILD)
