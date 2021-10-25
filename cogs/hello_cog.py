from twitchio.ext import commands

# Deco changes the class to AutoCog
@commands.cog()
class HelloCog:

    # AutoCogs only can accept bot as an init argument which is passed automatically
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="cog")
    async def autocog_test(self, ctx):
        await ctx.send("AutoCog Command exists!")
