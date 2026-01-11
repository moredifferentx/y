import os
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
        # ==================================================
        # INTENTS
        # ==================================================
        intents = discord.Intents.default()
        intents.message_content = True

        # ==================================================
        # COMMAND PREFIX (SAFE + FALLBACK)
        # ==================================================
        prefix = (
            os.getenv("DISCORD_PREFIX")
            or getattr(Config, "DISCORD_PREFIX", None)
            or "!"
        )

        super().__init__(
            command_prefix=prefix,
            intents=intents,
        )

        # ==================================================
        # DISCORD TOKEN (REQUIRED)
        # ==================================================
        self.token = (
            os.getenv("DISCORD_BOT_TOKEN")
            or os.getenv("DISCORD_TOKEN")
            or Config.get("DISCORD_BOT_TOKEN")
            or Config.get("DISCORD_TOKEN")
        )

        if not self.token:
            raise RuntimeError(
                "DISCORD_BOT_TOKEN or DISCORD_TOKEN is not set in environment"
            )

        # ==================================================
        # COGNITION COMPONENTS
        # ==================================================
        self.context_manager = ContextManager(MEMORY)
        self.personality = Personality()
        self.mood = MoodEngine()
        self.emotion = EmotionModel()
        self.expression = ExpressionEngine()
        self.reflection = SelfReflection()

    # ==================================================
    # DISCORD LIFECYCLE
    # ==================================================
    async def setup_hook(self):
        log("Discord bot setup complete")

    async def on_ready(self):
        log(f"Logged in as {self.user} (ID: {self.user.id})")

    # ==================================================
    # MESSAGE HANDLING
    # ==================================================
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        log(f"Message received from {message.author.id}")

        try:
            # ---- Emotion + mood ----
            emotions = self.emotion.analyze(message.content)
            self.mood.update(emotions)

            # ---- Context ----
            context = self.context_manager.build_context(
                user_id=str(message.author.id),
                content=message.content,
            )

            # ---- AI generation ----
            response = await ENGINE_ROUTER.generate(
                prompt=message.content,
                context=context,
                mood=self.mood.current,
                personality=self.personality.current,
            )

            # ---- Expression ----
            emoji = self.expression.emoji_for_mood(self.mood.current)
            final = f"{response} {emoji}".strip()

            for chunk in self.expression.split_message(final):
                await message.reply(chunk)

            # ---- Reflection ----
            await self.reflection.reflect(
                user_id=str(message.author.id),
                content=message.content,
                emotion_scores=emotions,
            )

        except Exception as e:
            log(f"Failed to generate response for user {message.author.id}: {e}")

        await self.process_commands(message)

    # ==================================================
    # SAFE START (USED BY main.py)
    # ==================================================
    async def start(self, *args, **kwargs):
        log("Starting Discord bot...")
        await super().start(self.token)
