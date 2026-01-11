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

log("Discord bot started")
log(f"Message received from {message.author.id}")
log(f"Failed to generate response for user {message.author.id}")



INTENTS = discord.Intents.default()
INTENTS.message_content = True


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=INTENTS,
        )

        # Cognition components (singleton per bot)
        self.personality = Personality()
        self.mood = MoodEngine()
        self.emotion_model = EmotionModel()
        self.expression = ExpressionEngine()
        self.reflection = SelfReflection()

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"[Discord] Logged in as {self.user}")

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # Emotion inference
        emotions = self.emotion_model.infer(message.content)
        dominant = max(emotions, key=emotions.get, default=None)
        if dominant:
            self.mood.update_from_emotion(dominant, emotions[dominant])

        # Memory fetch
        user_memory = await MEMORY.user.fetch(str(message.author.id))
        server_memory = (
            await MEMORY.server.fetch(str(message.guild.id))
            if message.guild
            else []
        )

        # Build AI context
        context = ContextManager.build(
            memory={
                "user": user_memory,
                "server": server_memory,
            },
            personality={
                "traits": self.personality.snapshot(),
                "style": self.personality.style_hint(),
            },
            mood=self.mood.snapshot(),
        )

        async with message.channel.typing():
            await self.expression.typing_delay()

            response = await ENGINE_ROUTER.generate(
                prompt=message.content,
                context=context,
            )

        # Expression shaping
        emoji = self.expression.emoji_for_mood(self.mood.current)
        final = f"{response} {emoji}".strip()

        for chunk in self.expression.split_message(final):
            await message.reply(chunk)

        # Self reflection
        await self.reflection.reflect(
            user_id=str(message.author.id),
            content=message.content,
            emotion_scores=emotions,
        )
