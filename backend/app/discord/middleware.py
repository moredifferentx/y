from discord.ext import commands


class Middleware:
    """
    Hook point for permissions, rate limits, filters.
    """

    @staticmethod
    async def before(ctx: commands.Context):
        return True

    @staticmethod
    async def after(ctx: commands.Context):
        return
