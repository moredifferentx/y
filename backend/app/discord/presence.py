import discord


async def set_presence(bot: discord.Client, status: str):
    await bot.change_presence(
        activity=discord.Game(name=status),
        status=discord.Status.online,
    )
