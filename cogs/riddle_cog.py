import asyncio
from twitchio.ext import commands
from web_scrapers import RiddleScraper

@commands.cog()
class RiddleCog:

    def __init__(self, bot):
        self.bot = bot
        self.riddle_scraper = RiddleScraper()
        self.waiting_to_answer = False
        self.ANSWER_DELAY = 30

    @commands.command(name='riddle')
    async def riddle_command(self, ctx):
        if not self.waiting_to_answer:
            await self.sendRiddle(ctx)

    async def sendRiddle(self, ctx):
        riddle = self.get_riddle()
        self.waiting_to_answer = True
        channel = ctx.channel
        loop = asyncio.get_event_loop()
        loop.create_task(channel.send(
            riddle.question + f" (I will give the answer in {self.ANSWER_DELAY} seconds!)"))
        await asyncio.sleep(self.ANSWER_DELAY)
        loop.create_task(channel.send(riddle.answer))
        self.waiting_to_answer = False

    def get_riddle(self):
        riddle = None
        while riddle is None or len(riddle.question) > 140 or len(riddle.answer) > 140:
            riddle = self.riddle_scraper.scrape()
        return riddle