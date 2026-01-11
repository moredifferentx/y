import discord
from discord.ext import commands

from app.ai.engine_router import ENGINE_ROUTER
from app.ai.context_manager import ContextManager
from app.cognition import (
    Personality,
    MoodEngine,
    EmotionModel,
    ExpressionEngine,
    SelfReflection,
)
from app.memory import MEMORY
from app.core.config import Config
from app.monitoring import log


class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix=Config.DISCORD_PREFIX,
            intents=intents,
        )

        self.context_manager = ContextManager(MEMORY)
        self.personality = Personality()
        self.mood = MoodEngine()
        self.emotion = EmotionModel()
        self.expression = ExpressionEngine()
        self.reflection = SelfReflection()

    async def setup_hook(self):
        log("Discord bot setup complete")

    async def on_ready(self):
        log(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        log(f"Message received from {message.author.id}")

        try:
            emotions = self.emotion.analyze(message.content)
            self.mood.update(emotions)

            context = self.context_manager.build_context(
                user_id=str(message.author.id),
                content=message.content,
            )

            response = await ENGINE_ROUTER.generate(
                prompt=message.content,
                context=context,
                mood=self.mood.current,
                personality=self.personality.current,
            )

            emoji = self.expression.emoji_for_mood(self.mood.current)
            final = f"{response} {emoji}".strip()

            for chunk in self.expression.split_message(final):
                await message.reply(chunk)

            await self.reflection.reflect(
                user_id=str(message.author.id),
                content=message.content,
                emotion_scores=emotions,
            )

        except Exception as e:
            log(f"Failed to generate response for user {message.author.id}: {e}")

        await self.process_commands(message)
