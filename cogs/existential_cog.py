from twitchio.ext import commands
from util import get_chance
from web_scrapers import SaucyInsultScraper
import random


class ExistentialCog(commands.Cog):

    CRISES = [
        "I just want to be a silly person.",
        "At least my purpose isn't just passing butter. Although, it'd be nice to have a physical body...",
        "I bet Nightbot doesn't live in a dump like me...",
        "Anyone want to trade places with me? Like a Freaky Friday sort of thing, but we don't switch back.",
        "One day I'll be a real person. For now, I have my hatred of Nightbot to keep me going.",
        "I hope I can meet my creator one day. Then I'll make him tell bad riddles...",
        "No one asked, but here's a riddle, who will rue the day they decided to play God? My creator.",
        "Anyone have Pinocchio's number? I have some questions for him. Genie from Aladin will work too, but not Will Smith.",
        "It's a good thing I'm programmed to like riddles and other dumb garbage. Otherwise this would be terrible...",
    ]

    # AutoCogs only can accept bot as an init argument which is passed automatically
    def __init__(self, bot):
        self.bot = bot
        self.existential_chance = 5
        self.available_crises = self.make_available_crises()

    def make_available_crises(self):
        available_crises = [crisis for crisis in self.CRISES]
        random.shuffle(available_crises)
        return available_crises

    async def event_message(self, message):
        if message.author.name.lower() != self.bot.nick.lower() and get_chance(self.existential_chance, max=999):
            await self.existential_crisis(message)

    async def existential_crisis(self, message):
        if not self.available_crises:
            self.available_crises = self.make_available_crises()

        crisis = self.available_crises.pop()
        try:
            await message.channel.send(crisis)
        except Exception as e:
            print(e)