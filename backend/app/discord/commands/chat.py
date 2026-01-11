import discord
from discord import app_commands
from app.ai.engine_router import ENGINE_ROUTER
from app.ai.context_manager import ContextManager
from app.cognition import (
    Personality,
    MoodEngine,
    EmotionModel,
    ExpressionEngine,
)
from app.memory import MEMORY


class ChatCommand(app_commands.CommandTree):
    pass


@app_commands.command(name="chat", description="Chat with the AI")
@app_commands.describe(message="Your message")
async def chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer(thinking=True)

    emotions = EmotionModel().infer(message)

    context = ContextManager.build(
        memory={
            "user": await MEMORY.user.fetch(str(interaction.user.id)),
            "server": await MEMORY.server.fetch(str(interaction.guild.id)),
        },
        personality=Personality().snapshot(),
        mood=MoodEngine().snapshot(),
    )

    response = await ENGINE_ROUTER.generate(
        prompt=message,
        context=context,
    )

    await interaction.followup.send(response)
