import time
import configparser
from datetime import datetime
from pyrogram import Client
from pyrogram import __version__
from pyrogram.raw.all import layer
from pyrogram.types import Message


class Assistant(Client):
    CREATOR_ID = 584305652
    ASSISTANT_ID = 1735803364
    chats = []
    parser = configparser.ConfigParser()
    def __init__(self):
        name = self.__class__.__name__.lower()
        self.parser.read('config.ini')
        self.cfgargs = self.parser['assistantir']
        Assistant.chats = [-1001187432108] # @PyrogramIR

        super().__init__(
            ':memory:',
            api_id=self.cfgargs['api_id'],
            api_hash=self.cfgargs['api_hash'],
            bot_token=self.cfgargs['bot_token'],
            workers=16,
            plugins=dict(
                root=f'assistantir.plugins',
            ),
            sleep_threshold=180
        )

        self.admins = {
            chat: {Assistant.CREATOR_ID}
            for chat in Assistant.chats
        }

        self.uptime_reference = time.monotonic_ns()
        self.start_datetime = datetime.utcnow()

    async def start(self):
        await super().start()

        me = await self.get_me()
        print(f"Assistant for Pyrogram v{__version__} (Layer {layer}) started on @{me.username}. Hi.")

        # Fetch current admins from chats
        for chat, admins in self.admins.items():
            async for admin in self.iter_chat_members(chat, filter="administrators"):
                admins.add(admin.user.id)

    async def stop(self, *args):
        await super().stop()
        print("Pyrogram Assistant stopped. Bye.")

    def is_admin(self, message: Message) -> bool:
        user_id = message.from_user.id
        chat_id = message.chat.id

        return user_id in self.admins[chat_id]