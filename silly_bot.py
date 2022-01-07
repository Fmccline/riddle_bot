"""
Twitch Chat bot that posts a riddle when commanded and posts the answer 30 seconds later.
Code used from these links.
https://github.com/TwitchIO/TwitchIOv
https://github.com/bsquidwrd/Example-TwitchIO-Bot
"""
from twitchio.ext import commands
import cogs
from environment import Env
import util

class Bot(commands.Bot):

    def __init__(self, irc_token, nick, client_id='test', initial_channels=[]):
        params = {
            'irc_token': irc_token,
            'client_id': client_id,
            'nick': nick,
            'prefix': '!',
            'initial_channels': initial_channels,
        }
        super().__init__(token=irc_token, client_id=client_id, nick=nick, initial_channels=initial_channels, prefix='!')
        self.log = util.LOG
        self.add_cog(cogs.FactCog(self))
        self.add_cog(cogs.RiddleCog(self))
        self.add_cog(cogs.ExistentialCog(self))
        self.add_cog(cogs.AboutCog(self))
        self.rival_cog = cogs.RivalCog(self)

    def get_author_prefix(self, message):
        user_prefix = ''
        if message.author.is_subscriber:
            user_prefix = '[Subscriber] '
        if message.author.is_mod:
            user_prefix = '[Moderator] '
        if message.author.name.lower() == self.nick.lower():
            user_prefix = '[Bot] '
        return user_prefix

    async def event_ready(self):
        ready_string = f'Ready: {self.nick}'
        self.log.info(ready_string)

    async def event_command_error(self, ctx, error):
        self.log.error(
            f'Error running command: {error} for {ctx.message.author.name}')
        # TODO: Fix this so it works with Nightbot and other commands I don't know...
        # message = f"Sorry {ctx.author.name}, I don't know that command! Maybe in the future, I can add your command."
        # await ctx.send(message)

    async def event_message(self, message):
        if message is None or message.author is None:
            return

        user_prefix = self.get_author_prefix(message)
        self.log.info(
            f'#{message.channel} - {user_prefix}{message.author.name} - {message.content}')

        author = message.author.name.lower()
        if author == self.nick.lower() or author == '':
            return
        elif self.rival_cog.should_insult(author):
            await self.rival_cog.insult_rival(message, author)
        elif message.content[0] == '!':
            await self.handle_commands(message)


if __name__ == '__main__':
    nick = Env.BOT_NICK
    irc_token = Env.BOT_TOKEN
    client_id = Env.CLIENT_ID

    channels = Env.CHANNELS
    bot = Bot(irc_token=irc_token, client_id=client_id, nick=nick, initial_channels=channels)
    bot.run() 
