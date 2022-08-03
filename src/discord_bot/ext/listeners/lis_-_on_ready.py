# imports
import os
import logging
import discord
from discord.ext import commands
from multiprocessing.connection import Client

# logging
"""create logger by inheriting configuration from root logger"""
logger = logging.getLogger(__name__)


# bot subbot communication
class BotCommunication:
    def __init__(self, client):
        # connection to the listener
        self.connection = Client(('localhost', 9999), authkey=None)
        self.client = client

    def authenticate(self) -> bool:
        self.connection.send(int(self.client.user.id))
        message = self.connection.recv()

        if message == 'authentication succeeded':
            return True

        self.connection.close()
        return False

    async def receive_and_handle(self) -> None:
        while True:
            message = self.connection.recv()
            message.strip()

            if message == 'shutdown':
                logger.info('shutting down...')
                await self.client.close()

            if message.startswith('repeat'):
                channel = await self.client.fetch_channel(967030034240012332)
                await channel.send(message[7:])


# extension
class OnReadyListener(commands.Cog, name='On Ready Listener', description='contains on_ready listener'):
    """cog for on_ready event"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """custom on_ready event"""
        # change the status of the bot
        await self.client.change_presence(activity=discord.Streaming(
            platform='twitch', url='https://twitch.tv/avoncess',
            name='.help'))

        # send a message when the bot was initialized successfully
        logging.info('\n------\n'
                     'The Bot is now up and running!'
                     '\n------')

        # connect to main bot and wait for commands
        logger.info('connecting to main bot...')

        communication = BotCommunication(self.client)
        if communication.authenticate():
            logger.info('Connection to main bot established!')
            await communication.receive_and_handle()
        else:
            logger.info('Could not connect to main bot.')
            logger.info('shutting down...')
            await self.client.close()


# cog related functions
def setup(client):
    """load extensions"""
    logger.info(f'loading extension: {os.path.basename(__file__)}')
    client.add_cog(OnReadyListener(client))


def teardown(client):
    """send information when extension is being unloaded"""
    logger.info(f'unloading extension: {os.path.basename(__file__)}')
