"""Enhanced Discord bot with full command support, reactions, buttons, modals."""
import os
import asyncio
import logging
from discord.ext import commands, tasks
from discord import Intents, app_commands, Interaction, TextChannel
import discord

logger = logging.getLogger(__name__)


def create_bot(ai_manager):
    """Create and configure the Discord bot."""
    intents = Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    # Store AI manager as bot attribute
    bot.ai_manager = ai_manager

    @bot.event
    async def on_ready():
        logger.info(f"Bot ready as {bot.user}")
        try:
            synced = await bot.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.exception(f"Failed to sync commands: {e}")

    # ===== TEXT COMMANDS =====
    @bot.command(name="ping")
    async def ping(ctx):
        """Ping command."""
        await ctx.send("Pong!")

    @bot.command(name="status")
    @commands.has_permissions(administrator=True)
    async def status(ctx):
        """Show bot status."""
        engine = bot.ai_manager.current_name
        await ctx.send(f"Engine: {engine}")

    # ===== SLASH COMMANDS =====
    @bot.tree.command(name="ai_chat", description="Chat with the AI")
    async def ai_chat(interaction: Interaction, prompt: str):
        """Slash command for AI chat."""
        await interaction.response.defer()
        try:
            # Simulate typing
            async with interaction.channel.typing():
                response = await bot.ai_manager.generate(prompt)
            await interaction.followup.send(response[:2000])  # Discord 2000 char limit
        except Exception as e:
            logger.exception(f"Error in ai_chat: {e}")
            await interaction.followup.send(f"Error: {str(e)}")

    @bot.tree.command(name="engine_status", description="Show current AI engine")
    async def engine_status(interaction: Interaction):
        """Show engine status."""
        await interaction.response.defer()
        engine = bot.ai_manager.current_name
        await interaction.followup.send(f"Current engine: **{engine}**")

    @bot.tree.command(name="switch_engine", description="Switch AI engine")
    @app_commands.describe(engine="Engine name (ollama or openai)")
    async def switch_engine(interaction: Interaction, engine: str):
        """Switch AI engine."""
        await interaction.response.defer()
        if engine not in bot.ai_manager.engines:
            await interaction.followup.send(f"Unknown engine: {engine}")
            return
        ok = await bot.ai_manager.switch_engine(engine)
        if ok:
            await interaction.followup.send(f"Switched to **{engine}**")
        else:
            await interaction.followup.send(f"Failed to switch to {engine}")

    @bot.tree.command(name="generate_image", description="Generate an image")
    async def generate_image(interaction: Interaction, prompt: str):
        """Generate image using AI."""
        await interaction.response.defer()
        try:
            from backend.image_gen import generator

            image_url = await generator.generate(prompt)
            if image_url:
                # If it's base64, embed it; otherwise link it
                if image_url.startswith("data:"):
                    await interaction.followup.send("Image generated (base64, display in client)")
                else:
                    await interaction.followup.send(f"[Image]({image_url})")
            else:
                await interaction.followup.send("Could not generate image.")
        except Exception as e:
            logger.exception(f"Image generation error: {e}")
            await interaction.followup.send(f"Error: {str(e)}")

    @bot.tree.command(name="memory_add", description="Add memory about you")
    async def memory_add(interaction: Interaction, key: str, value: str):
        """Add memory."""
        await interaction.response.defer()
        try:
            from backend.memory import store

            user_id = str(interaction.user.id)
            await store.add(user_id, key, value, importance=1.0)
            await interaction.followup.send(f"Memory saved: {key}")
        except Exception as e:
            logger.exception(f"Memory error: {e}")
            await interaction.followup.send(f"Error: {str(e)}")

    @bot.tree.command(name="memory_list", description="List memories")
    async def memory_list(interaction: Interaction):
        """List memories."""
        await interaction.response.defer()
        try:
            from backend.memory import store

            user_id = str(interaction.user.id)
            mems = await store.list_for_owner(user_id)
            if not mems:
                await interaction.followup.send("No memories found.")
                return
            lines = [f"**{m.key}**: {m.value}" for m in mems]
            await interaction.followup.send("\n".join(lines[:10]))  # limit to 10
        except Exception as e:
            logger.exception(f"Memory error: {e}")
            await interaction.followup.send(f"Error: {str(e)}")

    @bot.tree.command(name="personality_show", description="Show server personality")
    async def personality_show(interaction: Interaction):
        """Show personality settings."""
        await interaction.response.defer()
        try:
            from backend.personality import manager

            server_id = str(interaction.guild.id)
            profile = await manager.get_profile_for_server(server_id)
            mood = await manager.get_mood(server_id)
            msg = f"**Personality Profile**\n{profile}\n**Mood**: {mood}"
            await interaction.followup.send(msg)
        except Exception as e:
            logger.exception(f"Personality error: {e}")
            await interaction.followup.send(f"Error: {str(e)}")

    @bot.tree.command(name="set_mood", description="Set bot mood")
    async def set_mood(interaction: Interaction, mood: str):
        """Set bot mood."""
        await interaction.response.defer()
        valid_moods = ["happy", "neutral", "sad", "angry", "playful", "focused"]
        if mood not in valid_moods:
            await interaction.followup.send(f"Invalid mood. Choose: {', '.join(valid_moods)}")
            return
        try:
            from backend.personality import manager

            server_id = str(interaction.guild.id)
            await manager.set_mood(server_id, mood)
            await interaction.followup.send(f"Mood set to: **{mood}**")
        except Exception as e:
            logger.exception(f"Mood error: {e}")
            await interaction.followup.send(f"Error: {str(e)}")

    # ===== REACTIONS =====
    @bot.event
    async def on_message(message):
        """Handle messages and reactions."""
        if message.author == bot.user:
            return

        # Auto-react to mentions
        if bot.user in message.mentions:
            try:
                from backend.expression import engine as expr_engine
                from backend.personality import manager as personality

                server_id = str(message.guild.id)
                mood = await personality.get_mood(server_id)
                emojis = expr_engine.get_reaction_emojis(mood, message.content)
                for emoji in emojis:
                    await message.add_reaction(emoji)
            except Exception as e:
                logger.exception(f"Reaction error: {e}")

        await bot.process_commands(message)

    # ===== BACKGROUND TASKS =====
    @tasks.loop(minutes=30)
    async def memory_decay_task():
        """Periodic memory decay."""
        try:
            from backend.memory import store

            await store.decay(days=30)
            logger.info("Memory decay completed")
        except Exception as e:
            logger.exception(f"Memory decay error: {e}")

    @tasks.loop(hours=1)
    async def relationship_decay_task():
        """Periodic relationship decay."""
        try:
            from backend.relationships import manager as rel_manager

            await rel_manager.decay_relationships()
            logger.info("Relationship decay completed")
        except Exception as e:
            logger.exception(f"Relationship decay error: {e}")

    @bot.event
    async def on_ready():
        memory_decay_task.start()
        relationship_decay_task.start()

    return bot


async def start_discord_bot(ai_manager):
    """Start the Discord bot."""
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        logger.warning("DISCORD_BOT_TOKEN not set; Discord bot will not start")
        return

    bot = create_bot(ai_manager)

    try:
        await bot.start(token)
    except Exception as e:
        logger.exception(f"Discord bot error: {e}")
